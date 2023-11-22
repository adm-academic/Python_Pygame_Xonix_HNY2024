import pygame
import random
import os
import inspect
import sys

import settings
import scene_play

class Game():
    # допустимые сцены игры
    SCENE_INITIAL  = 1
    SCENE_SETTINGS = 2
    SCENE_LEVELS   = 3
    SCENE_PLAY     = 4
    SCENE_FINISH   = 5
    SCENE_EXIT     = 0
    def __init__(self):
        self.scene_code = self.SCENE_INITIAL
        print("Инициализация PyGame...")
        # ------ настройка интерпретатора питон
        sys.setrecursionlimit(50000)
        # ------ настройка путей для игры
        os.chdir(os.path.dirname(__file__))
        # ----- объект настроек для игры:
        self.settings = settings.Settings()
        # ------ создаем игру и окно
        pygame.init()  # инициализиуем pygame
        pygame.mixer.init()  # инициализиуем звуки pygame
        pygame.font.init() # инициализируем шрифты pygame
        pygame.display.set_caption("Xonix Happy New Year 2024 ! ")  # задаём заголовок окна игры
        self.screen = pygame.display.set_mode((self.settings.WIDTH,  # создаём окно игры и получаем объект-поверхность
                                          self.settings.HEIGHT))
        self.clock = pygame.time.Clock()  # создаём объект "Часы" для контоля за временем и частотой в игре
        self.pygame_font_name = pygame.font.match_font('arial')  # Получаем имя шрифта ближайшего к 'arial'

    def load_game(self):
        print("Старт загрузки игры Xonix HNY 2024...")

    def unload_game(self):
        print("Выгрузка игры...")
    def update(self):
        pass
    def draw(self):
        pass

    def exit_from_game(self):
        self.scene_code = self.SCENE_EXIT

    # функция отрисовки текста на поверхности
    def draw_text(self, surf, text, size, x, y):
        font = pygame.font.Font(self.pygame_font_name, size)  # создаём объект шрифта
        text_surface = font.render(text, True, self.settings.WHITE)  # рендерим текст шрифтом и получаем поверхность
        text_rect = text_surface.get_rect()  # получаем прямоугольник поверхности
        text_rect.midtop = (x, y)  # модифициуют прямоугольник, размещая его по переданным x,y
        surf.blit(text_surface, text_rect)  # блиттинг отрендеренного текста на переданную поверхность
    def main_loops(self): # здесь запускаются главные циклы сцен
        print("Запускаю главные циклы сцен...")
        while True:
            if   self.scene_code == self.SCENE_INITIAL:
                pass
            elif self.scene_code == self.SCENE_SETTINGS:
                pass
            elif self.scene_code == self.SCENE_LEVELS:
                pass
            elif self.scene_code == self.SCENE_PLAY:
                self.scene_play = scene_play.Scene_Play(self,self.settings)
                self.scene_play.scene_loop()
                pass
            elif self.scene_code == self.SCENE_FINISH:
                pass
            elif self.scene_code == self.SCENE_EXIT:
                print("Выход из обработки игровых сцен...")
                pygame.quit()
                exit()



game = Game()
game.load_game()
game.scene_code = game.SCENE_PLAY
game.main_loops()
game.unload_game()