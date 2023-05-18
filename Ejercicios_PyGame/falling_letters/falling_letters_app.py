import pygame
import os
import random
from letters import Letter

class Game:

    __screen_size = (640, 480)
    __title = "Falling Letters"
    __fps = 60
    __background_color = (0, 0, 0)
    __font_path = ["assets", "font", "Sansation.ttf"]
    __font_size = 40

    def __init__(self):
        pygame.init()

        self.__screen = pygame.display.set_mode(Game.__screen_size, 0, 32)
        pygame.display.set_caption(Game.__title)

        self.__running = False
        self.__fps_clock = pygame.time.Clock()

        self.__letters = []

        self.__font = pygame.font.Font(os.path.join(*Game.__font_path), Game.__font_size)

    def run(self):

        self.__running = True
        while self.__running:
            delta_time = self.__fps_clock.tick(Game.__fps)
            self.__process_events()
            self.__update(delta_time)
            self.__render()

        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                self.__spawn_letter(event.unicode)

    def __update(self, delta_time):
        
        for letter in self.__letters:
            if letter.is_alive():
                letter.update(delta_time)
            else:
                self.__letters.remove(letter)

    def __render(self):

        self.__screen.fill(Game.__background_color)

        for letter in self.__letters:
            letter.render(self.__screen)

        pygame.display.update()

    def __quit(self):
        pygame.quit()

    def __spawn_letter(self, text):
        x_pos = random.randrange(Game.__font_size, Game.__screen_size[0] - Game.__font_size)
        init_pos = pygame.math.Vector2(x_pos, -Game.__font_size)
        end_pos = pygame.math.Vector2(x_pos, Game.__screen_size[1] + Game.__font_size)

        self.__letters.append(Letter(text, init_pos, end_pos, self.__font))