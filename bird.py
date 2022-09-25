import pygame


class Bird():
    def __init__(self, filepath: str):
        self.x = 200
        self.y = 400
        self.yspeed = 0
        self.surface = pygame.image.load(filepath)

    def update(self, pressed, dt):
        if pressed:
            self.yspeed -= 7
        if self.y < 0: #avoid going higher
            self.yspeed = 5
        self.yspeed += 10 * dt  # deceleration of 2m/s^2
        self.y += self.yspeed
