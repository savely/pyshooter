import pygame
from engine.fsm.base_state import State
from configs.config import COLOR_WHITE


class SplashState(State):
    def enter(self, owner) -> None:
        self.timer = 0.0

    def update(self, context: dict) -> str | None:
        dt = context.get('dt', 0)
        owner = context.get('owner')
        self.timer += dt

        # Draw Splash Screen
        owner.screen.fill((10, 10, 10))
        font = pygame.font.SysFont(None, 64)
        text = font.render("SILLY GAMES PRESENTS", True, (200, 200, 200))
        owner.screen.blit(text, text.get_rect(center=owner.screen.get_rect().center))
        pygame.display.flip()

        # Transition to Menu after 2 seconds
        if self.timer > 2.0:
            return "MenuState"
        return None

    def exit(self) -> None:
        pass


class MenuState(State):
    def enter(self, owner) -> None:
        pass

    def update(self, context: dict) -> str | None:
        owner = context.get('owner')
        events = context.get('events', [])

        # Draw Menu Screen
        owner.screen.fill((40, 50, 60))
        font = pygame.font.SysFont(None, 48)
        text = font.render("MAIN MENU - Press ENTER to Play", True, COLOR_WHITE)
        owner.screen.blit(text, text.get_rect(center=owner.screen.get_rect().center))
        pygame.display.flip()

        # Check for Enter key to start the game
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "PlayState"
        return None

    def exit(self) -> None:
        pass


class PlayState(State):
    def enter(self, owner) -> None:
        # Initialize the game world fresh every time we enter the PlayState
        owner._init_map()
        owner._init_groups()
        owner._init_entities()

    def update(self, context: dict) -> str | None:
        dt = context.get('dt', 0)
        owner = context.get('owner')
        
        # If the player dies, transition to Game Over
        if not owner.player.is_alive:
            return "GameOverState"

        # Delegate to the Game's update and draw methods
        owner._update(dt)
        owner._draw()
        return None

    def exit(self) -> None:
        pass


class GameOverState(State):
    def enter(self, context) -> None:
        pass

    def update(self, context: dict) -> str | None:
        owner = context.get('owner')
        events = context.get('events', [])

        # Draw Game Over Screen
        owner.screen.fill((100, 20, 20))
        font = pygame.font.SysFont(None, 64)
        text = font.render("GAME OVER", True, (255, 255, 255))
        sub_text = pygame.font.SysFont(None, 32).render("Press ENTER to return to Menu", True, (200, 200, 200))
        
        center = owner.screen.get_rect().center
        owner.screen.blit(text, text.get_rect(center=(center[0], center[1] - 30)))
        owner.screen.blit(sub_text, sub_text.get_rect(center=(center[0], center[1] + 30)))
        pygame.display.flip()

        # Check for Enter key to return to the menu
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "MenuState"
        return None

    def exit(self) -> None:
        pass