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

	startOfPacket := 0

	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "")
		buffer := line[0:4]
		pointer := 4

		fmt.Printf("Line starting with '%s...'\n", strings.Join(line[:20], ""))
		for {
			if pointer >= len(line) {
				fmt.Println("No Start-of-Packet found :(")
				break
			}
			//fmt.Println("buffer:", buffer)
			// check if buffer contains unique chars
			chars := make(map[string]bool)
			list := []string{}
			for _, c := range buffer {
				if _, value := chars[c]; !value {
					chars[c] = true
					list = append(list, c)
				}
			}
			//fmt.Println("list:  ", list)

			if len(buffer) == len(list) {
				startOfPacket = pointer
				fmt.Println("  Start-of-Packet found after character", startOfPacket)
				break
			} else {
				//update buffer with a new char
				//fmt.Println(pointer, len(line), pointer >= len(line))
				// if pointer > len(line) {
				// 	fmt.Println("No Start-of-Packet found :(")
				// 	break
				// } else {
				buffer = append(buffer[1:], line[pointer])
				pointer++
				//}
			}
		}
	}
	//stacktops_2 := ""

	// Show us what we've got!
	//fmt.Println("\n-----------------------")
	//fmt.Println("Start-of-Packet found after character:", startOfPacket)
	//fmt.Println("Stack tops for CrateMover 9001:", stacktops_2)
}
