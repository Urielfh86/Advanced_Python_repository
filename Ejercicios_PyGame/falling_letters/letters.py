import random
import pygame

class Letter():

    __speed_range = [0.1, 1.0]

    def __init__(self, text, init_pos, end_pos, font):
        self.__speed = random.uniform(*Letter.__speed_range)
        self.__position = init_pos
        self.__end_pos = end_pos

        self.__image = font.render(f"{text}", True, self.__random_color(), None)

        self.__alive = True

    def update(self, delta_time):
        self.__position.y += self.__speed * delta_time

        if self.__position.y >= self.__end_pos.y:
            self.__alive = False

    def render(self, surface_dst):
        surface_dst.blit(self.__image, self.__position.xy)

    def __random_color(self):
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)

        return pygame.Color(r, g, b)

    def is_alive(self):
        return self.__alive

    
