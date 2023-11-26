import pygame
import random
import os
import inspect
import sys


class Menu_Button(pygame.sprite.Sprite):
    def __init__(self, game, scene, settings ):  # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.scene = scene
        self.settings = settings
    def set_params(self, y_center,  # координата кнопки
                   x_center,  # координата кнопки
                   height,  # высота кнопки
                   width,  # ширина кнопки
                   hot_key,  # "горячая клавиша" кнопки, от 0 до 9
                   text,  # текст, отобажаемый на кнопке
                   ):
        self.rect = pygame.Rect((0, 0), (width, height))
        self.rect.centerx = x_center
        self.rect.centery = y_center
        self.hot_key = hot_key
        self.text = text
        self.is_over = False
    def key_to_string(self,key):
        if   key==pygame.K_0:
            return "0"
        elif key==pygame.K_1:
            return "1"
        elif key==pygame.K_2:
            return "2"
        elif key==pygame.K_3:
            return "3"
        elif key==pygame.K_4:
            return "4"
        elif key==pygame.K_5:
            return "5"
        elif key==pygame.K_6:
            return "6"
        elif key==pygame.K_7:
            return "7"
        elif key==pygame.K_8:
            return "8"
        elif key==pygame.K_9:
            return "9"

    def update(self):
        pointer = pygame.mouse.get_pos()
        if self.rect.collidepoint(pointer):  # if pointer is inside btnRect
            self.is_over = True
        else:
            self.is_over = False
    def draw(self, surface):
        small_rect = self.rect.copy()
        small_rect.width = self.rect.height
        pygame.draw.rect( surface, self.settings.GRAY, self.rect )
        pygame.draw.rect( surface, self.settings.YELLOW, small_rect )
        if self.is_over:
            pygame.draw.rect( surface, self.settings.YELLOW, self.rect, 8 )
        self.game.draw_text(self.game.screen, self.key_to_string(self.hot_key), 50,
                            small_rect.centerx,
                            small_rect.top + 2,
                            self.settings.BLUE )
        self.game.draw_text(self.game.screen, self.text, 40,
                            self.rect.centerx + small_rect.width // 2,
                            small_rect.top + 6,
                            self.settings.ORANGE)

class Player_Button(pygame.sprite.Sprite):
    def __init__(self, game, scene, settings):  # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.scene = scene
        self.settings = settings
    def set_params(self,
                   y_top,  # координата кнопки
                   x_left,  # координата кнопки
                   height,  # высота кнопки
                   width,  # ширина кнопки
                   text,  # текст, отобажаемый на кнопке
                   ):
        self.rect = pygame.Rect((0, 0), (width, height))
        self.rect.left = x_left
        self.rect.top = y_top
        self.text = text
        self.is_over = False
    def update(self):
        pointer = pygame.mouse.get_pos()
        if self.rect.collidepoint(pointer):  # if pointer is inside btnRect
            self.is_over = True
        else:
            self.is_over = False
    def draw(self, surface):
        small_rect = self.rect.copy()
        small_rect.width = self.rect.height
        small_rect.x = self.rect.right - small_rect.width
        pygame.draw.rect(surface, self.settings.GRAY, self.rect)
        #pygame.draw.rect(surface, self.settings.BLUE, small_rect)
        if self.is_over:
            pygame.draw.rect(surface, self.settings.YELLOW, self.rect, 8)
        #self.game.draw_text(self.game.screen, "X", 50,
        #                    small_rect.centerx,
        #                    small_rect.top + 2,
        #                    self.settings.WHITE)
        self.game.draw_text(self.game.screen, self.text, 40,
                            self.rect.centerx ,
                            small_rect.top + 6,
                            self.settings.ORANGE)


class InputBox:
    def __init__(self,game,settings, x, y, w, h, text=''):
        self.game = game
        self.settings = settings
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.settings.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.settings.INPUT_FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.settings.COLOR_ACTIVE if self.active else self.settings.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.settings.INPUT_FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.settings.BLACK, self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Level_Button(pygame.sprite.Sprite):
    # кнопки уровней я решил сделать "умными", они сами "ходят" БД и сами
    # находят картинки. сами отрисовываются. Им нужны только координаты left-top
    # и номер уровня, который должна отображать кнопка
    def __init__(self, game, scene, settings):  # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.scene = scene
        self.settings = settings
    def set_params(self,
                   y_top,  # координата кнопки
                   x_left,  # координата кнопки
                   height,
                   width,
                   level_number  # номер уровня, открываемый кнопкой
                   ):
        self.rect = pygame.Rect((0, 0), (width, height))
        self.rect.left = x_left
        self.rect.top = y_top
        self.rect.width = width
        self.rect.height = height
        self.level_number = level_number
        self.allowed = True
        self.is_over = False
        self.lock_image = pygame.image.load( os.path.join( "levels", "lock.png") ).convert()
        self.lock_image.set_colorkey(self.settings.BLACK)
        self.lock_image = pygame.transform.scale(self.lock_image,
                                                (self.rect.width, self.rect.height))
        self.read_from_db()
    def read_from_db(self):
        query_level = """   select  p.id player_id, p.name name,
                                    cl.score score, 
                                    pl.id level_id, pl.backround_image image
                            from    Player p left outer join  
                                    Completed_Level cl on p.id = cl.player_id left outer join
                                    Possible_Level pl ON cl.possible_level_id = pl.id 
                            WHERE   p.id  = %s and
	                                pl.id = %s 
                     """ % ( self.game.player.id, self.level_number )
        cursor = self.settings.db_connection.cursor()
        cursor.execute(query_level)
        rows = cursor.fetchall()
        if len(rows)  <= 0:
            if self.level_number == 1:
                self.allowed = True
                image_path = os.path.join("levels", "dragon1.jpg")
                self.level_image = pygame.image.load(image_path).convert()
                self.level_image = pygame.transform.scale(self.level_image,
                                                          (self.rect.width, self.rect.height))
            else:
                self.allowed = False
            return
        elif len(rows) == 1:
            for row in rows:
                self.allowed = True
                image_path = os.path.join( "levels", row[4] )
                self.level_image = pygame.image.load( image_path ).convert()
                self.level_image = pygame.transform.scale(self.level_image,
                                                          (self.rect.width, self.rect.height))
                return
        else:
            self.allowed = False
            print("ERROR! Rows must be 1 ONE !!!! ")
            return
    def update(self):
        pointer = pygame.mouse.get_pos()
        if self.rect.collidepoint(pointer):  # if pointer is inside btnRect
            self.is_over = True
        else:
            self.is_over = False
    def draw(self, surface):
        image_rect = self.rect.copy()
        image_rect.x -= 4
        image_rect.y -= 4
        image_rect.width += 8
        image_rect.height += 8
        pygame.draw.rect(surface, self.settings.GRAY, image_rect)
        if self.allowed:
            self.game.screen.blit(self.level_image, self.rect)
        else:
            self.game.screen.blit(self.lock_image, self.rect)
        pygame.draw.rect(surface, self.settings.BLACK, self.rect, 5)
        if self.is_over:
            pygame.draw.rect(surface, self.settings.YELLOW, self.rect, 8)
        self.game.draw_text_center(self.game.screen, str(self.level_number), 50,
                            self.rect.centerx ,
                            self.rect.centery,
                            self.settings.RED)
