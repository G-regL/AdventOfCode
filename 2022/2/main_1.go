package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	scores := map[string]int{

		// 1 rock 		A	X
		// 2 paper		B	Y
		// 3 scisors	C	Z

		// win  6
		// draw 3
		// loss 0

		//		  them		me
		"A X": 4, //rock	rock
		"A Y": 8, //rock	paper
		"A Z": 3, //rock	scisors

		"B X": 1, //paper	rock
		"B Y": 5, //paper	paper
		"B Z": 9, //paper	scisors

		"C X": 7, //scisors	rock
		"C Y": 2, //scisors	paper
		"C Z": 6, //scisors	scisors
	}

	f, err := os.Open("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)

	total := 0

	for scanner.Scan() {

		total += scores[scanner.Text()]

		//fmt.Println(scanner.Text(), scores[scanner.Text()])
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Println(total)
}
