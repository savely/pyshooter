import pygame
from engine.entities.living_entity import LivingEntity

class Enemy(LivingEntity):
    LAYER = 1
    SPEED = 100.0           # Slower than the player
    AGGRO_RANGE = 300.0     # How far they can "see"
    COOL_DOWN_TIME = 1.0     # Seconds to wait after losing sight before calming down

    def __init__(self, position: pygame.Vector2, image: pygame.Surface):
        super().__init__(
            position=position,
            image=image,
            max_health=50,
            collision_shrink=(4, 4),
        )
        self.is_aggroed = False
        self.cooldown_timer = 0.0

    @property
    def tag(self) -> str:
        return 'enemy'

    def on_update(self, dt: float) -> None:
        if not self.is_aggroed:
            self.velocity = pygame.Vector2(0, 0)



    def chase_target(self, position: pygame.Vector2) -> None:
        """Calculates vector toward player and moves."""
        diff = position - self.position
        if diff.length() > 0:
            self.velocity = diff.normalize() * self.SPEED
            self.is_aggroed = True
            self.cooldown_timer = 0.0
            
    def cooldown(self, dt: float) -> None:
        """Called when player is out of sight; could be used to reset aggro after a delay."""
        if self.is_aggroed:
            self.cooldown_timer += dt
            if self.cooldown_timer >= self.COOL_DOWN_TIME:
                self.is_aggroed = False
                self.cooldown_timer = 0.0