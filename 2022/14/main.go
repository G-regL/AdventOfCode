package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

type coord struct {
	x, y int
}

func toInt(in string) (out int) {
	out, _ = strconv.Atoi(string(in))
	return out
}

func drawScan(points map[coord]string, maxY, minX, maxX int) {
	for y := 0; y <= maxY; y++ {
		for x := minX; x <= maxX; x++ {
			if marker, p := points[coord{x: x, y: y}]; p {
				fmt.Printf(marker)
			} else {
				fmt.Printf(".")
			}
		}
		fmt.Printf("\n")
	}
}

func checkBelow(scan map[coord]string, p coord) bool {

	u := coord{x: p.x, y: p.y + 1}
	r := coord{x: p.x + 1, y: p.y + 1}
	l := coord{x: p.x - 1, y: p.y + 1}
	if _, occupied_u := scan[u]; occupied_u {
		return true
	} else {
		if _, occupied_l := scan[l]; occupied_l {
			return true
		} else if _, occupied_r := scan[r]; !occupied_r {
			return true
		} else {
			return false
		}
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

	// Read in file as bytes, and convert to a string.
	bfile, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	sfile := string(bfile)

	scan := map[coord]string{}
	biggestY := 0
	scan[coord{x: 500, y: 0}] = "+"
	for _, line := range strings.Split(sfile, "\n") {
		//path := []string{}
		//fmt.Println("line", line)

		points := strings.Split(line, " -> ")
		//fmt.Println("points", points)
		last := coord{x: -1, y: -1}
		for _, point := range points {
			//fmt.Println("point", point)
			p := strings.Split(string(point), ",")
			//fmt.Println("p", p)
			cur := coord{x: toInt(p[0]), y: toInt(p[1])}
			scan[cur] = "#"
			//moving up/down
			if last.x == cur.x {
				//down
				if last.y > cur.y {
					//fmt.Println("  last.y > cur.y  ", last.y, cur.y, last.y > cur.y)
					for i := last.y; i >= cur.y; i-- {
						scan[coord{x: cur.x, y: i}] = "#"
						//fmt.Println("# at", coord{x: cur.x, y: i})
					}
					//up
				} else if last.y < cur.y {
					//fmt.Println("  last.y < cur.y  ", last.y, cur.y, last.y < cur.y)
					for i := last.y; i <= cur.y; i++ {
						scan[coord{x: cur.x, y: i}] = "#"
						//fmt.Println("# at", coord{x: cur.x, y: i})
					}
				}
			}

			// moving right/left
			if last.y == cur.y {
				//left
				if last.x > cur.x {
					//fmt.Println("  last.x > cur.x  ", last.x, cur.x, last.x > cur.x)
					for i := last.x; i >= cur.x; i-- {
						scan[coord{x: i, y: cur.y}] = "#"
						//fmt.Println("# at", coord{x: i, y: cur.y})
					}
					//right
				} else if last.x < cur.x {
					//fmt.Println("  last.x < cur.x  ", last.x, cur.x, last.x < cur.x)
					for i := last.x; i <= cur.x; i++ {
						scan[coord{x: i, y: cur.y}] = "#"
						//fmt.Println("# at", coord{x: i, y: cur.y})
					}
				}
			}
			last = cur
			//fmt.Println(scan)
			if cur.y > biggestY {
				biggestY = cur.y
			}

		}
	}

	fmt.Println(len(scan), biggestY)

	flowing := true
	for sandCounter := 1; sandCounter <= 5 && flowing == true; sandCounter++ {
		sand := coord{x: 500, y: 0}
		rested := false
		for rested == false {

			//if !checkBelow(scan, sand) {
			//
			//} else {

			_, sand_bb := scan[coord{x: sand.x, y: sand.y + 1}]
			_, sand_br := scan[coord{x: sand.x + 1, y: sand.y + 1}]
			_, sand_bl := scan[coord{x: sand.x - 1, y: sand.y + 1}]

			// rework loop to increment/decrement x, and increment y as needed
			if !sand_bb {
				sand.y++
				if sand.y > biggestY+5 {
					fmt.Println("overflow")
					flowing = false
					rested = true
				}
			} else {

				// find way to incrase X and loop again
				if _, occupied_bl := scan[sand_bl]; !occupied_bl {
					// check left

					rested = true

				} else if _, occupied_br := scan[sand_br]; !occupied_br {
					// check right
					//scan[coord{x: sand.x + 1, y: sand.y + 1}] = "o"
					rested = true
				} else {
					//scan[coord{x: sand.x, y: sand.y}] = "o"
					rested = true
				}
			}
			//}
		}
		scan[coord{x: sand.x, y: sand.y}] = "o"
		//fmt.Println(sandCounter)

	}

	drawScan(scan, biggestY, 493, 504)

	/*
		check below
			if !occupied below
				increment y + 1 && continue
	*/
	// Show us what we've got!
	//fmt.Println("Part 1 Monkey Business:", inspectedItems_p1[len(inspectedItems_p1)-1]*inspectedItems_p1[len(inspectedItems_p1)-2])

	fmt.Printf("Took %s\n", time.Since(start))

}
