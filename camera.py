

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