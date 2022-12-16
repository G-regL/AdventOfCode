package main

import (
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

var flag_Verbose = flag.Bool("verbose", false, "print a bunch of extra text stuff to say what we're doing")

type coord struct {
	x, y int
}

func verbose(msg ...any) {
	if *flag_Verbose {
		fmt.Fprintln(os.Stdout, msg...)
	}
}

func toInt(in string) (out int) {
	out, _ = strconv.Atoi(in)
	return out
}

func min(a, b int) (min int) {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) (min int) {
	if a > b {
		return a
	}
	return b
}

func distance(a, b coord) (dist int) {
	dx := float64(a.x - b.x)
	dy := float64(a.y - b.y)

	dist = int(math.Abs(dx) + math.Abs(dy))
	return
}

func drawGrid(points map[coord]string, bounds map[string]int) {
	for y := bounds["miny"]; y <= bounds["maxy"]; y++ {
		for x := bounds["minx"]; x <= bounds["maxx"]; x++ {
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

	// Detect the --test flag and use sample data it's set
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

	grid := map[coord]string{}
	sensors := map[coord]bool{}
	beacons := map[coord]bool{}
	pairs := []map[string]coord{}

	bounds := map[string]int{"minx": 0, "miny": 0, "maxx": 0, "maxy": 0}

	for _, line := range strings.Split(sfile, "\n") {

		verbose("got line " + line)
		sx, sy, bx, by := 0, 0, 0, 0

		_, _ = fmt.Sscanf(line, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &sx, &sy, &bx, &by)
		verbose("sensor at " + strconv.Itoa(sx) + "," + strconv.Itoa(sy) + "; beacon at " + strconv.Itoa(bx) + "," + strconv.Itoa(by))
		pairs = append(pairs, map[string]coord{"S": {x: sx, y: sy}, "B": {x: bx, y: by}})
		grid[coord{x: sx, y: sy}] = "S"
		sensors[coord{x: sx, y: sy}] = true

		grid[coord{x: bx, y: by}] = "B"
		beacons[coord{x: bx, y: by}] = true

		bounds["minx"] = min(bounds["minx"], sx-distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		//bounds["minx"] = min(bounds["minx"], bx-distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		bounds["miny"] = min(bounds["miny"], sy-distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		//bounds["miny"] = min(bounds["miny"], bx-distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))

		bounds["maxx"] = max(bounds["maxx"], sx+distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		//bounds["maxx"] = max(bounds["maxx"], bx+distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		bounds["maxy"] = max(bounds["maxy"], sy+distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		//bounds["maxy"] = max(bounds["maxy"], bx+distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
	}
	keyLine_P1 := 2000000
	// Detect the --test flag and use sample data it's set
	if *flag_testData {
		keyLine_P1 = 10
	}

	// this block borrowed from https://github.com/jasontconnell/advent/blob/master/2022/15/main.go
	totalP1 := 0
	for i := bounds["minx"]; i < bounds["maxx"]+1; i++ {
		pt := coord{i, keyLine_P1}

		inrange := false
		for _, p := range pairs {
			if distance(p["S"], pt) <= distance(p["S"], p["B"]) && pt != p["B"] {
				inrange = true
				break
			}
		}

		if inrange {
			totalP1++
		}
	}

	searchLow_P2 := 0
	searchHigh_P2 := 4000000
	multiplier_P2 := 4000000

	pt := coord{}
	found := false
	for y := searchLow_P2; y <= searchHigh_P2 && !found; y++ {
		for x := searchLow_P2; x <= searchHigh_P2 && !found; x++ {
			inrange := false
			for _, s := range pairs {
				d := distance(s["S"], coord{x, y})
				if d <= distance(s["S"], s["B"]) {
					inrange = true
					skip := distance(s["S"], s["B"]) - d

					x += skip
					break
				}
			}

			if !inrange {
				pt = coord{x, y}
				found = true
			}
		}
	}

	freq_P2 := pt.x*multiplier_P2 + pt.y

	// ------------ end borrowed

	counter := 0
	for _, p := range pairs {
		//p := pairs[6]
		for dist := 1; dist <= distance(p["S"], p["B"]); dist++ {

			for x := p["S"].x - dist; x <= p["S"].x+dist; x++ {
				for y := p["S"].y - dist; y <= p["S"].y+dist; y++ {
					thisPoint := coord{x: x, y: y}
					if _, occ := grid[thisPoint]; !occ && distance(p["S"], thisPoint) <= dist { //  && y == keyLine_P1

						if y == keyLine_P1 {
							counter++
						}
						if x <= bounds["maxx"] && x >= bounds["minx"] && y <= bounds["maxy"] && y >= bounds["miny"] {
							grid[coord{x: x, y: y}] = "#"
						}
						//bounds["minx"] = min(bounds["minx"], x)
						//bounds["miny"] = min(bounds["miny"], y)

						//bounds["maxx"] = max(bounds["maxx"], x)
						//bounds["maxy"] = max(bounds["maxy"], y)
					}
				}
			}
		}
	}

	drawGrid(grid, bounds)

	// fmt.Printf("\n\n")
	// for y := bounds["miny"] - 1; y <= bounds["maxy"]+1; y++ {
	// 	if marker, p := grid[coord{x: 10, y: y}]; p {
	// 		fmt.Printf(marker)
	// 	} else {
	// 		fmt.Printf(".")
	// 	}
	// }

	// fmt.Printf("\n")

	fmt.Println("Part 1 voids:", totalP1)

	fmt.Println("Part 2 beacon frequency:", freq_P2)

	//verbose(pairs)
	//verbose(len(grid), grid)
	//verbose(len(sensors), sensors)
	//verbose(len(beacons), beacons)

	fmt.Printf("Took %s\n", time.Since(start))
}
