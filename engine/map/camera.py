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
        ox, oy = self._group.map_layer.get_center_offset()
        return world_pos + pygame.Vector2(ox, oy)

    def screen_to_world(self, screen_pos: pygame.Vector2) -> pygame.Vector2:
        ox, oy = self._group.map_layer.get_center_offset()
        return screen_pos - pygame.Vector2(ox, oy)