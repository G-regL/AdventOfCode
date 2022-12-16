package main

import (
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

type input = []string
type output = int

type xy struct {
	x, y int
}

type sensor struct {
	pt       xy
	beacon   xy
	strength int
}

var isexample bool

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
	sfile := strings.Split(string(bfile), "\n")

	p1 := part1(sfile)
	p2 := part2(sfile)

	//w := common.TeeOutput(os.Stdout)
	fmt.Println("--2022 day 15 solution--")
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)

	fmt.Printf("Took %s\n", time.Since(start))
}

func part1(in input) output {
	sensors := parseInput(in)
	row := 2000000
	fmt.Println(minmax(sensors))
	if isexample {
		row = 10
	}
	return findVoids(sensors, row)
}

func part2(in input) output {
	sensors := parseInput(in)
	low := 0
	high := 4000000
	if isexample {
		high = 20
	}
	return findBeacon(sensors, low, high, 4000000)
}

func findBeacon(sensors []sensor, searchlow, searchhigh, mult int) int {
	pt := xy{}
	found := false
	for y := searchlow; y <= searchhigh && !found; y++ {
		for x := searchlow; x <= searchhigh && !found; x++ {
			inrange := false
			for _, s := range sensors {
				d := dist(s.pt, xy{x, y})
				if d <= s.strength {
					inrange = true
					skip := s.strength - d

					x += skip
					break
				}
			}

			if !inrange {
				pt = xy{x, y}
				found = true
			}
		}
	}

	return pt.x*mult + pt.y
}

func findVoids(sensors []sensor, row int) int {
	min, max := minmax(sensors)
	total := 0
	for i := min.x; i < max.x+1; i++ {
		pt := xy{i, row}

		inrange := false
		for _, s := range sensors {
			if dist(s.pt, pt) <= s.strength && pt != s.beacon {
				inrange = true
				break
			}
		}

		if inrange {
			total++
		}
	}
	return total
}

func minmax(sensors []sensor) (xy, xy) {
	min, max := xy{math.MaxInt32, math.MaxInt32}, xy{math.MinInt32, math.MinInt32}
	for _, s := range sensors {
		if s.pt.x-s.strength < min.x {
			min.x = s.pt.x - s.strength
		}

		if s.pt.x+s.strength > max.x {
			max.x = s.pt.x + s.strength
		}

		if s.pt.y-s.strength < min.y {
			min.y = s.pt.y - s.strength
		}

		if s.pt.y+s.strength > max.y {
			max.y = s.pt.y + s.strength
		}
	}
	return min, max
}

func dist(p1, p2 xy) int {
	dx := math.Abs(float64(p2.x - p1.x))
	dy := math.Abs(float64(p2.y - p1.y))
	return int(dx + dy)
}

func parseInput(in input) []sensor {
	reg := regexp.MustCompile(`Sensor at x=([0-9\-]+), y=([0-9\-]+): closest beacon is at x=([0-9\-]+), y=([0-9\-]+)`)
	sensors := []sensor{}
	for _, line := range in {
		m := reg.FindStringSubmatch(line)
		if len(m) == 5 {
			sx, _ := strconv.Atoi(m[1])
			sy, _ := strconv.Atoi(m[2])
			bx, _ := strconv.Atoi(m[3])
			by, _ := strconv.Atoi(m[4])

			sxy := xy{sx, sy}
			bxy := xy{bx, by}
			s := sensor{pt: sxy, beacon: bxy, strength: dist(sxy, bxy)}
			sensors = append(sensors, s)
		}
	}
	return sensors
}
