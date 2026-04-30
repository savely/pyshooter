from dataclasses import dataclass, field
import pygame
from engine.entities.entity import Entity
from engine.entities.living_entity import LivingEntity
from engine.entities.projectile import Projectile


@dataclass
class CollisionResult:
    hit_wall_x: bool = False
    hit_wall_y: bool = False
    hit_entities: list[LivingEntity] = field(default_factory=list)

    @property
    def hit_any_wall(self) -> bool:
        return self.hit_wall_x or self.hit_wall_y


class CollisionResolver:
    """
    Stateless collision resolver.

    All methods are static — no need to instantiate, but you can if you
    want to inject it as a dependency.

    Coordinate contract
    ────────────────────
    • entity.hitbox  : the rect used for ALL collision tests
    • entity.position: the Vector2 source of truth (hitbox is derived)
    • velocity       : pixels per SECOND — we multiply by dt here
    """

    # ------------------------------------------------------------------ #
    #  Main entry point — resolves one LivingEntity against walls         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def resolve_entity(
        entity: LivingEntity,
        walls: list[pygame.Rect],
        dt: float,
    ) -> CollisionResult:
        """
        Move entity by velocity*dt, resolving wall collisions on each axis.
        Modifies entity.position and entity.hitbox in place.
        Returns a CollisionResult so callers can react (stop sounds, etc.)
        """
        result = CollisionResult()

        # ── X axis ──────────────────────────────────────────────────────
        entity.position.x += entity.velocity.x * dt
        entity.hitbox.centerx = int(entity.position.x)

        hit_index = entity.hitbox.collidelist(walls)
        if hit_index != -1:
            result.hit_wall_x = True
            CollisionResolver._push_out_x(entity, walls[hit_index])

        # ── Y axis ──────────────────────────────────────────────────────
        entity.position.y += entity.velocity.y * dt
        entity.hitbox.centery = int(entity.position.y)

        hit_index = entity.hitbox.collidelist(walls)
        if hit_index != -1:
            result.hit_wall_y = True
            CollisionResolver._push_out_y(entity, walls[hit_index])

        # Keep the draw rect synced after resolution
        entity.rect.center = entity.hitbox.center

        return result

    # ------------------------------------------------------------------ #
    #  Projectile batch resolution                                         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def resolve_projectiles(
        projectiles: pygame.sprite.Group,
        walls: list[pygame.Rect],
        target_groups: list[pygame.sprite.Group],
        dt: float,
    ) -> None:
        """
        Move all projectiles, then test wall hits and entity hits.
        Projectiles are not pushed out — they simply die on contact.
        target_groups: e.g. [enemy_group] for player bullets,
                            [player_group] for enemy bullets.
        The owner_tag on each projectile determines which groups to test.
        """
        for proj in list(projectiles):           # list() — safe to kill mid-loop
            if not proj.alive():
                continue

            # Move (projectiles don't go through the entity resolver;
            # they die instead of sliding)
            proj.position += proj.velocity * dt
            proj.hitbox.center = (int(proj.position.x), int(proj.position.y))
            proj.rect.center = proj.hitbox.center

            # Wall test
            if proj.hitbox.collidelist(walls) != -1:
                proj.on_wall_hit()
                continue                         # already dead, skip entity test

            # Entity tests
            for group in target_groups:
                hit_sprites = pygame.sprite.spritecollide(
                    proj, group, False,
                    collided=lambda p, e: p.hitbox.colliderect(e.hitbox),
                )
                for target in hit_sprites:
                    if isinstance(target, LivingEntity):
                        proj.hit_entity(target)
                    break                        # one hit per frame per projectile

    # ------------------------------------------------------------------ #
    #  Entity vs entity (optional — overlap push-apart)                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def resolve_entity_overlap(
        entities: list[LivingEntity],
        push_force: float = 1.5,
    ) -> None:
        """
        Prevent entities from overlapping each other (e.g. enemies clumping).
        Simple push-apart: not physically accurate but feels fine for shooters.
        Call after wall resolution.
        """
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                a, b = entities[i], entities[j]
                if not a.hitbox.colliderect(b.hitbox):
                    continue

                diff = b.position - a.position
                distance = diff.length()
                if distance < 0.01:             # exactly overlapping — nudge randomly
                    diff = pygame.Vector2(1, 0)
                    distance = 1.0

                push = diff.normalize() * push_force
                a.position -= push
                b.position += push
                a.hitbox.center = (int(a.position.x), int(a.position.y))
                b.hitbox.center = (int(b.position.x), int(b.position.y))
                a.rect.center = a.hitbox.center
                b.rect.center = b.hitbox.center

    # ------------------------------------------------------------------ #
    #  Private push-out helpers                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _push_out_x(entity: Entity, wall: pygame.Rect) -> None:
        """Slide entity out of wall along X, then zero the X velocity."""
        if entity.velocity.x > 0:              # moving right → push to left edge of wall
            entity.hitbox.right = wall.left
        elif entity.velocity.x < 0:            # moving left  → push to right edge of wall
            entity.hitbox.left = wall.right

        entity.position.x = entity.hitbox.centerx
        entity.velocity.x = 0                  # killed only on the blocked axis

    @staticmethod
    def _push_out_y(entity: Entity, wall: pygame.Rect) -> None:
        """Slide entity out of wall along Y, then zero the Y velocity."""
        if entity.velocity.y > 0:              # moving down → push to top edge of wall
            entity.hitbox.bottom = wall.top
        elif entity.velocity.y < 0:            # moving up   → push to bottom edge of wall
            entity.hitbox.top = wall.bottom

        entity.position.y = entity.hitbox.centery
        entity.velocity.y = 0