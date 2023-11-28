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
        self.next_level = False
        self.lock_image = pygame.image.load( os.path.join( "levels", "lock.png") ).convert()
        self.lock_image.set_colorkey(self.settings.BLACK)
        self.lock_image = pygame.transform.scale(self.lock_image,
                                                (self.rect.width, self.rect.height))
        self.read_from_db()
    def read_from_db(self):
        # запрос строк БД соответствующих текущему игроку и номеру уровня кнопки
        query_playing_level = """   select  p.id player_id, p.name name,
                                    cl.score score, 
                                    pl.id level_id, pl.backround_image image
                            from    Player p inner join  
                                    Completed_Level cl on p.id = cl.player_id inner join
                                    Possible_Level pl ON cl.possible_level_id = pl.id 
                            WHERE   p.id  = %s and
	                                pl.id = %s 
                     """ % ( self.game.player.id, self.level_number )
        # запрос одной строки БД содержащей номер последнего сыгранного уровня для указанного игрока
        query_last_level =   """
                            select  p.id player_id, p.name name,
                                    cl.score score, 
                                    pl.id level_id, pl.backround_image image
                            from    Player p inner join  
                                    Completed_Level cl on p.id = cl.player_id inner join
                                    Possible_Level pl ON cl.possible_level_id = pl.id 
                            WHERE   p.id  = %s
                            ORDER by pl.id DESC 
                            LIMIT 1
                            """ % self.game.player.id
        cursor = self.settings.db_connection.cursor() # получим курсор БД
        cursor.execute(query_playing_level) # выполним курсор с запросом
        rows = cursor.fetchall() # получим все строки результата
        cursor.close()
        self.settings.db_connection.commit()
        if len(rows)  <= 0: # в базе данных не найдено строк
            if self.level_number == 1: # если на кнопку назначен 1 уровень -
                                       # то всё равно сделать её активной и загрузить картинку
               self.allowed = True
               image_path = os.path.join("levels", "lock_open.png")
               self.level_image = pygame.image.load(image_path).convert()
               self.level_image = pygame.transform.scale(self.level_image,
                                                         (self.rect.width, self.rect.height))
            else: # иначе сделать кнопку пассивной
                self.allowed = False
        elif len(rows) == 1: # из БД получена одна ожидаемая строка
            for row in rows: # сделать кнопку активной и загрузить картинку
                self.allowed = True
                image_path = os.path.join( "levels", row[4] )
                self.level_image = pygame.image.load( image_path ).convert()
                self.level_image = pygame.transform.scale(self.level_image,
                                                          (self.rect.width, self.rect.height))
                return
        else: # из БД получено больше одной строки, выводим ошибку !!!
            self.allowed = False
            print("1. ERROR for BUTTON LEVEL %s ! Rows must be 1 ONE !!!! " % self.level_number )
            return
        cursor = self.settings.db_connection.cursor()  # получим курсор БД
        cursor.execute( query_last_level )  # выполним курсор с запросом
        rows = cursor.fetchall()  # получим все строки результата
        cursor.close()
        self.settings.db_connection.commit()
        if len(rows) == 1: # из БД получено не 1 строка - наш случай, активируем кнопку и загрузим картинку
            row = rows[0]
            if row[3]+1 == self.level_number:
                self.next_level = True
                self.allowed = True
                image_path = os.path.join("levels", "lock_open.png")
                self.level_image = pygame.image.load(image_path).convert()
                self.level_image = pygame.transform.scale(self.level_image,
                                                          (self.rect.width, self.rect.height))
        elif len(rows)==0:
            return
        elif len(rows)>1:
            print("2. ERROR for BUTTON LEVEL %s ! Rows must be 1 ONE !!!! " % self.level_number)
            return

    def update(self):
        pointer = pygame.mouse.get_pos()
        if self.rect.collidepoint(pointer):  #
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
        text = str(self.level_number)
        self.game.draw_text_center(self.game.screen, text, 50,
                            self.rect.centerx ,
                            self.rect.centery,
                            self.settings.RED)

class Finish_Button(pygame.sprite.Sprite):
    def __init__(self, game, scene, settings):  # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.scene = scene
        self.settings = settings
    def set_params(self,
                   y_top,  # координата кнопки
                   x_center,  # координата кнопки
                   height,  # высота кнопки
                   width,  # ширина кнопки
                   text,  # текст, отобажаемый на кнопке
                   ):
        self.rect = pygame.Rect((0, 0), (width, height))
        self.rect.centerx = x_center
        self.rect.top = y_top
        self.text = text
        self.is_over = False
        self.visible = False
    def update(self):
        pointer = pygame.mouse.get_pos()
        if self.rect.collidepoint(pointer):  # if pointer is inside btnRect
            self.is_over = True
        else:
            self.is_over = False
    def draw(self, surface):
        if self.visible == False:
            return
        pygame.draw.rect(surface, self.settings.GOLD, self.rect)
        pygame.draw.rect(surface, self.settings.GRAY, self.rect, 4)
        if self.is_over:
            pygame.draw.rect(surface, self.settings.BLUE, self.rect, 8)
        self.game.draw_text_center(surface, self.text, 30,
                            self.rect.centerx ,
                            self.rect.centery+3,
                            self.settings.BLUE)
