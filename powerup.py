import pygame
import random
from constants import *
from circleshape import *

class PowerUp(CircleShape):
    def __init__(self, position, direction, velocity):
        super().__init__(position.x, position.y, ASTEROID_MIN_RADIUS)
        self.type = random.choice(["Shield", "Fire Rate", "Big Shot"])
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
        if self.wrap_count == 5:
            self.kill()

    def draw_fire_rate(self, screen):
        half = ASTEROID_MIN_RADIUS // 2
        bullet_width = half * 0.9
        bullet_height = half * 0.3
        
        for i in range(3):
            y_offset = (i - 1) * (bullet_height + 2) 
            points = [
                (self.position.x + bullet_width, self.position.y + y_offset),
                (self.position.x + bullet_width//2, self.position.y + y_offset - bullet_height//2),
                (self.position.x - bullet_width, self.position.y + y_offset - bullet_height//2),
                (self.position.x - bullet_width, self.position.y + y_offset + bullet_height//2),
                (self.position.x + bullet_width//2, self.position.y + y_offset + bullet_height//2),
            ]
            pygame.draw.polygon(screen, COLOR_SHOT, points)

    def draw_big_shot(self,screen):
        half = ASTEROID_MIN_RADIUS // 2
        points = [
            (self.position.x, self.position.y - half),
            (self.position.x + half//3, self.position.y - half//3),
            (self.position.x + half//3, self.position.y + half),
            (self.position.x - half//3, self.position.y + half),
            (self.position.x - half//3, self.position.y - half//3),
        ]
        pygame.draw.polygon(screen, COLOR_SHOT, points)

    def draw_shield(self, screen):
        half = ASTEROID_MIN_RADIUS // 2
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
        match self.type:
            case "Shield":
                self.draw_shield(screen)
            case "Fire Rate":
                self.draw_fire_rate(screen)
            case "Big Shot":
                self.draw_big_shot(screen)