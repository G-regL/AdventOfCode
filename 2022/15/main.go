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

type coord struct {
	x, y int
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

	pairs := []map[string]coord{}

	bounds := map[string]int{"minx": 0, "miny": 0, "maxx": 0, "maxy": 0}

	for _, line := range strings.Split(sfile, "\n") {

		sx, sy, bx, by := 0, 0, 0, 0

		_, _ = fmt.Sscanf(line, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &sx, &sy, &bx, &by)
		pairs = append(pairs, map[string]coord{"S": {x: sx, y: sy}, "B": {x: bx, y: by}})

		bounds["minx"] = min(bounds["minx"], sx-distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		bounds["miny"] = min(bounds["miny"], sy-distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))

		bounds["maxx"] = max(bounds["maxx"], sx+distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
		bounds["maxy"] = max(bounds["maxy"], sy+distance(coord{x: sx, y: sy}, coord{x: bx, y: by}))
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

	fmt.Println("Part 1 voids:", totalP1)
	fmt.Println("Part 2 beacon frequency:", freq_P2)

	fmt.Printf("Took %s\n", time.Since(start))
}
