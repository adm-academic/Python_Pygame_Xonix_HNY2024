import pygame
import random
import os
import inspect
import sys
from adm_gui import *

class Scene_Finish():
    def __init__(self, game, settings):  # констуктор
        self.game = game
        self.settings = settings
        pass
    def load_scene(self):
        self.FPS = 30
        self.image_backround = pygame.image.load("images/final/final_0.gif").convert()
        self.image_backround = pygame.transform.scale(self.image_backround,
                                                      (self.settings.WIDTH, self.settings.HEIGHT))
        self.image_backround_rect = self.image_backround.get_rect()
        self.animation_count = 0
        self.ANIMATION_MAX = 14
        self.button_exit = Menu_Button(self.game,self,self.settings)
        self.button_exit.set_params(self.settings.HEIGHT - 45,
                                    110,
                                    50,
                                    180,
                                    pygame.K_1,
                                    "Выйти")
        #self.button_save = Menu_Button(self.game,self,self.settings)
        #self.button_save.set_params( self.settings.HEIGHT - 45,
        #                             self.settings.WIDTH - 150,
        #                            50,
        #                            260,
        #                             pygame.K_2,
        #                            "Сохранить" )
        pass
    def unload_scene(self):
        self.game.screen.fill(self.settings.BLACK)  # заполняем всё окно чёрным
        pass
    def reload_scene(self):
        pass
    def update(self):
        self.animation_count += 1
        if self.animation_count > self.ANIMATION_MAX:
            self.animation_count = 0
        self.image_backround = pygame.image.load("images/final/final_" +
                                                 str(self.animation_count) + ".gif").convert()
        self.image_backround = pygame.transform.scale(self.image_backround,
                                                      (self.settings.WIDTH, self.settings.HEIGHT))
        self.image_backround_rect = self.image_backround.get_rect()
        #self.button_save.update()
        self.button_exit.update()
        pass
    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
        #self.button_save.draw(self.game.screen)
        self.button_exit.draw(self.game.screen)
        pass
    def scene_loop(self):
        try:
            while True:
                self.game.clock.tick(self.FPS)  # задаём кадры в секунду
                for event in pygame.event.get():  # перебираем все поступившие события
                    if event.type == pygame.QUIT:  # событие выхода из программы
                        self.game.exit_from_game()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game.go_to_scene(self.game.SCENE_INITIAL)
                        return
                    #if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    #    pass
                    #    pass
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                        self.game.go_to_scene(self.game.SCENE_LEVELS)
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        #if self.button_save.rect.collidepoint(mouse_position):
                        #    pass
                        #    pass
                        if self.button_exit.rect.collidepoint(mouse_position):
                            self.game.go_to_scene(self.game.SCENE_LEVELS)
                            return

                self.update()
                self.draw()

                pygame.display.flip()

        except Exception as e:
            print('EXCEPTION: ', e)
            self.game.go_to_scene(self.game.SCENE_INITIAL)
            return