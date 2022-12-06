package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

func sumSlice(input []int) (sum int) {
	for i := range input {
		sum += input[i]
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
	f, _ := os.Open(filename)
	defer f.Close()

	scanner := bufio.NewScanner(f)

	previous := 1000000
	depths := []int{}
	increases_p1 := 0
	increases_p2 := 0
	for scanner.Scan() {
		d, _ := strconv.Atoi(scanner.Text())
		if d > previous {
			increases_p1++
		}
		previous = d

		depths = append(depths, d)
	}

	previous = 1000000
	for i := 0; i <= len(depths); i++ {
		depth := sumSlice(depths[i : i+3])
		if depth > previous {
			increases_p2++
		}
		previous = depth
	}

	fmt.Println("P1 Depth increased", increases_p1, "times")
	fmt.Println("P2 Depth increased", increases_p2, "times")

}
