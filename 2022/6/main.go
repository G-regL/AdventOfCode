package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
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

func main() {
	flag.Parse()

	filename := "input.txt"

	// Detect the --test flag and use test data if needed
	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
	}

	// Open file for reading
	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()
	scanner := bufio.NewScanner(f)

	startOfPacket := map[int]int{}
	startOfSignal := map[int]int{}
	lineCounter := 1

	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "")
		fmt.Printf("Line starting with '%s...'\n", strings.Join(line[:20], ""))

		pointer_p1 := 4
		buffer_p1 := line[0:pointer_p1]
		_, SoPExists := startOfPacket[lineCounter]
		for !SoPExists {
			// Part 1
			if pointer_p1 >= len(line) {
				fmt.Println("No Start-of-Packet found :(")
				break
			}

			if len(buffer_p1) == len(dedup(buffer_p1)) {
				// capture pointer, and break out
				startOfPacket[lineCounter] = pointer_p1
				fmt.Println("  Start-of-Packet found after character", startOfPacket[lineCounter])
			} else {
				//move buffer forward 1 char, increment pointer
				buffer_p1 = append(buffer_p1[1:], line[pointer_p1])
				pointer_p1++
			}
			_, SoPExists = startOfPacket[lineCounter]
		}

		pointer_p2 := 14
		buffer_p2 := line[0:pointer_p2]
		_, SoSExists := startOfSignal[lineCounter]
		for !SoSExists {
			if len(buffer_p2) == len(dedup(buffer_p2)) {
				// capture pointer, and break out
				startOfSignal[lineCounter] = pointer_p2
				fmt.Println("  Start-of-Signal found after character", startOfSignal[lineCounter])
				break
			} else {
				if pointer_p2 >= len(line) {
					buffer_p2 = buffer_p2[1:]
				} else {
					buffer_p2 = append(buffer_p2[1:], line[pointer_p2])
				}
				pointer_p2++
			}
			_, SoSExists = startOfSignal[lineCounter]
		}
		lineCounter++
	}
}
