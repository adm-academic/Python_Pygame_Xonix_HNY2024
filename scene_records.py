import pygame
import random
import os
import inspect
import sys

class Scene_Records():
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

                self.update()
                self.draw()

                self.game.draw_text(self.game.screen, "Рекорды.", 40,
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

                query_top_5 = """
                              SELECT *
                              FROM   (
                              SELECT *
                              FROM  Player pi
                              ORDER BY pi.id 
                              ) as po
                              ORDER BY po.score desc
                              LIMIT 5;
                              """
                cursor = self.settings.db_connection.cursor()
                cursor.execute(query_top_5)
                rows = cursor.fetchall()
                cursor.close()
                yy = 250
                for row in rows:
                    self.game.draw_text_left_top(self.game.screen,
                                               str(row[1]) + " : " + str(row[2]),
                                               51,
                                               300,
                                               yy,
                                               self.settings.YELLOW
                                               )
                    yy += 70


                pygame.display.flip()
        except Exception as e:
            print('EXCEPTION: ', e)
            self.game.go_to_scene(self.game.SCENE_INITIAL)
            return