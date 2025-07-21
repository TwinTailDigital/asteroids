import pygame
from constants import *
from player import *

def main():
    pygame.init()
    group_updateable = pygame.sprite.Group()
    group_drawable = pygame.sprite.Group()
    Player.containers = (group_updateable,group_drawable)
    game_clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
    print("Starting Asteroids!")
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        group_updateable.update(dt)
        for item in group_drawable:
            item.draw(screen)
        pygame.display.flip()
        dt = game_clock.tick(60) / 1000


if __name__ == "__main__":
    main()
