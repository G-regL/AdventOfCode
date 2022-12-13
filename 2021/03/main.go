package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

func getRate(bits [][]int, least bool) (ret_s string) {
	ret := []int{}

	for _, b := range bits {
		if least {
			if b[0] < b[1] {
				ret = append(ret, 0)
				ret_s += strconv.Itoa(0)
			} else {
				ret = append(ret, 1)
				ret_s += strconv.Itoa(1)
			}
		} else {
			if b[0] > b[1] {
				ret = append(ret, 0)
				ret_s += strconv.Itoa(0)
			} else {
				ret = append(ret, 1)
				ret_s += strconv.Itoa(1)
			}
		}
	}

	return
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

	bits := make([][]int, len(sfile[1]))

	for _, line := range sfile {
		columns := strings.Split(string(line), "")
		for c, b := range columns {
			if len(bits[c]) <= 2 {
				bits[c] = append(bits[c], 0, 0)
			}
			b_i, _ := strconv.Atoi(b)
			bits[c][b_i]++
		}
	}
	fmt.Println(bits)

	gamma, _ := strconv.ParseInt(getRate(bits, false), 2, 32)
	epsilon, _ := strconv.ParseInt(getRate(bits, true), 2, 32)
	fmt.Println("gamma:", gamma)
	fmt.Println("epsilon:", epsilon)

	fmt.Println("Power Comsumption P1:", gamma*epsilon)
	//fmt.Println("highest scenic score:", highestScenicScore)

	elapsed := time.Since(start)
	fmt.Printf("Took %s\n", elapsed)
}
