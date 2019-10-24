import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=50,
                 speed: int=10) -> None:
        super().__init__(life)
        print(self.life)
        self.cell_size = cell_size
        self.width = self.life.rows * self.cell_size
        self.height = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        csz = self.cell_size
        for i in range(0, self.height, self.cell_size):
            for j in range(0, self.width, self.cell_size):
                c1 = i // csz
                c2 = j // csz

                pygame.draw.rect(self.screen, pygame.Color('black')
                                 if self.life.curr_generation[c1][c2] else
                                 pygame.Color('white'), (j, i, csz, csz))

    def run(self) -> None:
        pygame.init()
        paused = False
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.life.create_grid(True)
        running = True
        while running and self.life.is_changing and \
                not self.life.is_max_generations_exceed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                elif event.type == pygame.MOUSEBUTTONUP:
                    cli_x, cli_y = event.pos
                    cli_x //= self.cell_size
                    cli_y //= self.cell_size
                    self.life.curr_generation[cli_y][cli_x] = \
                        int(not bool(self.life.curr_generation[cli_y][cli_x]))
                    self.draw_grid()
                    pygame.display.flip()
            if paused:
                self.draw_grid()
                pygame.display.flip()
                continue
            self.draw_lines()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    ui = GUI(GameOfLife((10, 10), True, 50))
    ui.run()
