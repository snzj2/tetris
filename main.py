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

def bafs(x, z, c):
    font_size = 42
    font = pygame.font.Font(None, font_size)
    font_color = (0, 0, 0)

    K_z = pygame.image.load('data/K_z.png')
    K_z_rect = K_z.get_rect(center=(50, 100))
    screen.blit(K_z, K_z_rect)

    K_x = pygame.image.load('data/K_x.png')
    K_x_rect = K_x.get_rect(center=(50, 200))
    screen.blit(K_x, K_x_rect)

    K_c = pygame.image.load('data/K_c.png')
    K_c_rect = K_c.get_rect(center=(50, 300))
    screen.blit(K_c, K_c_rect)

    fire = pygame.image.load('data/small_bomb.png')
    fire_rect = fire.get_rect(center=(50, 75))
    screen.blit(fire, fire_rect)

    bomb1 = pygame.image.load('data/flame.png')
    bomb1_rect = fire.get_rect(center=(50, 175))
    screen.blit(bomb1, bomb1_rect)

    bomb2 = pygame.image.load('data/big_bomb.png')
    bomb2_rect = fire.get_rect(center=(50, 275))
    screen.blit(bomb2, bomb2_rect)

    fire_text = font.render(str(z), 1, font_color)
    screen.blit(fire_text, (25, 105))

    fire_bomb_1 = font.render(str(x), 1, font_color)
    screen.blit(fire_bomb_1, (25, 205))

    fire_bomb_2 = font.render(str(c), 1, font_color)
    screen.blit(fire_bomb_2, (25, 305))


def fonts(point, rec):
    font_size = 40
    font = pygame.font.Font(None, font_size)
    font_color = (255, 255, 255)
    text = font.render("Счёт", 1, font_color)
    screen.blit(text, (500, 300))
    text1 = font.render(str(point), 1, font_color)
    screen.blit(text1, (510, 350))

    record = font.render("Рекорд", 1, font_color)
    screen.blit(record, (490, 420))
    record1 = font.render(str(rec), 1, font_color)
    screen.blit(record1, (510, 470))


def start():
    font_size = 60
    font = pygame.font.Font(None, font_size)
    font_color = (255, 255, 255)
    text = font.render("Для начала игры", 1, font_color)
    screen.blit(text, (125, 200))

    record = font.render("Нажмите  Enter", 1, font_color)
    screen.blit(record, (150, 250))


def end():
    font_size = 60
    font = pygame.font.Font(None, font_size)
    font_color = "#ffff00"
    text = font.render("Начать заново игру", 1, font_color)
    screen.blit(text, (125, 200))

    record = font.render("Нажмите  Enter", 1, font_color)
    screen.blit(record, (150, 250))

def start_screen(image_fon, text):
    global FPS
    intro_text = ["Правила игры", "",
                  "",
                  "",
                  ""]
    fon = pygame.transform.scale(load_image(image_fon), (WIDTH, HEIGHT))
    main_speed = 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and (event.key == 13 or event.key == pygame.K_KP_ENTER):
                return main_speed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_speed != 0 and text == "settings_text":
                        main_speed -= 5
                if event.key == pygame.K_DOWN:
                    if text == "settings_text" and main_speed != 50:
                        main_speed += 5

        screen.blit(fon, (0, 0))

        font = pygame.font.Font(None, 30)
        if text == "controlers_text":
            text_coord = 20
            text_lines = ["Кнопки в игре:", "",
                          "Z - использовать маленькую бомбу",
                          "X - использовать огонь",
                          "C - использовать большую бомбу",
                          "",
                          "Подробнее о бонусах в пояснительной записке",
                          "",
                          "|| Увеличить скорость ",
                          "|| фигруры в 4 раза",
                          "\/",
                          "",
                          "-> подвинуть фигуру",
                          "   на 1 клеточку вправо",
                          "",
                          "<- подвинуть фигуку",
                          "   на 1 клеточку влево",
                          "",
                          "K - повернуть фигуру",
                          "   по часовой",
                          "",
                          "L - повернуть фигуру",
                          "  против часовой",
                          "",
                          "Enter чтобы начать"]
        if text == "settings_text":
            text_coord = 50
            text_lines = ["Кнопки в главном меню:", "",
                          "/\ увеличить начальную скорость",
                          "|| падения фигур",
                          "||",
                          "",
                          "",
                          "|| уменьшить начальную скорость",
                          "|| падения фигур",
                          "\/",
                          "",
                          "Enter чтобы продолжить",
                          "",
                          f"скорость сейчас: {(50 - main_speed) * 2}"]

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

    main_speed = start_screen("fon.jpg", "settings_text")
    start_screen("fon_2.jpg", "controlers_text")
    screen.fill((0, 0, 0))
    board = Board(23, 10)
    fon = pygame.transform.scale(load_image("fon_3.png"), (WIDTH, HEIGHT))
    running = True
    n = 0
    k = 0
    board.next_move()
    speed = 1
    text_coord = 50
    font = pygame.font.Font(None, 30)
    text_lines = ["Счёт", "", ]
    flag = 0
    x_mouse, y_mouse = 0, 0
    bomb_gr = pygame.sprite.Group()
    fireflag = 0
    new_bomb = None
    big_flag = 0
    keyy = None
    play_flag = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == 13:
                if play_flag == 2:
                    for i in all_sprites:
                        i.kill()
                    board = Board(23, 10)
                    board.next_move()
                    speed = 1
                    play_flag = 1
                    down_border = Border(100, HEIGHT, WIDTH - 100, HEIGHT)
                    left_border = Border(100, 0, 100, HEIGHT)
                    right_border = Border(WIDTH - 235, 0, WIDTH - 235, HEIGHT)

                play_flag = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z and not fireflag and not big_flag and not flag:
                if board.small_bomb > 0 and flag == 0 and fireflag == 0 and big_flag == 0:
                    board.small_bomb -= 1
                    flag = 1
                    new_bomb = Bomb(5, 0, "small")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c and not fireflag and not flag and not big_flag:
                if board.big_bomb > 0 and flag == 0 and fireflag == 0 and big_flag == 0:
                    board.big_bomb -= 1
                    big_flag = 1
                    new_bomb = Bomb(5, 0, "big")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x and not flag and not big_flag and not fireflag:
                if board.fire > 0 and fireflag == 0:
                    board.fire -= 1
                    fireflag = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                start_screen("fon_2.jpg", "controlers_text")
            elif event.type == pygame.KEYDOWN:
                if play_flag != 0:
                    keyy = event
                    if board.figuri != [] and flag < 2 and big_flag < 2:
                        fig = board.figuri[-1]
                        fig.move(event)
            if event.type == pygame.MOUSEMOTION:
                pos = board.get_cell(event.pos)
                if pos is not None:
                    y_mouse, x_mouse = pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag:
                    flag = 3
        screen.blit(fon, (0, 0))
        screen.blit(board.scale, board.rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            speed = main_speed // 4
        else:
            speed = 1
        text_coord = 50
        # Выводим очки
        play_flag = board.game_end(play_flag)
        fonts(board.points, board.record)
        bafs(board.fire, board.small_bomb, board.big_bomb)
        if board.figuri:
            fig = board.figuri[-1]
            if flag < 2 and big_flag < 2 and fig.update() is not None and play_flag != 2:
                if fireflag == 0 and flag == 0 and big_flag == 0:
                    board.next_move()
                    speed = 1
                elif fireflag == 1:
                    board.fires()
                    fireflag = 2
                elif flag == 1:
                    flag = 2
                elif big_flag == 1:
                    big_flag = 2
            if flag > 1:
                flag, new_bomb, n = board.boom(new_bomb, flag, x_mouse, y_mouse, n, main_speed, keyy)
            elif big_flag > 1:
                big_flag, new_bomb, n = board.boom(new_bomb, big_flag, 7, 0, n, main_speed, keyy)
        n += speed
        all_sprites.draw(screen)
        if big_flag < 2 and flag < 2 and main_speed - n <= 0:
            n = 0
            k += 1
            if fireflag == 2:
                fireflag = board.move_fire()
                fire.update()
            else:
                if play_flag != 0:
                    fig.down()

        board.render(screen)
        # if k % 8 == 0:
        #     k = 1
        #     board.next_move()
        keyy = None

        if play_flag == 0:
            start()
        if play_flag == 2:
            end()

        clock.tick(FPS)
        pygame.display.flip()
pygame.quit()

