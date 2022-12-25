import pygame
from settings import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()

pygame.quit()
