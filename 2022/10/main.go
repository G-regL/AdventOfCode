package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

type Instruction struct {
	operation string
	amount    int
}
type Operation struct {
	ins   Instruction
	cycle int
}

func main() {
	start := time.Now()

	flag.Parse()
	filename := "input.txt"

	// Detect the --test flag and use test data if needed
	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
	}

	// Open file for reading
	bfile, _ := os.ReadFile(filename)

	sfile := strings.Split(string(bfile), "\n")

	stack := []Operation{}

	cycle := 0
	for _, line := range sfile {
		value := 0
		instruction := ""
		_, _ = fmt.Sscanf(line, "%s %d", &instruction, &value)
		thisins := Instruction{operation: instruction, amount: value}
		if thisins.operation == "addx" {
			stack = append(stack, Operation{ins: thisins, cycle: cycle + 2})
			cycle++
		} else {
			stack = append(stack, Operation{ins: thisins, cycle: cycle + 1})
		}
		cycle++

	}

	breakPoints := map[int]int{20: 0, 60: 0, 100: 0, 140: 0, 180: 0, 220: 0}
	register := 1
	cycle_run := 0
	pixels := [][]string{}
	crtBreaks := map[int]bool{1: true, 41: true, 81: true, 121: true, 161: true, 201: true}
	crtLine := 0
	linepos := 0

	pixels = append(pixels, []string{})
	for len(stack) > 0 {
		if _, ok := crtBreaks[cycle_run+1]; ok {
			linepos = 0
			pixels = append(pixels, []string{})
			crtLine++
		}

		this := stack[0]
		if _, ok := breakPoints[cycle_run]; ok {
			breakPoints[cycle_run] = register
		}

		if this.cycle == cycle_run {
			if this.ins.operation == "addx" {
				register += this.ins.amount
			}

			stack = stack[1:]
		}
		if register-1 == linepos || register == linepos || register+1 == linepos {
			pixels[crtLine] = append(pixels[crtLine], "#")
		} else {
			pixels[crtLine] = append(pixels[crtLine], ".")
		}

		cycle_run++
		linepos++
	}

	sum := 0
	for b, s := range breakPoints {
		sum += b * s
	}
	fmt.Println("Part 1 Sum:", sum)
	fmt.Printf("Part 2 CRT output:")
	for _, r := range pixels {
		for _, p := range r {
			fmt.Printf("%s", p)
		}
		fmt.Printf("\n")
	}

	fmt.Printf("Took %s\n", time.Since(start))
}
