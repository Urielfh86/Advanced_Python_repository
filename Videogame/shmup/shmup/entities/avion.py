from importlib import resources
import pygame
from shmup.config import cfg_item
from shmup.entities.gameobject import GameObject
from shmup.entities.Projectiles.projectile_factory import ProjectileType

class Avion(GameObject):
    def __init__(self, screen, callback_spawn_projectile):
        super().__init__()
        self.__callback_spawn_projectile = callback_spawn_projectile
        self.__is_moving_left = False
        self.__is_moving_right = False
        self.__is_moving_up = False
        self.__is_moving_down = False
        self.__screen_width = screen.get_width()
        self.__screen_height = screen.get_height()
        self.__cool_down = 0

        with resources.path(cfg_item("entities", "avion", "image_file")[0], cfg_item("entities", "avion", "image_file")[1]) as avion_file:
            # "os.join" se encarga de determinar la forma en que se ponen las rutas en windows, linux, etc
            # "convert_alpha" me asegura de que el png que cargo lo convierte al mismo formato RGB de la ventana
            self.__avion_image = pygame.image.load(avion_file).convert_alpha()

        self.__avion_image_half_width = self.__avion_image.get_width() / 2
        self.__avion_image_half_height = self.__avion_image.get_height() / 2

        self._position = pygame.math.Vector2(self.__screen_width / 2, self.__screen_height / 2)
        self.render_rect = self.__avion_image.get_rect()
        self.rect = self.__avion_image.get_rect()
        self.rect.inflate_ip(self.rect.width * -0.6, self.rect.height * -0.2)

        self._center()

        self.__map_input()

    def handle_input(self, key, is_pressed):
        if key == self.__key_mapping["left"]:
            self.__is_moving_left = is_pressed
        if key == self.__key_mapping["right"]:
            self.__is_moving_right = is_pressed
        if key == self.__key_mapping["down"]:
            self.__is_moving_down = is_pressed
        if key == self.__key_mapping["up"]:
            self.__is_moving_up = is_pressed
        if key == self.__key_mapping["fire"]:
            if self.__cool_down <= 0:
                self.__fire_projectile()

    def update(self, delta_time):
        speed = pygame.math.Vector2(0.0, 0.0)

        if self.__is_moving_left:
            speed.x -= cfg_item("entities", "avion", "speed")
        if self.__is_moving_right:
            speed.x += cfg_item("entities", "avion", "speed")
        if self.__is_moving_down:
            speed.y += cfg_item("entities", "avion", "speed")
        if self.__is_moving_up:
            speed.y -= cfg_item("entities", "avion", "speed")

        # Calculo la distancia que ha recorrido el avion. d = v * t. Con esto, en todas las PC correrá a la misma velocidad.
        distance = speed * delta_time

        if self.__allow_move_inside_limits(distance):
            self._position += distance

        self._center()

        if self.__cool_down > 0:
            self.__cool_down -= delta_time

    def render(self, surface_dst):
        # Las coordenadas origen son arriba a la izquierda de la imagen
        x, y = pygame.mouse.get_pos() 

        # Centro el mouse al medio de la imagen
        x -= self.__avion_image_half_width
        y -= self.__avion_image_half_height

        # Copio una imagen (la que le paso en la ruta) y la ubico en la posicion que le paso. Ubica una imágen sobre otra.
        surface_dst.blit(self.__avion_image, self.render_rect)

    def release(self):
        pass

    def __allow_move_inside_limits(self, distance):
        new_pos = self._position + distance 
        if (new_pos.x < -self.__avion_image_half_width) or (new_pos.x > self.__screen_width - self.__avion_image_half_width) or (new_pos.y < -self.__avion_image_half_height) or (new_pos.y > self.__screen_height - self.__avion_image_half_height):
            return False
        return True

    def __map_input(self):
        key_mapping = cfg_item("input", "key_mapping")
        self.__key_mapping = {}

        for k, v in key_mapping.items():
            self.__key_mapping[k] = pygame.key.key_code(v)

    def __fire_projectile(self):
        self.__cool_down = cfg_item("entities", "avion", "cool_down")
        self.__callback_spawn_projectile(ProjectileType.AlliedProyectile, self.render_rect.midtop)