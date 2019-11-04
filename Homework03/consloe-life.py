import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)


    def draw_borders(self, screen) -> None:
        screen.refresh()
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')


    def draw_grid(self, screen) -> None:
        screen.refresh()
        for i in range(len(life.curr_generation)):
            for j in range(len(life.curr_generation[i])):
                screen.addch(i, j, ord('#'))


    def run(self) -> None:
        screen = curses.initscr()
        life.create_grid()
        curses.noecho()
        curses.nodelay()
        self.draw_borders(screen)
        pause = False
        while life.is_changing and not life.is_max_generations_exceed:
            if screen.getch() == 32:
                pause = not pause
            if screen.getch() == int('q'):
                break
            if screen.getch() == int('s'):
                self.life.save('mysave.txt')
            if pause:
                screen.refresh()
                continue
            self.draw_grid(screen)
            life.step()
            screen.refresh()
        curses.endwin()
if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=50)
    ui = Console(life)
    ui.run()
