import pygame
import os
from config import cfg_item

class Bitmapfont:

    __rest_letters = ["0", "-", ".", ":", "?", "!", "(", ")", " "]

    def __init__(self):
        self.__image = pygame.image.load(os.path.join(*cfg_item("font", "path"))).convert_alpha()
        self.__font = dict()

        columns = cfg_item("font", "columns")
        letter_size = cfg_item("font", "letter_size")

        for i in range(cfg_item("font", "total_letters")):
            left = letter_size[0] * (i % columns)
            top = letter_size[1] * int(i / columns)
            self.__font[self.__map(i)] = pygame.Rect(left, top, letter_size[0], letter_size[1])

    def render(self, surface_dst, pos, char):
        surface_dst.blit(self.__image, pos, self.__font[char.upper()])

    def __map(self, number):
        if number >= 0 and number <= 25:
            character = chr(number + 65)
        elif number >= 26 and number <= 34:
            character = chr(number + 23)
        else:
            character = Bitmapfont.__rest_letters[number - 35]

        return character