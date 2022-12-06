package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

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
	increases := 0
	for scanner.Scan() {
		depth, _ := strconv.Atoi(scanner.Text())
		if depth > previous {
			increases++
		}
		previous = depth

	}

	fmt.Println("Depth increased", increases, "times")
}
