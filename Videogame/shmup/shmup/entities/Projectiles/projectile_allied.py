from shmup.entities.Projectiles.projectile import Projectile
import pygame
from importlib import resources
from shmup.config import cfg_item

class ProjectileAllied(Projectile):
    
    def __init__(self, position):

        with resources.path(cfg_item("projectile", "allied", "image_file")[0], cfg_item("projectile", "allied", "image_file")[1]) as allied_file:
            self._image = pygame.image.load(allied_file).convert_alpha()

            velocity = cfg_item("projectile", "allied", "velocity")

        super().__init__(position, velocity)