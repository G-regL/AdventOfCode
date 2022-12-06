package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
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

	xpos := 0
	zpos := 0
	direction := ""
	distance := 0
	for scanner.Scan() {
		_, _ = fmt.Sscanf(string(scanner.Text()), "%s %d", &direction, &distance)

		switch direction {
		case "forward":
			xpos += distance
		case "up":
			zpos -= distance
		case "down":
			zpos += distance
		}
	}

	fmt.Println("P1 product:", xpos*zpos)
	//fmt.Println("P2 Depth increased", increases_p2, "times")

}
