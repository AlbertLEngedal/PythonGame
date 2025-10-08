import pygame as pg
def scale_to_width(image, target_w: int):
    w, h = image.get_size()
    target_h = int(h * (target_w / w))
    return pg.transform.smoothscale(image, (target_w, target_h))


class Player:
    def __init__(self, x, y):
        self.image = pg.image.load("assets/jet/afterburner0.png").convert_alpha()
        self.image = scale_to_width(self.image,200)
        self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.x = x
        self.y = y
        
    def new_image(self, variation):
        if variation == 0:
            self.image = pg.image.load("assets/jet/afterburner0.png").convert_alpha()
            # self.speed = 5
        if variation == 1:
            self.image = pg.image.load("assets/jet/afterburner3.png").convert_alpha()
            # self.speed = 5
            
        self.image = scale_to_width(self.image,200)
        self.image = pg.transform.flip(self.image, True, False)
        # self.rect = self.image.get_rect(center=(self.x, self.y))
            

    def handle_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
            self.new_image(1)
        else:
            self.new_image(0)
            
        if keys[pg.K_UP]:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
