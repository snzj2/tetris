import os
import sys

import pygame
from random import choice
from settings import *


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

        self.left = 100
        self.top = 0
        self.cell_size = 35
        self.figuri = []

    def render(self, screen):
        for i, h in enumerate(self.board):
            for k, w in enumerate(h):
                if w == 1:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (self.left + i * self.cell_size, self.top + k * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + i * self.cell_size, self.top + k * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def on_click(self, cell):
        if cell != None:
            self.board[cell[0]][cell[1]] += 1
            if self.board[cell[0]][cell[1]] >= 2:
                self.board[cell[0]][cell[1]] = 0

    def get_cell(self, mouse_pos):
        cell = ()
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

    def next_move(self):
        #if not bool(self.figuri):
        self.figuri.append(Figures(7, 0))
        # for i in self.figuri:
        #     pass

all_sprites = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
figure_group = pygame.sprite.Group()

tile_width = tile_height = 35


class Figures(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(figure_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = load_image(f"{choice(figure)}.png")
        self.rect = self.image.get_rect().move(
            self.pos_x * tile_width - 5, tile_height * self.pos_y)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x - 5, tile_height * self.pos_y)
        fl = 0
        for i in figure_group:
            if pygame.sprite.collide_mask(self, i):
                fl += 1
        fl -= 1
        if fl or pygame.sprite.collide_mask(self, down_border):
            self.pos_y -= 1
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x - 5, tile_height * self.pos_y)
            return "Next"
        return None

    def down(self):
        self.pos_y += 1

    def move(self, event):
        if event.key == pygame.K_LEFT:
            if not pygame.sprite.collide_mask(self, left_border):
                self.pos_x -= 1
        if event.key == pygame.K_RIGHT:
            if not pygame.sprite.collide_mask(self, right_border):
                self.pos_x += 1
        if event.key == 107:
            self.image = pygame.transform.rotate(self.image, 90)
            self.image = pygame.transform.flip(self.image, False, True)
        if event.key == 108:
            self.image = pygame.transform.rotate(self.image, -90)
            self.image = pygame.transform.flip(self.image, False, True)
        if event.key == pygame.K_DOWN:
            self.pos_y = 21

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

down_border = Border(100, HEIGHT, WIDTH - 100, HEIGHT)
left_border = Border(100, 0, 100, HEIGHT)
right_border = Border(WIDTH - 135, 0, WIDTH - 135, HEIGHT)