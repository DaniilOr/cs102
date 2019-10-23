import pathlib
import random
import copy
from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, size: Tuple[int, int], randomize: bool=True, max_generations: Optional[int]=None) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        grid = []
        for i in range(self.rows):
            sub_array = []
            for j in range(self.cols):
                sub_array.append(randomize * random.randint(0, 1))
            grid.append(sub_array)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        cells = []
        g = copy.deepcopy(self.curr_generation)
        coordinates = set([(x, y)])
        x = x -1
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
        new_grid = copy.deepcopy(self.curr_generation)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[i])):
                neighbours = self.get_neighbours((i, j)).count(1)
                if neighbours == 3:
                    new_grid[i][j] = 1
                elif neighbours == 2 and self.curr_generation[i][j] == 1:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
        self.n_generation += 1
        return new_grid


    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.n_generation >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, 'r')
        grid = []
        strings = f.read().split('\n')
        rows = len(strings)
        cols = len(strings[0])
        strings = strings[:-1]
        for s in strings:
            sub_array = []
            for char in s:
                sub_array.append(int(char))
            grid.append(sub_array)
        game = GameOfLife((rows, cols), False)
        game.curr_generation = copy.deepcopy(grid)
        f.close()
        return game



    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, 'w')
        for s in self.curr_generation:
            for item in s:
                f.write(str(item).replace("'", ''))
            f.write('\n')

if __name__ == '__main__':
    life = GameOfLife.from_file('4')
    #life.save(pathlib.Path('glider-4-steps.txt'))
    life.save('41')
    print(life.curr_generation)
