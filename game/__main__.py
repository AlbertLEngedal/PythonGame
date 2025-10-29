import os
import sys
import time

import pygame as pg

from player import Jet, Heli
from game_logic import *


# --- scrolling bg uses a parallax factor instead of fixed speed_x ---
class ScrollingBG:
    """
    Simple horizontally tiling background layer with parallax scrolling.

    - `factor` controls how fast this layer scrolls relative to the base world speed.
      Values < 1 move slower (farther away), > 1 move faster (closer).
    - Positive `base_speed` in `update()` moves scenery to the left (camera moves right).
    - The image is repeated to fill the screen width.
    """
    def __init__(self, image_path: str, factor: float, screen_size: tuple[int, int],
                 align_bottom: bool = True, y: int | None = None, convert_alpha: bool = True):
        # Load the image (convert for faster blitting).
        img = pg.image.load(image_path)
        self.image = img.convert_alpha() if convert_alpha else img.convert()

        # Cache dimensions for clarity.
        self.image_width, self.image_height = self.image.get_size()
        self.screen_width, self.screen_height = screen_size

        # Parallax factor and current horizontal offset.
        self.parallax_factor = factor
        self.offset_x = 0.0

        # Decide the vertical position:
        # - If an explicit y is provided, use it.
        # - Otherwise, either align to the bottom of the screen or to the top.
        if y is not None:
            self.y = y
        elif align_bottom:
            self.y = self.screen_height - self.image_height
        else:
            self.y = 0

    def update(self, delta_time: float, base_speed: float) -> None:
        """
        Advance the horizontal offset based on time and base speed.
        Keeps the offset within [0, image_width) using simple wrap logic.
        """
        # Move according to parallax; positive base_speed moves background left.
        self.offset_x += self.parallax_factor * base_speed * delta_time

        # Wrap the offset so it never grows unbounded.
        while self.offset_x >= self.image_width:
            self.offset_x -= self.image_width
        while self.offset_x < 0:
            self.offset_x += self.image_width

    def draw(self, surface: pg.Surface) -> None:
        """
        Draw enough tiles of the image to fill the entire screen width.
        """
        start_x = -int(self.offset_x)
        x = start_x
        while x < self.screen_width:
            surface.blit(self.image, (x, self.y))
            x += self.image_width




class Game: 
    
    def __init__(self):
        

        pg.init()

        WIDTH = 1920
        HEIGHT = 1080
        # WIDTH = 1000
        # HEIGHT = 500


        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Fighter Jet Game")

        screen_size = (WIDTH, HEIGHT)

        Player1 = Heli(self, 600, 400) 
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
        MAX_V = 400
        MIN_V = -400


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
            # print(Player1.accelearation)
            # BASE_V = Player1.accelearation * dt
            BASE_V = Player1.bakgrunnsfart #Legge til min og max
            BASE_V = max(MIN_V, min(MAX_V, BASE_V))
            
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

if __name__ == "__main__":
    TheGame = Game()