from shmup.entities.gameobject import GameObject
import pygame
from shmup.config import cfg_item

class Projectile(GameObject):

    def __init__(self, position, velocity):
        super().__init__()

        self._position = pygame.math.Vector2(position)
        self.__velocity = pygame.math.Vector2(velocity)

        self.render_rect = self._image.get_rect()
        self.rect = self._image.get_rect()
        self._center()

    def handle_input(self):
        pass

    def update(self, delta_time):
        self._position += self.__velocity * delta_time
        self._center()

        if self._position.y > cfg_item("game", "screen_size")[1] + self._image.get_height() or self._position.y < (0 - self._image.get_height()):
            self.kill()

    def render(self, surface_dst):
        surface_dst.blit(self._image, self.render_rect)


    def release(self):
        pass