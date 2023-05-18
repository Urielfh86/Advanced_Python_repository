from shmup.entities.gameobject import GameObject
from importlib import resources
import pygame
from shmup.config import cfg_item
from shmup.entities.gameobject import GameObject
import random
from shmup.entities.Projectiles.projectile_factory import ProjectileType

class Enemy(GameObject):

    def __init__(self, callback_spawn_projectile):
        super().__init__()
        self.score = random.randrange(10, 50)
        self.__callback_spawn_projectile = callback_spawn_projectile

        with resources.path(cfg_item("entities", "enemy", "image_file")[0], cfg_item("entities", "enemy", "image_file")[1]) as enemy_file:
            self.__enemy_image = pygame.image.load(enemy_file).convert_alpha()

        self.__enemy_image_half_width = self.__enemy_image.get_width() / 2
        self.__enemy_image_half_height = self.__enemy_image.get_height() / 2

        x_pos = random.randrange(self.__enemy_image_half_width, cfg_item("game", "screen_size")[0] - self.__enemy_image_half_width)
        y_pos = -self.__enemy_image.get_height()     

        self._position = pygame.math.Vector2(x_pos, y_pos)

        self.render_rect = self.__enemy_image.get_rect()
        self.rect = self.__enemy_image.get_rect()
        self._center()

        self.__speed_y = random.uniform(cfg_item("entities", "enemy", "speed_range")[0], cfg_item("entities", "enemy", "speed_range")[1])

    def handle_input(self):
        pass

    def update(self, delta_time):
        distance_y = self.__speed_y * delta_time
        self._position.y += distance_y
        self._center()

        if self._position.y > cfg_item("game", "screen_size")[1] + self.__enemy_image.get_height():
            self.kill()

        self.fire()

    def render(self, surface_dst):
        surface_dst.blit(self.__enemy_image, self.render_rect)


    def release(self):
        pass

    def fire(self):
        if random.random() <= cfg_item("entities", "enemy", "fire_prob"):
            self.__callback_spawn_projectile(ProjectileType.EnemyProjectile, self.render_rect.midbottom)