import pygame
import random
from os import path, chdir
import inspect
import sys

# ------ настройка интерпретатора питон
sys.setrecursionlimit(50000)
# ------ настройка путей для игры
chdir(path.dirname(__file__))
dragons_dir = "dragons" # папка с картинками драконов !
# ------ переменные настройки игры
SPRITE_SIZE = 15
WIDTH = 1024 # константа ширины окна игры
HEIGHT = 768 # константа высоты окна игры
FPS = 60 # константа частоты обновления кадров игры
WIDTH = (WIDTH // SPRITE_SIZE)*SPRITE_SIZE
HEIGHT = (HEIGHT // SPRITE_SIZE)*SPRITE_SIZE

#-------- переменные цветов для игры
WHITE = (255, 255, 255) # белый
BLACK = (0, 0, 0) # чёрный
RED = (255, 0, 0) # красный
GREEN = (0, 255, 0) # зелёный
BLUE = (0, 0, 255) # синий
YELLOW = (255, 255, 0) # жёлтый

# ------ создаем игру и окно
pygame.init() # инициализиуем pygame
pygame.mixer.init() # инициализиуем звуки pygame
screen = pygame.display.set_mode( ( WIDTH,HEIGHT ) ) # создаём окно игры и получаем объект-поверхность
pygame.display.set_caption("Xonix Happy New Year 2024 ! ") # задаём заголовок окна игры
clock = pygame.time.Clock() # создаём объект "Часы" для контоля за временем и частотой в игре

# ------ загружаем ресурсы
font_name = pygame.font.match_font('arial') # Получаем имя шрифта ближайшего к 'arial'
image_border    = pygame.image.load("border.png").convert()
image_snow      = pygame.image.load("snow.png").convert()
image_snow_crushed = pygame.image.load("snow_crushed.png").convert()
image_snow_old  = pygame.image.load("snow_old.png").convert()
image_ded_moroz = pygame.image.load("ded_moroz.png").convert()
image_enemy     = pygame.image.load("enemy.png").convert()

# функция отрисовки текста на поверхности
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size) # создаём объект шрифта
    text_surface = font.render(text, True, WHITE) # рендерим текст шрифтом и получаем поверхность
    text_rect = text_surface.get_rect() # получаем прямоугольник поверхности
    text_rect.midtop = (x, y) # модифициуют прямоугольник, размещая его по переданным x,y
    surf.blit(text_surface, text_rect) # блиттинг отрендеренного текста на переданную поверхность

class Border(pygame.sprite.Sprite): # Класс спрайта "Граница"
    def __init__(self, yy, xx, scene ): # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.image = pygame.transform.scale(image_border, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        #self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        self.rect.x = xx  # изменим прямоугольник, это изменит и позицию
        self.rect.y = yy  # изменим прямоугольник, это изменит и позицию
        pass

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        pass

class Snow(pygame.sprite.Sprite): # Класс спрайта "Снег"
    def __init__(self, yy, xx, scene): # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.image = pygame.transform.scale(image_snow, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        # self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        self.rect.x = xx  # изменим прямоугольник, это изменит и позицию
        self.rect.y = yy  # изменим прямоугольник , это изменит и позицию
        self.crushed = False # флаг примятого снега, нужен для заливки областей
        pass
        self.logic_color = "" # логический цвет для заполнения и определения областей
        pass

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        if self.crushed:
            self.image = pygame.transform.scale(image_snow_crushed, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        else:
            self.image = pygame.transform.scale(image_snow, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки

class DedMoroz(pygame.sprite.Sprite): # Класс спрайта "Дед Мороз"
    MOVE_STOP  = 0
    MOVE_DOWN  = 1
    MOVE_RIGHT = 2
    MOVE_UP    = 3
    MOVE_LEFT  = 4
    def __init__(self, scene): # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.image = pygame.transform.scale(image_ded_moroz, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        # self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        self.rect.x = SPRITE_SIZE  # изменим прямоугольник, это изменит и позицию
        self.rect.y = 0  # изменим прямоугольник, это изменит и позицию
        self.old_rect = self.rect.copy()
        pass
        self.keyboard_timer = pygame.time.get_ticks()  # сохраним временную засечку для управления дедом морозом
        self.keyboard_timer_delay = 5  # задержка для деда мороза в миллисекундах
        pass
        self.speed_timer = pygame.time.get_ticks()  # сохраним временную засечку для скорости перемещения деда мороза
        self.speed_delay = 20
        pass
        self.move_direction = self.MOVE_STOP
        pass
        self.wins_remaining_percent = 25 # Победа игрока происходит когда снега остаётся меньше этих процентов
        pass



    def coordinates_adjustment(self): # корректирует координаты предотвращая выход за границы игрового поля
        # ----- обрабатываем выход спрайта за границы экрана
        if self.rect.right > WIDTH:  # ограничиваем выход за пределы экрана
            self.rect.right = WIDTH  #
        if self.rect.left < 0:  # ограничиваем выход за пределы экрана
            self.rect.left = 0  #
        if self.rect.bottom > HEIGHT:  # ограничиваем выход за пределы экрана
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:  # ограничиваем выход за пределы экрана
            self.rect.top = 0

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        self.coordinates_adjustment()

    def rect_located_on_border(self,rect):# возвращает истину если прямоугольник расположен на границе
        if rect.x<=0 or \
           rect.y<=0 or \
           rect.right >= WIDTH-1 or \
           rect.bottom >= HEIGHT-1:
            return True
        else:
            return False

    def located_on_border(self): # возвращает истину если дед мороз расположен на границе
         return self.rect_located_on_border(self.rect)

    def move_auto(self): # метод перемещающий дед мороза по экрану
        if pygame.time.get_ticks() - self.speed_timer > self.speed_delay:  # делает если прошло время задержки
            if self.move_direction == self.MOVE_DOWN:
                self.old_rect = self.rect.copy()
                self.rect.y += SPRITE_SIZE
                self.process_colliions()
            elif self.move_direction == self.MOVE_RIGHT:
                self.old_rect = self.rect.copy()
                self.rect.x += SPRITE_SIZE
                self.process_colliions()
            elif self.move_direction == self.MOVE_UP:
                self.old_rect = self.rect.copy()
                self.rect.y -= SPRITE_SIZE
                self.process_colliions()
            elif self.move_direction == self.MOVE_LEFT:
                self.old_rect = self.rect.copy()
                self.rect.x -= SPRITE_SIZE
                self.process_colliions()
            elif self.move_direction == self.MOVE_STOP:
                self.old_rect = self.rect.copy()
            else:
                self.old_rect = self.rect
            self.speed_timer = pygame.time.get_ticks()


    def keyboard_processing(self): # метод, осущестляющий движение спрайта от нажатий на клавиатуру
        # обрабатываем клавиши с залипанием
        keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() - self.keyboard_timer > self.keyboard_timer_delay:# делает если прошло время задержки
            if self.located_on_border():
                if keys[pygame.K_KP2] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.move_direction = self.MOVE_DOWN
                elif keys[pygame.K_KP6] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.move_direction = self.MOVE_RIGHT
                elif keys[pygame.K_KP8] or keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.move_direction = self.MOVE_UP
                elif keys[pygame.K_KP4] or keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.move_direction = self.MOVE_LEFT
                else:
                    if self.located_on_border(): # на границах экрана возможен останов деда мороза
                        self.move_direction = self.MOVE_STOP
            else:
                if (keys[pygame.K_KP2] or keys[pygame.K_DOWN] or keys[pygame.K_s]) and \
                    self.move_direction!=self.MOVE_UP:
                    self.move_direction = self.MOVE_DOWN
                elif (keys[pygame.K_KP6] or keys[pygame.K_RIGHT] or keys[pygame.K_d]) and \
                        self.move_direction!=self.MOVE_LEFT:
                    self.move_direction = self.MOVE_RIGHT
                elif (keys[pygame.K_KP8] or keys[pygame.K_UP] or keys[pygame.K_w]) and \
                        self.move_direction!=self.MOVE_DOWN:
                    self.move_direction = self.MOVE_UP
                elif (keys[pygame.K_KP4] or keys[pygame.K_LEFT] or keys[pygame.K_a]) and \
                        self.move_direction!=self.MOVE_RIGHT:
                    self.move_direction = self.MOVE_LEFT
            self.keyboard_timer = pygame.time.get_ticks()  # сохраним временную засечку для управления дедом морозом
            pass

    def process_colliions(self): # обрабатываем коллизии деда мороза
        self.coordinates_adjustment() # обработаем выход за пределы экрана
        # ----- вычислим индекс старого и нового положений деда мороза в матрице спрайтов
        iXOn = self.old_rect.x // SPRITE_SIZE
        iYOn = self.old_rect.y // SPRITE_SIZE
        iXNn = self.rect.x // SPRITE_SIZE
        iYNn = self.rect.y // SPRITE_SIZE
        # ----- вычислим момент возвращения деда мороза на границу
        if ( not self.rect_located_on_border(self.old_rect) ) and \
           ( self.rect_located_on_border(self.rect) ) and \
           ( self.scene.sprites_matrix[iYOn][iXOn] != None ):
            begin_cell_1, begin_cell_2 = self.determine_begin_fill_cells() # определим точки заливки
            self.scene.process_hide_snow_sprites( begin_cell_1, begin_cell_2 ) # запустим метод гашения участка спрайтов
        # ----- вычислим момент выхода деда мороза со снега на открытую поверхность
        if ( self.scene.sprites_matrix[iYOn][iXOn] != None ) and \
           ( self.scene.sprites_matrix[iYNn][iXNn] == None ) and \
           ( not self.rect_located_on_border(self.old_rect) ) :
            begin_cell_1, begin_cell_2 = self.determine_begin_fill_cells() # определим точки заливки
            self.scene.process_hide_snow_sprites( begin_cell_1, begin_cell_2 ) # запустим метод гашения участка спрайтов
        # обрабатываем коллизии деда мороза со снегом для обеспечения работы со следом
        hits = pygame.sprite.spritecollide(self, self.scene.snow_sprites, False)
        for hit in hits:
            if (hit.crushed==False): # дед мороз попал на чистый снег
                hit.crushed = True # помечаем снег как примятый
                self.scene.crushed_sprites.add(hit) #
            else: # дед мороз попал на примятый снег, на свой след
                self.scene.player_lose_scene()

    def determine_begin_fill_cells(self): # возвращает координаты (Y, X) в матрице двух ячеек по разные стороны от "следа"
                                          # если вызыать когда нужно, то обеспечиает стопроцентное попадание в
                                          # истинные точки заливки на игровой матрице
        iXOn = self.old_rect.x // SPRITE_SIZE
        iYOn = self.old_rect.y // SPRITE_SIZE
        begin_cells = [None] * 2
        if ( self.old_rect.y != self.rect.y ):
            begin_cells[0] = ( iYOn, iXOn -1 )
            begin_cells[1] = ( iYOn, iXOn+1  )
        elif (self.old_rect.x != self.rect.x ):
            begin_cells[0] = ( iYOn-1, iXOn  )
            begin_cells[1] = ( iYOn+1, iXOn  )
        return  begin_cells

class Enemy(pygame.sprite.Sprite):
    def __init__(self, scene):  # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.image = pygame.transform.scale(image_enemy, (SPRITE_SIZE, SPRITE_SIZE))  # ресайз картинки
        self.image.set_colorkey(BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        self.rect.x = random.randrange( SPRITE_SIZE, WIDTH - SPRITE_SIZE )
        self.rect.y = random.randrange( SPRITE_SIZE, HEIGHT - SPRITE_SIZE )
        self.dx = 1 * SPRITE_SIZE
        self.dy = 1 * SPRITE_SIZE
        pass
        self.speed_delay = 50
        self.speed_timer = pygame.time.get_ticks()  # сохраним временную засечку для скорости перемещения врагов
        pass


    def update(self):
        if pygame.time.get_ticks() - self.speed_timer > self.speed_delay:
            tx = self.rect.x + self.dx
            ty = self.rect.y + self.dy
            if tx > (WIDTH-SPRITE_SIZE*2):  # ограничиваем выход за пределы экрана
                tx = (WIDTH-SPRITE_SIZE*2)  # вписываем в экран
                self.dx = - self.dx
            if tx < (SPRITE_SIZE):  # ограничиваем выход за пределы экрана
                tx = SPRITE_SIZE  # вписываем в экран
                self.dx = - self.dx
            if ty > (HEIGHT-SPRITE_SIZE*2):  # ограничиваем выход за пределы экрана
                ty = (HEIGHT-SPRITE_SIZE*2) # вписываем в экран
                self.dy = - self.dy
            if ty < SPRITE_SIZE:  # ограничиваем выход за пределы экрана
                ty = SPRITE_SIZE # вписываем в экран
                self.dy = - self.dy
            # ----- вычислим индекс старого и нового положений врага на матрице спрайтов
            iXOn = self.rect.x // SPRITE_SIZE
            iYOn = self.rect.y // SPRITE_SIZE
            iXNn = tx // SPRITE_SIZE
            iYNn = ty // SPRITE_SIZE
            # обработаем выход за территорию со снегом
            if ( isinstance( self.scene.sprites_matrix[iYOn][iXOn], Snow) ) and \
                   not isinstance(self.scene.sprites_matrix[iYNn][iXNn], Snow ) : # вышли за пределы снега
                if not isinstance(self.scene.sprites_matrix[iYNn-1][iXNn], Snow) and \
                    not isinstance( self.scene.sprites_matrix[iYNn+1][iXNn], Snow ): # это вертикальная граница снега
                    self.dx = - self.dx # отразим от вертикальной границы снега
                    return
                elif not isinstance( self.scene.sprites_matrix[iYNn][iXNn-1], Snow ) and \
                    not  isinstance( self.scene.sprites_matrix[iYNn][iXNn+1], Snow ): # это горизонтальная граница снега
                    self.dy = - self.dy # отразим от горизонтальной границы снега
                    return
                else:
                    self.dx = - self.dx
                    self.dy = - self.dy

            self.rect.x = tx
            self.rect.y = ty
            self.speed_timer = pygame.time.get_ticks()  # обновим временную засечку для скорости перемещения врагов
            self.process_collissions()

    def process_collissions(self):
        hits = pygame.sprite.spritecollide(self, self.scene.crushed_sprites, False)
        for hit in hits:
            self.scene.player_lose_scene()

class Scene(): # класс представляющий и управляющий сценой игры
    def __init__(self):  # констуктор
        self.load_scene()

    def load_scene(self): # код по инициализации и загрузке всей сцены....
        self.player_win_in_this_scene = False
        self.REMAINING_PERCENTS_WIN = 15
        # ------ скрытая картинка для сцены
        self.image_hidden = pygame.image.load(path.join(dragons_dir, "drakon4.jpg")).convert()
        print("*****", path.join(dragons_dir, "drakon4.jpg"))
        self.image_hidden = pygame.transform.scale(self.image_hidden, (WIDTH, HEIGHT))
        self.image_hidden_rect = self.image_hidden.get_rect()
        self.BLUR_RATIO = 50
        self.blured_hidden_image = True
        # ------ инициализация матрицы спрайтов
        self.MATRIX_WIDTH = WIDTH // SPRITE_SIZE
        self.MATRIX_HEIGHT = HEIGHT // SPRITE_SIZE
        self.sprites_matrix = []
        for iy in range(self.MATRIX_HEIGHT):
            self.sprites_matrix.append([])
            for ix in range(self.MATRIX_WIDTH):
                self.sprites_matrix[iy].append( None )
        # ------ ниже инициализация спрайтов
        self.all_sprites = pygame.sprite.Group()  # группа всех спрайтов
        # ------ создаём коллекцию спрайтов для границы и поместим их в матрицу и в коллекции
        self.border_sprites = pygame.sprite.Group()
        y = 0
        for x in range(self.MATRIX_WIDTH):
            sp = Border(SPRITE_SIZE * y, SPRITE_SIZE * x, self)
            self.sprites_matrix[y][x] = sp
            self.border_sprites.add(sp)
            self.all_sprites.add(sp)
        x = 0
        for y in range(1, self.MATRIX_HEIGHT - 1):
            sp = Border(SPRITE_SIZE * y, SPRITE_SIZE * x, self)
            self.sprites_matrix[y][x] = sp
            self.border_sprites.add(sp)
            self.all_sprites.add(sp)
        x = self.MATRIX_WIDTH - 1
        for y in range(1, self.MATRIX_HEIGHT - 1):
            sp = Border(SPRITE_SIZE * y, SPRITE_SIZE * x, self)
            self.sprites_matrix[y][x] = sp
            self.border_sprites.add(sp)
            self.all_sprites.add(sp)
        y = self.MATRIX_HEIGHT - 1
        for x in range(self.MATRIX_WIDTH):
            sp = Border(SPRITE_SIZE * y, SPRITE_SIZE * x, self)
            self.sprites_matrix[y][x] = sp
            self.border_sprites.add(sp)
            self.all_sprites.add(sp)
        # ------ создадим спрайты снега и поместим их в матрицу и в коллекции
        self.snow_sprites = pygame.sprite.Group()
        for iy in range(1, self.MATRIX_HEIGHT - 1):
            for ix in range(1, self.MATRIX_WIDTH - 1):
                sp = Snow(SPRITE_SIZE * iy, SPRITE_SIZE * ix, self)
                self.sprites_matrix[iy][ix] = sp
                self.snow_sprites.add(sp)
                self.all_sprites.add(sp)
        # ----- группа спрайтов для примятого снега
        self.crushed_sprites = pygame.sprite.Group()
        # ----- создадим спрайт деда мороза, который ходит о снегу
        # Этот спрайт у нас очень самостоятельный, сам читает клавиатуру, сам просчитывает своё движение,
        # сам просчитывает координаты с которых идёт заливка и гашение снега,
        # но вот сам floofill и гашение блоков снега у него лучше отобрать.
        self.sprite_ded_moroz = DedMoroz(self)
        self.all_sprites.add(self.sprite_ded_moroz)
        pass
        self.logic_colors_counts = {"green": 0, "red": 0}  # счётчик клеток для зон заливки алгоритма floofill
        pass
        self.enemy1 = Enemy(self)
        self.all_sprites.add(self.enemy1)
        self.enemy2 = Enemy(self)
        self.all_sprites.add(self.enemy2)
        # ------- инициализиуем падающий снег --------
        self.snow_list = []
        # Пройдемся 50 раз циклом и добавьм снежинки в рандомную позицию x,y
        for i in range(500):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            self.snow_list.append([x, y])

    def unload_scene(self):
        self.blured_hidden_image = True
        self.clear_colors()
        for iy in range(0, self.MATRIX_HEIGHT ):
            for ix in range(0, self.MATRIX_WIDTH ):
                if self.sprites_matrix[iy][ix]  != None:
                    self.sprites_matrix[iy][ix].kill()
                    self.sprites_matrix[iy][ix]=None
        self.sprite_ded_moroz.y=0
        self.sprite_ded_moroz.x=SPRITE_SIZE
        self.all_sprites.remove( self.sprite_ded_moroz )
        self.sprite_ded_moroz.kill()
        self.enemy1.kill()
        self.enemy2.kill()

    def reload_scene(self):
        self.unload_scene()
        self.load_scene()

    def player_win_scene(self):
        self.unload_scene()
        self.player_win_in_this_scene = True
        self.blured_hidden_image = False
        print("!!!!!!!!!! PLAYER WIN !!!!!!!!!!!!!!")

    def player_lose_scene(self):
        self.reload_scene()
        print("!!!!!!!!!! PLAYER LOSE !!!!!!!!!!!!!!")

    def get_blurSurf(self, surface, amt): # размывает указанную поверхность
        """
        Blur the given surface by the given 'amount'.  Only values 1 and greater
        are valid.  Value 1 = no blur.
        """
        if amt < 1.0:
            raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s" % amt)
        scale = 1.0 / float(amt)
        surf_size = surface.get_size()
        scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf

    def draw_hidden_image(self):
        if self.blured_hidden_image:
            imgb_hidden = self.get_blurSurf(self.image_hidden, self.BLUR_RATIO)
            screen.blit( imgb_hidden, self.image_hidden_rect )  # выводим фоновую картинку с размытием
        else:
            screen.blit(self.image_hidden, self.image_hidden_rect)

    def draw_snow_fall(self):
        # обработка каждой снежинки
        for i in range(len(self.snow_list)):
            # нарисовать снежинку
            pygame.draw.circle(screen, WHITE, self.snow_list[i], 2)
            # снежинка вниз на 1
            self.snow_list[i][1] += 1
            if self.snow_list[i][1] > HEIGHT:
                y = random.randrange(-50, -10)
                self.snow_list[i][1] = y
                x = random.randrange(0, WIDTH)
                self.snow_list[i][0] = x

    def matrix_index_of(self, sprites_matrix_var, sprite):  # реализация функции index_of для матриц спрайтов
                                                          # возвращает индекс в матрице по объекту спрайта
        y_idx = -1
        for y in range(self.MATRIX_HEIGHT):
            try:
                x_idx = sprites_matrix_var[y].index(sprite)
            except:
                x_idx = -1
            if x_idx >= 0:
                y_idx = y
                break
        return (y_idx, x_idx)

    def keyboard_processing(self):
        self.sprite_ded_moroz.keyboard_processing()

    def move_auto(self):
        self.sprite_ded_moroz.move_auto()

    def update(self):
        self.all_sprites.update()  # вызовем методы update для всех спрайтов в коллекции

    def get_remaining_percents(self):
        total_snow = self.MATRIX_HEIGHT * self.MATRIX_WIDTH
        remaining_snow = 0
        for tile in self.snow_sprites:
            if isinstance(tile, Snow):
                if not tile.crushed:
                    remaining_snow += 1
        one_percent = float(total_snow / 100)
        remaining_percents = remaining_snow / one_percent
        return remaining_percents

    def clear_colors(self): #
        self.logic_colors_counts = {"green": 0, "red": 0}
        for iy in range(1, self.MATRIX_HEIGHT - 1):
            for ix in range(1, self.MATRIX_WIDTH - 1):
                if isinstance( self.sprites_matrix[iy][ix] , Snow ):
                    self.sprites_matrix[iy][ix].logic_color = ""

    def enemy_in_the_block(self,block_color): # возвращает истину если в блоке указанного цвета есть враг
        hits = pygame.sprite.spritecollide(self.enemy1, self.snow_sprites, False)
        for hit in hits:
            if hit.logic_color == block_color:
                return True
        hits = pygame.sprite.spritecollide(self.enemy2, self.snow_sprites, False)
        for hit in hits:
            if hit.logic_color == block_color:
                return True
        return False


    def process_hide_snow_sprites(self, begin_cell_1, begin_cell_2 ): # обрабатываем скрытие зон спрайтов на поле
        self.floodfill_sprites_zone( begin_cell_1[0], begin_cell_1[1], "green"  )
        self.floodfill_sprites_zone( begin_cell_2[0], begin_cell_2[1],  "red" )
        if self.logic_colors_counts["green"] < self.logic_colors_counts["red"]:
            lowest_color = "green"
            biggest_color = "red"
        else:
            lowest_color = "red"
            biggest_color = "green"
        if ( self.enemy_in_the_block(lowest_color) == False ): # в отсечённой меньшей зоне нет врагов
            for iy in range(1, self.MATRIX_HEIGHT - 1): # погасим зону цвета lowest_color
                for ix in range(1, self.MATRIX_WIDTH - 1):
                    if isinstance( self.sprites_matrix[iy][ix] , Snow ):
                        if ( self.sprites_matrix[iy][ix].logic_color == lowest_color ) or \
                           ( self.sprites_matrix[iy][ix].crushed == True ):
                            self.sprites_matrix[iy][ix].kill()
                            self.sprites_matrix[iy][ix]=None
                        else:
                            self.sprites_matrix[iy][ix].logic_color = ""
        elif ( self.enemy_in_the_block(biggest_color) == False ): # если в отсечённой бОльшей зоне нет врагов:
            for iy in range(1, self.MATRIX_HEIGHT - 1): # погасим зону цвета biggest_color
                for ix in range(1, self.MATRIX_WIDTH - 1):
                    if isinstance(self.sprites_matrix[iy][ix], Snow):
                        if (self.sprites_matrix[iy][ix].logic_color == biggest_color ) or \
                                (self.sprites_matrix[iy][ix].crushed == True):
                            self.sprites_matrix[iy][ix].kill()
                            self.sprites_matrix[iy][ix] = None
                        else:
                            self.sprites_matrix[iy][ix].logic_color = ""
        else: # в обоих блоках есть враги!
            for tile in self.crushed_sprites: # погасим след деда мороза
                iy, ix = self.matrix_index_of( self.sprites_matrix, tile )
                tile.kill()
                self.sprites_matrix[iy][ix] = None
        pass
        self.clear_colors()
        pass
        if self.get_remaining_percents() <= self.REMAINING_PERCENTS_WIN:
            self.player_win_scene()

    def floodfill_sprites_zone(self, begin_y , begin_x,  logic_color  ):# возвращает количество заполненых ячеек
        if not isinstance( self.sprites_matrix[begin_y][begin_x] , Snow ) :
            return
        if self.sprites_matrix[begin_y][begin_x].crushed == True:
            return
        if self.sprites_matrix[begin_y][begin_x].logic_color !="":
            return
        self.sprites_matrix[begin_y][begin_x].logic_color = logic_color
        self.logic_colors_counts[logic_color] += 1
        pass
        self.floodfill_sprites_zone( begin_y, begin_x-1, logic_color )
        self.floodfill_sprites_zone( begin_y, begin_x+1, logic_color )
        self.floodfill_sprites_zone( begin_y-1, begin_x, logic_color )
        self.floodfill_sprites_zone( begin_y+1, begin_x, logic_color )
        pass



# !!!----------------------------------
flip_image_hidden = False
# !!!----------------------------------

scene = Scene() # создадим игровую сцену

# главный цикл
while True:
    clock.tick(FPS) # задаём кадры в секунду

    for event in pygame.event.get(): # перебираем все поступившие события
        if event.type == pygame.QUIT: # событие выхода из программы
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f: # чит показывает фоновую картинку
            flip_image_hidden = not flip_image_hidden

    scene.keyboard_processing() # обрабатываем ввод для деда мороза
    scene.move_auto() # перемещает деда мороза по экрану

    scene.update() # вызыает метод update для спрайтов всей сцены


    # Рендеринг сцены
    screen.fill(BLACK)  # заполняем всё окно чёрным
    if flip_image_hidden:
        scene.all_sprites.draw(screen)  # отрисовываем все спрайты встроенной функцией pygame
        scene.draw_hidden_image()  # выводим фоновую картинку
    else:
        scene.draw_hidden_image()  # выводим фоновую картинку
        scene.all_sprites.draw(screen)  # отрисовываем все спрайты встроенной функцией pygame

    if scene.player_win_in_this_scene:
        scene.draw_hidden_image()  # выводим фоновую картинку
        draw_text(screen, "Победа за Вами ! ", 72, WIDTH // 2, 0)
        scene.draw_snow_fall()

    # После отрисовки всего, меняем экранные страницы #
    pygame.display.flip()

pygame.quit()