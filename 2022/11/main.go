package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

type Monkey struct {
	items       []int
	opType      string
	opNumber    int
	testDivisor int
	destTrue    int
	destFalse   int
}

func toInt(in string) (out int) {
	out, _ = strconv.Atoi(in)
	return out
}

func showMonkeys(monkeys []Monkey) {
	for mID, m := range monkeys {
		fmt.Printf("Monkey %d:\n", mID)
		fmt.Printf("  Starting items: %d:\n", m.items)
		if m.opNumber == -1 {
			fmt.Printf("  Operation: new = old %s old:\n", m.opType)
		} else {
			fmt.Printf("  Operation: new = old %s %d:\n", m.opType, m.opNumber)
		}
		fmt.Printf("  Test: divisible by %d:\n", m.testDivisor)
		fmt.Printf("    If true: throw to monkey %d:\n", m.destTrue)
		fmt.Printf("    If false: throw to monkey %d:\n\n", m.destFalse)
	}
}

func updateWorryLevel(m Monkey, item int) (wl int, text string) {
	n := m.opNumber
	if n == -1 {
		n = item
	}

	if m.opType == "*" {
		wl = item * n
		text = fmt.Sprintf("    Worry level is multiplied by %d to %d.", n, wl)
	} else if m.opType == "+" {
		wl = item + n
		text = fmt.Sprintf("    Worry level increases  by %d to %d.", n, wl)
	} else {
		log.Fatal("Unknown operator", m.opType, "in updateWorryLevel")
		os.Exit(1)
	}
	return
}

// ----------- Taken from https://siongui.github.io/2017/06/03/go-find-lcm-by-gcd/
// greatest common divisor (GCD) via Euclidean algorithm
func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

// find Least Common Multiple (LCM) via GCD
func LCM(a, b int, integers ...int) int {
	result := a * b / GCD(a, b)

	for i := 0; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}

// -----------

func main() {
	start := time.Now()
	flag.Parse()

	filename := "input.txt"

	// Detect the --test flag and use test data if needed
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

	// Split the file into the stack definitions, and moves
	inputMonkeys := strings.Split(sfile, "\n\n")

	Monkeys := make([]Monkey, len(inputMonkeys))
	Monkeys_p2 := make([]Monkey, len(inputMonkeys))
	divisors := make([]int, len(inputMonkeys))
	foobar := 1

	for num, m := range inputMonkeys {
		props := strings.Split(m, "\n")
		mID := 0

		//fmt.Println(props)
		_, _ = fmt.Sscanf(props[0], "Monkey %d:", &mID)

		items := strings.Split(props[1], ": ")
		//_, _ = fmt.Sscanf(props[1], "  Starting items: %s", &items)
		//fmt.Println(items)
		for _, i := range strings.Split(items[1], ", ") {
			Monkeys[num].items = append(Monkeys[num].items, toInt(i))
		}

		opNumber := ""
		_, _ = fmt.Sscanf(props[2], "  Operation: new = old %s %s", &Monkeys[num].opType, &opNumber)
		if opNumber == "old" {
			Monkeys[num].opNumber = -1
		} else {
			Monkeys[num].opNumber = toInt(opNumber)
		}

		_, _ = fmt.Sscanf(props[3], "  Test: divisible by %d", &Monkeys[num].testDivisor)
		divisors[num] = Monkeys[num].testDivisor
		foobar *= Monkeys[num].testDivisor

		_, _ = fmt.Sscanf(props[4], "    If true: throw to monkey %d", &Monkeys[num].destTrue)
		_, _ = fmt.Sscanf(props[5], "    If false: throw to monkey %d", &Monkeys[num].destFalse)

	}

	//showMonkeys(Monkeys)

	copy(Monkeys_p2, Monkeys)

	inspectedItems_p1 := make([]int, len(inputMonkeys))

	for round_p1 := 1; round_p1 <= 20; round_p1++ {
		//fmt.Printf("----- Round Part 1 - %2d -----\n", round_p1)

		for mID, Monkey := range Monkeys {
			inspectedItems_p1[mID] += len(Monkey.items)
			//fmt.Printf("Monkey %d:\n", mID)
			for _, Item := range Monkey.items {
				//fmt.Printf("  Monkey inspects an item with a worry level of %d. \n", Item)

				worryLevel, _ := updateWorryLevel(Monkey, Item)
				//worryLevel, wlText := updateWorryLevel(Monkey, Item)
				//fmt.Println(wlText)

				worryLevel = worryLevel / 3
				//fmt.Printf("    Monkey gets bored with item. Worry level is divided by 3 to %d.\n", worryLevel)

				//remainder := worryLevel % 23
				if worryLevel%Monkey.testDivisor == 0 {
					//fmt.Printf("    Current worry level is divisible by %d.\n", Monkey.testDivisor)
					//fmt.Printf("    Item with worry level %d is thrown to monkey %d.\n", worryLevel, Monkey.destTrue)
					Monkeys[Monkey.destTrue].items = append(Monkeys[Monkey.destTrue].items, worryLevel)
				} else {
					//fmt.Printf("    Current worry level is not divisible by %d.\n", Monkey.testDivisor)
					//fmt.Printf("    Item with worry level %d is thrown to monkey %d.\n", worryLevel, Monkey.destFalse)
					Monkeys[Monkey.destFalse].items = append(Monkeys[Monkey.destFalse].items, worryLevel)
				}

				Monkeys[mID].items = Monkeys[mID].items[1:]
			}
			// WORK OUT WHY IT WON'T REMOVE OLD ITEMS FROM THE LIST
			//Monkey.items = []int{}
		}

		// for mID, Monkey := range Monkeys {
		// 	fmt.Printf("Monkey %d: %d\n", mID, Monkey.items)
		// }
		// if round_p1 == 1 || round_p1 == 20 {
		// 	fmt.Printf("----- Round Part 1 - %2d -----\n", round_p1)
		// 	for mID, count := range inspectedItems_p1 {
		// 		fmt.Printf("Monkey %d inspected items %d times.\n", mID, count)
		// 	}
		// }
	}

	//fmt.Println("\n-----------------------")

	// There was *no* way I was going to get this without reading this reddit post:
	// https://www.reddit.com/r/adventofcode/comments/ziyd5u/comment/iztfur8/?utm_source=share&utm_medium=web2x&context=3
	// That led me to https://siongui.github.io/2017/06/03/go-find-lcm-by-gcd/
	// Which then gave me the the below line, and the "LCM" it calls as the new worryLevel reducer
	lcm := LCM(divisors[0], divisors[1], divisors[2:]...)
	// could also get this by '*='-ing each divisor when building the Monkeys slice - a la 'foobar' var above

	inspectedItems_p2 := make([]int, len(inputMonkeys))
	for round_p2 := 1; round_p2 <= 10000; round_p2++ {
		for mID, Monkey := range Monkeys_p2 {
			inspectedItems_p2[mID] += len(Monkey.items)
			for _, Item := range Monkey.items {

				worryLevel, _ := updateWorryLevel(Monkey, Item)
				//worryLevel, wlText := updateWorryLevel(Monkey, Item)
				//fmt.Println(wlText)

				worryLevel = worryLevel % lcm

				if worryLevel%Monkey.testDivisor == 0 {
					Monkeys_p2[Monkey.destTrue].items = append(Monkeys_p2[Monkey.destTrue].items, worryLevel)
				} else {
					Monkeys_p2[Monkey.destFalse].items = append(Monkeys_p2[Monkey.destFalse].items, worryLevel)
				}

				Monkeys_p2[mID].items = Monkeys_p2[mID].items[1:]
			}
		}
		// if round_p2 == 1 || round_p2 == 20 || round_p2%1000 == 0 {
		// 	fmt.Printf("----- Round Part 2 - %2d -----\n", round_p2)
		// 	for mID, count := range inspectedItems_p2 {
		// 		fmt.Printf("Monkey %d inspected items %d times.\n", mID, count)
		// 		//fmt.Println("items:", Monkeys_p2[mID].items)
		// 	}
		// }
	}

	sort.Ints(inspectedItems_p1)
	sort.Ints(inspectedItems_p2)

	// Show us what we've got!
	fmt.Println("Part 1 Monkey Business:", inspectedItems_p1[len(inspectedItems_p1)-1]*inspectedItems_p1[len(inspectedItems_p1)-2])
	fmt.Println("Part 2 Monkey Business:", inspectedItems_p2[len(inspectedItems_p2)-1]*inspectedItems_p2[len(inspectedItems_p2)-2])

	fmt.Printf("Took %s\n", time.Since(start))

}
