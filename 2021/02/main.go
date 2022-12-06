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

	horizontal := 0
	depth_p1 := 0
	depth_p2 := 0
	aim := 0
	direction := ""
	distance := 0
	for scanner.Scan() {
		_, _ = fmt.Sscanf(string(scanner.Text()), "%s %d", &direction, &distance)

		switch direction {
		case "forward":
			horizontal += distance
			depth_p2 += aim * distance
		case "up":
			depth_p1 -= distance
			aim -= distance
		case "down":
			depth_p1 += distance
			aim += distance
		}
	}

	fmt.Printf("P1 product: %-15d (h%d, d%d)\n", horizontal*depth_p1, horizontal, depth_p1)
	fmt.Printf("P2 product: %-15d (h%d, d%d, a%d)\n", horizontal*depth_p2, horizontal, depth_p2, aim)

}
