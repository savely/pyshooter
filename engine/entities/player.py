# entities/player.py
import pygame
from .living_entity import LivingEntity


class Player(LivingEntity):
    """
    Controlled by keyboard/mouse.

    Input contract
    ───────────────
    Movement : WASD / arrow keys
    Aim      : mouse position (world coords, converted by Camera)
    Shoot    : left mouse button → emits a shoot_requested event or
               returns a factory call; actual Projectile creation is
               handled by the game scene so Player stays decoupled.
    """

    LAYER = 1
    SPEED = 180.0           # pixels per second
    SHOOT_COOLDOWN = 0.25   # seconds between shots

    def __init__(self, position: pygame.Vector2, image: pygame.Surface):
        super().__init__(
            position=position,
            image=image,
            max_health=100,
            collision_shrink=(6, 8),
            iframes_duration=0.6,
        )
        self._shoot_timer: float = 0.0
        self.facing: pygame.Vector2 = pygame.Vector2(1, 0)  # direction player faces
        self.wants_to_shoot: bool = False   # set by input, read by scene

    @property
    def tag(self) -> str:
        return 'player'
    # ------------------------------------------------------------------ #
    #  Input → intent (no game-state side effects here)                   #
    # ------------------------------------------------------------------ #

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Call once per frame with the current key state."""
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:    move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: move.x += 1

        if move.length() > 0:
            move.normalize_ip()

        self.velocity = move * self.SPEED   # pixels/sec; multiplied by dt later

    def handle_mouse(
        self,
        mouse_world_pos: pygame.Vector2,
        buttons: tuple[bool, bool, bool],
    ) -> None:
        """Call once per frame with world-space mouse position."""
        diff = mouse_world_pos - self.position
        if diff.length() > 0:
            self.facing = diff.normalize()

        self.wants_to_shoot = buttons[0]    # left mouse button

    # ------------------------------------------------------------------ #
    #  Update                                                              #
    # ------------------------------------------------------------------ #

    def on_update(self, dt: float) -> None:
        # Tick shoot cooldown
        if self._shoot_timer > 0:
            self._shoot_timer -= dt

    def can_shoot(self) -> bool:
        return self.wants_to_shoot and self._shoot_timer <= 0

    def consume_shoot(self) -> None:
        """Called by the scene after spawning a projectile."""
        self._shoot_timer = self.SHOOT_COOLDOWN

    # ------------------------------------------------------------------ #
    #  Hooks                                                               #
    # ------------------------------------------------------------------ #

    def on_damaged(self, amount, source) -> None:
        print(f"[Player] took {amount} damage, hp={self.health}")   # → replace with flash/sound

    def on_death(self) -> None:
        print("[Player] died")   # → trigger game-over screen
        self.kill()