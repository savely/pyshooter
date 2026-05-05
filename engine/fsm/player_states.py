import pygame
from engine.entities.living_entity import LivingEntity
from ..fsm.fsm import FSM
from ..fsm.base_state import State

# ── Player states ──────────────────────────────────────────────────────────

class Idle(State):
    def enter(self, ctx):
        ctx["owner"].velocity = pygame.Vector2(0, 0)

    def update(self, ctx) -> str | None:
        owner = ctx["owner"]
        if not owner.is_alive:           return "Dead"
        if owner.velocity.length() > 5:  return "Run"
        if owner.wants_to_shoot:         return "Shoot"

    def exit(self, ctx):
        pass

class Run(State):
    def enter(self, ctx):
        pass
    
    def update(self, ctx) -> str | None:
        owner = ctx["owner"]
        if not owner.is_alive:            return "Dead"
        if owner.velocity.length() <= 5:  return "Idle"
        if owner.wants_to_shoot:          return "Shoot"
    
    def exit(self, ctx):
        pass


class Shoot(State):
    
    def enter(self, ctx):
        print("[Player] shoots")         # → swap for actual shooting logic        

    def update(self, ctx) -> str | None:
        owner = ctx["owner"]
        if not owner.is_alive:    return "Dead"
        if owner.can_shoot():     return "Shoot"   # re-enter = fire again
        if not owner.wants_to_shoot:
            if owner.velocity.length() > 5: return "Run"
            return "Idle"
        
    def exit(self, ctx):
        pass
        

class Hurt(State):
    priority   = 3
    _DURATION  = 0.3

    def enter(self, ctx):
        self._timer = self._DURATION

    def update(self, ctx) -> str | None:
        self._timer -= ctx["dt"]
        if not ctx["owner"].is_alive: return "Dead"
        if self._timer <= 0:          return "Idle"
    
    def exit(self, ctx):
        pass



class Dead(State):
    priority = 99

    def enter(self, ctx):
        owner = ctx["owner"]
        owner.velocity = pygame.Vector2(0, 0)
        print("[Player] died")          # → swap for game-over trigger

    def update(self, ctx) -> str | None:
        return None                     # terminal
    
    def exit(self, ctx):
        pass

