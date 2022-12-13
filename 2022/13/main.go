package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
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

func breakUpLine(search string) (matches []string) {
	re := regexp.MustCompile(`,\[([^\[\]]+)\]`)
	search = "[1,[2,[3,[4,[5,6,7]]]],8,9]"

	//matches := []string{}
	match := re.FindString(search)

	replacer := strings.NewReplacer(",[", "", "[", "", "]", "")
	//myString = replacer.Replace(myString)

	for match != "" {

		//fmt.Printf("%q\n", match)
		matches = append(matches, replacer.Replace(match))

		search = strings.Replace(search, match, "", 3)
		//fmt.Printf("%q\n", search)

		match = re.FindString(search)

		//matches = append(matches, match)
		//fmt.Printf("%q\n", match)

		//search = strings.Replace(search, match, "", 3)
		//fmt.Printf("%q\n", search)

	}

	//matches = append(matches, replacer.Replace(match))

	matches = append(matches, replacer.Replace(search))
	//fmt.Printf("%q\n", search)
	//fmt.Printf("%q\n", matches)
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

	// Read in file as bytes, and convert to a string.
	bfile, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	sfile := string(bfile)

	pairs := [][]any{}
	for _, line := range strings.Split(sfile, "\n") {
		if line == "" {
			continue
		}
		//fmt.Println("line", line)
		var pair []any
		json.Unmarshal([]byte(line), &pair)
		fmt.Println(pair)
		pairs = append(pairs, pair)
	}

	//fmt.Println(pairs[0])
	fmt.Println(pairs)

	// Show us what we've got!
	//fmt.Println("Part 1 Monkey Business:", inspectedItems_p1[len(inspectedItems_p1)-1]*inspectedItems_p1[len(inspectedItems_p1)-2])

	fmt.Printf("Took %s\n", time.Since(start))

}
