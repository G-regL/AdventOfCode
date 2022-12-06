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

// moves a single create from one stack to another
func MoveCrate(stacks [][]string, src int, dst int) {
	//Identify which creates to move
	crate := stacks[src-1][0]
	//... and remove from source stack
	stacks[src-1] = stacks[src-1][1:]

	//Put it on top of destination stack
	stacks[dst-1] = append([]string{crate}, stacks[dst-1]...)
}

// moves a number of crates from one stack to another in one move; preserves order
func MoveCrates(stacks [][]string, cnt int, src int, dst int) {
	//Identify which creates to move
	crates := stacks[src-1][0:cnt]
	//... and remove from source stack
	stacks[src-1] = stacks[src-1][cnt:]

	//Put them on top of destination stack
	// 'crates' is resliced here such that its capacity is now equal to its length
	// This guarantees that a new underlying array is always created for 'stacks9001[dst-1]'
	// --found at https://freshman.tech/snippets/go/concatenate-slices/
	stacks[dst-1] = append(crates[:len(crates):len(crates)], stacks[dst-1]...)
}

func main() {
	flag.Parse()

	filename := "input.txt"
	// define which text columns in the file represent stacks
	columns := []int{1, 5, 9, 13, 17, 21, 25, 29, 33}

	// Detect the --test flag and use test data if needed
	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
		columns = []int{1, 5, 9}
	}

	// Read in file as bytes, and convert to a string.
	bfile, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	sfile := string(bfile)

	// Split the file into the stack definitions, and moves
	parts := strings.Split(sfile, "\n\n")

	// split the stack definition into lines, and initalize the stacks for each crane type
	stackdef := strings.Split(parts[0], "\n")
	stacks_CM9000 := make([][]string, len(columns))
	stacks_CM9001 := make([][]string, len(columns))
	// initialize the move slice
	moves := strings.Split(parts[1], "\n")

	// build the stack slices
	for _, e := range stackdef[:len(stackdef)-1] {
		for i, c := range columns {
			if e[c] != ' ' {
				stacks_CM9000[i] = append(stacks_CM9000[i], string(e[c]))
			}
		}
	}
	copy(stacks_CM9001, stacks_CM9000)

	// Loop through the moves
	for _, move := range moves {
		// Break each move into it's key parts
		moveparts := strings.Split(move, " ")
		move_cnt, _ := strconv.Atoi(moveparts[1])
		move_src, _ := strconv.Atoi(moveparts[3])
		move_dst, _ := strconv.Atoi(moveparts[5])

		// The CM9000 (part 1) can only do one create at a time, so do move each create individiually
		for m := 1; m <= move_cnt; m++ {
			MoveCrate(stacks_CM9000, move_src, move_dst)
		}

		// The CM9001 can pick up many crates, so we only have to do it once per move
		MoveCrates(stacks_CM9001, move_cnt, move_src, move_dst)
	}

	// Build slices of top crates from each stack
	stacktops_1 := ""
	stacktops_2 := ""
	for _, s := range stacks_CM9000 {
		stacktops_1 += s[0]
	}
	for _, s := range stacks_CM9001 {
		stacktops_2 += s[0]
	}

	// Show us what we've got!
	fmt.Println("\n-----------------------")
	fmt.Println("Stack tops for CrateMover 9000:", stacktops_1)
	fmt.Println("Stack tops for CrateMover 9001:", stacktops_2)
}
