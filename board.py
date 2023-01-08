import os
import sys

import pygame

from random import choice, randint
from settings import *


def delete_no(r, x1, y1, x2, y2):
    if (r >= ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5):
        return True
    return False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board_2 = [[0] * width for _ in range(height)]
        self.left = 100
        self.top = 0
        # переменная для бафов
        self.fire = 1
        self.small_bomb = 5
        self.big_bomb = 10

        self.cell_size = 35
        self.t = Table(1, self.left, self.top)
        self.next_figura = choice(figure)
        self.next_picture()
        self.points = 0
        self.figuri = []

    def render(self, screen):
        for i, h in enumerate(self.board):
            for k, w in enumerate(h):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + i * self.cell_size, self.top + k * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def next_picture(self):
        self.image = load_image(f"{self.next_figura}.png")
        self.scale = pygame.transform.scale(
            self.image, (self.image.get_width() // 1.75,
                         self.image.get_height() // 1.75))
        self.rect = self.image.get_rect(center=(635 - (self.scale.get_height() // 2),
                                                155 - (self.scale.get_width() // 2)))

    def block(self):
        # что-бы не нагружать
        for i, h in enumerate(self.board):
            for k, w in enumerate(h):
                if w == 1:
                    Block(i + 3, k, "red")
                elif w == 2:
                    Block(i + 3, k, "green")
                elif w == 3:
                    Block(i + 3, k, "blue")

    def vzriv(self, r, x1, y1):
        sp = []
        for i in range(len(self.board)):
            ss = []
            for j in range(len(self.board[i])):
                if delete_no(r, x1, y1, j, i):
                    ss.append(True)
                else:
                    ss.append(False)
            sp.append(ss)
        return sp

    def on_click(self, cell):
        if cell != None:
            self.board[cell[0]][cell[1]] += 1
            if self.board[cell[0]][cell[1]] >= 2:
                self.board[cell[0]][cell[1]] = 0

    def get_cell(self, mouse_pos):
        for i, h in enumerate(self.board):
            for k, w in enumerate(h):
                n1 = self.left + i * self.cell_size
                n2 = self.left + (i + 1) * self.cell_size
                n3 = self.top + k * self.cell_size
                n4 = self.top + (k + 1) * self.cell_size
                if n1 < mouse_pos[0] and n2 > mouse_pos[0] and n3 < mouse_pos[1] and n4 > mouse_pos[1]:
                    return (i, k)

        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def fires(self):
        self.havefire = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.tables()
        self.figuri = []
        for i in range(23):
            for k in range(10):
                if self.board[k][i] != 0:
                    self.havefire[k] += 1
        for i in range(len(self.havefire)):
            n = 0
            for k in range(self.havefire[i]):
                r = randint(1, 100)
                if r <= chance[k]:
                    n += 1
            self.havefire[i] = n
        for k in range(10):
            Fire(k + 3, 0, self.havefire[k])

    def move_fire(self):
        global figure_group
        a = []
        for i in fire:
            k = i.prikosnoveniie()
            if k is not None and i.life >= 0:
                del self.board[k[0] - 3][k[1] + 1]
                self.board[k[0] - 3].insert(0, 0)
            i.down()
            a.append(i.life)

        for i in figure_group:
            i.kill()
        if max(a) == 0:
            self.figuri = []
            self.figuri.append(Figures(7, 0, self.next_figura))
            self.next_figura = choice(figure)
            self.next_picture()
            self.block()
            return 0
        figure_group = pygame.sprite.Group()
        # делаем по блоку из списка
        self.block()
        return 2

    def boom(self, bomb, flag, x_m, y_m, n, main_speed, event):
        global figure_group
        if flag == 1:
            return 0, None, n
        if bomb is None:
            self.tables()
            for i in figure_group:
                i.kill()
            self.figuri = []
            self.figuri.append(Figures(7, 0, self.next_figura))
            figure_group = pygame.sprite.Group()
            # делаем по блоку из списка
            self.block()
            return 0, None, n
        if flag == 2 and bomb.fl == 0:
            fl = bomb.update(x_m, y_m, n, main_speed, event)
            if fl is not None:
                return 2, bomb, 0
            return 2, bomb, n
        if flag == 3 or bomb.fl == 3:
            self.tables()
            self.figuri = []
            tab = self.vzriv(bomb.r, (bomb.rect.y // tile_height - 1) + 1, (bomb.rect.x // tile_width - 1) - 1)
            for i in range(len(tab)):
                for j in range(len(tab[i])):
                    if tab[i][j]:
                        self.board[i][j] = 0
            bomb.image = load_image("empty.png")
            for i in figure_group:
                i.kill()
            self.figuri = []
            self.figuri.append(Figures(7, -2, self.next_figura))
            figure_group = pygame.sprite.Group()
            # делаем по блоку из списка
            self.block()
        return 0, None, n

    def examination(self):
        # какую линию нужно удалить
        delete = []
        for i in range(23):
            j = []
            tr = True
            for k in range(10):
                j.append(self.board[k][i])
                if self.board[k][i] == 0:
                    tr = False
            if tr and len(set(j)) <= 2:
                delete.append(i)
        if len(delete) == 1:
            self.points += 100

        if len(delete) == 2:
            self.points += 300
            self.small_bomb += 1
        if len(delete) == 3:
            self.points += 700
            self.fire += 1
        if len(delete) == 4:
            self.points += 1500
            self.big_bomb += 1
        for i in delete:
            for k in range(10):
                del self.board[k][i]
                self.board[k].insert(0, 0)

    def tables(self):
        global figure_group
        # заполняем двухмерный массив где находятся блоки
        self.board = self.t.markup(self.board_2)
        self.examination()
        # удаляем группу
        for i in figure_group:
            i.kill()
        figure_group = pygame.sprite.Group()
        # делаем по блоку из списка
        self.block()

    def next_move(self):
        self.tables()
        self.figuri = []
        self.figuri.append(Figures(7, 0, self.next_figura))
        self.next_figura = choice(figure)
        self.next_picture()


all_sprites = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
figure_group = pygame.sprite.Group()
fire = pygame.sprite.Group()

tile_width = tile_height = 35


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, life):
        super().__init__(fire, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.life = life
        self.proverka = 0
        if self.life != 0:
            self.image = load_image("flame.png")
        else:
            self.image = load_image("empty.png")
        self.rect = self.image.get_rect().move(
            self.pos_x * tile_width - 5, tile_height * self.pos_y)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x - 5, tile_height * self.pos_y)

    def down(self):
        self.pos_y += 1

    def examination(self):
        fl = 0
        for i in figure_group:
            if pygame.sprite.collide_mask(self, i):
                fl += 1
        fl -= 1
        return fl

    def prikosnoveniie(self):
        if self.life != 0:
            self.pos_y += 1
            self.update()
            fl = self.examination()
            if not fl:
                self.image = load_image("fire.png")
                self.life -= 1
                self.pos_y -= 1
                self.update()
                return self.pos_x, self.pos_y
            else:
                self.image = load_image("flame.png")
            self.pos_y -= 1
            self.update()
        else:
            self.image = load_image("empty.png")
        return None


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color):
        super().__init__(figure_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.proverka = 0
        self.color = color
        if color == "blue":
            self.image = load_image("blue.png")
        elif color == "red":
            self.image = load_image("red.png")
        elif color == "green":
            self.image = load_image("green.png")
        elif color == "small_bomb":
            self.image = load_image("small_bomb.jpg")
        self.rect = self.image.get_rect().move(
            self.pos_x * tile_width - 5, tile_height * self.pos_y)


class Figures(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, figura):
        super().__init__(figure_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.proverka = 0
        self.color = figura
        self.image = load_image(f"{self.color}.png")

        self.rect = self.image.get_rect().move(
            self.pos_x * tile_width - 5, tile_height * self.pos_y)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x - 5, tile_height * self.pos_y)
        fl = self.examination()
        if fl or pygame.sprite.collide_mask(self, down_border):
            self.pos_y -= 1
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x - 5, tile_height * self.pos_y)
            return "Next"
        self.proverka = False
        return None

    def examination(self):
        fl = 0
        for i in figure_group:
            if pygame.sprite.collide_mask(self, i):
                fl += 1
        fl -= 1
        return fl

    def down(self):
        self.pos_y += 1
        for i in fire:
            i.kill()

    def move(self, event):
        if event.key == pygame.K_LEFT:
            if not pygame.sprite.collide_mask(self, left_border):
                self.pos_x -= 1
                self.rect = self.image.get_rect().move(
                    self.pos_x * tile_width - 5, tile_height * self.pos_y)
                fl = self.examination()
                if fl:
                    self.pos_x += 1

        if event.key == pygame.K_RIGHT:
            if not pygame.sprite.collide_mask(self, right_border):
                self.pos_x += 1
                self.rect = self.image.get_rect().move(
                    self.pos_x * tile_width - 5, tile_height * self.pos_y)
                fl = self.examination()
                if fl:
                    self.pos_x -= 1

        if event.key == 107:
            self.image = pygame.transform.rotate(self.image, 90)
            fl = self.examination()
            k = self.rect.height - 35
            if pygame.sprite.collide_mask(self, right_border):
                if pygame.sprite.collide_mask(self, right_border)[0] != k:
                    fl += 1
            if fl:
                self.image = pygame.transform.rotate(self.image, -90)
        if event.key == 108:
            self.image = pygame.transform.rotate(self.image, -90)
            fl = self.examination()
            k = self.rect.height - 35
            if pygame.sprite.collide_mask(self, right_border):
                if pygame.sprite.collide_mask(self, right_border)[0] != k:
                    fl += 1
            if fl:
                self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect().move(
            self.pos_x * tile_width - 5, tile_height * self.pos_y)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Table(pygame.sprite.Sprite):
    # Класс который будет возвращать таблицу где находятся фигурки
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((1, 1),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (1, 1), 1)
        self.rect = pygame.Rect(x + 17.5, y + 17.5, 2 * 1, 2 * 1)

    def markup(self, board):
        for i, h in enumerate(board):
            for k, w in enumerate(h):
                self.rect = pygame.Rect(100 + 17.5 + i * 35, 17.5 + k * 35, 1, 1)
                for n in figure_group:
                    if pygame.sprite.collide_mask(self, n):
                        if n.color[:1] == "r":
                            board[i][k] = 1
                        if n.color[:1] == "g":
                            board[i][k] = 2
                        if n.color[:1] == "b":
                            board[i][k] = 3

        return board


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type):
        super().__init__(all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.fl = 0
        self.r = 3
        self.image = load_image("small_bomb.png")
        if type != "small":
            self.r = 5
            self.image = load_image("big_bomb.png")

        if type == "small":
            self.deistv = "following"
        else:
            self.deistv = "falling"
        self.rect = self.image.get_rect().move(
            (pos_x + 3) * tile_width - 5, tile_height * pos_y)

    def examination(self):
        fl = 0
        for i in figure_group:
            if pygame.sprite.collide_mask(self, i):
                fl += 1
        return fl

    def update(self, *args):
        if args[4] is not None:
            if args[4].key == pygame.K_LEFT:
                if not pygame.sprite.collide_rect(self, left_border):
                    self.rect.x -= tile_width

            if args[4].key == pygame.K_RIGHT:
                if not pygame.sprite.collide_rect(self, right_border):
                    self.rect.x += tile_width
        if self.deistv == "falling":
            if args[3] - args[2] <= 0:
                self.rect.y += tile_height
                if self.examination() or pygame.sprite.collide_rect(self, down_border):
                    self.fl = 3
                return 0
        else:
            self.rect.y = args[0] * tile_height
            self.rect.x = (args[1] + 3) * tile_width - 5
        return None


down_border = Border(100, HEIGHT, WIDTH - 100, HEIGHT)
left_border = Border(100, 0, 100, HEIGHT)
right_border = Border(WIDTH - 235, 0, WIDTH - 235, HEIGHT)