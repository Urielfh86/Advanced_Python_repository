import pygame
from config import cfg_item
from bitmapfont import Bitmapfont

class Scroll:
    def __init__(self):
        self.__text = cfg_item("scroll", "text")
        self.__pos = pygame.math.Vector2(cfg_item("screen_size")[0], cfg_item("screen_size")[1] / 2)
        self.__bitmapfont = Bitmapfont()
        self.__letters_in_screen = int(cfg_item("screen_size")[0] / cfg_item("font", "letter_size")[0]) + 1
        self.__current_letter_index = 0

    def update(self, delta_time):
        self.__pos.x -= cfg_item("scroll", "speed") * delta_time

        if self.__pos.x <= -cfg_item("font", "letter_size")[0]:
            self.__pos.x = 0
            self.__current_letter_index += 1

    def render(self, surface_dst):
        for i in range(self.__letters_in_screen):
            index = (self.__current_letter_index + i) % len(self.__text)
            letter = self.__text[index]
            pos = (self.__pos.x + (cfg_item("font", "letter_size")[0] * i), self.__pos.y)
            self.__bitmapfont.render(surface_dst, pos, letter)