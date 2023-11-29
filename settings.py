import pygame
import sqlite3

class Settings(): # класс хранящий все настройки игры
    def __init__( self ): # констуктор
        # --------- папка с картинками драконов
        self.DRAGONS_DIR = "dragons"
        # -------- переменные цветов для игры
        self.WHITE = (255, 255, 255)  # белый
        self.BLACK = (0, 0, 0)  # чёрный
        self.RED = (255, 0, 0)  # красный
        self.GREEN = (0, 255, 0)  # зелёный
        self.BLUE = (0, 0, 255)  # синий
        self.YELLOW = (255, 255, 0)  # жёлтый
        self.GRAY = (100,100,100) # серый
        self.ORANGE = (255,165,0)
        self.GOLD = (255, 215, 0)
        self.BRIGHT_BLUE = (66,170,255)
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        # ------ переменные настройки игры
        self.SPRITE_SIZE = 15  # размер спрайта игры
        self.FPS = 60  # частоты обновления кадров игры
        self.WIDTH = 1024  # ширина окна игры
        self.HEIGHT = 768  # высота окна игры
        self.WIDTH = (self.WIDTH // self.SPRITE_SIZE) * self.SPRITE_SIZE
        self.HEIGHT = (self.HEIGHT // self.SPRITE_SIZE) * self.SPRITE_SIZE
        pygame.font.init()  # инициализируем шрифты pygame
        self.pygame_font_name = pygame.font.match_font('Arial')  # Получаем имя шрифта ближайшего к 'arial'
        self.INPUT_FONT_SIZE = 72
        self.INPUT_FONT = pygame.font.Font(None, self.INPUT_FONT_SIZE )
        self.LABEL_FONT_SIZE = 50
        self.LABEL_FONT = pygame.font.Font(None, self.LABEL_FONT_SIZE)
        pass
        self.db_connection = sqlite3.connect('hny_xonix_game.db')
        pass

    def save_FPS(self,FPS):
        self.FPS = FPS
        self.KV_set_value( "FPS", self.FPS )

    def get_FPS(self):
        self.FPS = int(self.KV_get_value("FPS"))
        return self.FPS

    def KV_key_exist(self,key):
        query_check = " select * from Settings_Key_Value where key='%s'; " % (key)
        cursor = self.db_connection.cursor()
        cursor.execute( query_check )
        rows = cursor.fetchall()
        return len(rows) > 0

    def KV_set_value( self, key, value ):
        if self.KV_key_exist(key):
            query_set = " update Settings_Key_Value set value='%s' where key='%s'; " % (value,key)
        else:
            query_set = "insert into Settings_Key_Value(key,value) values ('%s','%s');" % (key,value)
        cursor = self.db_connection.cursor()
        cursor.execute( query_set )
        cursor.close()
        self.db_connection.commit()

    def KV_get_value(self,key):
        query_get = " select value from Settings_Key_Value where key='%s'; " % (key)
        cursor = self.db_connection.cursor()
        cursor.execute(query_get)
        rows = cursor.fetchall()
        if ( len(rows) <= 0 ):
            return None
        return rows[0][0]

    def get_player_last_name(self):
        return self.KV_get_value("player_last_name")

    def set_player_last_name(self, name):
        self.KV_set_value("player_last_name", name )
