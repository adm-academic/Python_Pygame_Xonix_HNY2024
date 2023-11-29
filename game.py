import sys
import os
sys.path.append( os.path.dirname(__file__) )
import pygame
import random
import inspect

import settings
import player
import level_load_info
import scene_initial
import scene_levels
import scene_play
import scene_settings
import scene_records
import scene_player_new
import scene_player_select
import scene_finish
import scene_help

class Game():
    # допустимые сцены игры
    SCENE_INITIAL     = 1
    SCENE_SETTINGS    = 2
    SCENE_LEVELS      = 3
    SCENE_PLAY        = 4
    SCENE_FINISH      = 5
    SCENE_RECORDS     = 6
    SCENE_PLAYER_NEW  = 7
    SCENE_PLAYER_SELECT = 8
    SCENE_HELP        = 9
    SCENE_EXIT        = 0
    def __init__(self):
        self.code_of_scene = self.SCENE_INITIAL
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

    def load_game(self):
        print("Старт загрузки игры Xonix HNY 2024...")
        self.player = player.Player(self,self.settings)
        self.level_load_info = level_load_info.Level_Load_Info(self, self.settings)
        self.scene_initial = scene_initial.Scene_Initial(self, self.settings)
        self.scene_play = scene_play.Scene_Play(self, self.settings)
        self.scene_settings = scene_settings.Scene_Settings(self, self.settings)
        self.scene_levels = scene_levels.Scene_Levels(self, self.settings)
        self.scene_finish = scene_finish.Scene_Finish(self, self.settings)
        self.scene_records = scene_records.Scene_Records(self,self.settings)
        self.scene_player_new = scene_player_new.Scene_Player_New(self, self.settings)
        self.scene_player_select = scene_player_select.Scene_Player_Select(self,self.settings)
        self.scene_help = scene_help.Scene_Help(self,self.settings)

    def unload_game(self):
        print("Выгрузка игры...")

    def update(self):
        pass

    def draw(self):
        pass

    def exit_from_game(self):
        self.code_of_scene = self.SCENE_EXIT

    def go_to_scene(self,scene_code):
        self.scene_initial.unload_scene()
        self.scene_settings.unload_scene()
        self.scene_levels.unload_scene()
        self.scene_play.unload_scene()
        self.scene_finish.unload_scene()
        self.scene_records.unload_scene()
        self.scene_player_new.unload_scene()
        self.scene_help.unload_scene()
        pass
        self.code_of_scene = scene_code
        pass

    # функция отрисовки текста на поверхности
    def draw_text(self, surf, text, size, x, y, color ):
        font = pygame.font.Font(self.settings.pygame_font_name, size)  # создаём объект шрифта
        text_surface = font.render(text, True, color )  # рендерим текст шрифтом и получаем поверхность
        text_rect = text_surface.get_rect()  # получаем прямоугольник поверхности
        text_rect.midtop = (x, y)  # модифициуют прямоугольник, размещая его по переданным x,y
        surf.blit(text_surface, text_rect)  # блиттинг отрендеренного текста на переданную поверхность

    def draw_text_center(self, surf, text, size, x, y, color ):
        font = pygame.font.Font(self.settings.pygame_font_name, size)  # создаём объект шрифта
        text_surface = font.render(text, True, color )  # рендерим текст шрифтом и получаем поверхность
        text_rect = text_surface.get_rect()  # получаем прямоугольник поверхности
        text_rect.center = (x, y)  # модифициуют прямоугольник, размещая его по переданным x,y
        surf.blit(text_surface, text_rect)  # блиттинг отрендеренного текста на переданную поверхность
    def draw_text_left_top(self, surf, text, size, x, y, color ):
        font = pygame.font.Font(self.settings.pygame_font_name, size)  # создаём объект шрифта
        text_surface = font.render(text, True, color )  # рендерим текст шрифтом и получаем поверхность
        text_rect = text_surface.get_rect()  # получаем прямоугольник поверхности
        text_rect.topleft = (x, y)  # модифициуют прямоугольник, размещая его по переданным x,y
        surf.blit(text_surface, text_rect)  # блиттинг отрендеренного текста на переданную поверхность
    def main_loops(self): # здесь запускаются главные циклы сцен
        print("Запускаю главные циклы сцен...")
        while True:
            if self.code_of_scene == self.SCENE_PLAYER_NEW:
                self.scene_player_new.unload_scene()
                self.scene_player_new.load_scene()
                self.scene_player_new.scene_loop()
            elif self.code_of_scene == self.SCENE_PLAYER_SELECT:
                self.scene_player_select.unload_scene()
                self.scene_player_select.load_scene()
                self.scene_player_select.scene_loop()
            elif self.code_of_scene == self.SCENE_INITIAL:
                self.scene_initial.unload_scene()
                self.scene_initial.load_scene()
                self.scene_initial.scene_loop()
                pass
            elif self.code_of_scene == self.SCENE_SETTINGS:
                self.scene_settings.unload_scene()
                self.scene_settings.load_scene()
                self.scene_settings.scene_loop()
                pass
            elif self.code_of_scene == self.SCENE_LEVELS:
                self.scene_levels.unload_scene()
                self.scene_levels.load_scene()
                self.scene_levels.scene_loop()
                pass
            elif self.code_of_scene == self.SCENE_PLAY:
                self.scene_play.unload_scene()
                self.scene_play.load_scene()
                self.scene_play.scene_loop()
                pass
            elif self.code_of_scene == self.SCENE_RECORDS:
                self.scene_records.unload_scene()
                self.scene_records.load_scene()
                self.scene_records.scene_loop()
            elif self.code_of_scene == self.SCENE_FINISH:
                self.scene_finish.unload_scene()
                self.scene_finish.load_scene()
                self.scene_finish.scene_loop()
                pass
            elif self.code_of_scene == self.SCENE_HELP:
                self.scene_help.unload_scene()
                self.scene_help.load_scene()
                self.scene_help.scene_loop()
            elif self.code_of_scene == self.SCENE_EXIT:
                print("Выход из обработки игровых сцен...")
                pygame.quit()
                exit()
            else:
                pygame.time.delay(300)


game = Game()
game.load_game()
game.go_to_scene( game.SCENE_INITIAL )
game.main_loops()
game.unload_game()
