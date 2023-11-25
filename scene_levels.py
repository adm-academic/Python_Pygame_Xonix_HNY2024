import pygame
import random
import os
import inspect
import sys

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
    def unload_scene(self):
        self.game.screen.fill(self.settings.BLACK)  # заполняем всё окно чёрным
        pass
    def reload_scene(self):
        pass
    def update(self):
        pass
    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
    def scene_loop(self):
        while True:
            self.game.clock.tick(self.settings.FPS)  # задаём кадры в секунду
            for event in pygame.event.get():  # перебираем все поступившие события
                if event.type == pygame.QUIT:  # событие выхода из программы
                    self.game.exit_from_game()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game.go_to_scene(self.game.SCENE_INITIAL)
                    return

            self.update()
            self.draw()

            self.game.draw_text (self.game.screen, "Сцена выбора уровней.", 72,
                                 self.settings.WIDTH // 2,
                                 self.settings.HEIGHT // 2 ,
                                 self.settings.GREEN)

            pygame.display.flip()