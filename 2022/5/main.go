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
	//Identify which creates to move
	crate := stacks[src-1][0]
	//... and remove from source stack
	stacks[src-1] = stacks[src-1][1:]

	//Put it on top of destination stack
	stacks[dst-1] = append([]string{crate}, stacks[dst-1]...)
func MoveCrates(stacks [][]string, cnt int, src int, dst int) {
	//Identify which creates to move
	crates := stacks[src-1][0:cnt]
	//... and remove from source stack
	stacks[src-1] = stacks[src-1][cnt:]
	//Put them on top of destination stack
	// crates is resliced here such that its capacity is now equal to its length
	// This guarantees that a new underlying array is always created for stacks9001[dst-1]
	// --found at https://freshman.tech/snippets/go/concatenate-slices/
	stacks[dst-1] = append(crates[:len(crates):len(crates)], stacks[dst-1]...)
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
	stacks_CM9000 := make([][]string, len(columns))
	stacks_CM9001 := make([][]string, len(columns))
	moves := strings.Split(parts[1], "\n")

	for _, e := range stackdef[:len(stackdef)-1] {
		for i, c := range columns {
			if e[c] != ' ' {
				stacks_CM9000[i] = append(stacks_CM9000[i], string(e[c]))
			}
		}
	}
	copy(stacks_CM9001, stacks_CM9000)

	for _, move := range moves {
		moveparts := strings.Split(move, " ")
		move_cnt, _ := strconv.Atoi(moveparts[1])
		move_src, _ := strconv.Atoi(moveparts[3])
		move_dst, _ := strconv.Atoi(moveparts[5])

		for m := 1; m <= move_cnt; m++ {
			MoveCrate(stacks_CM9000, move_src, move_dst)
		}
		MoveCrates(stacks_CM9001, move_cnt, move_src, move_dst)
	}

	stacktops_1 := ""
	stacktops_2 := ""
	for _, s := range stacks_CM9000 {
		stacktops_1 += s[0]
	}
	for _, s := range stacks_CM9001 {
		stacktops_2 += s[0]
	}

	fmt.Println("\n-----------------------")
	fmt.Println("Stack tops for CrateMover 9000:", stacktops_1)
	fmt.Println("Stack tops for CrateMover 9001:", stacktops_2)
}
