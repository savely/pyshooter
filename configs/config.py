COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60

MAP_TILE_SIZE = 32

MAPS_DIR = "assets/maps/"

STARTING_MAP = MAPS_DIR + "grasslands/grasslands.tmx"




class Config:
    """Holds all game configuration constants and settings."""

    def __init__(self):
        pass
    @property
    def screen_size(self) -> tuple[int, int]:
        return (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    @property
    def map_tile_size(self) -> int:
        return MAP_TILE_SIZE
    
    @property
    def maps_dir(self) -> str:
        return MAPS_DIR
    
    @property
    def starting_map(self) -> str:
        return STARTING_MAP
    
    @property
    def bg_color(self) -> tuple[int, int, int]:
        return COLOR_BLACK
    
    @property
    def fps(self) -> int:
        return FPS
    @property
    def starting_map(self) -> str:
        return STARTING_MAP
    
    # layers
    @property
    def wall_layer_name(self) -> str:
        return "Walls"
    
    @property
    def entity_layer_name(self) -> str:
        return "Player"
    @property
    def prjectile_layer_name(self) -> str:
        return "Projectiles"
    @property
    def enemy_layer_name(self) -> str:
        return "Enemies"
    
    # spawn points
    @property
    def spawn_point_name(self) -> str:
        return "spawn"
