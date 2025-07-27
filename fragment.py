import pygame
from constants import COLOR_ASTEROID

class Fragment(pygame.sprite.Sprite):
    def __init__(self, position, direction, length, lifetime):
        super().__init__(self.containers)
        self.position = position
        self.direction = direction
        self.length = length
        self.current_length = 0.0
        self.lifetime = lifetime
        self.timer = 0.0
        self.age = 0.0
    
    def update(self, dt):
        self.timer += dt
        self.age = self.timer / self.lifetime
        if self.age >= 1.0:
            self.kill()
            return
        if self.age <= 0.5:
            line_growth = self.age * 2
            self.current_length = self.length * line_growth
        else:
            self.current_length = self.length
        self.current_length = self.length * self.age
        if self.current_length > self.length:
            self.current_length = self.length

    def draw(self, screen):
        if self.age <= 0.5:
            end_point = self.position + self.direction * self.current_length
            start_point = self.position
        else:
            shrinkage = 2 * (1 - self.age)
            end_point = self.position + self.direction * self.length
            start_point = self.position + self.direction * self.length * (1 - shrinkage)
        pygame.draw.line(screen, COLOR_ASTEROID, start_point, end_point, 1)