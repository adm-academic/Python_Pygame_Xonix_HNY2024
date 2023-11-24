import pygame
import random
import os
import inspect
import sys

class Snow_Flake(pygame.sprite.Sprite):  # Класс спрайта "Снежинка"
    def __init__(self, scene_initial, settings ):  # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.scene_initial = scene_initial
        self.image = random.choice( self.scene_initial.snow_flakes_list )
        self.image.set_colorkey(self.settings.BLACK)  # установка прозрачного цвета спрайта
        self.rect = self.image.get_rect()  # получим прямоугольник для спрайта
        pass
        self.rect.x = random.randrange(self.settings.WIDTH - self.rect.width)  #
        self.rect.y = random.randrange(self.settings.HEIGHT - self.rect.height)  #
        self.speedx = random.randrange(-2, 2)  #
        self.speedy = random.randrange(4, 7)  #
        pass

    def update(self):  # метод обновляющий спрайт в соответсвии с игровой логикой
        self.rect.x += self.speedx  # сместить по горизонтали
        self.rect.y += self.speedy  # сместить по вертикали
        if (self.rect.top > self.settings.HEIGHT + 10 or self.rect.left < -25
                or self.rect.right > self.settings.WIDTH + 20):  # если снежинка
            # вылетела за пределы окна, то переместить её в зону спауна
            self.rect.x = random.randrange(self.settings.WIDTH - self.rect.width)  #
            self.rect.y = random.randrange(-100, -40)  #
            self.speedx = random.randrange(-3, 3)  #
            self.speedy = random.randrange(1, 8)  #


class Menu_Button(pygame.sprite.Sprite):
    def __init__(self, game, scene_initial, settings ):  # констуктор
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.scene_initial = scene_initial
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


class Scene_Initial():
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
        self.menu_buttons_group = pygame.sprite.Group()
        pass
        self.menu_button_player_new = Menu_Button(self.game, self, self.settings)
        self.menu_button_player_new.set_params(150, self.settings.WIDTH // 2, 50, 500,
                                        pygame.K_1, "Создать нового игрока.")
        self.menu_buttons_group.add(self.menu_button_player_new)
        pass
        self.menu_button_new_game = Menu_Button(self.game, self, self.settings)
        self.menu_button_new_game.set_params(250, self.settings.WIDTH // 2, 50, 500,
                                             pygame.K_2, "Новая игра.")
        self.menu_buttons_group.add(self.menu_button_new_game)
        pass
        self.menu_button_continue = Menu_Button(self.game, self, self.settings)
        self.menu_button_continue.set_params(350, self.settings.WIDTH // 2, 50, 500,
                                        pygame.K_3, "Продолжить игру.")
        self.menu_buttons_group.add(self.menu_button_continue)
        pass
        self.menu_button_settings = Menu_Button(self.game, self, self.settings)
        self.menu_button_settings.set_params(450, self.settings.WIDTH // 2, 50, 500,
                                        pygame.K_4, "Настройки.")
        self.menu_buttons_group.add(self.menu_button_settings)
        pass
        self.menu_button_records = Menu_Button(self.game, self, self.settings)
        self.menu_button_records.set_params(550, self.settings.WIDTH // 2, 50, 500,
                                             pygame.K_5, "Рекорды.")
        self.menu_buttons_group.add(self.menu_button_records)
        self.menu_button_quit = Menu_Button(self.game, self, self.settings)
        self.menu_button_quit.set_params(650, self.settings.WIDTH // 2, 50, 500,
                                            pygame.K_6, "Выйти из игры.")
        self.menu_buttons_group.add(self.menu_button_quit)
        pass
        self.snow_flakes_list = []
        self.snow_flakes_list.append( pygame.image.load("images/sf1.png").convert() )
        self.snow_flakes_list.append( pygame.image.load("images/sf2.png").convert() )
        self.snow_flakes_list.append( pygame.image.load("images/sf3.png").convert() )
        self.snow_flakes_list.append( pygame.image.load("images/sf4.png").convert() )
        self.snow_flakes_list.append( pygame.image.load("images/sf5.png").convert() )
        pass
        self.sfs = pygame.sprite.Group()
        for i in range(20):
            self.sfs.add( Snow_Flake(self,self.settings) )
        pass
        self.spruce = pygame.image.load('images/spruce.png').convert_alpha()
        self.spruce.set_colorkey(self.settings.BLACK)
        pass


    def unload_scene(self):
        self.game.screen.fill(self.settings.BLACK)  # заполняем всё окно чёрным
        self.image_backround = None
        self.menu_button_new_game = None
        pass
    def reload_scene(self):
        pass
    def update(self):
        self.sfs.update()
        for button in self.menu_buttons_group:
            button.update()

    def draw(self):
        self.game.screen.blit(self.image_backround, self.image_backround_rect)
        self.game.screen.blit(self.spruce, (self.settings.WIDTH - self.spruce.get_width(),
                                            self.settings.HEIGHT - self.spruce.get_height()))
        self.sfs.draw(self.game.screen)
        for button in self.menu_buttons_group:
            button.draw(self.game.screen)

    def scene_loop(self):
        while True:
            self.game.clock.tick(self.settings.FPS)  # задаём кадры в секунду
            for event in pygame.event.get():  # перебираем все поступившие события
                if event.type == pygame.QUIT:  # событие выхода из программы
                    self.game.exit_from_game()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game.go_to_scene(self.game.SCENE_NEW_PLAYER)
                        return
                    if event.key == pygame.K_2:
                        self.game.go_to_scene(self.game.SCENE_PLAY)
                        return
                    if event.key == pygame.K_3:
                        self.game.go_to_scene(self.game.SCENE_LEVELS)
                        return
                    if event.key == pygame.K_4:
                        self.game.go_to_scene(self.game.SCENE_SETTINGS)
                        return
                    if event.key == pygame.K_5:
                        self.game.go_to_scene(self.game.SCENE_RECORDS)
                        return
                    if event.key == pygame.K_6:
                        self.game.exit_from_game()
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if self.menu_button_player_new.rect.collidepoint(mouse_position):
                        self.game.go_to_scene(self.game.SCENE_NEW_PLAYER)
                        return
                    if self.menu_button_new_game.rect.collidepoint(mouse_position):
                        self.game.go_to_scene(self.game.SCENE_PLAY)
                        return
                    elif self.menu_button_continue.rect.collidepoint(mouse_position):
                        self.game.go_to_scene(self.game.SCENE_LEVELS)
                        return
                    elif self.menu_button_settings.rect.collidepoint(mouse_position):
                        self.game.go_to_scene(self.game.SCENE_SETTINGS)
                        return
                    elif self.menu_button_records.rect.collidepoint(mouse_position):
                        self.game.go_to_scene(self.game.SCENE_RECORDS)
                        return
                    elif self.menu_button_quit.rect.collidepoint(mouse_position):
                        self.game.exit_from_game()
                        return

            self.update()
            self.draw()


            pygame.display.flip()