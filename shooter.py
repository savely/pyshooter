import pygame
from engine.game import Game

class Shooter(Game):
    def __init__(self):
        screen = pygame.display.set_mode((1200, 800))
        super().__init__(screen)
        
if __name__ == "__main__":
    pygame.init()
    
    shooter = Shooter() 
    shooter.run()
    
    pygame.quit()
    exit()