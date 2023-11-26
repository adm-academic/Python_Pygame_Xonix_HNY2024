import pygame
import random
import os
import inspect
import sys
from adm_gui import *

class Scene_Player_Select():
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
        self.button_cancel.set_params(130, 225, 50, 390,
                                      pygame.K_1, "Отменить и выйти.")
        pass
        self.buttons_players = pygame.sprite.Group()
        self.init_buttons_from_db()
        pass
    def unload_scene(self):
        pass
    def reload_scene(self):
        pass
    def init_buttons_from_db(self):
        query_players = " select * from Player; "
        cursor = self.settings.db_connection.cursor()
        cursor.execute(query_players)
        rows = cursor.fetchall()
        if len(rows) <= 0:
            return
        xx = 30
        yy = 200
        bwidth = 310
        bheight = 50
        vspace = 15
        hspace = 15
        idx = 1
        for row in rows:
            if (yy + bheight) >= self.settings.HEIGHT:
                xx = xx + bwidth + hspace
                yy = 200
            player_btn = Player_Button( self.game, self, self.settings )
            player_btn.set_params( yy, xx, bheight, bwidth, row[1] )
            self.buttons_players.add( player_btn )
            yy = yy + bheight + 15
            idx += 1
        pass
    def update(self):
        self.button_cancel.update()
        for btn in self.buttons_players:
            btn.update()
        pass
    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
        self.button_cancel.draw(self.game.screen)
        for btn in self.buttons_players:
            btn.draw( self.game.screen )
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game.go_to_scene(self.game.SCENE_INITIAL)
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if self.button_cancel.rect.collidepoint(mouse_position):
                        self.game.go_to_scene(self.game.SCENE_INITIAL)
                        return
                    for button in self.buttons_players:
                        if button.rect.collidepoint(mouse_position):
                            self.game.player.load_from_db( button.text )
                            pass

            self.update()
            self.draw()

            self.game.draw_text(self.game.screen, "Выбираем имеющегося игрока.", 40,
                                self.settings.WIDTH // 2,
                                0,
                                self.settings.GREEN)
            self.game.draw_text(self.game.screen, '''играет "%s"''' % self.game.player.name, 40,
                                self.settings.WIDTH // 2,
                                50,
                                self.settings.GREEN)

            pygame.display.flip()