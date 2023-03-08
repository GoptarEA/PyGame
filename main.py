import pygame
import sys

element_images = {
    "grey_point": pygame.image.load("Sprites/Objects/grey_point.png"),
    "green_point": pygame.image.load("Sprites/Objects/green_point.png"),
    "red_point": pygame.image.load("Sprites/Objects/red_point.png"),
    "shape_point": pygame.image.load("Sprites/Objects/shape_point.png"),
    "small_tower": pygame.image.load("Sprites/Objects/small_tower.png"),
    "big_tower": pygame.image.load("Sprites/Objects/big_tower.png")
}

element_width = 100

elements_group = pygame.sprite.Group()


class PointElement(pygame.sprite.Sprite):
    def __init__(self, element_type, pos_x):
        super().__init__(elements_group)
        self.image = element_images[element_type]
        self.rect = self.image.get_rect().move((element_width + 20) * pos_x + 20,
                                               pygame.display.get_window_size()[1] - self.image.get_height() - 50)

    def change_color(self):
        pass

    def touch_animation(self):
        pass


def load_level(level_filename):
    level_filename = "Levels/" + level_filename
    return [elem for elem in open(level_filename, 'r').readline()]


def generate_level(level):
    for x in range(len(level)):
        if level[x] == '.':
            PointElement("grey_point", x)
        elif level[x] == ',':
            PointElement("green_point", x)
        elif level[x] == '|':
            PointElement("big_tower", x)
        elif level[x] == '+':
            PointElement("shape_point", x)


class MenuPoint(pygame.sprite.Sprite):
    def __init__(self, small_version, normal_version, coords):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/Objects/' + small_version)
        self.rect = self.image.get_rect()
        self.rect.w = self.rect.width
        self.rect.h = self.rect.height
        self.small_image = pygame.image.load('Sprites/Objects/' + small_version)
        self.normal_image = pygame.image.load('Sprites/Objects/' + normal_version)
        self.rect.center = coords

    def change_size(self, pos):
        if self.rect.left <= pos[0] <= self.rect.right and self.rect.top <= pos[1] <= self.rect.bottom:
            self.image = self.normal_image
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.image = self.small_image
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self):
        pass



class Play(MenuPoint):
    def __init__(self, small_version, normal_version, coords):
        super().__init__(small_version, normal_version, coords)

    def update(self):
        super().update()

    def start_game(self):
        pass


class Settings(MenuPoint):
    def __init__(self, small_version, normal_version, coords):
        super().__init__(small_version, normal_version, coords)

    def update(self):
        super().update()


class Records(MenuPoint):
    def __init__(self, small_version, normal_version, coords):
        super().__init__(small_version, normal_version, coords)

    def update(self):
        super().update()


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/Objects/bg.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0, 0)

    def set_width(self, counts):
        pass


class Camera:
    def __init__(self, all_sprites_list, elements_group):
        self.dx = 0
        self.all_sprites_list = all_sprites_list
        self.elements_group = elements_group

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 800 // 2)
        for element in self.all_sprites_list:
            self.apply(element)

        for element in self.elements_group:
            self.apply(element)


class Capitoshka(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/Objects/red_point.png")
        self.rect = self.image.get_rect()
        self.rect.w = self.rect.width
        self.rect.h = self.rect.height
        self.rect.center = (300, 400)
        self.gravitation = 3
        self.current_time = time.time()
        self.is_jumping = False
        self.jump_counter = 100

    def animation(self):
        pass

    def update(self):
        # self.rect.y += self.gravitation
        if self.is_jumping:
            self.jump()
        pygame.key.set_repeat(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 10
        elif keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True

    def jump(self):
        if self.jump_counter >= -100:
            self.rect.y -= self.jump_counter / 2.5
            self.jump_counter -= 10
        else:
            self.jump_counter = 100
            self.is_jumping = False


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Jumper")
pygame.display.set_icon(pygame.image.load('Sprites/Objects/icon.png'))

all_sprites_list = pygame.sprite.Group()


# Создание меню
menu_play = Play('play_small.png', 'play.png', (400, 200))
menu_settings = Settings('settings_small.png', 'settings.png', (130, 250))
menu_records = Records('records_small.png', 'records.png', (670, 250))
all_sprites_list.add(menu_play)
all_sprites_list.add(menu_settings)
all_sprites_list.add(menu_records)

# Создание фона игры
bg = Background()
all_sprites_list.add(bg)


generate_level(load_level('1.txt'))
pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    menu_play.update()
    menu_settings.update()
    menu_records.update()

    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

