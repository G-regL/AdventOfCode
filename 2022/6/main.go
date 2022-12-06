package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"
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

func find(line []string, frameSize int) (position int) {
	position = frameSize
	buffer := line[0:frameSize]
	found := false
	for !found {
		if len(buffer) == len(dedup(buffer)) {
			found = true
		} else {
			//move buffer forward 1 char, increment pointer
			buffer = append(buffer[1:], line[position])
			position++
		}
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

	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "")
		fmt.Printf("Line starting with '%s...'\n", strings.Join(line[:20], ""))

		fmt.Println("  Start-of-Packet found after character", find(line, 4))
		fmt.Println("  Start-of-Signal found after character", find(line, 14))
	}
}
