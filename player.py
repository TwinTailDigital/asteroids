import pygame
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.shot_timer = 0.0
        self.muzzle_flash_timer = 0.0
        self.muzzle_flash_direction = []
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent
        self.rect = self.image.get_rect(center=(x, y))

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen,"white",self.triangle(),2)
        if self.muzzle_flash_timer > 0.0:
            for flash_angle in self.muzzle_flash_direction:
                direction = pygame.Vector2(0,1).rotate(flash_angle)
                flash_end = self.triangle()[0] + direction * 16
                pygame.draw.line(screen,"white",self.triangle()[0],flash_end,1)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            if not self.shot_timer > 0.0:
                self.shoot()
                self.shot_timer = SHOT_RATE
        
        self.rect.center = self.position
        self.muzzle_flash_direction = [self.rotation - 45,self.rotation - 30,self.rotation + 30, self.rotation + 45]
        self.shot_timer -= dt
        self.muzzle_flash_timer -= dt
    
    def move(self, dt):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        spawn_point = self.triangle()[0]
        shot = Shot(spawn_point.x,spawn_point.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * SHOT_SPEED
        self.muzzle_flash_timer = 0.1