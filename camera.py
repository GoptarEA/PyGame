import pygame

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 800 // 2)