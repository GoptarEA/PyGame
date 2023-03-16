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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.frame_count = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.frame_count > 10 ** 20:
            self.frame_count %= 10


class Button(pygame.Surface):
    def __init__(self, button_text, color, hovercolor, coords, onclickfunc=None):
        super().__init__((pygame.font.Font("Roboto-Medium.ttf", 30).render(button_text, 1, (0, 0, 0)).get_width() + 20,
                          pygame.font.Font("Roboto-Medium.ttf", 30).render(
                              button_text,
                              1,
                              (0, 0, 0)).get_height() + 15))
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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = pygame.image.load('Sprites/Objects/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10
        self.direction = 1 if not direction else -1

    def update(self):
        self.rect.x += self.speedx * self.direction
        if self.rect.left > 800:
            self.kill()


class PauseGameButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 50)).convert_alpha()
        self.image.fill((255, 255, 255, 50))
        self.rect = self.image.get_rect().move(30, 10)
        font = pygame.font.Font(None, 30)
        text = font.render("Пауза", 1, (50, 70, 0))
        self.image.blit(text, ((100 - text.get_width()) // 2, 20))


class PointsCount(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50)).convert_alpha()
        self.image.fill((255, 255, 255, 50))
        self.rect = self.image.get_rect().move(730, 10)
        self.points = 100
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.points), 1, (50, 70, 0))
        self.image.blit(text, ((50 - text.get_width()) // 2, 20))

    def increase_points(self):
        self.points -= 5
        self.image.fill((255, 255, 255, 50))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.points), 1, (50, 70, 0))
        self.image.blit(text, ((50 - text.get_width()) // 2, 20))

    def decrease_points(self):
        self.points += 15
        self.image.fill((255, 255, 255, 50))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.points), 1, (50, 70, 0))
        self.image.blit(text, ((50 - text.get_width()) // 2, 20))

    def extra_decrease(self):
        self.points -= 50
        self.image.fill((255, 255, 255, 50))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.points), 1, (50, 70, 0))
        self.image.blit(text, ((50 - text.get_width()) // 2, 20))

    def refresh_point(self):
        self.points = 100
        self.image.fill((255, 255, 255, 50))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.points), 1, (50, 70, 0))
        self.image.blit(text, ((50 - text.get_width()) // 2, 20))

class GameRules(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((500, 300)).convert_alpha()
        self.image.fill((255, 255, 255, 200))
        self.rect = self.image.get_rect().move(150, 50)

        font = pygame.font.Font(None, 30)
        text = font.render("Текст правил игры", 1, (50, 70, 0))
        self.image.blit(text, ((500 - text.get_width()) // 2, 20))

        text_rules1 = font.render("Нажимайте пробел чтобы ", 1, (50, 70, 0))
        self.image.blit(text_rules1, ((500 - text_rules1.get_width()) // 2, 70))

        text_rules2 = font.render("выполнить прыжок и S", 1,
                                  (50, 70, 0))
        self.image.blit(text_rules2, ((500 - text_rules2.get_width()) // 2, 100))

        text_rules3 = font.render("чтобы стрелять по врагам", 1,
                                  (50, 70, 0))
        self.image.blit(text_rules3, ((500 - text_rules3.get_width()) // 2, 130))

        self.button1 = Button("Начинаем", (200, 0, 0, 100), (0, 255, 0, 100), (100, 250), self.start_game)
        buttons_list.append(self.button1)
        self.image.blit(self.button1, (100, 250))

        self.button2 = Button("Отбой", (200, 0, 0, 100), (0, 255, 0, 100), (300, 250), self.quit_rules)
        buttons_list.append(self.button2)
        self.image.blit(self.button2, (300, 250))

    def quit_rules(self):
        self.kill()
        for enemy in enemies:
            enemy.kill()
        for point in level_group:
            point.kill()
        for player in player_group:
            player.kill()
        for sprite in all_sprites_list:
            sprite.kill()
        all_sprites_list.add(bg)
        all_sprites_list.add(menu_play)
        all_sprites_list.add(menu_settings)
        all_sprites_list.add(menu_records)
        menu_play.make_freeze()

    def start_game(self):
        self.kill()
        for sprite in all_sprites_list:
            print(sprite)
            sprite.kill()

        for enemy in enemies:
            enemy.kill()
        for point in level_group:
            point.kill()

        print(all_sprites_list)
        for player in player_group:
            player.kill()

        generate_level(load_level("1.txt"))
        print("Игра началась")


class FinalWindow(pygame.sprite.Sprite):
    def __init__(self, game_result):
        super().__init__()
        self.image = pygame.Surface((500, 300)).convert_alpha()
        self.image.fill((255, 255, 255, 200))
        self.rect = self.image.get_rect().move(150, 50)

        font = pygame.font.Font(None, 30)
        text = font.render(game_result, 1, (50, 70, 0))
        self.image.blit(text, ((500 - text.get_width()) // 2, 20))

        self.button1 = Button("В меню", (200, 0, 0, 100), (0, 255, 0, 100), (100, 250), self.back_to_menu)
        buttons_list.append(self.button1)
        self.image.blit(self.button1, (100, 250))
        if game_result == "Вы проиграли!":
            self.button2 = Button("Заново", (200, 0, 0, 100), (0, 255, 0, 100), (300, 250), self.start_game)
            buttons_list.append(self.button2)
            self.image.blit(self.button2, (300, 250))
        else:
            self.button2 = Button(
                "Следующий уровень",
                (200, 0, 0, 100),
                (0, 255, 0, 100),
                (300, 250),
                self.start_game
            )
            buttons_list.append(self.button2)
            self.image.blit(self.button2, (300, 250))

    def back_to_menu(self):
        self.kill()
        for enemy in enemies:
            enemy.kill()
        for point in level_group:
            point.kill()
        for player in player_group:
            player.kill()
        for sprite in all_sprites_list:
            sprite.kill()
        all_sprites_list.add(bg)
        all_sprites_list.add(menu_play)
        all_sprites_list.add(menu_settings)
        all_sprites_list.add(menu_records)
        menu_play.make_freeze()


    def start_game(self):
        menu_play.make_freeze()
        for sprite in all_sprites_list:
            print(sprite)
            sprite.kill()
        print(all_sprites_list)
        print("-------------------")
        for sprite in all_sprites_list:
            print(sprite)
        print("-------------------")
        self.kill()
        for player in player_group:
            player.kill()
        generate_level(load_level(str(CURRENT_LEVEL) + ".txt"))
        print(pc.points)
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
    all_sprites_list.add(bg)
    all_sprites_list.add(pc)
    all_sprites_list.add(PauseGameButton())
    count = -1
    for x in range(len(level)):
        if level[x] == '.':
            count += 1
            level_group.add(PointElement("grey_point", count))
        elif level[x] == ',':
            count += 1
            level_group.add(PointElement("green_point", count))
        elif level[x] == '|':
            count += 1
            level_group.add(PointElement("big_tower", count))
        elif level[x] == '+':
            count += 1
            level_group.add(PointElement("shape_point", count))
        elif level[x] == "*":
            if "$" in level[x + 1:]:
                enemies.add(AnimatedSprite(
                    pygame.image.load("Sprites/Objects/Scan.png"),
                    8,
                    1,
                    120 * count + 50,
                    int("".join(level[x + 1: level.index("$", x + 1)]))
                ))

    player_group.add(cap)


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
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.target_pos_x = 70

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = self.target_pos_x - target.rect.x
        self.target_pos_x = target.rect.x

    def refresh_pos_x(self):
        print("Бфыл вызван рефреш", self.target_pos_x)
        self.target_pos_x = 70
        self.dx = 0

class Capitoshka(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/Objects/player.png")
        self.rect = self.image.get_rect()
        self.rect.w = self.rect.width
        self.rect.h = self.rect.height
        self.rect.center = (70, 310)
        self.gravitation = 2
        self.current_time = time.time()
        self.is_jumping = False
        self.jump_counter = 120
        self.direction = 0

    def animation(self):
        pass

    def update(self):
        # self.rect.y += self.gravitation
        if self.direction:
            self.image = pygame.image.load("Sprites/Objects/player_left.png")
        else:
            self.image = pygame.image.load("Sprites/Objects/player.png")
        if self.is_jumping:
            self.jump()
        pygame.key.set_repeat(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
            self.direction = 1
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 10
            self.direction = 0
        elif keys[pygame.K_SPACE] and not self.is_jumping:
            print("сработал джамп")
            pc.increase_points()
            self.is_jumping = True

    def shoot(self):
        bullets.add(Bullet(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2, self.direction))
        pc.increase_points()

    def jump(self):
        if self.jump_counter >= -120:
            self.rect.y -= self.jump_counter / 2.5
            self.jump_counter -= 10
        else:
            self.jump_counter = 120
            self.is_jumping = False
    def refresh_position(self):
        self.rect.center = (70, 310)

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Jumper")
pygame.display.set_icon(pygame.image.load('Sprites/Objects/icon.png'))

all_sprites_list = pygame.sprite.Group()
level_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Создание фона игры
bg = Background()
all_sprites_list.add(bg)

# Создание камеры
camera = Camera()

pc = PointsCount()


cap = Capitoshka()
# Создание меню
menu_play = Play('play_small.png', 'play.png', (400, 200))
menu_settings = Settings('settings_small.png', 'settings.png', (130, 250))
menu_records = Records('records_small.png', 'records.png', (670, 250))

all_sprites_list.add(menu_play)
all_sprites_list.add(menu_settings)
all_sprites_list.add(menu_records)

CURRENT_LEVEL = 1
GAME_WAS_STARTED = False

running = True
while running:
    if pc.points <= 0:
        cap.refresh_position()
        camera.refresh_pos_x()
        for sprite in all_sprites_list:
            sprite.kill()
        for player in player_group:
            player.kill()

        for point in level_group:
            point.kill()
        for enemy in enemies:
            enemy.kill()
        for bullet in bullets:
            bullet.kill()
        print("--------------")
        print(all_sprites_list)
        all_sprites_list.add(FinalWindow("Вы проиграли!"))
        pc.refresh_point()

    elif len(enemies) == 0 and len(player_group) != 0:
        cap.refresh_position()
        camera.refresh_pos_x()
        for sprite in all_sprites_list:
            sprite.kill()
        for player in player_group:
            player.kill()

        for point in level_group:
            point.kill()
        for enemy in enemies:
            enemy.kill()
        for bullet in bullets:
            bullet.kill()
        print("--------------")
        print(all_sprites_list)
        all_sprites_list.add(FinalWindow("Вы выиграли!"))
        pc.refresh_point()
        CURRENT_LEVEL += 1

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                for player in player_group:
                    player.shoot()

    pygame.sprite.groupcollide(level_group, bullets, False, True)

    hit_enemy = pygame.sprite.groupcollide(enemies, bullets, True, True)

    hit_player = pygame.sprite.groupcollide(player_group, enemies, False, True)

    if hit_player:
        pc.extra_decrease()

    if hit_enemy:
        pc.decrease_points()

    for points in level_group:
        camera.apply(points)
        for player in player_group:
            if player.rect.right > points.rect.left and not player.is_jumping:
                player.rect.bottom = points.rect.top - 10

    for bullet in bullets:
        bullet.update()
        camera.apply(bullet)

    for player in player_group:
        player.update()
        camera.update(player)

    for sprite in all_sprites_list:
        sprite.update()
        # camera.apply(sprite)

    for enemy in enemies:
        enemy.update()
        camera.apply(enemy)

    all_sprites_list.draw(screen)
    level_group.draw(screen)
    player_group.draw(screen)
    bullets.draw(screen)
    enemies.draw(screen)

    pygame.display.flip()
    clock.tick(60)

