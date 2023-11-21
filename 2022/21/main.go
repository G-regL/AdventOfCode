package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

type operation string

const (
	multiply operation = "*"
	devide   operation = "/"
	add      operation = "+"
	subtract operation = "-"
)

type monkey struct {
	name         string
	job          string
	operation    operation
	term1        int
	term2        int
	term1_monkey string
	term2_monkey string
	number       int
	yells        bool
}

func toInt(in string) (out int) {
	out, _ = strconv.Atoi(in)
	return out
}

func solvePart1(monkeys map[string]monkey, solve string) int {
	unsolved := 0

	for _, m := range monkeys {
		if !m.yells {
			unsolved++
		}

	}

	for unsolved > 0 {
		for _, monkey := range monkeys {
			//fmt.Println("monkey", monkey.name)
			if monkey.yells == false {
				if monkeys[monkey.term1_monkey].number != 0 && monkeys[monkey.term2_monkey].number != 0 {
					//fmt.Println(" ", monkey.operation, "on monkeys", monkey.term1_monkey, monkey.term2_monkey)
					switch monkey.operation {
					case "+":
						monkey.number = monkeys[monkey.term1_monkey].number + monkeys[monkey.term2_monkey].number

					case "-":
						monkey.number = monkeys[monkey.term1_monkey].number - monkeys[monkey.term2_monkey].number

					case "*":
						monkey.number = monkeys[monkey.term1_monkey].number * monkeys[monkey.term2_monkey].number

					case "/":
						monkey.number = monkeys[monkey.term1_monkey].number / monkeys[monkey.term2_monkey].number

					}
					//fmt.Println("  monkey.number", monkey.number)
					monkey.yells = true

					monkeys[monkey.name] = monkey

					unsolved--
				}

			}

		}
		//fmt.Println("------------------- Done cycle", cycle, "-------------------")
		//fmt.Println("Unsolved:", unsolved)
		//cycle++
	}

	return monkeys[solve].number
}

func solvePart2(monkeys map[string]monkey) int {
	cycle := 1

	equal := false

	monkeyL_ID := monkeys["root"].term1_monkey
	monkeyR_ID := monkeys["root"].term2_monkey
	fmt.Printf("root monkey tests %s (%d), %s (%d)\n", monkeyL_ID, monkeys[monkeyL_ID].number, monkeyR_ID, monkeys[monkeyR_ID].number)

	delete(monkeys, "root")

	for !equal { //&& cycle < 10

		monkeys2 := map[string]monkey{}
		for k, v := range monkeys {
			monkeys2[k] = v
		}

		left := solvePart1(monkeys2, monkeyL_ID)
		right := solvePart1(monkeys2, monkeyR_ID)

		// 	fmt.Println(monkeys2)
		// 	for _, monkey := range monkeys2 {
		// 		fmt.Println("monkey", monkey.name)
		// 		if monkey.yells == false {
		// 			fmt.Println("  monkeys", monkey.term1_monkey, monkey.term2_monkey)
		// 			if monkeys2[monkey.term1_monkey].number != 0 && monkeys2[monkey.term2_monkey].number != 0 {
		// 				fmt.Println(" ", monkeys2[monkey.term1_monkey].number, monkey.operation, monkeys2[monkey.term2_monkey].number)
		// 				switch monkey.operation {
		// 				case "+":
		// 					monkey.number = monkeys2[monkey.term1_monkey].number + monkeys2[monkey.term2_monkey].number

		// 				case "-":
		// 					monkey.number = monkeys2[monkey.term1_monkey].number - monkeys2[monkey.term2_monkey].number

		// 				case "*":
		// 					monkey.number = monkeys2[monkey.term1_monkey].number * monkeys2[monkey.term2_monkey].number

		// 				case "/":
		// 					monkey.number = monkeys2[monkey.term1_monkey].number / monkeys2[monkey.term2_monkey].number

		// 				}
		// 				fmt.Println("  monkey.number", monkey.number)
		// 				monkey.yells = true

		// 				monkeys2[monkey.name] = monkey
		// 			}

		// 		}
		// 	}

		fmt.Println(monkeys2)
		fmt.Println(left, right)

		if monkeys2[monkeyL_ID].number < monkeys2[monkeyR_ID].number {
			humn := monkeys["humn"]
			humn.number--
			monkeys["humn"] = humn
			fmt.Println("  decrement")
		} else if monkeys2[monkeyL_ID].number > monkeys2[monkeyR_ID].number {
			humn := monkeys["humn"]
			humn.number++
			monkeys["humn"] = humn
			fmt.Println("  increment")
		} else {
			equal = true
			fmt.Println("  equal")
		}
		fmt.Printf("  %d; %s (%d), %s (%d)\n", monkeys["humn"].number, monkeyL_ID, monkeys2[monkeyL_ID].number, monkeyR_ID, monkeys2[monkeyR_ID].number)

		fmt.Println("------------------- Done cycle", cycle, "-------------------")

		cycle++
	}

	//fmt.Println(monkeys["root"])
	return monkeys["humn"].number
}

func main() {
	start := time.Now()
	flag.Parse()

	filename := "input.txt"

	// Detect the --test flag and use sample data it's set
	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
	}

	// Read in file as bytes, and convert to a string.
	bfile, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	sfile := string(bfile)

	monkeys := map[string]monkey{}
	unsolved := 0

	for _, line := range strings.Split(sfile, "\n") {

		thisMonkey := monkey{}
		lineParts := strings.Split(line, ": ")
		thisMonkey.name = lineParts[0]
		thisMonkey.job = lineParts[1]
		monkeyValue, err := strconv.Atoi(thisMonkey.job)
		if err != nil {
			jobParts := strings.Split(thisMonkey.job, " ")
			thisMonkey.term1, _ = strconv.Atoi(jobParts[0])
			thisMonkey.term1_monkey = jobParts[0]
			thisMonkey.term2, _ = strconv.Atoi(jobParts[2])
			thisMonkey.term2_monkey = jobParts[2]
			thisMonkey.operation = operation(jobParts[1])
			thisMonkey.yells = false

			unsolved++
		} else {
			//fmt.Println("converted", monkeyValue)
			thisMonkey.number = monkeyValue
			thisMonkey.yells = true
		}
		monkeys[thisMonkey.name] = thisMonkey
	}

	//fmt.Println(unsolved)

	fmt.Println("Part 1 - root yells:", solvePart1(monkeys, "root"))
	//fmt.Println("Part 2 - humn yells:", solvePart2(monkeys))

	//fmt.Println("Part 2 beacon frequency:", freq_P2)

	fmt.Printf("Took %s\n", time.Since(start))
}
