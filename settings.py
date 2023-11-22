

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
        # ------ переменные настройки игры
        self.SPRITE_SIZE = 15  # размер спрайта игры
        self.FPS = 60  # частоты обновления кадров игры
        self.WIDTH = 1024  # ширина окна игры
        self.HEIGHT = 768  # высота окна игры
        self.WIDTH = (self.WIDTH // self.SPRITE_SIZE) * self.SPRITE_SIZE
        self.HEIGHT = (self.HEIGHT // self.SPRITE_SIZE) * self.SPRITE_SIZE