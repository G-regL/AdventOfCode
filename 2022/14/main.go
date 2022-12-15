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
var flag_Draw = flag.Bool("draw", false, "Draw out the blocks")

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
	scanP1 := map[coord]string{}
	biggestY := 0
	smallestX, biggestX := 500, 500
	scan[coord{x: 500, y: 0}] = "+"
	for _, line := range strings.Split(sfile, "\n") {

		points := strings.Split(line, " -> ")
		last := coord{x: -1, y: -1}
		for _, point := range points {
			p := strings.Split(string(point), ",")
			cur := coord{x: toInt(p[0]), y: toInt(p[1])}
			scan[cur] = "#"
			//moving up/down
			if last.x == cur.x {
				//down
				if last.y > cur.y {
					for i := last.y; i >= cur.y; i-- {
						scan[coord{x: cur.x, y: i}] = "#"
					}
					//up
				} else if last.y < cur.y {
					for i := last.y; i <= cur.y; i++ {
						scan[coord{x: cur.x, y: i}] = "#"
					}
				}
			}

			// moving right/left
			if last.y == cur.y {
				//left
				if last.x > cur.x {
					for i := last.x; i >= cur.x; i-- {
						scan[coord{x: i, y: cur.y}] = "#"
					}
					//right
				} else if last.x < cur.x {
					for i := last.x; i <= cur.x; i++ {
						scan[coord{x: i, y: cur.y}] = "#"
					}
				}
			}
			last = cur
			if cur.y > biggestY {
				biggestY = cur.y
			}
			if cur.x > biggestX {
				biggestX = cur.x
			}
			if cur.x < smallestX {
				smallestX = cur.x
			}

		}
	}

	minx, maxx := smallestX, biggestX
	for f := smallestX - 200; f <= biggestX+200; f++ {
		scan[coord{x: f, y: biggestY + 2}] = "#"

		if f < minx {
			minx = f
		}
		if f > maxx {
			maxx = f
		}
	}
	smallestX, biggestX = minx, maxx

	flowing := true
	sandCounter := 0
	sand_P1 := 0

	//for loop := 1; loop <= 100 && flowing == true; loop++ {
	//for loop := 1; loop <= 100; loop++ {
	for flowing == true {

		sand := coord{x: 500, y: 0}
		rested := false
		for rested == false {

			_, sand_bb := scan[coord{x: sand.x, y: sand.y + 1}]
			_, sand_br := scan[coord{x: sand.x + 1, y: sand.y + 1}]
			_, sand_bl := scan[coord{x: sand.x - 1, y: sand.y + 1}]

			if !sand_bb {
				sand.y++
				if sand.y > biggestY && sand_P1 == 0 {
					//sand overflows the rock, and would keep going, so capture the number now for P1
					sand_P1 = sandCounter
					for k, v := range scan {
						scanP1[k] = v
					}
				}
			} else {

				if !sand_bl {
					sand.x--
				} else if !sand_br {
					sand.x++
				} else {
					scan[coord{x: sand.x, y: sand.y}] = "o"
					rested = true
				}
			}
			//}
		}
		scan[coord{x: sand.x, y: sand.y}] = "o"
		if scan[coord{x: 500, y: 0}] == "o" {
			flowing = false
		}
		sandCounter++
	}

	if *flag_Draw {
		fmt.Printf("\n-----------------------------------------------   Part 1   ---------------------------------\n")
		drawScan(scanP1, biggestY+1, smallestX, biggestX)
		fmt.Printf("\n-----------------------------------------------   Part 2   ---------------------------------\n")
		drawScan(scan, biggestY+2, smallestX, biggestX)
	}

	// Show us what we've got!
	fmt.Println("Part 1 Sand:", sand_P1)
	fmt.Println("Part 2 Sand:", sandCounter)

	fmt.Printf("Took %s\n", time.Since(start))

}
