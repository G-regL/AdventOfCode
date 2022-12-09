package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")
var flag_testData2 = flag.Bool("test2", false, "Use Test dataset #2")

func dedup(in []string) (out []string) {
	chars := make(map[string]bool)
	for _, c := range in {
		if _, value := chars[c]; !value {
			chars[c] = true
			out = append(out, c)
		}
	}
	return
}

func moveKnot(tail map[string]int, head map[string]int) map[string]int {

	// x_diff := head["x"] - tail["x"]
	// y_diff := head["y"] - tail["y"]

	// if y_diff == 2 || y_diff == -2 {
	// 	tail["x"] = head["x"]
	// 	tail["y"] = tail["y"] + (y_diff / 2)
	// } else if x_diff == 2 || x_diff == -2 {
	// 	tail["y"] = head["y"]
	// 	tail["x"] = tail["x"] + (x_diff / 2)
	// }

	// new positions algorithm taken from function `moveOne` in https://github.com/jasontconnell/advent/blob/master/2022/09/main.go
	if dist2(head, tail) > 1 {

		tdx, tdy := 0, 0

		if tail["y"] > head["y"] {
			tdy = 1
		} else if tail["y"] < head["y"] {
			tdy = -1
		}

		if tail["x"] > head["x"] {
			tdx = -1
		} else if tail["x"] < head["x"] {
			tdx = 1
		}

		// take care of diagonal
		if tail["x"] < head["x"] {
			tdx = 1
		} else if tail["x"] > head["x"] {
			tdx = -1
		}

		if tail["y"] < head["y"] {
			tdy = 1
		} else if tail["y"] > head["y"] {
			tdy = -1
		}
		tail["x"] += tdx
		tail["y"] += tdy
	}

	return tail
}

func getMax(max map[string]int, head1 map[string]int, head2 map[string]int, tail map[string]int, knot9 map[string]int) map[string]int {
	//max = map[string]int{"x": 0, "y": 0}

	card := []string{"x", "y"}

	for _, d := range card {
		if max[d] < head1[d] {
			max[d] = head1[d]
		}
		if max[d] < head2[d] {
			max[d] = head2[d]
		}
		if max[d] < tail[d] {
			max[d] = tail[d]
		}
		if max[d] < knot9[d] {
			max[d] = knot9[d]
		}
	}

	return max
}

// adapted from `dist` in https://github.com/jasontconnell/advent/blob/master/2022/09/main.go
func dist2(p1, p2 map[string]int) int {
	y := math.Abs(float64(p2["y"] - p1["y"]))
	x := math.Abs(float64(p2["x"] - p1["x"]))
	if y > 1 || x > 1 { //1,1 is diagonal but still touching
		return int(y + x)
	}
	return 1
}

// //taken from https://github.com/jasontconnell/advent/blob/master/2022/09/main.go
// // ----------------------------------

// type dir string

// const (
// 	U dir = "U"
// 	D dir = "D"
// 	L dir = "L"
// 	R dir = "R"
// )

// type move struct {
// 	dir dir
// 	num int
// }

// type xy struct {
// 	x, y int
// }

// func traverse(moves []move, n int) int {
// 	pos := make([]xy, n)
// 	visit := make([]map[xy]int, n)
// 	for i := 0; i < n; i++ {
// 		pos[i] = xy{}
// 		visit[i] = make(map[xy]int)
// 		visit[i][pos[i]] = 1
// 	}

// 	for _, mv := range moves {
// 		for i := 0; i < mv.num; i++ {
// 			moveOne(mv.dir, pos, visit)
// 		}
// 	}

// 	return len(visit[n-1])
// }

// func moveOne(d dir, pos []xy, visit []map[xy]int) {
// 	var dx, dy int
// 	switch d {
// 	case U:
// 		dy = 1
// 	case D:
// 		dy = -1
// 	case L:
// 		dx = -1
// 	case R:
// 		dx = 1
// 	}

// 	pos[0].x += dx
// 	pos[0].y += dy
// 	visit[0][pos[0]]++

// 	for i := 1; i < len(pos); i++ {
// 		fpos, bpos := pos[i-1], pos[i]
// 		if dist(fpos, bpos) > 1 {
// 			tdx, tdy := 0, 0

// 			if bpos.y > fpos.y {
// 				tdy = 1
// 			} else if bpos.y < fpos.y {
// 				tdy = -1
// 			}

// 			if bpos.x > fpos.x {
// 				tdx = -1
// 			} else if bpos.x < fpos.x {
// 				tdx = 1
// 			}

// 			// take care of diagonal
// 			if bpos.x < fpos.x {
// 				tdx = 1
// 			} else if bpos.x > fpos.x {
// 				tdx = -1
// 			}

// 			if bpos.y < fpos.y {
// 				tdy = 1
// 			} else if bpos.y > fpos.y {
// 				tdy = -1
// 			}

// 			pos[i].x += tdx
// 			pos[i].y += tdy
// 			visit[i][pos[i]]++
// 		}
// 	}
// }

// func dist(p1, p2 xy) int {
// 	y := math.Abs(float64(p2.y - p1.y))
// 	x := math.Abs(float64(p2.x - p1.x))
// 	if y > 1 || x > 1 { //1,1 is diagonal but still touching
// 		return int(y + x)
// 	}
// 	return 1
// }

// // -----------------------------------

func buildGrid(knots map[int]map[string]int, max map[string]int) {
	for y := 0; y <= max["y"]; y++ {
		for x := 0; x <= max["x"]; x++ {
			cell := "."
			if knots[0]["x"] == x && knots[0]["y"] == y {
				cell = fmt.Sprintf("H")
			}
			for k := 1; k < len(knots); k++ {
				if knots[k]["x"] == x && knots[k]["y"] == y {
					cell = fmt.Sprintf("%d", k)
				}
			}

			if x == 0 && y == 0 {
				cell = "S"
			}

			fmt.Printf(cell)

		}
		fmt.Printf("\n")
	}
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
	// Detect the --test flag and use test data if needed
	if *flag_testData2 {
		fmt.Println("***** USING TEST DATA #2 *****")
		filename = "test2.txt"
	}

	// Open file for reading
	bfile, _ := os.ReadFile(filename)

	sfile := strings.Split(string(bfile), "\n")

	positions_p1 := []string{}
	positions_p2 := []string{}

	head_p1 := map[string]int{"x": 0, "y": 0}
	//head_p2 := map[string]int{"x": 0, "y": 0}
	tail_p1 := map[string]int{"x": 0, "y": 0}
	knots_p1 := map[int]map[string]int{
		0: {"x": 0, "y": 0}, //head
		1: {"x": 0, "y": 0}}
	max := map[string]int{"x": 0, "y": 0}
	knots := map[int]map[string]int{
		0: {"x": 0, "y": 0}, //head
		1: {"x": 0, "y": 0}, 2: {"x": 0, "y": 0}, 3: {"x": 0, "y": 0},
		4: {"x": 0, "y": 0}, 5: {"x": 0, "y": 0}, 6: {"x": 0, "y": 0},
		7: {"x": 0, "y": 0}, 8: {"x": 0, "y": 0}, 9: {"x": 0, "y": 0},
	}

	//moves := []move{}

	for _, line := range sfile {
		// //taken from https://github.com/jasontconnell/advent/blob/master/2022/09/main.go
		// // ------------
		// sp := strings.Split(line, " ")
		// if len(sp) == 2 {
		// 	d := dir(sp[0])
		// 	n, _ := strconv.Atoi(sp[1])
		// 	moves = append(moves, move{dir: d, num: n})
		// }
		// // ------------

		//fmt.Println("---", line, "---")
		direction := ""
		distance := 0
		_, _ = fmt.Sscanf(line, "%s %d", &direction, &distance)

		//head_p2_moved := false
		for i := 1; i <= distance; i++ {
			if direction == "U" {
				head_p1["y"] += 1
				knots[0]["y"] += 1
			} else if direction == "D" {
				head_p1["y"] -= 1
				knots[0]["y"] -= 1
			} else if direction == "L" {
				head_p1["x"] -= 1
				knots[0]["x"] -= 1
			} else if direction == "R" {
				head_p1["x"] += 1
				knots[0]["x"] += 1
			}

			tail_p1 = moveKnot(tail_p1, head_p1)

			//knots[1] = moveKnot(knots[1], head_p2)
			for k := 1; k < len(knots); k++ {
				knots[k] = moveKnot(knots[k], knots[k-1])
			}

			//fmt.Printf("%d:%d\n", tail_p1["x"], tail_p1["y"])
			positions_p1 = append(positions_p1, fmt.Sprintf("%d:%d", tail_p1["x"], tail_p1["y"]))
			positions_p2 = append(positions_p2, fmt.Sprintf("%d:%d", knots[9]["x"], knots[9]["y"]))

			max = getMax(max, head_p1, knots[0], tail_p1, knots[9])

		}
		//fmt.Printf("%d:%d\n", knots[9]["x"], knots[9]["y"])

		knots_p1[0] = head_p1
		knots_p1[1] = tail_p1

		if *flag_testData {
			buildGrid(knots_p1, max)
		} else if *flag_testData2 {
			buildGrid(knots, max)
		}

	}

	//fmt.Println(knots)
	if *flag_testData {
		fmt.Println("Unique Positions P1:", len(dedup(positions_p1)))
		//fmt.Println("Unique Positions P1-cheat:", traverse(moves, 2))
		fmt.Println("Unique Positions P2: N/A")
	} else if *flag_testData2 {
		fmt.Println("Unique Positions P1: N/A")
		fmt.Println("Unique Positions P2:", len(dedup(positions_p2)))
		//fmt.Println("Unique Positions P2-cheat:", traverse(moves, 10))
	} else {
		fmt.Println("Unique Positions P1:", len(dedup(positions_p1)))
		fmt.Println("Unique Positions P2:", len(dedup(positions_p2)))
		//fmt.Println("Unique Positions P1-cheat:", traverse(moves, 2))
		//fmt.Println("Unique Positions P2-cheat:", traverse(moves, 10))
	}

	elapsed := time.Since(start)
	fmt.Printf("Took %s\n", elapsed)
}
