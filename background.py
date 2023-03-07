import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/Objects/bg.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0, 0)

    def set_width(self, counts):
        pass
