import pygame
import sys
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
                direction = pygame.Vector2(0,1).rotate(flash_angle)
                flash_end = self.triangle()[0] + direction * 16
                pygame.draw.line(screen,"white",self.triangle()[0],flash_end,1)
        if self.shield_timer > 0:
            pygame.draw.circle(screen,"purple",self.position,self.radius+4,3)
            pygame.draw.polygon(screen,"darkgray",self.triangle(),2)
        else:
            pygame.draw.polygon(screen,"white",self.triangle(),2)
        score_text = self.font.render(f"{self.score}", True, "darkgray")
        score_area = score_text.get_rect(midtop=(screen.get_size()[0] // 2,10))
        lives_text = self.font.render(f"Lives: {self.lives}", True, "darkgray")
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
            self.shield_timer = 2
            self.lives -= 1
        else:
            print(f"===== Game over! =====")
            print(f"You survived for {self.timer:.3f} seconds.")
            print(f"Your score is: {self.score}")
            sys.exit()