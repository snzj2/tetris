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
        self.figuri.append(Figures(4, 0))
        for i in self.figuri:
            pass


all_sprites = pygame.sprite.Group()
border_group = pygame.sprite.Group()
figure_group = pygame.sprite.Group()

tile_width = tile_height = 35


class Figures(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(figure_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = load_image(f"{choice(figure)}.png")

        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x - 5, tile_height * self.pos_y)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x - 5, tile_height * self.pos_y)

    def down(self):
        self.pos_y += 1

    def move(self, event):
        if event.key == pygame.K_LEFT:
            self.pos_x -= 1
        if event.key == pygame.K_RIGHT:
            self.pos_x += 1
        if event.key == 107:
            self.image = pygame.transform.rotate(self.image, 90)
            self.image = pygame.transform.flip(self.image, False, True)
        if event.key == 108:
            self.image = pygame.transform.rotate(self.image, -90)
            self.image = pygame.transform.flip(self.image, False, True)

