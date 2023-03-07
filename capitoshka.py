import pygame
import time


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
