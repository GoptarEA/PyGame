import pygame
import sys
import time

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

buttons_list = []


class Button(pygame.Surface):
    def __init__(self, button_text, color, hovercolor, coords, onclickfunc=None):
        super().__init__((pygame.font.Font(None, 30).render(button_text, 1, (0, 0, 0)).get_width() + 20,
                          pygame.font.Font(None, 30).render(button_text, 1, (0, 0, 0)).get_height() + 15))
        font = pygame.font.Font(None, 30)
        text = font.render(button_text, 1, (0, 0, 0))
        self.hovercolor = hovercolor
        self.coords = coords[0] + 150, coords[1] + 50
        self.fill(color)
        self.convert_alpha()
        self.blit(text, (10, 10))

        self.onclickfunc = onclickfunc

    def click(self, pos):
        print(pos)
        print(self.coords)
        if self.coords[0] <= pos[0] <= self.coords[0] + self.get_width() and \
                self.coords[1] <= pos[1] <= self.coords[1] + self.get_height():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.fill(self.hovercolor)
            self.convert_alpha()
            self.onclickfunc()
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def hover(self, pos):
        if self.coords[0] <= pos[0] <= self.coords[0] + self.get_width() and \
                self.coords[1] <= pos[1] <= self.coords[1] + self.get_height():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class GameRules(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((500, 300)).convert_alpha()
        self.image.fill((255, 255, 255, 200))
        self.rect = self.image.get_rect().move(150, 50)

        font = pygame.font.Font(None, 30)
        text = font.render("Текст правил игры", 1, (50, 70, 0))
        self.image.blit(text, ((500 - text.get_width()) // 2, 20))
        self.button1 = Button("Начинаем", (200, 0, 0, 100), (0, 255, 0, 100), (100, 250), self.start_game)
        buttons_list.append(self.button1)
        self.image.blit(self.button1, (100, 250))

        self.button2 = Button("Отбой", (200, 0, 0, 100), (0, 255, 0, 100), (300, 250), self.quit_rules)
        buttons_list.append(self.button2)
        self.image.blit(self.button2, (300, 250))

    def quit_rules(self):
        print("ок, закрылись")
        menu_play.make_freeze()
        self.kill()

    def start_game(self):
        print("Игра началась")


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

        self.freeze = False

    def change_size(self, pos):
        if not self.freeze:
            if self.rect.left <= pos[0] <= self.rect.right and self.rect.top <= pos[1] <= self.rect.bottom:
                self.image = self.normal_image
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.image = self.small_image
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def check_click(self, pos):
        print('Нажалось')
        if not self.freeze:
            if self.rect.left <= pos[0] <= self.rect.right and self.rect.top <= pos[1] <= self.rect.bottom:
                all_sprites_list.add(GameRules())
                self.make_freeze()

    def make_freeze(self):
        self.freeze = not self.freeze
        print(self.freeze)


class Play(MenuPoint):
    def __init__(self, small_version, normal_version, coords):
        super().__init__(small_version, normal_version, coords)

    def start_game(self):
        pass


class Settings(MenuPoint):
    def __init__(self, small_version, normal_version, coords):
        super().__init__(small_version, normal_version, coords)


class Records(MenuPoint):
    def __init__(self, small_version, normal_version, coords):
        super().__init__(small_version, normal_version, coords)


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

# Создание фона игры
bg = Background()
all_sprites_list.add(bg)


# Создание меню
menu_play = Play('play_small.png', 'play.png', (400, 200))
menu_settings = Settings('settings_small.png', 'settings.png', (130, 250))
menu_records = Records('records_small.png', 'records.png', (670, 250))
all_sprites_list.add(menu_play)
all_sprites_list.add(menu_settings)
all_sprites_list.add(menu_records)



pygame.display.update()
generate_level(load_level('1.txt'))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            menu_play.change_size(event.pos)
            menu_records.change_size(event.pos)
            menu_settings.change_size(event.pos)

            for bt in buttons_list:
                bt.hover(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for bt in buttons_list:
                bt.click(event.pos)


            menu_play.check_click(event.pos)

    for sprite in all_sprites_list:
        sprite.update()
    all_sprites_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)

