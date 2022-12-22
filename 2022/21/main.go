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

	//cycle := 1

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

	fmt.Println("Part 1 - root yells:", monkeys["root"].number)
	//fmt.Println("Part 2 beacon frequency:", freq_P2)

	fmt.Printf("Took %s\n", time.Since(start))
}
