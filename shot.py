import pygame
import math
import random
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self,x,y,radius):
        super().__init__(x,y,radius)
        self.current_radius = 0.0

    
    def draw(self, screen):
        pygame.draw.circle(screen,COLOR_SHOT,self.position,self.current_radius,2)

    def update(self, dt):
        self.position += self.velocity * dt
        if self.current_radius <= self.radius:
            self.current_radius += (self.radius * 10) * dt