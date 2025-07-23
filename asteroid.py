import pygame
import random
import math
from circleshape import *
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, num_points, jaggeyness,spin_speed):
        super().__init__(x, y, radius)
        self.spin_speed = spin_speed
        self._shape_offsets = []
        for p in range(num_points):
            angle = p * (2 * math.pi / num_points)
            min_radius = self.radius * (1 - jaggeyness)
            max_radius = self.radius * (1 + jaggeyness)
            r = random.uniform(min_radius, max_radius)
            x_offset = r * math.cos(angle)
            y_offset = r * math.sin(angle)
            self._shape_offsets.append((x_offset, y_offset))
    
    def draw(self, screen):
        rad_rotation = math.radians(self.rotation)
        points = []
        for (x_offset, y_offset) in self._shape_offsets:
            x_rotation = x_offset * math.cos(rad_rotation) - y_offset * math.sin(rad_rotation)
            y_rotation = x_offset * math.sin(rad_rotation) + y_offset * math.cos(rad_rotation)
            points.append((self.position.x + x_rotation, self.position.y + y_rotation))
        pygame.draw.polygon(screen, "white", points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation = (self.rotation + self.spin_speed * dt) % 360
        if self.position.x > (SCREEN_WIDTH + self.radius):
            self.position.x = 0 - self.radius
        elif self.position.x < (0 - self.radius):
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.y > (SCREEN_HEIGHT + self.radius):
            self.position.y = 0 - self.radius
        elif self.position.y < (0 - self.radius):
            self.position.y = SCREEN_HEIGHT + self.radius
    
    def split(self):
        self.kill()
        kind = int(self.radius // ASTEROID_MIN_RADIUS)
        if kind == 1:
            return math.floor(self.velocity.length())
        else:
            num_points = 0
            match(kind):
                case 3: 
                    num_points = int(random.uniform(20,24))
                case 2: 
                    num_points = int(random.uniform(14,18))
            impulse = random.uniform(1.1,1.5)
            random_angle = random.uniform(15.0,50.0)
            new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid_a = Asteroid(self.position.x,self.position.y,new_asteroid_radius,num_points,random.uniform(0.05,0.20),self.spin_speed * (impulse * 2))
            asteroid_a.velocity = (self.velocity.rotate(random_angle)) * impulse
            asteroid_b = Asteroid(self.position.x,self.position.y,new_asteroid_radius,num_points,random.uniform(0.05,0.20),self.spin_speed * (impulse * 2))
            asteroid_b.velocity = (self.velocity.rotate(-random_angle)) * impulse
            return math.floor(self.velocity.length() / kind)