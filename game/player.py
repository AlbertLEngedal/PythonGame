import pygame as pg


def scale_to_width(image, target_width: int):
    width, height = image.get_size()
    target_height = int(height * (target_width / width))
    return pg.transform.smoothscale(image, (target_width, target_height))


class Jet:
    def __init__(self, x, y):
        # self.current_unchanged_image = pg.image.load(
        #     "assets/jet/afterburner0.png"
        # ).convert_alpha()
        # self.current_unchanged_image = scale_to_width(self.image, 200)
        # self.current_unchanged_image = pg.transform.flip(self.image, True, False)
        # self.image_original = self.image
        self.original_dimentions = 450, 135

        # self.rect = self.image.get_rect(center=(x, y))
        self.brakespeed = 15
        self.idlespeed = 5
        self.speed_cap = 8
        self.speed = self.idlespeed
        self.x = x
        self.y = y
        self.afterburner_timer = 0

        self.new_image("idle")

    def new_image(self, variation, afterburner_size=1):

        if variation == "spoiler":
            if afterburner_size <= 0:
                self.current_image = pg.image.load(
                    "assets/jet/spoiler/spoiler_afterburner0.png"
                ).convert_alpha()
            if afterburner_size == 1:
                self.current_image = pg.image.load(
                    "assets/jet/spoiler/spoiler_afterburner1.png"
                ).convert_alpha()
            if afterburner_size == 2:
                self.current_image = pg.image.load(
                    "assets/jet/spoiler/spoiler_afterburner2.png"
                ).convert_alpha()
            if afterburner_size == 3:
                self.current_image = pg.image.load(
                    "assets/jet/spoiler/spoiler_afterburner3.png"
                ).convert_alpha()

        if variation == "idle":
            if afterburner_size <= 0:
                self.current_image = pg.image.load(
                    "assets/jet/idle/idle_afterburner0.png"
                ).convert_alpha()
            if afterburner_size == 1:
                self.current_image = pg.image.load(
                    "assets/jet/idle/idle_afterburner1.png"
                ).convert_alpha()
            if afterburner_size == 2:
                self.current_image = pg.image.load(
                    "assets/jet/idle/idle_afterburner2.png"
                ).convert_alpha()
            if afterburner_size == 3:
                self.current_image = pg.image.load(
                    "assets/jet/idle/idle_afterburner3.png"
                ).convert_alpha()

        self.current_image = scale_to_width(self.current_image, 150)
        self.current_image = pg.transform.flip(self.current_image, True, False)
        self.active_image = self.current_image

        self.rect = self.active_image.get_rect(center=(self.x, self.y))

    def handle_keys(self):
        keys = pg.key.get_pressed()

        if self.afterburner_timer < 0:
            self.afterburner_timer = 0

        if keys[pg.K_UP]:
            self.y -= self.speed
        elif keys[pg.K_DOWN]:
            self.y += self.speed

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            show_image = "spoiler"
            self.x -= self.brakespeed

            self.afterburner_timer -= 5
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            show_image = "idle"
            self.x += self.speed

            self.afterburner_timer += 0.5
        else:
            show_image = "idle"
            self.afterburner_timer -= 5

        if self.afterburner_timer <= 0:
            self.new_image(show_image, 0)
            self.speed = self.idlespeed
        elif self.afterburner_timer > 0 and self.afterburner_timer < 15:
            self.new_image(show_image, 1)
            if not self.speed >= self.speed_cap:
                self.speed += 2
        elif self.afterburner_timer >= 10 and self.afterburner_timer < 30:
            self.new_image(show_image, 2)
            if not self.speed >= self.speed_cap:
                self.speed += 2
        elif self.afterburner_timer >= 20:
            self.new_image(show_image, 3)
            if not self.speed >= self.speed_cap:
                self.speed += 2

        # clamp angle to reasonable range

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)


class Heli:

    def __init__(self, x, y):
        self.original_dimentions = 1414, 420

        # self.rect = self.image.get_rect(center=(x, y))
        self.brakespeed = 15
        self.idlespeed = 10
        self.speed_cap = 15
        self.speed = self.idlespeed
        self.x = x
        self.y = y
        self.afterburner_timer = 0
        self.target_tilt = 0
        self.tilt = 0
        
        self.accelearation = 0
        self.last_accs = self.accelearation
        
        self.allow_movement = True
        
        self.new_image("side", 1, self.tilt)

    def new_image(self, variation, blades, tilt):

        if not self.tilt >= self.target_tilt:
            self.tilt += 1
        elif self.tilt > self.target_tilt:
            self.tilt -= 1

        if variation == "side":
            if blades == "revolve":
                if self.last_blade == 1:
                    blades = 2
                else:
                    blades = 1

            if blades == 1:
                self.current_image = pg.transform.rotate(
                    pg.image.load(
                        r"assets\attack_helicopter\pngs\flying_side_view\attack_helicopter_side_view_frame_1.png"
                    ),
                    self.tilt,
                )
            if blades == 2:
                self.current_image = pg.transform.rotate(
                    pg.image.load(
                        r"assets\attack_helicopter\pngs\flying_side_view\attack_helicopter_side_view_frame_2.png"
                    ),
                    self.tilt,
                )

        self.last_blade = blades
        self.current_image = scale_to_width(self.current_image, 300)
        self.current_image = pg.transform.flip(self.current_image, True, False)
        self.active_image = self.current_image

        self.rect = self.active_image.get_rect(center=(self.x, self.y))

    def handle_keys(self):
        keys = pg.key.get_pressed()

        # self.new_image("side", "revolve")
        # if self.afterburner_timer < 0:
        #     self.afterburner_timer = 0

        if keys[pg.K_UP]:
            self.y -= self.speed
        elif keys[pg.K_DOWN]:
            self.y += self.speed

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.target_tilt = -15
            
            if self.allow_movement:
                self.x -= self.brakespeed
            self.accelearation -= self.brakespeed
            
            self.last_accs = -1

            self.last_accs = self.accelearation
            self.afterburner_timer -= 5
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.target_tilt = 15
            if self.allow_movement:
                self.x += self.speed
            self.accelearation += self.speed

            self.afterburner_timer += 0.5
            
            self.last_accs = self.accelearation
        else:
            if self.accelearation == self.last_accs:
                self.accelearation = self.accelearation * -1
            
            
            self.target_tilt = 0
            self.afterburner_timer -= 5

        # if self.afterburner_timer <= 0:
        #     self.new_image(show_image, 0)
        #     self.speed = self.idlespeed
        # elif self.afterburner_timer > 0 and self.afterburner_timer < 15:
        #     self.new_image(show_image, 1)
        #     if not self.speed >= self.speed_cap:
        #         self.speed += 2
        # elif self.afterburner_timer >= 10 and self.afterburner_timer < 30:
        #     self.new_image(show_image, 2)
        #     if not self.speed >= self.speed_cap:
        #         self.speed += 2
        # elif self.afterburner_timer >= 20:
        #     self.new_image(show_image, 3)
        #     if not self.speed >= self.speed_cap:
        #         self.speed += 2

        self.new_image("side", "revolve", self.tilt)

        # clamp angle to reasonable range

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)
