package main

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"path/filepath"
	"time"
)

func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}

func Min(x, y int) int {
	if x > y {
		return y
	}
	return x
}
func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}
func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filtered_values := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filtered_values = append(filtered_values, v)
		}
	}
	return filtered_values
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func group(values []byte, n int) [][]byte {

	var additional int = boolToInt(len(values)%n != 0)
	var ans = make([][]byte, len(values)/n+additional)

	var l int
	for l = 0; l < len(ans); l++ {
		ans[l] = make([]byte, n)
	}

	var i, j int
	for i = 0; i < len(ans); i++ {
		for j = 0; j < n; j++ {
			if n*i+j >= len(values) {
				break
			}
			ans[i][j] = values[n*i+j]
		}

	}
	return ans
}

func getRow(grid [][]byte, row int) []byte {

	return grid[row]
}

func getCol(grid [][]byte, col int) []byte {
	var ans = make([]byte, len(grid))
	for i := 0; i < len(grid); i++ {
		ans[i] = grid[i][col]
	}
	return ans
}

func getBlock(grid [][]byte, row int, col int) []byte {
	var br int = row / 3 * 3
	var bc int = col / 3 * 3
	var ans []byte
	ans = make([]byte, 9)
	var counter int = 0
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			ans[counter] = grid[br+i][bc+j]
			counter++
		}
	}
	return ans
}

func findEmptyPosition(grid [][]byte) (int, int) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid[i]); j++ {
			if grid[i][j] == '.' {
				return i, j
			}
		}
	}
	return -1, -1
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
	var set_of_used = make(map[byte]bool)
	var field []byte = getBlock(grid, row, col)
	for i := 0; i < len(field); i++ {
		set_of_used[field[i]] = true
	}
	var rows []byte = getRow(grid, row)
	for i := 0; i < len(rows); i++ {
		set_of_used[rows[i]] = true
	}
	var cols []byte = getCol(grid, col)
	for i := 0; i < len(cols); i++ {
		set_of_used[cols[i]] = true
	}
	var ok bool
	var i byte
	var counter int = 0
	var possible_vals []byte
	for i = 49; i < 58; i++ {
		_, ok = set_of_used[i]
		if !ok {
			counter++
		}
	}
	possible_vals = make([]byte, counter)
	counter = 0

	for i = 49; i < 58; i++ {
		_, ok = set_of_used[i]
		if !ok {
			possible_vals[counter] = i
			counter++
		}
	}
	return possible_vals
}

func solve(grid [][]byte) ([][]byte, bool) {
	var row, col int
	row, col = findEmptyPosition(grid)
	if row == -1 && col == -1 {
		return grid, true
	}
	var solved bool
	var values []byte = findPossibleValues(grid, row, col)
	for i := 0; i < len(values); i++ {
		grid[row][col] = values[i]
		grid, solved = solve(grid)
		if solved {
			return grid, true
		}
	}
	grid[row][col] = '.'
	return grid, false
}

func checkSolution(grid [][]byte) bool {
	var ok bool
	var c byte
	for i := 0; i < len(grid); i++ {

		var set_of_used = make(map[byte]bool)
		var cols []byte = getCol(grid, i)
		for j := 0; j < len(cols); j++ {
			set_of_used[cols[j]] = true
		}
		for c = 49; c < 58; c++ {
			_, ok = set_of_used[c]
			if !ok {

				return false
			}
		}

	}
	for i := 0; i < len(grid); i++ {
		var set_of_used = make(map[byte]bool)
		var rows []byte = getRow(grid, i)
		for j := 0; j < len(rows); j++ {
			set_of_used[rows[j]] = true
		}
		for c = 49; c < 58; c++ {
			_, ok = set_of_used[c]
			if !ok {

				return false
			}
		}

	}
	var rind = []int{0, 3, 6}
	var cind = []int{0, 3, 6}

	for ii := 0; ii < len(rind); ii++ {
		for jj := 0; jj < len(cind); jj++ {
			var set_of_used = make(map[byte]bool)
			var block []byte = getBlock(grid, rind[ii], cind[jj])
			for j := 0; j < len(block); j++ {
				set_of_used[block[j]] = true
			}
			for c = 49; c < 58; c++ {
				_, ok = set_of_used[c]
				if !ok {
					return false
				}
			}

		}

	}
	return true
}

func generateSudoku(N int) [][]byte {

	var template [][]byte
	
	for i:= 0; i<9; i++{
		template[i] = make([]byte, 9)
		for j:=0; j<9; j++{
		template[i][j] = '.'
		}
	}
	var grid, _ = solve(template)
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)
	for N = 81 - Min(81, Max(N, 0)); N != 0; N += 0 {
		var row int = r1.Intn(8)
		var col int = r1.Intn(8)
		if grid[row][col] == '.' {
			continue
		} else {
			N--
		}
	}
	return grid
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			fmt.Println("Solution for", fname)
			display(solution)

			fmt.Println(checkSolution(solution))
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
	/*
	   	var line = []byte{1,2,3,4}
	   	var res [][]byte
	   res=group(line,3)
	   for i:=0; i< len(res); i++ {
	   	for j:=0; j<len(res[i]); j++ {
	   		fmt.Println(res[i][j])
	   	}
	   	fmt.Println("ss")
	   }
	   var test = [][]byte{
	   								{'1', '2', '.'},
	   								{'4', '5', '6'},
	   								{'7', '8', '9'}}
	   	fmt.Println(findPossibleValues(test, 0,2))
	*/
}
