import pygame
import random
from os import path


SPRITE_SIZE = 20
WIDTH = 1024 # константа ширины окна игры
HEIGHT = 768 # константа высоты окна игры
FPS = 60 # константа частоты обновления кадров игры
WIDTH = (WIDTH // SPRITE_SIZE)*SPRITE_SIZE
HEIGHT = (HEIGHT // SPRITE_SIZE)*SPRITE_SIZE

# Задаем цвета
WHITE = (255, 255, 255) # белый
BLACK = (0, 0, 0) # чёрный
RED = (255, 0, 0) # красный
GREEN = (0, 255, 0) # зелёный
BLUE = (0, 0, 255) # синий
YELLOW = (255, 255, 0) # жёлтый

# Создаем игру и окно
pygame.init() # инициализиуем pygame
pygame.mixer.init() # инициализиуем звуки pygame
screen = pygame.display.set_mode( ( WIDTH,HEIGHT ) ) # создаём окно игры и получаем объект-поверхность
pygame.display.set_caption("Xonix Happy New Year 2024 ! ") # задаём заголовок окна игры
clock = pygame.time.Clock() # создаём объект "Часы" для контоля за временем и частотой в игре

# Загружаем ресурсы
font_name = pygame.font.match_font('arial') # Получаем имя шрифта ближайшего к 'arial'
image_border    = pygame.image.load("border.png").convert()
image_snow      = pygame.image.load("snow.png").convert()
image_snow_crushed = pygame.image.load("snow_crushed.png").convert()
image_ded_moroz = pygame.image.load("ded_moroz.png").convert()
image_hidden    = pygame.image.load("drakon3.jpg").convert()
image_hidden    = pygame.transform.scale(image_hidden, (WIDTH, HEIGHT))
image_hidden_rect = image_hidden.get_rect()

def draw_text(surf, text, size, x, y): # функция отрисовки текста на поверхности
    font = pygame.font.Font(font_name, size) # создаём объект шрифта
    text_surface = font.render(text, True, WHITE) # рендерим текст шрифтом и получаем поверхность
    text_rect = text_surface.get_rect() # получаем прямоугольник поверхности
    text_rect.midtop = (x, y) # модифициуют прямоугольник, размещая его по переданным x,y
    surf.blit(text_surface, text_rect) # блиттинг отрендеренного текста на переданную поверхность

class Border(pygame.sprite.Sprite): # Класс спрайта "Граница"
    def __init__(self, yy, xx ): # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image_border, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        #self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        self.rect.x = xx  # изменим прямоугольник, это изменит и позицию
        self.rect.y = yy  # изменим прямоугольник, это изменит и позицию
        pass

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        pass

class DedMoroz(pygame.sprite.Sprite): # Класс спрайта "Дед Мороз"
    def __init__(self): # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image_ded_moroz, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        # self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        self.rect.x = 20  # изменим прямоугольник, это изменит и позицию
        self.rect.y = 0    # изменим прямоугольник, это изменит и позицию
        pass

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        if self.rect.right > WIDTH: # ограничиваем выход за пределы экрана
            self.rect.right = WIDTH #
        if self.rect.left < 0: # ограничиваем выход за пределы экрана
            self.rect.left = 0 #
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0 :
            self.rect.top = 0

class Snow(pygame.sprite.Sprite): # Класс спрайта "Снег"
    def __init__(self, yy, xx ): # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image_snow, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        # self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        self.rect.x = xx  # изменим прямоугольник, это изменит и позицию
        self.rect.y = yy  # изменим прямоугольник , это изменит и позицию
        self.crushed = False # флаг примятого снега, нужен для заливки областей
        pass

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        if self.crushed:
            self.image = pygame.transform.scale(image_snow_crushed, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
            # self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        else:
            self.image = pygame.transform.scale(image_snow, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки

def matrix_index_of( sprites_matrix_var, sprite ): # реализация функции index_of для матриц спрайтов
    y_idx = -1
    for y in range(MATRIX_HEIGHT):
        try:
            x_idx = sprites_matrix_var[y].index(sprite)
        except:
            x_idx = -1
        if x_idx >= 0:
            y_idx = y
            break
    return (y_idx,x_idx)


#----------------------------------------------------------------------------------------
# инициализация спрайтов #
# инициализация матрицы спрайтов
# ....................................................................
MATRIX_WIDTH = WIDTH // SPRITE_SIZE
MATRIX_HEIGHT = HEIGHT // SPRITE_SIZE
sprites_matrix = []
for y in range( MATRIX_HEIGHT ):
    sprites_matrix.append( [] )
    for x in range( MATRIX_WIDTH ):
        sprites_matrix[y].append( 1 )
# ....................................................................

# Создаём общую коллекцию спрайтов
all_sprites = pygame.sprite.Group()


# создаём коллекцию спрайтов для границы и поместим их в матрицу и в коллекции
# ....................................................................
border_sprites = pygame.sprite.Group()
y=0
for x in range(MATRIX_WIDTH):
    sp = Border(SPRITE_SIZE*y, SPRITE_SIZE*x)
    sprites_matrix[y][x] = sp
    border_sprites.add(sp)
    all_sprites.add(sp)
x=0
for y in range(1,MATRIX_HEIGHT-1):
    sp = Border(SPRITE_SIZE*y, SPRITE_SIZE*x)
    sprites_matrix[y][x] = sp
    border_sprites.add(sp)
    all_sprites.add(sp)
x=MATRIX_WIDTH-1
for y in range(1,MATRIX_HEIGHT-1):
    sp = Border(SPRITE_SIZE*y, SPRITE_SIZE*x)
    sprites_matrix[y][x] = sp
    border_sprites.add(sp)
    all_sprites.add(sp)
y=MATRIX_HEIGHT-1
for x in range(MATRIX_WIDTH):
    sp = Border(SPRITE_SIZE*y, SPRITE_SIZE*x)
    sprites_matrix[y][x] = sp
    border_sprites.add(sp)
    all_sprites.add(sp)
# ....................................................................

# создадим спрайты снега и поместим их в матрицу и в коллекции
# ....................................................................
snow_sprites = pygame.sprite.Group()
for y in range(1,MATRIX_HEIGHT-1):
    for x in range(1,MATRIX_WIDTH-1):
        sp = Snow( SPRITE_SIZE*y, SPRITE_SIZE*x )
        sprites_matrix[y][x] = sp
        snow_sprites.add(sp)
        all_sprites.add(sp)
# ....................................................................

# создадим спрайт деда мороза
sprite_ded_moroz = DedMoroz()
all_sprites.add(sprite_ded_moroz)
#----------------------------------------------------------------------------------------

# ???????????????????????????????????
flip_image_hidden = False
keyboard_timer_ded_moroz = pygame.time.get_ticks()  # сохраним временную засечку для управления дедом морозом
keyboard_timer_ded_moroz_delay = 40 # задержка для деда мороза в миллисекундах
# ???????????????????????????????????

# главный цикл
while True:
    clock.tick(FPS) # задаём кадры в секунду

    for event in pygame.event.get(): # перебираем все поступившие события
        if event.type == pygame.QUIT: # событие выхода из программы
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            flip_image_hidden = not flip_image_hidden

    # обрабатываем клавиши с залипанием
    keys = pygame.key.get_pressed()
    if pygame.time.get_ticks() - keyboard_timer_ded_moroz > keyboard_timer_ded_moroz_delay:  # делает если прошло время задержки
        if   keys[pygame.K_KP2] or keys[pygame.K_DOWN]  or keys[pygame.K_s]:
            sprite_ded_moroz.rect.y += SPRITE_SIZE
        elif keys[pygame.K_KP6] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            sprite_ded_moroz.rect.x += SPRITE_SIZE
        elif keys[pygame.K_KP8] or keys[pygame.K_UP]    or keys[pygame.K_w]:
            sprite_ded_moroz.rect.y -= SPRITE_SIZE
        elif keys[pygame.K_KP4] or keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            sprite_ded_moroz.rect.x -= SPRITE_SIZE
        keyboard_timer_ded_moroz = pygame.time.get_ticks()  # сохраним временную засечку для управления дедом морозом

    all_sprites.update()  # вызовем методы update для всех спрайтов в коллекции

    # получаем список коллизий
    hits = pygame.sprite.spritecollide(sprite_ded_moroz, snow_sprites, False )
    for hit in hits:
        hit.crushed = True # помечаем снег как примятый
        hit.kill()

    # Рендеринг сцены #
    screen.fill(BLACK)  # заполняем всё окно чёрным
    if flip_image_hidden:
        all_sprites.draw(screen)  # отрисовываем все спрайты встроенной функцией pygame
        screen.blit(image_hidden, image_hidden_rect)  # выводим фоновую картинку
    else:
        screen.blit(image_hidden, image_hidden_rect)  # выводим фоновую картинку
        all_sprites.draw(screen)  # отрисовываем все спрайты встроенной функцией pygame


    # После отрисовки всего, меняем экранные страницы #
    pygame.display.flip()  # ...

pygame.quit()