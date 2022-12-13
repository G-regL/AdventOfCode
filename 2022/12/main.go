package main

import (
	"bufio"
	"flag"
	"fmt"
	"math"
	"os"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

// type point struct {
// 	x      int
// 	y      int
// 	height int
// }

// func toInt(in string) (out int) {
// 	out, _ = strconv.Atoi(in)
// 	return out
// }

// func getPoint(points []point, x, y int) (out int) {
// 	for id, p := range points {
// 		if p.x == x && p.y == y {
// 			return id
// 		}
// 	}
// 	return

// }

type coord struct {
	x, y int
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
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

	f, _ := os.Open(filename)

	//bulk of today's code is taken from https://github.com/Nikscorp/advent_of_code_2022/blob/master/days/day12.go
	// I don't really get how it works, but I'm certain that given enough time I could work it out..

	reader := bufio.NewReader(f)
	grid := make([][]byte, 0)
	for {
		var line string
		_, err := fmt.Fscanf(reader, "%s\n", &line)
		if err != nil {
			break
		}
		grid = append(grid, []byte(line))
	}

	var (
		starts_p1 coord
		starts_p2 []coord
		end       coord
	)

	for i := range grid {
		for j := range grid[i] {
			//if grid[i][j] == 'S' || grid[i][j] == 'a' { // or just grid[i][j] == 'S' for task 1
			//if grid[i][j] == 'S' { // or just grid[i][j] == 'S' for task 1
			if grid[i][j] == 'S' {
				starts_p1 = coord{i, j}
				starts_p2 = append(starts_p2, coord{i, j})
			} else if grid[i][j] == 'a' {
				starts_p2 = append(starts_p2, coord{i, j})
			} else if grid[i][j] == 'E' {
				end = coord{i, j}
			}
		}
	}

	minSteps_p2 := math.MaxInt

	//fmt.Println(starts)
	// to remove E from grid
	grid[end.x][end.y] = 'z'
	grid[starts_p1.x][starts_p1.y] = 'a'
	minSteps_p1 := bfs(grid, starts_p1, end)
	for _, start := range starts_p2 {
		// to remove possible 'S' from grid
		grid[start.x][start.y] = 'a'
		curSteps := bfs(grid, start, end)
		minSteps_p2 = min(minSteps_p2, curSteps)
	}

	fmt.Println("Minimum steps for Part1:", minSteps_p1)
	fmt.Println("Minimum steps for Part2:", minSteps_p2)

	fmt.Printf("Took %s\n", time.Since(start))

}

func bfs(grid [][]byte, start, end coord) int {
	seen := make(map[coord]bool)
	seen[start] = true
	queue := []coord{start}
	steps := 0
	var dirs = []coord{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	found := false

	// simple BFS
L:
	for len(queue) > 0 {
		k := len(queue)
		for i := 0; i < k; i++ {
			cur := queue[0]
			queue = queue[1:]

			if cur == end {
				found = true
				break L
			}

			for _, dir := range dirs {
				newCoord := coord{cur.x + dir.x, cur.y + dir.y}
				// isInvalid?
				if newCoord.x < 0 || newCoord.x >= len(grid) || newCoord.y < 0 || newCoord.y >= len(grid[0]) {
					continue
				}
				// isSeen?
				if seen[newCoord] {
					continue
				}
				// isTooHigh?
				isNewCoordGreater := grid[newCoord.x][newCoord.y] > grid[cur.x][cur.y]
				if isNewCoordGreater && grid[newCoord.x][newCoord.y]-grid[cur.x][cur.y] > 1 {
					continue
				}
				seen[newCoord] = true
				queue = append(queue, newCoord)
			}
		}
		steps++
	}

	if !found {
		//fmt.Println(start, "to", end, "not fund")
		return math.MaxInt
	}

	return steps
}
