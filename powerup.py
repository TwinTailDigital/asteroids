import pygame
import random
from constants import *
from circleshape import *

class PowerUp(CircleShape):
    def __init__(self, position, direction, velocity):
        super().__init__(position.x, position.y, ASTEROID_MIN_RADIUS)
        self.type = random.choice(["Shield"])
        self.position = position
        self.direction = direction
        self.velocity = velocity
        self.wrap_count = 0

    def update(self, dt):
        self.position += self.velocity * dt
        if self.position.x > (SCREEN_WIDTH + self.radius):
            self.wrap_count += 1
            self.position.x = 0 - self.radius
        elif self.position.x < (0 - self.radius):
            self.wrap_count += 1
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.y > (SCREEN_HEIGHT + self.radius):
            self.wrap_count += 1
            self.position.y = 0 - self.radius
        elif self.position.y < (0 - self.radius):
            self.wrap_count += 1
            self.position.y = SCREEN_HEIGHT + self.radius
        if self.wrap_count == 3:
            self.kill()

    def draw_shield(self, screen):
        half = 20 // 2
        points = [
            (self.position.x, self.position.y - half),           # Top
            (self.position.x + half, self.position.y - half//3), # Top right
            (self.position.x + half, self.position.y + half//3), # Bottom right
            (self.position.x, self.position.y + half),           # Bottom point
            (self.position.x - half, self.position.y + half//3), # Bottom left
            (self.position.x - half, self.position.y - half//3), # Top left
        ]
        pygame.draw.polygon(screen, COLOR_SHIELD, points)

    def draw(self, screen):
        self.draw_shield(screen)