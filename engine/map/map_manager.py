from .game_map import TiledGameMap
from .camera import Camera

class MapManager:
    
    """
    Owns the active map and camera.
    Swap maps via load().
    """

    def __init__(self, screen_size: tuple[int, int]):
        self._screen_size = screen_size
        self.current_map: TiledGameMap | None = None
        self.camera: Camera | None = None

    def load(self, tmx_path: str) -> TiledGameMap:
        game_map = TiledGameMap(tmx_path, self._screen_size)
        group = game_map.make_camera_group()
        self.current_map = game_map
        self.camera = Camera(group)
        return game_map