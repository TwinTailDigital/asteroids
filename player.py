import pygame
import sys
import random
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.timer = 0.0
        self.shot_timer = 0.0
        self.shield_timer = 0.0
        self.score = 0
        self.lives = 3
        self.muzzle_flash_timer = 0.0
        self.muzzle_flash_direction = []
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent
        self.rect = self.image.get_rect(center=(x, y))
        self.font_score = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 32)


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.muzzle_flash_timer > 0.0:
            for flash_angle in self.muzzle_flash_direction:
                direction = pygame.Vector2(0,1).rotate(flash_angle + random.uniform(-10,10))
                flash_end = self.triangle()[0] + direction * random.uniform(8,16)
                pygame.draw.line(screen,COLOR_SHOT,self.triangle()[0],flash_end,1)
        if self.shield_timer > 0:
            pygame.draw.circle(screen,COLOR_SHIELD,self.position,self.radius * 1.5,3)
            pygame.draw.polygon(screen,COLOR_PLAYER,self.triangle(),2)
        else:
            pygame.draw.polygon(screen,COLOR_PLAYER,self.triangle(),2)
        score_text = self.font_score.render(f"{self.score}", True, COLOR_UI)
        score_area = score_text.get_rect(midtop=(screen.get_size()[0] // 2,10))
        if self.lives > 1:
            lives_text = self.font.render(f"{self.lives} SHIPS LEFT // TIME: {int(self.timer)}s", True, COLOR_UI)
        elif self.lives == 1:
            lives_text = self.font.render(f"{self.lives} SHIP LEFT // TIME: {int(self.timer)}s", True, COLOR_UI)
        else:
            lives_text = self.font.render(f"LAST SHIP // TIME: {int(self.timer)}s", True, COLOR_UI)
        lives_area = lives_text.get_rect(midbottom=(screen.get_size()[0] // 2, screen.get_size()[1] - 10))
        screen.blit(score_text,(score_area))
        screen.blit(lives_text,(lives_area))

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        forward = pygame.Vector2(0,1).rotate(self.rotation)

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.velocity += forward * PLAYER_ACCELERATION * dt
        if keys[pygame.K_s]:
            self.velocity -= forward * PLAYER_ACCELERATION * dt
        if keys[pygame.K_SPACE]:
            if not self.shot_timer > 0.0:
                self.shoot()
                self.shot_timer = SHOT_RATE
        
        self.position += self.velocity * dt
        self.velocity *= (1 - PLAYER_DRAG * dt)

        if self.position.x > (SCREEN_WIDTH):
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

        if self.shield_timer > 0:
            self.shield_timer -= dt
        elif self.shield_timer <= 0:
            self.shield_timer = 0.0
        self.rect.center = self.position
        self.muzzle_flash_direction = [self.rotation - 45,self.rotation - 30,self.rotation + 30, self.rotation + 45]
        self.shot_timer -= dt
        self.muzzle_flash_timer -= dt
        self.timer += dt
    
    def shoot(self):
        spawn_point = self.triangle()[0]
        shot = Shot(spawn_point.x,spawn_point.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * SHOT_SPEED
        self.muzzle_flash_timer = 0.1

    def add_score(self, points):
        self.score += points

    def die(self):
        if self.lives >= 1:
            self.shield_timer = 3
            self.lives -= 1
        else:
            print(f"===== Game over! =====")
            print(f"You survived for {self.timer:.3f} seconds.")
            print(f"Your score is: {self.score}")
            sys.exit()