import os
import sys
import time

import pygame as pg

from player import Player

class ScrollingBG:
    def __init__(self, image_path: str, speed: tuple[int, int], screen_size: tuple[int, int]):
        self.img = pg.image.load(image_path).convert()
        self.w, self.h = self.img.get_size()
        self.speed_x, self.speed_y = speed
        
        # self.img = pg.image.load(image_path).convert()
        self.img = pg.transform.smoothscale_by(self.img, 1)
        
        self.off_x = 0
        self.off_y = 0
        self.screen_w, self.screen_h = screen_size

    def update(self, dt: float):
        self.off_x = (self.off_x + self.speed_x * dt) % self.w
        self.off_y = (self.off_y + self.speed_y * dt) % self.h

    def draw(self, surf: pg.Surface):
        ox, oy = int(self.off_x), int(self.off_y)
        # top-left tile start
        start_x = -ox
        start_y = -oy 
        # draw just enough tiles to cover screen (at most 4)
        for y in (start_y, start_y + self.h):
            for x in (start_x, start_x + self.w):
                surf.blit(self.img, (x, y))




pg.init()

# def get_scaled_resolution(scale: float) -> tuple[int, int]:
#     base_width, base_height = 1920, 1080
#     width = int(base_width * scale)
#     height = int(base_height * scale)
#     return width, height

# Screen
# WIDTH, HEIGHT = get_scaled_resolution(1)
WIDTH = 1920
HEIGHT = 1080

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fighter Jet Game")

# Clock (for FPS control)
clock = pg.time.Clock()
FPS = 60


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

Player1 = Player(300, 300)  

# init
# screen_size = (screen.get_width, screen.get_height)
screen_size = (1920, 1080)
bg = ScrollingBG("assets/background/bg.png", speed=( +80, 0 ), screen_size=screen_size)




# --- Game Loop ---
running = True
while running:
    # --- Events ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # main loop
    dt = clock.get_time() / 1000.0
    bg.update(dt)
    bg.draw(screen)
  

    Player1.handle_keys()
    
    # screen.fill(BLACK)
    Player1.draw(screen)
    

    
    # keys = pg.key.get_pressed()
    # if keys[pg.K_LEFT]:
    #     screen.fill(BLUE)
    # if keys[pg.K_RIGHT]:
    #     screen.fill(RED)



   
    
    

    pg.display.flip()  # update screen
    # --- Limit FPS ---
    clock.tick(FPS)


pg.quit()
sys.exit()


