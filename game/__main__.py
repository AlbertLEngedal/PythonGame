import os
import sys
import time

import pygame as pg

from player import Jet, Heli
from game_logic import *


# --- scrolling bg uses a parallax factor instead of fixed speed_x ---
class ScrollingBG:
    def __init__(self, image_path: str, factor: float, screen_size: tuple[int, int],
                 align_bottom: bool = True, y: int | None = None, convert_alpha: bool = True):
        img = pg.image.load(image_path)
        self.img = img.convert_alpha() if convert_alpha else img.convert()
        self.w, self.h = self.img.get_size()
        self.factor = factor
        self.off_x = 0.0
        self.screen_w, self.screen_h = screen_size
        self.y = (self.screen_h - self.h) if (align_bottom and y is None) else (0 if y is None else y)

    # now needs base_v
    def update(self, dt: float, base_v: float):
        # positive base_v moves scenery left (camera right)
        self.off_x = (self.off_x + self.factor * base_v * dt) % self.w

    def draw(self, surf: pg.Surface):
        ox = int(self.off_x)
        x = -ox
        while x < self.screen_w:
            surf.blit(self.img, (x, self.y))
            x += self.w






pg.init()

WIDTH = 1920
HEIGHT = 1080

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fighter Jet Game")

screen_size = (WIDTH, HEIGHT)

Player1 = Heli(300, 300) 
# Basisfart (px/s) – juster denne for hele scenens tempo
BASE = Player1.accelearation

# Lag: bakerst til forrest (langsomme -> raske)
bg_layers = [
    ScrollingBG("assets/desert_sky.png",       factor=0.35, screen_size=screen_size, align_bottom=False, y=80),
    ScrollingBG("assets/desert_moon.png",      factor=0.40, screen_size=screen_size, align_bottom=False, y=40),
    ScrollingBG("assets/desert_cloud.png",     factor=0.50, screen_size=screen_size, align_bottom=False, y=80),
    ScrollingBG("assets/desert_mountain.png",  factor=0.75, screen_size=screen_size),
    ScrollingBG("assets/desert_dunemid.png",   factor=1.00, screen_size=screen_size),
    ScrollingBG("assets/desert_dunefront.png", factor=1.30, screen_size=screen_size),
]







# Clock (for FPS control)
clock = pg.time.Clock()
FPS = 60


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

 


screen_size = (1920, 1080)
# bg = ScrollingBG("assets/background/mountain.png", speed=( +300, 0 ), screen_size=screen_size)

BASE_V = 0
MAX_V = 1400
MIN_V = -1400


# --- Game Loop ---
running = True
while running:
    
    # BASE =
    # --- Events ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # main loop
    dt = clock.get_time() / 1000.0
    print(Player1.accelearation)
    BASE_V = max(MIN_V, min(MAX_V, BASE_V + Player1.accelearation * dt))
    
    if BASE_V >= MAX_V:
        Player1.allow_movement = False
    else:
        Player1.allow_movement = True

    screen.fill((0, 0, 0))
    for bg in bg_layers:
        bg.update(dt, BASE_V)
        bg.draw(screen)
        
    

  

    Player1.handle_keys()
    Player1.draw(screen)

    pg.display.flip()
    clock.tick(FPS)


pg.quit()
sys.exit()


print("Game Over")