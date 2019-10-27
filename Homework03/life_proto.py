import pygame
import random
import time
from pygame.locals import *
from typing import List, Tuple
import copy

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.create_grid(True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.grid = copy.deepcopy(self.get_next_generation())
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        self.grid = []
        for i in range(self.cell_height):
            sub_array = []
            for j in range(self.cell_width):
                sub_array.append(randomize * (random.randint(0, 1)))
            self.grid.append(sub_array)
        return self.grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        csz = self.cell_size
        for i in range(0, self.height, self.cell_size):
            for j in range(0, self.width, self.cell_size):
                c1 = i // csz
                c2 = j // csz

                pygame.draw.rect(self.screen, pygame.Color('black')
                                 if self.grid[c1][c2] else pygame.Color('white'),
                                 (j, i, csz, csz))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x, y = cell
        cells = []
        g = copy.deepcopy(self.grid)
        coordinates = set([(x, y)])
        x = x - 1
        y = y - 1
        for i in range(0, 3):
            for j in range(0, 3):
                new_x = max(0, min(x + i, len(g)-1))
                new_y = max(0, min(y + j, len(g[0])-1))
                tup = ((new_x, new_y))
                coordinates.update([tup])
        for item in coordinates:
            if not (item[0] == x + 1 and item[1] == y + 1):
                cells.append(g[item[0]][item[1]])
        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = copy.deepcopy(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                neighbours = self.get_neighbours((i, j)).count(1)
                if neighbours == 3:
                    new_grid[i][j] = 1
                elif neighbours == 2 and self.grid[i][j] == 1:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
        return new_grid

if __name__ == '__main__':
    game = GameOfLife(320, 240, 40)
    game.run()
