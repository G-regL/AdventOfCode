package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
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
	start := time.Now()

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

	grid := [][]int{}
	grid_90 := [][]int{}
	visible := 0

	for lineNumber, row := range sfile {
		grid = append(grid, []int{})
		for column, tree_s := range strings.Split(string(row), "") {
			tree_i, _ := strconv.Atoi(tree_s)
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
			// first and last tree of each row
			visible += 2
		}
	}

	highestScenicScore := 0
	//loop through tree grids, skipping first and last rows/columns
	for r := 1; r < len(grid)-1; r++ {
		for c := 1; c < len(grid[r])-1; c++ {
			//got a tree at grid[r][c]
			tree := grid[r][c]
			trees_left := grid[r][:c]
			trees_right := grid[r][c+1:]
			trees_up := grid_90[c][:r]
			trees_down := grid_90[c][r+1:]

			//check for visibility
			if isTaller(trees_left, tree) || isTaller(trees_right, tree) || isTaller(trees_up, tree) || isTaller(trees_down, tree) {
				visible++
			}

			// Calculate tree scores
			//  the outer for loops skip first and last rows/columns, but it's very unlikely that one of those would have the higest score
			treeScenicScore := getScore(reverse(trees_left), tree) * getScore(trees_right, tree) * getScore(reverse(trees_up), tree) * getScore(trees_down, tree)
			if treeScenicScore > highestScenicScore {
				// ... and update highest if it's bigger than current highest
				highestScenicScore = treeScenicScore
			}
		}
	}
	fmt.Println("Visible Trees:", visible)
	fmt.Println("highest scenic score:", highestScenicScore)

	elapsed := time.Since(start)
	fmt.Printf("Took %s\n", elapsed)
}
