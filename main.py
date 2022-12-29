import os
import sys

import pygame
from settings import *
from board import *


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


def start_screen(image_fon, text):
    global FPS
    intro_text = ["Правила игры", "",
                  "",
                  "",
                  ""]
    fon = pygame.transform.scale(load_image(image_fon), (WIDTH, HEIGHT))
    speed = 60

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and (event.key == 13 or event.key == pygame.K_KP_ENTER):
                return speed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if speed != 1 and text == "settings_text":
                        speed -= 5

                if event.key == pygame.K_UP:
                    if text == "settings_text":
                        speed += 5

        screen.blit(fon, (0, 0))

        font = pygame.font.Font(None, 30)
        if text == "controlers_text":
            text_coord = 20
            text_lines = ["Кнопки в игре:", "",
                          "/\ Использовать бонус",
                          "|| (Нарисован в верхнем ",
                          "|| левом углу)",
                          "",
                          "",
                          "|| Увеличить скорость ",
                          "|| фигрурки до предела",
                          "\/",
                          "",
                          "-> подвинуть фигурку",
                          "   на 1 клуточку вправо",
                          "",
                          "<- подвинуть фигурку",
                          "   на 1 клуточку влево",
                          "",
                          "K - повернуть фигурку",
                          "   по чесовой",
                          "",
                          "L - повернуть фигурку",
                          "  против часовой",
                          "",
                          "Enter чтобы начать"]
        if text == "settings_text":
            text_coord = 50
            text_lines = ["Кнопки в главном меню:", "",
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
                          f"скорость сейчас: {speed}"]

        for line in text_lines:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    speed = start_screen("fon.jpg", "settings_text")
    start_screen("fon_2.jpg", "controlers_text")
    screen.fill((0, 0, 0))
    board = Board(23, 10)

    running = True
    n = 0
    k = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                fig = board.figuri[-1]
                fig.move(event)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()

        n += 1
        if n % speed == 0:
            n = 0
            k += 1
            fig = board.figuri[-1]
            fig.down()

        board.render(screen)
        if k % 8 == 0:
            k = 1
            board.next_move()

        clock.tick(FPS)
        pygame.display.flip()
pygame.quit()