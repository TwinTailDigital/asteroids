import pygame
import math
from constants import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from fragment import *
from powerup import *

def main():
    pygame.init()
    pygame.font.init()
    group_updateable = pygame.sprite.Group()
    group_drawable = pygame.sprite.Group()
    group_asteroids = pygame.sprite.Group()
    group_shots = pygame.sprite.Group()
    group_powerups = pygame.sprite.Group()
    Asteroid.containers = (group_asteroids,group_updateable,group_drawable)
    AsteroidField.containers = (group_updateable)
    Player.containers = (group_updateable,group_drawable)
    Shot.containers = (group_shots,group_updateable,group_drawable)
    Fragment.containers = (group_updateable,group_drawable)
    PowerUp.containers = (group_powerups,group_updateable,group_drawable)
    asteroid_field = AsteroidField()
    game_clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
    print("Starting Asteroids!")
    run = True
    while run:
        asteroid_field.spawn_count_max = ASTEROID_SPAWN_COUNT_MULTIPLIER * (round(player.timer / 30) + 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        group_updateable.update(dt)
        for asteroid in group_asteroids:
            if asteroid.collision_check(player):
                if player.shield_timer <= 0:
                    player.die()
            for bullet in group_shots:
                if asteroid.collision_check(bullet):
                    bullet.kill()
                    points, kind = asteroid.split() # Returns points based on the kind of asteroid destroyed and how fast it was going
                    distance = math.floor(player.position.distance_to(asteroid.position))
                    player.add_score(points + max(0, MAX_BONUS - distance))
                    if kind > 1:
                        asteroid_field.spawn_count += 1
                    else:
                        asteroid_field.spawn_count -= 1
        for powerup in group_powerups:
            if powerup.collision_check(player):
                match powerup.type:
                    case "Shield":
                        player.shield_timer += 3
                powerup.kill()
        for item in group_drawable:
            item.draw(screen)
        pygame.display.flip()
        dt = game_clock.tick(60) / 1000


if __name__ == "__main__":
    main()
