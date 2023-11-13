# Игра Shmup - 14 часть
# Конец игры
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
# Комментарии от Алексеева Дмитрия Михайловича
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img') # определяем путь до папки с картинками
snd_dir = path.join(path.dirname(__file__), 'snd') # определяем путь до папки со звуками

WIDTH = 480 # константа ширины окна игры
HEIGHT = 600 # константа высоты окна игры
FPS = 60 # константа частоты обновления кадров игры
POWERUP_TIME = 5000 # константа таймаута для бонусов

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
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём окно игры и получаем объект-поверхность
pygame.display.set_caption("Shmup!") # задаём заголовок окна игры
clock = pygame.time.Clock() # создаём объект "Часы" для контоля за временем и частотой в игре

font_name = pygame.font.match_font('arial') # Получаем имя шрифта ближайшего к 'arial'


def draw_text(surf, text, size, x, y): # функция отрисовки текста на поверхности
    font = pygame.font.Font(font_name, size) # создаём объект шрифта
    text_surface = font.render(text, True, WHITE) # рендерим текст шрифтом и получаем поверхность
    text_rect = text_surface.get_rect() # получаем прямоугольник поверхности
    text_rect.midtop = (x, y) # модифициуют прямоугольник, размещая его по переданным x,y
    surf.blit(text_surface, text_rect) # блиттинг отрендеренного текста на переданную поверхность


def newmob(): # создаёт новый моб-метеорит
    m = Mob() # создадим объект метеорита
    all_sprites.add(m) # добавим объект метеорита в коллекцию всех спрайтов
    mobs.add(m) # добавим объект  коллекцию мобов-метеоритов


def draw_shield_bar(surf, x, y, pct): # отрисовывает полоску "щита"
    if pct < 0: # pct - величина полоски щита
        pct = 0 # если она меньше нуля - сбрасываем в ноль
    BAR_LENGTH = 100 # длинна каймы полоски щита
    BAR_HEIGHT = 10 # высота каймы полоски щита
    fill = (pct / 100) * BAR_LENGTH # процент заполненности полоски щита
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) # прямоугольник каймы щита
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT) # прямоугольник полоски щита
    pygame.draw.rect(surf, GREEN, fill_rect) # рисуем прямоугольник полоски щита
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # рисуем кайму полоски щита


def draw_lives(surf, x, y, lives, img): # отрисовывает количество жизней на экране
    # в img хранится маленькая картинка корабля
    for i in range(lives): # цикл по количеству жизней
        img_rect = img.get_rect() # получим прямоугольник картинки
        img_rect.x = x + 30 * i # изменим прямоугольник
        img_rect.y = y # изменим прямоугольник
        surf.blit(img, img_rect) # блиттинг маленкой картинки корабля в указанный прямоугольник


def show_go_screen(): # отобажает начальный экран игры
    screen.blit(background, background_rect) # блиттинг фоновой картинки на экран
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4) # выводим назание игры
    draw_text(screen, "Arrow keys move, Space to fire", 22, #
              WIDTH / 2, HEIGHT / 2) # выводим справку по клавишам
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4) # выводим press any key
    pygame.display.flip() # переключаем страницы, то есть выводим на экран
    waiting = True # флаг ожидания для начального экрана
    while waiting: # цикл ожидания для начального экрана
        clock.tick(FPS) # устанавливаем FPS
        for event in pygame.event.get(): # цикл событий интефейса
            if event.type == pygame.QUIT: # пришло событие выхода из игры
                pygame.quit() # выйдем из игры
            if event.type == pygame.KEYUP: # пришло событие "Любая клавиша"
                waiting = False # опустим флаг ожидания началного экрана


class Player(pygame.sprite.Sprite): # Класс спрайта "Игрок"
    def __init__(self): # констуктор
        pygame.sprite.Sprite.__init__(self) # вызов родительского конструктора
        self.image = pygame.transform.scale(player_img, (50, 38)) # ресайз картинки игрока
        self.image.set_colorkey(BLACK) # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect() # получим прямоугольник для игрока
        self.radius = 20 # установим радиус для игрока
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2 # изменим прямоугольник игрока, это изменит и позицию
        self.rect.bottom = HEIGHT - 10 # изменим прямоугольник игрока, это изменит и позицию
        self.speedx = 0 # установим скорость игрока по горизонтали
        self.shield = 100 # установим значение щита игрока
        self.shoot_delay = 250 # сколько времени должно пройти между появлением пуль
        self.last_shot = pygame.time.get_ticks() # сколько прошло с момента последней пули
        self.lives = 3 # устанавливваем сколько жизней у игрока
        self.hidden = False # флаг скрытости игрока
        self.hide_timer = pygame.time.get_ticks() # таймер скрывания игрока в игровых тиках
        self.power = 1 # ????
        self.power_time = pygame.time.get_ticks() # ????

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        # timeout for powerups #
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME: # обрабатывает силу выстрелов
            self.power -= 1 # ????
            self.power_time = pygame.time.get_ticks() # ????

        # показать, если скрыто #
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000: # обрабатвает скрытость игрока
            self.hidden = False # опускаем флаг скрытости игрока
            self.rect.centerx = WIDTH / 2 # устаналиваем прямоугольник игрока
            self.rect.bottom = HEIGHT - 10 # устаналиваем прямоугольник игрока

        self.speedx = 0 # скорость по гоизонтали равна нулю
        keystate = pygame.key.get_pressed() # читаем состояние ввода
        if keystate[pygame.K_LEFT]: # если нажата клавиша влево
            self.speedx = -8 # ...
        if keystate[pygame.K_RIGHT]: # если нажата клавиша вправо
            self.speedx = 8 # ...
        if keystate[pygame.K_SPACE]: # если нажата клавиша "пробел"
            self.shoot() # ...
        self.rect.x += self.speedx # меняем прямоуголник игрока
        if self.rect.right > WIDTH: # ограничиваем выход за пределы экрана
            self.rect.right = WIDTH # ...
        if self.rect.left < 0: # ограничиваем выход за пределы экрана
            self.rect.left = 0 # ...

    def powerup(self): # ????
        self.power += 1 # ????
        self.power_time = pygame.time.get_ticks() # ????

    def shoot(self): # метод производит выстрел
        now = pygame.time.get_ticks() # получает текущий тик игры
        if now - self.last_shot > self.shoot_delay: # делает если прошло время задержки
            self.last_shot = now # обновляем засечку задержки
            if self.power == 1: # если показатель силы равен одному
                bullet = Bullet(self.rect.centerx, self.rect.top) # создадим одну пулю
                all_sprites.add(bullet) # добавим пулю в коллекцию всех спрайтов
                bullets.add(bullet) # добавим пулю  коллекцию пуль
                shoot_sound.play() # проиграем звук выстрела
            if self.power >= 2: # если показатель силы два и больше
                bullet1 = Bullet(self.rect.left, self.rect.centery) # Создадим две пули
                bullet2 = Bullet(self.rect.right, self.rect.centery) # ...
                all_sprites.add(bullet1) # ...
                all_sprites.add(bullet2) # ...
                bullets.add(bullet1) # ...
                bullets.add(bullet2) # ...
                shoot_sound.play() # ...

    def hide(self): # метод скрывает игрока
        # временно скрыть игрока #
        self.hidden = True # поднимем флаг о скрытии игрока
        self.hide_timer = pygame.time.get_ticks() # обновим таймер скрытости игрока
        self.rect.center = (WIDTH / 2, HEIGHT + 200) # меняем прямоугольник игрока


class Mob(pygame.sprite.Sprite): # Класс спрайта "Моб", "Метеорит"
    def __init__(self): # констуктор класса
        pygame.sprite.Sprite.__init__(self) # вызываем родителский конструктор
        self.image_orig = random.choice(meteor_images) # случайным образом выбиаем одну из катинок метеоритов и ложим её атрибут
        self.image_orig.set_colorkey(BLACK) # установим прозрачный цвет спрайта
        self.image = self.image_orig.copy() # атрибут image - реально отображаемая картинка
        self.rect = self.image.get_rect() # установим прямоугольник картинки
        self.radius = int(self.rect.width * .85 / 2) # установим атрибут радиуса - для коллизий
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #
        self.rect.x = random.randrange(WIDTH - self.rect.width) # случайная позиция x в рамках ширины окна
        self.rect.y = random.randrange(-150, -100) # случайная позиция за пределами видимого окна
        self.speedy = random.randrange(1, 8) # случайная вертикальная скорость
        self.speedx = random.randrange(-3, 3) # случайная горизонтальная скорость
        self.rot = 0 # на сколько градусов должен вращаться астероид
        self.rot_speed = random.randrange(-8, 8) # на сколько градусов астероид будет поворачиваться каждый раз -
                                                      # чем больше число, тем быстрее будет происходить вращение
        self.last_update = pygame.time.get_ticks() # последнее обновление состояния спрайта метеорита

    def rotate(self): # метод осуществляет поворот спрайта
        now = pygame.time.get_ticks() # получаем текущее значение тиков таймера
        if now - self.last_update > 50: # если прошло более 50 тиков
            self.last_update = now # обновим атрибут последнего обновления
            self.rot = (self.rot + self.rot_speed) % 360 # вычислим поворот метеорита на угол self.rot_speed
                                                         # и запишем угол  атибут
            new_image = pygame.transform.rotate(self.image_orig, self.rot) # создадим повёрнутое изображение на угол
            old_center = self.rect.center # сохраним старый центр метеоита
            self.image = new_image # положим повёрнутое изображение в атрибут картинки
            self.rect = self.image.get_rect() # ...
            self.rect.center = old_center # разместим центр нового повёрнутого изображения  старом центре

    def update(self): # метод обновляющий спрайт в соответсвии с игровой логикой
        self.rotate() # повернуть спрайт
        self.rect.x += self.speedx # сместить по горизонтали
        self.rect.y += self.speedy # сместить по вертикали
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: # если метеорит
                        # вылетел за пределы окна, то переместить его в зону спауна
            self.rect.x = random.randrange(WIDTH - self.rect.width) #
            self.rect.y = random.randrange(-100, -40) #
            self.speedy = random.randrange(1, 8) #


class Bullet(pygame.sprite.Sprite): # Класс, описывающий пулю.
    def __init__(self, x, y): # конструктор пули
        pygame.sprite.Sprite.__init__(self) # вызов родительского конструктора
        self.image = bullet_img # устанавливаем картинку для пули
        self.image.set_colorkey(BLACK) # устанавливаем прозрачный свет для спрайта пули
        self.rect = self.image.get_rect() # устанавливаем прямоугольник пули
        self.rect.bottom = y # ...
        self.rect.centerx = x # ...
        self.speedy = -10 # устаналиваем скорость пули

    def update(self): # метод, обрабатывающий игровую логику пули
        self.rect.y += self.speedy # перемещаем со скоростью из атрибута
        # убить, если он заходит за верхнюю часть экрана #
        if self.rect.bottom < 0: # ...
            self.kill() # ...


class Pow(pygame.sprite.Sprite): # Класс игрового бонуса
    def __init__(self, center): # конструктор
        pygame.sprite.Sprite.__init__(self) # вызываем родительский конструктор
        self.type = random.choice(['shield', 'gun']) # случайным образом выбираем тип бонуса
        self.image = powerup_images[self.type] # загрузим картинку бонуса исходя из типа
        self.image.set_colorkey(BLACK) # зададим прозрачный цвет для картинки бонуса
        self.rect = self.image.get_rect() # установим прямоугольник бонуса
        self.rect.center = center # установим позицию бонуса
        self.speedy = 2 # установим скорость бонуса по вертикали

    def update(self): # обновляет бонус в соответвии с игровой логикой
        self.rect.y += self.speedy # перемещаем по вертикали
        # убить, если он сдвинется с нижней части экрана #
        if self.rect.top > HEIGHT: # ...
            self.kill() # ...


class Explosion(pygame.sprite.Sprite): # Класс для эффекта взрыва
    def __init__(self, center, size): # конструктор
        pygame.sprite.Sprite.__init__(self) # вызвать родительский конструктор
        self.size = size # ????
        self.image = explosion_anim[self.size][0] # ????
        self.rect = self.image.get_rect() # установим прямоугольник взрыва
        self.rect.center = center # установим центр взрыва
        self.frame = 0 # ????
        self.last_update = pygame.time.get_ticks() # получим и установим текущий счётчик тиков
        self.frame_rate = 50 # FPS присвоим 50

    def update(self): # метод игровой логики взрыва
        now = pygame.time.get_ticks() # сколько текущих тиков
        if now - self.last_update > self.frame_rate: # если прошло 'self.frame_rate' тиков с прошлого вызова метода
            self.last_update = now # обновим засечку тиков
            self.frame += 1 # ????
            if self.frame == len(explosion_anim[self.size]): # ????
                self.kill() # ????
            else: # не прошло 'self.frame_rate' тиков.
                center = self.rect.center # ????
                self.image = explosion_anim[self.size][self.frame] # ????
                self.rect = self.image.get_rect() # ????
                self.rect.center = center # ????


# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert() # загружаем фоновую картинку
background_rect = background.get_rect() # получим прямоугольник фоновой картинки и запомним
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert() # загузим катртинку игрока
player_mini_img = pygame.transform.scale(player_img, (25, 19)) # уменьшим картинку игрока
player_mini_img.set_colorkey(BLACK) # установим прозрачный фон для картинки игрока
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert() # загрузим картинку для пули
meteor_images = [] # создадим список для картинок метеоритов
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png', #
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', #
               'meteorBrown_tiny1.png'] # зададим в коде имена файлов метеоритов
for img in meteor_list: # цикл по именам файлов с картинками метеоритов
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert()) # загрузим все картинки метеоритов
                                                        # в список meteor_images

###  этот блок кода загружает картинки взрывов
explosion_anim = {} # ????
explosion_anim['lg'] = [] # ????
explosion_anim['sm'] = [] # ????
explosion_anim['player'] = [] # ????
for i in range(9): #
    filename = 'regularExplosion0{}.png'.format(i) #
    img = pygame.image.load(path.join(img_dir, filename)).convert() #
    img.set_colorkey(BLACK) #
    img_lg = pygame.transform.scale(img, (75, 75)) #
    explosion_anim['lg'].append(img_lg) #
    img_sm = pygame.transform.scale(img, (32, 32)) #
    explosion_anim['sm'].append(img_sm) #
    filename = 'sonicExplosion0{}.png'.format(i) #
    img = pygame.image.load(path.join(img_dir, filename)).convert() #
    img.set_colorkey(BLACK) #
    explosion_anim['player'].append(img) #


powerup_images = {} # словарь картинок с бонусами
# загружаем картинку с бонусом-щитом
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
# загружаем картинку с бонусом-молнией
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()


# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav')) # загружаем звук
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav')) # загружаем звук
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav')) # загружаем звук
expl_sounds = [] # список со звуками ввзрывов
for snd in ['expl3.wav', 'expl6.wav']: # загрузим звуки взрывов и добавим в список
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd))) #

all_sprites = pygame.sprite.Group() # группа всех спрайтов в игре
mobs = pygame.sprite.Group() # группа всех мобов-метеоритов в игре
bullets = pygame.sprite.Group() # группа всех пуль в игре
powerups = pygame.sprite.Group() # группа всех бонусов в игре
player = Player() # объект игрока
all_sprites.add(player) # добавим спрайт игрока во все спрайты
for i in range(8): # создадим 8 мобов-метеоитов
    newmob() #
score = 0 # установим счёт равным нулю

# Цикл игры
game_over = True # флаг завершения игры поднят
running = True # флаг работы игры поднят
while running: # пока работаем...
    if game_over: # если флаг конца игры поднят
        show_go_screen() # отрисовываем и показываем главный экран, ждём нажатия любой клавиши на нём
        game_over = False # опускаем флаг конца игры
        all_sprites = pygame.sprite.Group() # обнулим коллекцию всех спрайтов
        mobs = pygame.sprite.Group() # обнулим коллекцию метеоитов
        bullets = pygame.sprite.Group() # обнулим коллекцию пуль
        powerups = pygame.sprite.Group() # обнулим коллекцию бонусов
        player = Player() # пеесоздадим объект игрока
        all_sprites.add(player) # добавим объект игрока в коллекцию всех спрайтов
        for i in range(8): # создадим 8 метеоритов
            newmob() # ...
        score = 0 # установим счёт игрока в 0

    # Установим скорость смены кадров в секунду
    clock.tick(FPS) #
    for event in pygame.event.get(): # Считываем событие ввода
        if event.type == pygame.QUIT: # проверка для закрытия окна
            running = False # опустим флаг работы

    # Обновление #
    all_sprites.update() # вызовем методы update для всех спрайтов в коллекции

    # проверьте, не попала ли пуля в моб #
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)#получаем список коллизий групп mobs и bullets
    for hit in hits: # цикл по всем коллизиям
        score += 50 - hit.radius # прибавим счёт игроку
        random.choice(expl_sounds).play() # проиграем звук
        expl = Explosion(hit.rect.center, 'lg') # создадим объект взрыва
        all_sprites.add(expl) # добавим объект взрыва ко всем спрайтам
        if random.random() > 0.9: # с вероятностью 0.1
            pow = Pow(hit.rect.center) # создадим объект бонуса
            all_sprites.add(pow) # добавим в глобальную коллекцию
            powerups.add(pow) # добавим в глобальную коллекцию
        newmob() # создадим новый метеорит вместо того, с которым столкнулись

    #  Проверка, не ударил ли моб игрока #
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # получаем список коллизий
    for hit in hits: # перебираем все коллизии
        player.shield -= hit.radius * 2 # уменьшаем щит игрока
        expl = Explosion(hit.rect.center, 'sm') # создадим объект взрыва
        all_sprites.add(expl) # добавим его вв глобальный список спрайтов
        newmob() # создадим моба вместо того, который врезался в игрока
        if player.shield <= 0: # если щит у игрока меньше ноля
            death_explosion = Explosion(player.rect.center, 'player') # создадим объект взрыва
            all_sprites.add(death_explosion) # добавим его в глобальную коллекцию
            player.hide() # скроем игрока, ведь щит у него меньше ноля
            player.lives -= 1 # уменьшим кол-во жизней у игрока на единицу
            player.shield = 100 # щит снова сотка - ведь мы отняли одну жизнь

    # Проверка столкновений игрока и бонуса #
    hits = pygame.sprite.spritecollide(player, powerups, True) # получаем список коллизий
    for hit in hits: # для каждой коллизии
        if hit.type == 'shield': # если бонус это "Щит", тогда
            player.shield += random.randrange(10, 30) #
            if player.shield >= 100: # добавим показателей щиту если их не хватает
                player.shield = 100 # ...
        if hit.type == 'gun': # если бонус это 'пушка'
            player.powerup() # переключим объект игрока в режим 'powerup'
            power_sound.play() # и проиграем звук

    # Если игрок умер, игра окончена #
    if player.lives == 0 and not death_explosion.alive():
        game_over = True # поднимаем флажок конца игры

    # Рендеринг сцены #
    screen.fill(BLACK) # заполняем всё окно чёрным
    screen.blit(background, background_rect) # выводим фоновую картинку
    all_sprites.draw(screen) # отрисовываем все спрайты встроенной функцией pygame
    draw_text(screen, str(score), 18, WIDTH / 2, 10) # выводим счёт игрока текстом
    draw_shield_bar(screen, 5, 5, player.shield) # выводим полоску щита
    draw_lives(screen, WIDTH - 100, 5, player.lives, #
               player_mini_img) # отрисовываем количество жизней игрока

    # После отрисовки всего, меняем экранные страницы #
    pygame.display.flip() # ...

pygame.quit() # завершает приложение на базе pygame