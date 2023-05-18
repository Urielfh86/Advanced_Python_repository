import pygame
import os
from config import cfg_item

class Girl:

    def __init__(self):
        self.__walking_animation = pygame.image.load(os.path.join(*cfg_item("image", "path"))).convert_alpha()
        self.__initial_girl_pos = (cfg_item("girl", "pos"))
        self.__girl_pos = pygame.math.Vector2(self.__initial_girl_pos[0], self.__initial_girl_pos[1])
        self.__girl_frame = 0
        self.__girl_direction = "default" # Dirección en la que se está moviendo ("right", "left")
        self.__girl_jump = "no_jump" # ("jump")
        self.__jump_impulse = 10
        self.__key_is_pressed = False
        self.__last_time_frame = pygame.time.Clock()
        self.__time_frame = 0

        self.__girl_walking_right = {0 : self.__walking_animation.subsurface((0, 0), (64, 128)),
                                     1 : self.__walking_animation.subsurface((64, 0), (64, 128)),
                                     2 : self.__walking_animation.subsurface((128, 0), (64, 128)),
                                     3 : self.__walking_animation.subsurface((256, 0), (64, 128)),
                                     4 : self.__walking_animation.subsurface((320, 0), (64, 128)),
                                     5 : self.__walking_animation.subsurface((384, 0), (64, 128)),
                                     6 : self.__walking_animation.subsurface((448, 0), (64, 128)),
                                     7 : self.__walking_animation.subsurface((512, 0), (64, 128)),
                                     8 : self.__walking_animation.subsurface((576, 0), (64, 128))
                                    }

        self.__girl_walking_left = {0 : self.__walking_animation.subsurface((0, 128), (64, 128)),
                                    1 : self.__walking_animation.subsurface((64, 128), (64, 128)),
                                    2 : self.__walking_animation.subsurface((128, 128), (64, 128)),
                                    3 : self.__walking_animation.subsurface((256, 128), (64, 128)),
                                    4 : self.__walking_animation.subsurface((320, 128), (64, 128)),
                                    5 : self.__walking_animation.subsurface((384, 128), (64, 128)),
                                    6 : self.__walking_animation.subsurface((448, 128), (64, 128)),
                                    7 : self.__walking_animation.subsurface((512, 128), (64, 128)),
                                    8 : self.__walking_animation.subsurface((576, 128), (64, 128))    
                                    }

        self.__initial_image = self.__girl_walking_right[0]

    def update(self, delta_time):
        distance_to_move = cfg_item("girl", "speed") * delta_time

        if self.__girl_is_moving_right_and_right_arrow_is_pressed() and self.__girl_jump == "no_jump":
            self.__girl_pos.x += distance_to_move
        elif self.__girl_is_moving_left_and_left_arrow_is_pressed() and self.__girl_jump == "no_jump":
            self.__girl_pos.x -= distance_to_move
        elif self.__girl_is_moving_right_and_right_arrow_is_pressed() and self.__girl_jump == "jump":
            self.__girl_pos.x += distance_to_move
            self.__jump_handle()
        elif self.__girl_is_moving_left_and_left_arrow_is_pressed() and self.__girl_jump == "jump":
            self.__girl_pos.x -= distance_to_move
            self.__jump_handle()
        elif self.__girl_jump == "jump":
            self.__jump_handle()

    def render(self, surface):
        if self.__the_game_has_started_and_no_key_has_been_pressed():
            surface.blit(self.__initial_image, self.__girl_pos.xy)
        elif self.__girl_is_within_the_limits_of_the_screen_and_walking_right():
            frame = self.__obtain_frame_girl(self.__girl_walking_right)
            surface.blit(frame, self.__girl_pos.xy) 
        elif self.__girl_is_within_the_limits_of_the_screen_and_walking_left():
            frame = self.__obtain_frame_girl(self.__girl_walking_left)
            surface.blit(frame, self.__girl_pos.xy) 
        elif self.__girl_is_not_within_the_limits_of_the_screen_or_not_walking_right():
            surface.blit(self.__girl_walking_right[0], self.__girl_pos.xy)
        elif self.__girl_is_not_within_the_limits_of_the_screen_or_not_walking_left():
            surface.blit(self.__girl_walking_left[0], self.__girl_pos.xy)

    def handle_inputs(self, key, key_up):
        if key == pygame.K_RIGHT and not key_up:
            self.__key_is_pressed = True
            self.__girl_direction = "right"
        elif key == pygame.K_LEFT and not key_up:
            self.__key_is_pressed = True
            self.__girl_direction = "left"
        elif key == pygame.K_SPACE:
            self.__girl_jump = "jump"
        elif key_up and (key == pygame.K_RIGHT or key == pygame.K_LEFT):
            self.__key_is_pressed = False

    def __obtain_frame_girl(self, walking_animation_dict):
        delta_time_frame = self.__last_time_frame.tick(cfg_item("timing", "fps"))
        self.__time_frame += delta_time_frame  

        if self.__time_frame > cfg_item("timing", "time_to_change_frame_girl"):
            self.__time_frame = 0
            self.__girl_frame += 1
        if self.__girl_frame > (len(walking_animation_dict) - 1):
            self.__girl_frame = 1

        return walking_animation_dict[self.__girl_frame]

    def __the_game_has_started_and_no_key_has_been_pressed(self):
        if self.__girl_direction == "default" and not self.__key_is_pressed:
            return True
        else:
            return False

    def __girl_is_within_the_limits_of_the_screen_and_walking_right(self):
        if self.__girl_direction == "right" and self.__key_is_pressed and self.__girl_pos.x < (cfg_item("screen_size")[0] - cfg_item("girl", "size")[0]):
            return True
        else:
            return False

    def __girl_is_within_the_limits_of_the_screen_and_walking_left(self):
        if self.__girl_direction == "left" and self.__key_is_pressed and self.__girl_pos.x > 0:
            return True
        else:
            return False

    def __girl_is_not_within_the_limits_of_the_screen_or_not_walking_right(self):
        if self.__girl_direction == "right" and not self.__key_is_pressed or self.__girl_pos.x > (cfg_item("screen_size")[0] - cfg_item("girl", "size")[0]):
            return True
        else:
            return False

    def __girl_is_not_within_the_limits_of_the_screen_or_not_walking_left(self):
        if self.__girl_direction == "left" and not self.__key_is_pressed or self.__girl_pos.x < 0:
            return True
        else:
            return False

    def __girl_is_moving_right_and_right_arrow_is_pressed(self):
        if self.__girl_direction == "right" and self.__girl_pos.x < (cfg_item("screen_size")[0] - cfg_item("girl", "size")[0]) and self.__key_is_pressed:
            return True
        else:
            return False

    def __girl_is_moving_left_and_left_arrow_is_pressed(self):
        if self.__girl_direction == "left" and self.__girl_pos.x > 0 and self.__key_is_pressed:
            return True
        else:
            return False

    def __jump_handle(self):
        if self.__jump_impulse >= -10:
            if self.__jump_impulse < 0:
                self.__girl_pos.y += ((self.__jump_impulse ** 2) / 2) # Es una ecuación que describe una parábola invertida --> y = -(x^2)/2
            else:
                self.__girl_pos.y -= ((self.__jump_impulse ** 2) / 2)
            self.__jump_impulse -= 1
        else:
            self.__jump_impulse = 10
            self.__girl_jump = "no_jump"

    def release(self):
        pass