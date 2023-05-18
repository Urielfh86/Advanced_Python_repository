import pygame
import os
from config import cfg_item
from girl import Girl
from fps_stats import FPSStats

class Game:

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(cfg_item("screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("title"))
        font = pygame.font.Font(os.path.join(*cfg_item("font", "path")), cfg_item("font", "size"))

        self.__running = False

        self.__girl = Girl()
        self.__fps_stats = FPSStats(font)

    def run(self):
        last_time = pygame.time.get_ticks()
        time_since_last_update = 0

        self.__running = True
        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time) 
            time_since_last_update += delta_time

            while time_since_last_update > cfg_item("timing", "time_per_frame"):
                time_since_last_update -= cfg_item("timing", "time_per_frame")
                self.__process_events()
                self.__update(cfg_item("timing", "time_per_frame"))
            
            self.__render()
                
        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                self.__girl.release()
            if event.type == pygame.KEYDOWN:
                __key_up = False
                self.__girl.handle_inputs(event.key, __key_up)
            if event.type == pygame.KEYUP:
                __key_up = True
                self.__girl.handle_inputs(event.key, __key_up)
                
    def __update(self, delta_time):
        self.__girl.update(delta_time)
        self.__fps_stats.update(delta_time)

    def __render(self):
        self.__screen.fill(cfg_item("background_color"))
        pygame.draw.rect(self.__screen, cfg_item("scene", "floor_color"), (cfg_item("scene", "floor_pos"), cfg_item("scene", "floor_size")))
        pygame.draw.circle(self.__screen, cfg_item("scene", "sun_color"), cfg_item("scene", "sun_pos"), cfg_item("scene", "sun_radio"))

        self.__girl.render(self.__screen)
        self.__fps_stats.render(self.__screen)

        pygame.display.update()

    def __quit(self):
        pygame.quit()

    def __calc_delta_time(self, last_time):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        return delta_time, current_time

    
            
        


