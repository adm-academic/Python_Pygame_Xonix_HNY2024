import pygame
import random
import os
import inspect
import sys
from adm_gui import *

class Scene_Levels():
    def __init__(self, game, settings):  # констуктор
        self.game = game
        self.settings = settings
        pass
    def load_scene(self):
        self.image_backround = pygame.image.load("images/initial_background.jpg").convert()
        self.image_backround = pygame.transform.scale(self.image_backround,
                                                      (self.settings.WIDTH, self.settings.HEIGHT))
        self.image_backround_rect = self.image_backround.get_rect()
        pass
        self.button_cancel = Menu_Button(self.game, self, self.settings)
        self.button_cancel.set_params(130, 140, 50, 200,
                                      pygame.K_1, "Выйти.")
        pass
        self.buttons_levels = pygame.sprite.Group()
        idx = 1
        b_width = 160
        b_height = 120
        b_horizontal_space = 45
        b_vertical_space = 15
        b_x_start = 130
        b_y_start = 170
        for i_vertical in range(4):
            for j_horizontal in range(4):
                button_level = Level_Button( self.game, self, self.settings )
                button_level.set_params(
                        b_y_start + (i_vertical * b_height)+(i_vertical * b_vertical_space),
                        b_x_start + (j_horizontal * b_width)+(j_horizontal * b_horizontal_space),
                        b_height,
                        b_width,
                        idx
                                         )
                self.buttons_levels.add(button_level)
                idx += 1
        pass
    def unload_scene(self):
        self.game.screen.fill(self.settings.BLACK)  # заполняем всё окно чёрным
        pass
    def reload_scene(self):
        pass
    def update(self):
        for btn in self.buttons_levels:
            btn.update()
        self.button_cancel.update()
        pass
    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
        for btn in self.buttons_levels:
            btn.draw(self.game.screen)
        self.button_cancel.draw(self.game.screen)
    def scene_loop(self):
        try:
            while True:
                self.game.clock.tick(self.settings.FPS)  # задаём кадры в секунду
                for event in pygame.event.get():  # перебираем все поступившие события
                    if event.type == pygame.QUIT:  # событие выхода из программы
                        self.game.exit_from_game()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game.go_to_scene(self.game.SCENE_INITIAL)
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.game.go_to_scene(self.game.SCENE_INITIAL)
                            return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        if self.button_cancel.rect.collidepoint(mouse_position):
                            self.game.go_to_scene(self.game.SCENE_INITIAL)
                            return
                        for button_level in self.buttons_levels:
                            if button_level.rect.collidepoint(mouse_position):
                                if button_level.allowed:
                                    self.game.level_load_info.read_level_with_number_from_db(button_level.level_number)
                                    print( "@@@ MUST BE LOAD LEVEL - ", button_level.level_number )
                                    self.game.go_to_scene( self.game.SCENE_PLAY )
                                    return

                self.update()
                self.draw()

                self.game.draw_text (self.game.screen, "Сцена выбора уровней.", 40,
                                     self.settings.WIDTH // 2,
                                     0 ,
                                     self.settings.GREEN)
                self.game.draw_text(self.game.screen, '''играет "%s"''' % self.game.player.name, 40,
                                    self.settings.WIDTH // 2,
                                    50,
                                    self.settings.GREEN)

                pygame.display.flip()
        except Exception as e:
            print('EXCEPTION: ', e)
            self.game.go_to_scene(self.game.SCENE_INITIAL)
            return