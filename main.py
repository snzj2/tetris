import os
import sys

import pygame
from settings import *



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Правила игры", "",
                  "",
                  "",
                  ""]

    settings_text = ["Кнопки в главном меню:", "",
                     "/\ увеличить начальную скорость",
                     "|| падения кубиков",
                     "||",
                     "",
                     "",
                     "|| уменьшить начальную скорость",
                     "|| падения кубиков",
                     "\/",
                     "",
                     "Enter чтобы продолжить",
                     "",
                     f"скорость сейчас: {FPS}"]

    controlers_text = ["Кнопки в игре:", "",
                       "/\ Использовать бонус",
                       "|| (Нарисован в верхнем левом углу",
                       "||",
                       "",
                       "",
                       "|| Увеличить скорость фигрурки до предела",
                       "|| ",
                       "\/",
                       "",
                       "-> подвинуть фигурку на 1 клуточку вправо",
                       "",
                       "<- подвинуть фигурку на 1 клуточку влево"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in settings_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and (event.key == 13 or event.key == pygame.K_KP_ENTER):
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 5
    start_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()

pygame.quit()
