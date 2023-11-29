import pygame
import random
import os
import inspect
import sys
from adm_gui import *

class Scene_Settings():
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
        self.input_box_FPS = InputBox(self.game, self.settings,
                                      200,
                                      300,
                                      620, 64,
                                      text=str(self.settings.get_FPS()),
                                      label="FPS игрового уровня.")
        pass
        self.button_cancel = Menu_Button(self.game, self, self.settings)
        self.button_cancel.set_params(400, 310, 50, 390,
                                      pygame.K_q, "Отменить и выйти.")
        self.button_confirm = Menu_Button(self.game, self, self.settings)
        self.button_confirm.set_params(400, 710, 50, 390,
                                       pygame.K_w, "Сохранить.")
        pass

    def unload_scene(self):
        self.game.screen.fill(self.settings.BLACK)  # заполняем всё окно чёрным
        pass
    def reload_scene(self):
        pass
    def update(self):
        self.button_cancel.update()
        self.button_confirm.update()
        self.input_box_FPS.update()
        pass
    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
        self.button_cancel.draw(self.game.screen)
        self.button_confirm.draw(self.game.screen)
        self.input_box_FPS.draw(self.game.screen)
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
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        self.game.go_to_scene(self.game.SCENE_INITIAL)
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        fps = self.input_box_FPS.text
                        if fps.strip() != "":
                            self.settings.save_FPS(float(self.input_box_FPS.text))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        if self.button_cancel.rect.collidepoint(mouse_position):
                            self.game.go_to_scene(self.game.SCENE_INITIAL)
                            return
                        if self.button_confirm.rect.collidepoint(mouse_position):
                            fps = self.input_box_FPS.text
                            if fps.strip() != "":
                                self.settings.save_FPS(int(self.input_box_FPS.text))

                    self.input_box_FPS.handle_event(event)

                self.update()
                self.draw()

                self.game.draw_text(self.game.screen, "Настройки.", 40,
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