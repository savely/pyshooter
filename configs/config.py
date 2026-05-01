# common configuration constants for the game
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# game screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60

# map settings
MAP_TILE_SIZE = 32

MAPS_DIR = "assets/maps/"

#STARTING_MAP = MAPS_DIR + "simple/simple.tmx"
STARTING_MAP = MAPS_DIR + "grasslands/grasslands.tmx"

# projectile settings

BULLET_SPEED = 600.0  # Pixels per second
BULLET_DAMAGE = 25
BULLET_LIFETIME = 2.0

# enemy settings

#ENEMY_AGGRO_RADIUS = 200.0 # pixels; how close player must be for enemy to start chasing

# player settings


from dataclasses import dataclass

@dataclass
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
        return "walls"
    
    @property
    def entity_layer_name(self) -> str:
        return "player"
    @property
    def prjectile_layer_name(self) -> str:
        return "projectiles"
    @property
    def enemy_layer_name(self) -> str:
        return "enemies"
    
    # spawn points
    @property
    def spawn_point_name(self) -> str:
        return "spawn"
    
    @property
    def player_spawn_point_name(self) -> str:
        return "player_start"
    
    @property
    def enemy_spawn_point_name(self) -> str:
        return "enemy_start"

    # projectile settings
    @property
    def bullet_speed(self) -> float:
        return BULLET_SPEED    
    @property
    def bullet_damage(self) -> int:
        return BULLET_DAMAGE
    @property
    def bullet_lifetime(self) -> float:
        return BULLET_LIFETIME