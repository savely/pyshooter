import pygame
from .entity import Entity


class Projectile(Entity):
    """
    Does NOT inherit LivingEntity — it has no health; it just hits and dies.

    owner_tag  : 'player' | 'enemy' — prevents friendly fire
    on_hit     : callback(target) called when the projectile hits something;
                 the scene passes a lambda that applies damage + effects
    lifetime   : auto-kills after N seconds even without a hit
    """

    LAYER = 2   # draw above characters

    def __init__(
        self,
        position: pygame.Vector2,
        direction: pygame.Vector2,
        image: pygame.Surface,
        speed: float,
        damage: int,
        owner_tag: str,
        lifetime: float = 3.0,
    ):
        super().__init__(position, image)

        self.direction = direction.normalize() if direction.length() > 0 else pygame.Vector2(1, 0)
        self.velocity = self.direction * speed
        self.damage = damage
        self.owner_tag = owner_tag
        self.lifetime = lifetime
        self._alive = True

    # ------------------------------------------------------------------ #
    #  Update                                                              #
    # ------------------------------------------------------------------ #

    def on_update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return

    # ------------------------------------------------------------------ #
    #  Hit handling                                                        #
    # ------------------------------------------------------------------ #

    def hit_entity(self, target: pygame.sprite.Sprite) -> None:
        """Called by the scene's collision system when touching a LivingEntity."""
        self.kill()

    def on_wall_hit(self) -> None:
        """Override to add ricochet, explosion, etc."""
        self.kill()