package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

func toint(str string) (retint int) {
	retint, _ = strconv.Atoi(str)
	return
}
func main() {
	flag.Parse()

	filename := "input.txt"

	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
	}

	f, err := os.Open(filename)

	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)

	total_1 := 0
	total_2 := 0

	for scanner.Scan() {
		pair := strings.Split(scanner.Text(), ",")
		e1, e2 := strings.Split(pair[0], "-"), strings.Split(pair[1], "-")

		//fmt.Println(e1, e2, toint(e1[0]) <= toint(e2[0]) && toint(e1[1]) >= toint(e2[1])) || (toint(e2[0]) <= toint(e1[0]) && toint(e2[1]) >= toint(e1[1]))
		if (toint(e1[0]) <= toint(e2[0]) && toint(e1[1]) >= toint(e2[1])) || (toint(e2[0]) <= toint(e1[0]) && toint(e2[1]) >= toint(e1[1])) {
			total_1++
		}

		//fmt.Println(e1, e2, toint(e1[1]) >= toint(e2[0]) && toint(e1[0]) <= toint(e2[1]))
		if toint(e1[1]) >= toint(e2[0]) && toint(e1[0]) <= toint(e2[1]) {
			total_2++
		}

	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Total for Puzzle #1:", total_1)
	fmt.Println("Total for Puzzle #2:", total_2)
}
