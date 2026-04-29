import pygame
from engine.map.map_manager import MapManager
from configs.config import Config 

class Game:
    """
    Owns the map manager and other global game state.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.config = Config()
        
        self.is_running = False
        self._init_map()
        self._init_groups()
        self._init_entities()
        self.is_running = True
        

    
    def _init_map(self) -> None:
        self._screen_size = self.config.screen_size
        self.map_manager = MapManager(self._screen_size)        
        self.game_map = self.map_manager.load(self.config.starting_map)
        self.camera = self.map_manager.camera
        self.walls = self.game_map.get_layer_rects(self.config.wall_layer_name)
    
    def _init_groups(self) -> None:
        self.player_group      = pygame.sprite.GroupSingle()
        self.enemy_group       = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles  = pygame.sprite.Group()
    
    def _init_entities(self) -> None:
        pass

    def run(self) -> None:
        while self.is_running:
            dt = min(0.05, self.clock.tick(self.config.fps) / 1000.0)   # clamp: prevents tunnelling on lag spikes
            self._handle_events()
            self._update(dt)
            self._draw()
    
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False 
    
    def _update(self, dt: float) -> None:
        pass
    
    def _draw(self) -> None:
        self.screen.fill(self.config.bg_color)
        self.camera.draw(self.screen)
        pygame.display.flip()
        
        
if __name__ == "__main__":
    pygame.init()
    game = Game(pygame.Surface(Config().screen_size))
    game.run()
    pygame.quit()
    exit()