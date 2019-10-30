package main

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"strings"
)

func B2i(b bool) int {
	if b {
		return 1
	}
	return 0
}

type GameOfLife struct {
	current_generation [][]rune
	rows, cols         int
	prev_generation    [][]rune
	max_generations    int
	n_generations      int
}

func (g *GameOfLife) create_grid(randomize bool) {
	g.current_generation = make([][]rune, g.rows)
	for i := range g.current_generation {
		g.current_generation[i] = make([]rune, g.cols)
	}
	for i := range g.current_generation {
		for j := range g.current_generation[i] {
			if rand.Intn(B2i(randomize)+1) == 1 {
				g.current_generation[i][j] = '1'
			} else {
				g.current_generation[i][j] = '0'
			}
		}
	}
}
func (g *GameOfLife) Init(rows int, cols int, randomize bool, max_generations int) {
	g.rows = rows
	g.cols = cols
	g.max_generations = max_generations
	g.n_generations = 1
	g.create_grid(randomize)

}

func (g *GameOfLife) get_neighbours(x int, y int) []rune {
	var cells []rune
	if x-1 >= 0 && y-1 >= 0 {
		cells = append(cells, g.current_generation[x-1][y-1])
	}
	if x-1 >= 0 {
		cells = append(cells, g.current_generation[x-1][y])
	}
	if x-1 >= 0 && y+1 < g.cols {
		cells = append(cells, g.current_generation[x-1][y+1])
	}
	if y-1 >= 0 {
		cells = append(cells, g.current_generation[x][y-1])
	}
	if y+1 < g.cols {
		cells = append(cells, g.current_generation[x][y+1])
	}
	if x+1 < g.rows && y-1 >= 0 {
		cells = append(cells, g.current_generation[x+1][y-1])
	}

	if x+1 < g.rows {
		cells = append(cells, g.current_generation[x+1][y])
	}

	if x+1 < g.rows && y+1 < g.cols {
		cells = append(cells, g.current_generation[x+1][y+1])
	}
	return cells
}
func (g *GameOfLife) get_next_generation() [][]rune {
	var new_grid [][]rune
	new_grid = make([][]rune, g.rows)
	for i := range g.current_generation {
		new_grid[i] = make([]rune, g.cols)
	}

	for i := range g.current_generation {
		for j := range g.current_generation[i] {
			var cells []rune
			var counter int
			cells = g.get_neighbours(i, j)
			for k := range cells {
				if cells[k] == '1' {
					counter = counter + 1
				}
			}
			if counter == 2 && g.current_generation[i][j] == '1' {
				new_grid[i][j] = '1'
			} else {
				if counter == 3 {
					new_grid[i][j] = '1'
				} else {
					new_grid[i][j] = '0'
				}
			}

		}
	}

	g.n_generations = g.n_generations + 1
	return new_grid
}

func (g *GameOfLife) step() {
	g.prev_generation = g.current_generation
	g.current_generation = g.get_next_generation()

}
func (g *GameOfLife) is_n_generations_exceed() bool {
	return g.n_generations >= g.max_generations
}
func (g *GameOfLife) is_changing() bool {
	for i := range g.current_generation {
		for j := range g.current_generation[i] {
			if g.current_generation[i][j] != g.prev_generation[i][j] {
				return true
			}
		}
	}
	return false
}

func (g *GameOfLife) read(filename string) {
	content, _ := ioutil.ReadFile(filename)
	lines := strings.Split(string(content), "\n")
	for i := range lines {
		for j := range lines[i] {
			g.current_generation[i][j] = rune(lines[i][j])
		}
	}
}
func (g *GameOfLife) write(filename string) {
	f, err := os.OpenFile("save.txt", os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println(err)
		return
	}
	for i := range g.current_generation {
		new_line := g.current_generation[i]
		fmt.Fprintln(f, new_line)
	}
	f.Close()
}
func main() {
	game := new(GameOfLife)
	game.Init(8, 24, true, 50)
	var state bool
	state = false
	for state != true {
		fmt.Println()
		for i := range game.current_generation {
			for j := range game.current_generation[i] {
				fmt.Printf("%d", game.current_generation[i][j]-48)
			}
			fmt.Printf("\n")
		}
		game.step()
		fmt.Println()
		for i := range game.current_generation {
			for j := range game.current_generation[i] {
				fmt.Printf("%d", game.current_generation[i][j]-48)
			}
			fmt.Printf("\n")
		}
		fmt.Println(game.n_generations)
		state = !(game.is_changing()) || game.is_n_generations_exceed()
	}
}
