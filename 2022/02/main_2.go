package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	scores := map[string]int{

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
