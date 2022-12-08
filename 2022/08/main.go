package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

func isTaller(check []int, tree int) (taller bool) {
	taller = false
	max := 0
	for _, v := range check {
		if v >= max {
			max = v
		}
	}
	if tree > max {
		return true
	}
	return
}

func getScore(check []int, tree int) (score int) {
	score = 0

	for _, v := range check {
		if tree > v {
			score++
		} else if tree <= v {
			score++
			return score
		}
	}
	return
}

func reverse(src []int) (out []int) {
	for i := range src {
		// reverse the order
		out = append(out, src[len(src)-1-i])
	}
	return
}

func main() {

	flag.Parse()
	filename := "input.txt"

	// Detect the --test flag and use test data if needed
	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
	}

	// Open file for reading
	bfile, _ := os.ReadFile(filename)

	sfile := strings.Split(string(bfile), "\n")

	//fmt.Println("len_sfile:", len(sfile))

	//grid := map[int]map[int]int{}
	//grid_90 := map[int]map[int]int{}
	grid := [][]int{}
	grid_90 := [][]int{}
	visible := 0
	for lineNumber, row := range sfile {
		//fmt.Println("line:", lineNumber, strings.Split(string(row), ""))
		grid = append(grid, []int{})
		for column, tree_s := range strings.Split(string(row), "") {
			tree_i, _ := strconv.Atoi(tree_s)
			//fmt.Println("  column", column)
			grid[lineNumber] = append(grid[lineNumber], tree_i)
			if len(grid_90) <= column {
				grid_90 = append(grid_90, []int{})
			}
			grid_90[column] = append(grid_90[column], lineNumber)
			grid_90[column][lineNumber] = tree_i
		}

		if lineNumber == 0 || lineNumber == len(sfile)-1 {
			// first and last row
			visible += len(string(row))
		} else {
			// first and last tree
			visible += 2
		}
	}

	//fmt.Println("grid:", grid)
	//fmt.Println("grid_90:", grid_90)

	for r := 1; r < len(grid)-1; r++ {
		for c := 1; c < len(grid[r])-1; c++ {
			//got a tree at grid[r][c]
			tree := grid[r][c]
			//fmt.Printf("tree at (%d,%d) is height %d\n", r, c, tree)

			//check row
			if isTaller(grid[r][:c], tree) || isTaller(grid[r][c+1:], tree) || isTaller(grid_90[c][:r], tree) || isTaller(grid_90[c][r+1:], tree) {
				//fmt.Printf("tree at (%d,%d) with height %d is taller\n", r, c, tree)
				visible++
			}
			//fmt.Printf("tree at (%d,%d) with height %d is smaller\n", r, c, tree)
			////fmt.Println("row ", tree, grid[r][:c], isTaller(grid[r][:c], tree))
			////fmt.Println("row ", tree, grid[r][c:], isTaller(grid[r][c:], tree))
			//fmt.Println("   row: ", isTaller(grid[r][:c], tree), grid[r][:c], "", tree, ">", grid[r][c+1:], isTaller(grid[r][c+1:], tree))
			////fmt.Println("col ", tree, grid_90[c][:r], isTaller(grid_90[c][:r], tree))
			////fmt.Println("col ", tree, grid_90[c][r:], isTaller(grid_90[c][r:], tree))
			//fmt.Println("   col: ", isTaller(grid_90[c][:r], tree), grid_90[c][:r], "", tree, "", grid_90[c][r+1:], isTaller(grid_90[c][r+1:], tree))

		}
	}

	highestScenicScore := 0
	for r := 0; r < len(grid); r++ {
		for c := 0; c < len(grid[r]); c++ {
			//got a tree at grid[r][c]
			tree := grid[r][c]

			treeScenicScore := getScore(reverse(grid[r][:c]), tree) * getScore(grid[r][c+1:], tree) * getScore(reverse(grid_90[c][:r]), tree) * getScore(grid_90[c][r+1:], tree)
			//fmt.Printf("tree at (%d,%d) with height %d has scenic score of %d\n", r, c, tree, treeScenicScore)
			////fmt.Println("row ", reverse(grid[r][:c]), tree, getScore(reverse(grid[r][:c]), tree))
			////fmt.Println("row ", tree, grid[r][c+1:], getScore(grid[r][c+1:], tree))
			//fmt.Println("row", grid[r][:c], tree, grid[r][c+1:], getScore(reverse(grid[r][:c]), tree), getScore(grid[r][c+1:], tree))
			////fmt.Println("col ", reverse(grid_90[c][:r]), tree, getScore(reverse(grid_90[c][:r]), tree))
			////fmt.Println("col ", tree, grid_90[c][r+1:], getScore(grid_90[c][r+1:], tree))
			//fmt.Println("col", grid_90[c][:r], tree, grid_90[c][r+1:], getScore(reverse(grid_90[c][:r]), tree), getScore(grid_90[c][r+1:], tree))

			if treeScenicScore > highestScenicScore {
				highestScenicScore = treeScenicScore
			}

		}
	}

	fmt.Println("Visible Trees:", visible)
	fmt.Println("highest scenic score:", highestScenicScore)

}
