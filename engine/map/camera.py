import pygame
import pyscroll

class Camera:
    """
    Call center_on(target) every frame before draw().
    """

    def __init__(self, group: pyscroll.PyscrollGroup):
        self._group = group

    def add(self, *sprites: pygame.sprite.Sprite) -> None:
        self._group.add(*sprites)

    def remove(self, *sprites: pygame.sprite.Sprite) -> None:
        self._group.remove(*sprites)

    def center_on(self, target: pygame.sprite.Sprite) -> None:
        self._group.center(target.rect.center)

    def draw(self, surface: pygame.Surface) -> None:
        self._group.draw(surface)

    def world_to_screen(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        # 1. Get the camera's top-left position
        cam_x, cam_y = self._group.view.topleft
        
        # 2. Get the current zoom level
        zoom = self._group._map_layer.zoom
        
        # 3. Calculate the difference, then scale it UP by the zoom
        screen_x = (world_pos.x - cam_x) * zoom
        screen_y = (world_pos.y - cam_y) * zoom
        
        return pygame.Vector2(screen_x, screen_y)

    def screen_to_world(self, screen_pos: pygame.Vector2) -> pygame.Vector2:
        # 1. Get the camera's top-left position
        cam_x, cam_y = self._group.view.topleft
        
        # 2. Get the current zoom level
        zoom = self._group._map_layer.zoom
        
        # 3. Scale the screen position DOWN by the zoom, then add the camera offset
        world_x = cam_x + (screen_pos.x / zoom)
        world_y = cam_y + (screen_pos.y / zoom)
        
        return pygame.Vector2(world_x, world_y)

            
        