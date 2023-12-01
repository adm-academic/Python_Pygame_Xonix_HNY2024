import pygame
import random
import os
import inspect
import sys
from adm_gui import *

class Scene_Help():
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
    def unload_scene(self):
        self.game.screen.fill(self.settings.BLACK)  # заполняем всё окно чёрным
        pass
    def reload_scene(self):
        pass
    def update(self):
        self.button_cancel.update()
        pass
    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
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

                self.update()
                self.draw()

                self.game.draw_text(self.game.screen, "Помощь.", 40,
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

                pygame.draw.rect( self.game.screen, self.settings.DARK_GRAY,
                                  (105,170,
                                        825, 560 ) )
                pygame.draw.rect(self.game.screen, self.settings.GREEN,
                                 (115, 180,
                                  805, 540), 5)

                self.game.draw_text_left_top(self.game.screen,
                                             "Это игра Xonix созданная к 'Году Деревянного Дракона',",
                                             25,
                                             140,
                                             170+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "который наступает в 2024 году. Xonix (читается Ксоникс)",
                                             25,
                                             140,
                                             200+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "очень простая игра. Игровое поле состоит из границы ",
                                             25,
                                             140,
                                             230+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "оранжевого цвета, маленького красного квадрата - это " ,
                                             25,
                                             140,
                                             260+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "игрок, маленьких синих кружочков - это 'враги'. И ",
                                              25,
                                              140,
                                              290+30,
                                              self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "конечно большого голубого пространства которое нужно ",
                                             25,
                                             140,
                                             320+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "воспринимать как поляну со снегом, под которой скрыта",
                                             25,
                                             140,
                                             350+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "новогодняя картинка с драконом. Игрок перемещается с помощью",
                                             25,
                                             140,
                                             380+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "стрелок на клавиатуре. Во время движения по снежной 'поляне' ",
                                             25,
                                             140,
                                             410+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "он оставляет за собой след. Нужно 'рисовать' этим следом  ",
                                             25,
                                             140,
                                             440+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "замкнутые области на 'снегу', после этого замкнутая область ",
                                             25,
                                             140,
                                             470+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "со снегом исчезнет. Если врезатся в свой след или допустить ",
                                             25,
                                             140,
                                             500+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "столкновение 'врагов' со своим следом - то уровень игры ",
                                             25,
                                             140,
                                             530+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "перезапустится и у игрока спишутся очки.Если 'открыть' 85 ",
                                             25,
                                             140,
                                             560+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "и более процентов снежной поляны то игроку засчитается выигрыш",
                                             25,
                                             140,
                                             590+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "и открывается картинка с новогодним Драконом.И игроку ",
                                             25,
                                             140,
                                             620+30,
                                             self.settings.GREEN)
                self.game.draw_text_left_top(self.game.screen,
                                             "начисляются очки. Переигрывать можно сколько угодно раз.",
                                             25,
                                             140,
                                             650+30,
                                             self.settings.GREEN)

                pygame.display.flip()
        except Exception as e:
            print('EXCEPTION: ', e)
            self.game.go_to_scene(self.game.SCENE_INITIAL)
            return