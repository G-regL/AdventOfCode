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

	//instructions := []Instruction{}
	stack := []Operation{}

	cycle := 0
	for _, line := range sfile {
		value := 0
		instruction := ""
		_, _ = fmt.Sscanf(line, "%s %d", &instruction, &value)
		//instructions = append(instructions, Instruction{operation: ins, amount: value})
		thisins := Instruction{operation: instruction, amount: value}
		if thisins.operation == "addx" {
			stack = append(stack, Operation{ins: thisins, cycle: cycle + 2})
			cycle++
		} else {
			stack = append(stack, Operation{ins: thisins, cycle: cycle + 1})
		}
		cycle++

	}
	//fmt.Println(instructions)

	fmt.Println(stack)

	breakPoints := map[int]int{20: 0, 60: 0, 100: 0, 140: 0, 180: 0, 220: 0}
	register := 1
	cycle_run := 0
	for len(stack) > 0 {
		fmt.Println("c:", cycle_run, " start; register:", register)
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

		fmt.Println("c:", cycle_run, " end; register:", register)
		cycle_run++
	}

	fmt.Println("breakPoint:", breakPoints)

	sum := 0
	for b, s := range breakPoints {
		sum += b * s

		fmt.Println("breakPoint:", b, s, b*s)
	}
	fmt.Println("sum:", sum)

	//fmt.Println("Visible Trees:", visible)
	//fmt.Println("highest scenic score:", highestScenicScore)

	elapsed := time.Since(start)
	fmt.Printf("Took %s\n", elapsed)
}
