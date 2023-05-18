from shmup.entities.Projectiles.projectile import Projectile
import pygame
import random
from importlib import resources
from shmup.config import cfg_item

class ProjectileEnemy(Projectile):
    
    def __init__(self, position):

        with resources.path(cfg_item("projectile", "enemy", "image_file")[0], cfg_item("projectile", "enemy", "image_file")[1]) as enemy_file:
            self._image = pygame.image.load(enemy_file).convert_alpha()

        velocity = cfg_item("projectile", "enemy", "velocity")
        velocity_y = random.uniform(cfg_item("projectile", "enemy", "speed_range")[0], cfg_item("projectile", "enemy", "speed_range")[1])

        super().__init__(position, [velocity[0], velocity_y])