package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

func MoveCrate(stacks [][]string, src int, dst int) {
	//// take crate off source stack
	crate := stacks[src-1][0]
	stacks[src-1] = stacks[src-1][1:]

	//put it on top of destination stack
	stacks[dst-1] = append([]string{crate}, stacks[dst-1]...)
}

func main() {
	flag.Parse()

	filename := "input.txt"
	columns := []int{1, 5, 9, 13, 17, 21, 25, 29, 33}

	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
		columns = []int{1, 5, 9}
	}

	bfile, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	sfile := string(bfile)
	parts := strings.Split(sfile, "\n\n")

	stackdef := strings.Split(parts[0], "\n")
	stacks := make([][]string, len(columns))
	moves := strings.Split(parts[1], "\n")

	for _, e := range stackdef[:len(stackdef)-1] {
		for i, c := range columns {
			if e[c] != ' ' {
				stacks[i] = append(stacks[i], string(e[c]))
			}
		}
	}

	for _, move := range moves {
		moveparts := strings.Split(move, " ")
		move_cnt, _ := strconv.Atoi(moveparts[1])
		move_src, _ := strconv.Atoi(moveparts[3])
		move_dst, _ := strconv.Atoi(moveparts[5])

		for m := 1; m <= move_cnt; m++ {
			MoveCrate(stacks, move_src, move_dst)
		}
	}

	stacktops_1 := ""

	for _, s := range stacks {
		stacktops_1 += s[0]
	}

	// stacktops_2 := ""

	fmt.Println("\n-----------------------")
	fmt.Println("Stack tops for Puzzle #1:", stacktops_1)
	//fmt.Println("Total for Puzzle #2:", total_2)
}
