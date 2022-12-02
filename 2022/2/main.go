package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	scores_1 := map[string]int{
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

	scores_2 := map[string]int{

		// 1 rock 		A
		// 2 paper		B
		// 3 scisors	C

		// win  6	Z
		// draw 3	Y
		// loss 0	X

		//		   result	them		me
		"A X": 3, //loss 	rock		sisors
		"A Y": 4, //draw	rock		rock
		"A Z": 8, //win		rock		paper

		"B X": 1, //loss	paper		rock
		"B Y": 5, //draw	paper		paper
		"B Z": 9, //win		paper		scisors

		"C X": 2, //loss	scisors		paper
		"C Y": 6, //draw	scisors		scisors
		"C Z": 7, //win		scisors		rock
	}

	f, err := os.Open("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)

	total_1 := 0
	total_2 := 0

	for scanner.Scan() {

		total_1 += scores_1[scanner.Text()]
		total_2 += scores_2[scanner.Text()]

		//fmt.Println(scanner.Text(), scores[scanner.Text()])
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Total for Puzzle #1:", total_1)
	fmt.Println("Total for Puzzle #2:", total_2)
}
