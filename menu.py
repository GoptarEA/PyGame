import pygame

class MenuPoint(pygame.sprite.Sprite):
    def __init__(self, small_version, normal_version, coords):
        pass


    def update(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.colliderect(pygame.Rect((x, y, x, y))):
            self.image = pygame.image.load('Sprites/Objects/play.png')
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.image = pygame.image.load('Sprites/Objects/play_small.png')
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)



class Play(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/Objects/play_small.png')
        self.rect = self.image.get_rect()
        self.rect.w = self.rect.width
        self.rect.h = self.rect.height
        self.rect.center = 400, 200

    def update(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.colliderect(pygame.Rect((x, y, x, y))):
            self.image = pygame.image.load('Sprites/Objects/play.png')
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.image = pygame.image.load('Sprites/Objects/play_small.png')
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)