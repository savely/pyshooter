# entities/entity.py
import pygame
from abc import ABC, abstractmethod


class Entity(pygame.sprite.Sprite, ABC):
    """
    Root of every visible, moving object in the world.

    Responsibilities
    ─────────────────
    • Owns world-space position (Vector2) as the single source of truth.
    • Keeps rect in sync with position for pyscroll / collision code.
    • Holds velocity and applies it each frame (move-and-collide is done
      *outside* this class, by the collision system, so velocity is just
      the *intended* displacement).
    • Owns the surface (image) and the collision rect.
    • Provides a layer value so pyscroll draws sprites in the right order.
    """

    # Override in subclasses to control draw order inside pyscroll
    LAYER: int = 1

    def __init__(
        self,
        position: pygame.Vector2,
        image: pygame.Surface,
        collision_shrink: tuple[int, int] = (0, 0),  # shrink hitbox (x, y) per side
    ):
        super().__init__()

        self.image = image

        # World position is always the *center* of the sprite
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)

        # rect is what pyscroll uses for drawing — keep it synced
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

        # Separate, smaller hitbox for gameplay collision (walls, projectiles)
        sx, sy = collision_shrink
        self.hitbox = self.rect.inflate(-sx * 2, -sy * 2)
        
        # For FSM context access if needed (e.g. for state transitions)
        self._fsm = None    # set by subclasses after super().__init__()

    # ------------------------------------------------------------------ #
    #  Sync helpers                                                        #
    # ------------------------------------------------------------------ #

    def _sync_rects(self) -> None:
        """Call after any position change to keep rect & hitbox aligned."""
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.hitbox.center = self.rect.center

    # ------------------------------------------------------------------ #
    #  Frame update                                                        #
    # ------------------------------------------------------------------ #

    def update(self, dt: float) -> None:
        """
        Base update: applies velocity to position, then syncs rects.
        Subclasses call super().update() first, then do their own logic,
        OR let the collision system move them and skip velocity here.
        """
        self._sync_rects()
        if self._fsm:
            context = self._build_context(dt)
            self._fsm.update(context)
        else:
            self.on_update(dt)   # default dt=0 for non-collision movement

    def _build_context(self, dt: float) -> dict:
        """
        Base context passed to every state.
        Subclasses extend this to add entity-specific data (target, etc.).
        """
        return {"dt": dt}  
    
    # ------------------------------------------------------------------ #
    #  Abstract interface                                                  #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def on_update(self, dt: float) -> None:
        """Per-frame logic (input / AI / lifetime). Called by update()."""
        pass
        
      