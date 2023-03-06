import pygame
import sys
from car import Car
from background import Background
from level_generator import generate_level, load_level, elements_group

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Jumper")
pygame.display.set_icon(pygame.image.load('Sprites/Objects/icon.png'))


all_sprites_list = pygame.sprite.Group()

car = Car("Sprites/Objects/red_point.png", (300, 400))
background = Background("Sprites/Objects/фон.jpg", (0, 0))
all_sprites_list.add(background)
all_sprites_list.add(car)

generate_level(load_level('1.txt'))
pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    car.update()
    all_sprites_list.draw(screen)
    elements_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)

