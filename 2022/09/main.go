package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

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

	positions := []string{}
	head := map[string]int{"x": 0, "y": 0}
	tail := map[string]int{"x": 0, "y": 0}
	for _, line := range sfile {
		direction := ""
		distance := 0
		_, _ = fmt.Sscanf(line, "%s %d", &direction, &distance)

		for i := 1; i <= distance; i++ {
			if direction == "U" {
				head["y"] += 1
			} else if direction == "D" {
				head["y"] -= 1

			} else if direction == "L" {
				head["x"] -= 1

			} else if direction == "R" {
				head["x"] += 1
			}

			x_diff := head["x"] - tail["x"]
			y_diff := head["y"] - tail["y"]

			//fmt.Println(x_diff_abs, y_diff_abs)
			//fmt.Println(head, tail)
			if y_diff == 2 || y_diff == -2 {
				tail["x"] = head["x"]
				tail["y"] = tail["y"] + (y_diff / 2)
			} else if x_diff == 2 || x_diff == -2 {
				tail["y"] = head["y"]
				tail["x"] = tail["x"] + (x_diff / 2)
			}

			//fmt.Printf("%d:%d\n", tail["x"], tail["y"])
			positions = append(positions, fmt.Sprintf("%d:%d", tail["x"], tail["y"]))

			//fmt.Println(head["x"], head["y"], tail["x"], tail["y"])
		}
		//fmt.Println("---")

	}

	//fmt.Println(dedup(positions))
	fmt.Println("Unique Positions:", len(dedup(positions)))
	//fmt.Println("highest scenic score:", highestScenicScore)

	elapsed := time.Since(start)
	fmt.Printf("Took %s\n", elapsed)
}
