import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.spawn_count = 0
        self.spawn_count_max = ASTEROID_SPAWN_COUNT_MULTIPLIER

    def spawn(self, radius, position, velocity, kind):
        num_points = 0
        jaggeyness = random.uniform(0.05,0.20)
        spin_speed = random.uniform(-30,30)
        match(kind):
            case 3: 
                num_points = int(random.uniform(24,28))
            case 2: 
                num_points = int(random.uniform(16,20))
            case 1: 
                num_points = int(random.uniform(10,14))
        asteroid = Asteroid(position.x, position.y, radius,num_points,jaggeyness,spin_speed)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_count < self.spawn_count_max:
            if self.spawn_timer > ASTEROID_SPAWN_RATE:
                self.spawn_timer = 0
                self.spawn_count += 1

                # spawn a new asteroid at a random edge
                edge = random.choice(self.edges)
                speed = random.randint(40, 100)
                velocity = edge[0] * speed
                velocity = velocity.rotate(random.randint(-30, 30))
                position = edge[1](random.uniform(0, 1))
                kind = random.randint(1, ASTEROID_KINDS)
                self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity,kind)