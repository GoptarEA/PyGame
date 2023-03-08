import pygame


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

    def update(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.colliderect(pygame.Rect((x, y, x, y))):
            self.image = self.normal_image
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.image = self.small_image
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


class Play(MenuPoint):
    def __init__(self, small_version, normal_version, coords):
        super().__init__(small_version, normal_version, coords)

    def update(self):
        super().update()


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