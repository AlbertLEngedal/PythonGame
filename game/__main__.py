import os
import sys
import time

import pygame as pg

from game.player import Player


pg.init()

def get_scaled_resolution(scale: float) -> tuple[int, int]:
    base_width, base_height = 1920, 1080
    width = int(base_width * scale)
    height = int(base_height * scale)
    return width, height

# Screen
WIDTH, HEIGHT = get_scaled_resolution(1)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fighter Jet Game")

# Clock (for FPS control)
clock = pg.time.Clock()
FPS = 60


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

Player1 = Player(200, 200)  

# --- Game Loop ---
running = True
while running:
    # --- Events ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


  

    Player1.handle_keys()
    
    screen.fill(BLACK)
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
