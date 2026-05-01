import pygame
import pytmx
import pyscroll
from abc import ABC, abstractmethod

class GameMap(ABC):
    """Abstract base – defines what every map must provide."""

    @abstractmethod
    def get_layer_rects(self, name: str) -> list[pygame.Rect]:
        """Return all solid collision rects in world coordinates."""
        ...

    @abstractmethod
    def get_spawn_point(self, name: str) -> pygame.Vector2:
        """Return a named spawn location (player start, enemy waypoints…)."""
        ...

    @abstractmethod
    def make_camera_group(self) -> pygame.sprite.Group:
        """Return the sprite group that handles scrolled rendering."""
        ...

    @abstractmethod
    def get_world_size(self) -> tuple[int, int]:
        """Return (width, height) of the full map in pixels."""
        ...


class TiledGameMap(GameMap):
    """A map loaded from a Tiled .tmx file, using pytmx and pyscroll."""

    def __init__(self, filename: str, screen_size: tuple[int, int]):
        self.tmx_data = pytmx.util_pygame.load_pygame(filename)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, screen_size)
        self.map_layer.zoom = 1.0

    def get_layer_rects(self, layer_name: str) -> list[pygame.Rect]:
        """Return all solid collision rects from an Object Layer."""
        rects = []
        try:
  
            layer = self.tmx_data.get_layer_by_name(layer_name)
  
            for obj in layer:
                rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                
        except ValueError:
            print(f"Warning: Object Layer '{layer_name}' not found!")
            
        return rects

    def get_spawn_point(self, name: str) -> pygame.Vector2:
        for obj in self.tmx_data.objects:
            if obj.name == name:
                return pygame.Vector2(obj.x, obj.y)
        raise ValueError(f"Spawn point '{name}' not found in map.")

    def make_camera_group(self) -> pygame.sprite.Group:
        return pyscroll.PyscrollGroup(map_layer=self.map_layer)

    def get_world_size(self) -> tuple[int, int]:
        width = self.tmx_data.width * self.tmx_data.tilewidth
        height = self.tmx_data.height * self.tmx_data.tileheight
        return (width, height)
    