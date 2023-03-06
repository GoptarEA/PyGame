import pygame

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


print(load_level('1.txt'))
