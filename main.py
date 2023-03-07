import pygame
import sys
from capitoshka import Capitoshka
from level_generator import generate_level, load_level, elements_group
from camera import Camera
from menu import Play
from background import Background

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Jumper")
pygame.display.set_icon(pygame.image.load('Sprites/Objects/icon.png'))

all_sprites_list = pygame.sprite.Group()

menu_play = Play()
camera = Camera(all_sprites_list, elements_group)
# cap = Capitoshka()

bg = Background()






# all_sprites_list.add(cap)
all_sprites_list.add(bg)
all_sprites_list.add(menu_play)

# generate_level(load_level('1.txt'))
pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    menu_play.update()
    # cap.update()
    # camera.update(cap)

    all_sprites_list.draw(screen)
    elements_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)

