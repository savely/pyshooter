import pygame
from engine.game import Game
from configs.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Shooter(Game):
    def __init__(self):
        super().__init__(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)))
        
if __name__ == "__main__":
    pygame.init()
    
    shooter = Shooter() 
    shooter.run()
    
    pygame.quit()
    exit()