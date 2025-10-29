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

    def handle_keys(self, dt=None):
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

    def __init__(self, Game, x, y):
        self.original_dimentions = 1414, 420

        # self.rect = self.image.get_rect(center=(x, y))
        self.accelearation_backward = 420.0
        self.accelearation_foreward = 420.0
        self.speed_cap = 450.0
        # self.speed = self.idlespeed
        self.x = x
        self.y = y
        self.afterburner_timer = 0
        self.target_tilt = 0
        self.tilt = 0
        self.tilt_speed = 1
        self.reached_right_tilt = False
        self.just_reached_idle = True
        
        self.direction = "idle"
        self.hover_tilt = 3
        self.hover_tilt_speed = 0.1
        self.hover_speed_eps = 5.0  # consider "stopped" when below this speed
        self.is_hovering = False
        self.bakgrunnsfart = 0

        # Simple time-based physics parameters for braking/drag
        self.brake_acceleration = 630.0
        self.drag_coefficient = 2.0
        self.vertical_speed_per_s = 420.0

        
        self.reach_stop = True
        self.accelearation = 0
        self.last_accs = self.accelearation
        
        self.allow_movement = True
        
        self.new_image("side", 1, self.tilt)

    def new_image(self, variation, blades, tilt):
        
        # self.target_tilt = 15
        if self.direction == "right":
            print(f"\nTarget tilt: " + str(self.target_tilt))
            print(f"True tilt: " + str(round(self.tilt, 2)))
        # Approach target tilt smoothly and snap when within one step
        delta = self.target_tilt - self.tilt
        step = self.tilt_speed
        if abs(delta) <= step:
            self.tilt = self.target_tilt
        else:
            self.tilt += step if delta > 0 else -step

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

    def handle_keys(self, dt):
        keys = pg.key.get_pressed()

        vertical_step = self.vertical_speed_per_s * dt
        if keys[pg.K_UP]:
            self.y -= vertical_step
        elif keys[pg.K_DOWN]:
            self.y += vertical_step

        move_left = keys[pg.K_LEFT] or keys[pg.K_a]
        move_right = keys[pg.K_RIGHT] or keys[pg.K_d]

        horizontal_accel = 0.0

        if move_left and not move_right:
            self.direction = "left"
            self.tilt_speed = 1
            self.is_hovering = False
            self.target_tilt = -15
            if self.bakgrunnsfart > 0:
                horizontal_accel = -self.brake_acceleration
            else:
                horizontal_accel = -self.accelearation_backward
            self.afterburner_timer -= 5
        elif move_right and not move_left:
            self.direction = "right"
            self.tilt_speed = 1
            self.is_hovering = False
            self.target_tilt = 15
            horizontal_accel = self.accelearation_foreward
            self.afterburner_timer += 0.5
        else:
            self.direction = "idle"
            self.afterburner_timer -= 5

        self.bakgrunnsfart += horizontal_accel * dt

        # Apply simple linear drag towards zero for more physical braking
        if self.bakgrunnsfart != 0:
            drag = self.bakgrunnsfart * self.drag_coefficient
            self.bakgrunnsfart -= drag * dt

        # Clamp to configured speed limits
        self.bakgrunnsfart = max(-self.speed_cap, min(self.speed_cap, self.bakgrunnsfart))

        if self.direction == "idle":
            if abs(self.bakgrunnsfart) > self.hover_speed_eps:
                self.tilt_speed = 0.7
                self.target_tilt = 0
                self.is_hovering = False
            else:
                self.bakgrunnsfart = 0
                self.tilt_speed = self.hover_tilt_speed
                if not self.is_hovering:
                    self.is_hovering = True
                    self.target_tilt = -self.hover_tilt
                elif abs(round(self.tilt, 3)) >= abs(self.target_tilt):
                    self.target_tilt *= -1
        else:
            self.is_hovering = False

        self.new_image("side", "revolve", self.tilt)

        # clamp angle to reasonable range

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)
