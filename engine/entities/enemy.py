import pygame
from engine.entities.living_entity import LivingEntity

class Enemy(LivingEntity):
    LAYER = 1
    SPEED = 100.0           # Slower than the player
    AGGRO_RANGE = 300.0     # How far they can "see"
    COOL_DOWN_TIME = 1.0     # Seconds to wait after losing sight before calming down
    DAMAGE_AMOUNT = 20
    DAMAGE_COOLDOWN = 1.5   # Seconds between attacks

    def __init__(self, position: pygame.Vector2, image: pygame.Surface):
        super().__init__(
            position=position,
            image=image,
            max_health=50,
            collision_shrink=(4, 4),
        )
        self.is_aggroed = False
        self._cooldown_timer = 0.0

    @property
    def tag(self) -> str:
        return 'enemy'

    def on_update(self, dt: float) -> None:
        if not self.is_alive: return

        if not self.is_aggroed:
            self.velocity = pygame.Vector2(0, 0)



    def chase_target(self, position: pygame.Vector2) -> None:
        """Calculates vector toward player and moves."""
        diff = position - self.position
        if diff.length() > 0:
            self.velocity = diff.normalize() * self.SPEED
            self.is_aggroed = True
            self._cooldown_timer = 0.0
            
    def cooldown(self, dt: float) -> None:
        """Called when player is out of sight; could be used to reset aggro after a delay."""
        if self.is_aggroed:
            self._cooldown_timer += dt
            if self._cooldown_timer >= self.COOL_DOWN_TIME:
                self.is_aggroed = False
                self._cooldown_timer = 0.0

    def try_damage(self, entity: LivingEntity) -> None:
        """Checks if touching the player and deals damage if cooldown is ready."""
        if self._cooldown_timer <= 0:
            if self.hitbox.colliderect(entity.hitbox):
                # We hit the player! Calculate the direction of the impact
                direction = (entity.position - self.position)
                if direction.length() > 0:
                    direction = direction.normalize()
                else:
                    direction = pygame.Vector2(1, 0) # Fallback if exactly overlapping
                
                # Tell the player to take damage
                damage_applied = entity.take_damage(self.DAMAGE_AMOUNT, direction)
                
                if damage_applied:
                    # Reset the enemy's attacown
                    self._cooldown_timer = self.DAMAGE_COOLDOWN

    def on_death(self) -> None:
        super().on_death()