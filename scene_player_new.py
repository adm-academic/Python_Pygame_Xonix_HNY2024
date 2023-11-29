import pygame
import random
import os
import inspect
import sys
from adm_gui import *

class Scene_Player_New():
    def __init__(self, game, settings):  # констуктор
        self.game = game
        self.settings = settings
        pass
    def load_scene(self):
        self.image_backround = pygame.image.load("images/initial_background.jpg").convert()
        self.image_backround = pygame.transform.scale(self.image_backround,
                                                      (self.settings.WIDTH, self.settings.HEIGHT))
        self.image_backround_rect = self.image_backround.get_rect()
        self.input_box_new_player_name = InputBox(self.game, self.settings,
                                                  self.settings.WIDTH // 2 - 400,
                                                  self.settings.HEIGHT // 2,
                                                  800, 64, )
        self.button_cancel = Menu_Button(self.game, self, self.settings)
        self.button_cancel.set_params(self.settings.HEIGHT // 2 + 100, 310, 50, 390,
                                        pygame.K_1, "Отменить и выйти.")
        self.button_confirm = Menu_Button(self.game, self, self.settings)
        self.button_confirm.set_params(self.settings.HEIGHT // 2 + 100, 710, 50, 390,
                                        pygame.K_2, "Создать игрока.")
        pass
    def unload_scene(self):
        self.game.screen.fill(self.settings.BLACK)  # заполняем всё окно чёрным
        if hasattr(self,'input_box_new_player_name') and \
            self.input_box_new_player_name != None:
            del self.input_box_new_player_name
            self.input_box_new_player_name = None
        pass
    def reload_scene(self):
        pass
    def update(self):
        self.input_box_new_player_name.update()
        self.button_cancel.update()
        self.button_confirm.update()
    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
        self.input_box_new_player_name.draw(self.game.screen)
        self.button_cancel.draw(self.game.screen)
        self.button_confirm.draw(self.game.screen)
    def create_player(self,player_name):
        pass
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
                        if event.key == pygame.K_2:
                            new_pl_name = self.input_box_new_player_name.text
                            if new_pl_name.strip() != "":
                                self.game.player.create_new_player(new_pl_name)
                                self.game.go_to_scene(self.game.SCENE_INITIAL)
                                return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        if self.button_cancel.rect.collidepoint(mouse_position):
                            self.game.go_to_scene(self.game.SCENE_INITIAL)
                            return
                        if self.button_confirm.rect.collidepoint(mouse_position):
                            new_pl_name = self.input_box_new_player_name.text
                            if new_pl_name.strip() != "":
                                self.game.player.create_new_player(new_pl_name)
                                self.game.go_to_scene(self.game.SCENE_INITIAL)
                                return

                    self.input_box_new_player_name.handle_event(event)

                self.update()

                self.draw()

                self.game.draw_text(self.game.screen, "Регистрируем нового игрока.", 40,
                                    self.settings.WIDTH // 2,
                                    0,
                                    self.settings.GREEN)
                self.game.draw_text(self.game.screen,
                                    '''играет "%s". Очков: %s''' % (
                                        self.game.player.name, self.game.player.get_score()),
                                    40,
                                    self.settings.WIDTH // 2,
                                    40,
                                    self.settings.GREEN)

                pygame.display.flip()
        except Exception as e:
            print('EXCEPTION: ', e)
            self.game.go_to_scene(self.game.SCENE_INITIAL)
            return