# entities/living_entity.py
import pygame
from .entity import Entity


class LivingEntity(Entity):
    """
    Adds health, damage reception, invincibility frames,
     and a death hook.

    Subclasses implement on_death() and on_damaged().
    """

    def __init__(
        self,
        position: pygame.Vector2,
        image: pygame.Surface,
        max_health: int,
        collision_shrink: tuple[int, int] = (0, 0),
        iframes_duration: float = 0.5,      # seconds of invincibility after a hit
    ):
        super().__init__(position, image, collision_shrink)

        self.max_health = max_health
        self.health = max_health

        self._iframes_duration = iframes_duration
        self._iframes_timer: float = 0.0    # counts DOWN to 0


    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def is_invincible(self) -> bool:
        return self._iframes_timer > 0

    @property
    def health_ratio(self) -> float:
        return self.health / self.max_health

    @property
    def tag(self) -> str:
        return 'alive'

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def take_damage(self, amount: int, source : pygame.Vector2 ) -> bool:
        """
        Returns True if damage was actually applied (not blocked by iframes).
           """
        if self.is_invincible or not self.is_alive:
            return False

        self.health = max(0, self.health - amount)
        self._iframes_timer = self._iframes_duration

        self.on_damaged(amount, source)

        if not self.is_alive:
            self.on_death()

        return True

    def heal(self, amount: int) -> None:
        self.health = min(self.max_health, self.health + amount)

    # ------------------------------------------------------------------ #
    #  Frame update                                                        #
    # ------------------------------------------------------------------ #

    def update(self, dt: float) -> None:
        # Tick down iframes
        if self._iframes_timer > 0:
            self._iframes_timer -= dt
            self._iframes_timer = max(0, self._iframes_timer)
        super().update(dt)

    # ------------------------------------------------------------------ #
    #  Hooks — override in subclasses                                      #
    # ------------------------------------------------------------------ #
    def on_update(self, dt: float) -> None:
        pass
        
    def on_damaged(self, amount: int, source: pygame.Vector2 | None) -> None:
        if self._fsm:
            self._fsm.transition("Hurt", force=True)

    def on_death(self) -> None:
        if self._fsm:
            self._fsm.transition("Dead", force=True)
        else:
            self.kill()        