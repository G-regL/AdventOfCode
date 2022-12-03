package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// Stolen from https://stackoverflow.com/a/50694373/4483858
func intersection(s1, s2 []string) (inter []string) {
	hash := make(map[string]bool)
	for _, e := range s1 {
		hash[e] = true
	}
	for _, e := range s2 {
		// If elements present in the hashmap then append intersection list.
		if hash[e] {
			inter = append(inter, e)
		}
	}
	//Remove dups from slice.
	inter = removeDups(inter)
	return
}

// Stolen from https://stackoverflow.com/a/50694373/4483858
// Remove dups from slice.
func removeDups(elements []string) (nodups []string) {
	encountered := make(map[string]bool)
	for _, element := range elements {
		if !encountered[element] {
			nodups = append(nodups, element)
			encountered[element] = true
		}
	}
	return
}
func getPriority(item string) (priority int) {
	if int(item[0]) >= 97 {
		priority += int(item[0]) - 96
	} else {
		priority += int(item[0]) - 38
	}
	return
}
func main() {

	f, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)

	total_1 := 0
	total_2 := 0

	var group []string

	for scanner.Scan() {
		rucksack := scanner.Text()
		group = append(group, rucksack)

		compartment_1 := strings.Split(rucksack[len(rucksack)/2:], "")
		compartment_2 := strings.Split(rucksack[:len(rucksack)/2], "")
		common_type := strings.Join(intersection(compartment_1, compartment_2), "")

		//fmt.Println(compartment_1, len(compartment_1), " - ", compartment_2, len(compartment_2))

		//fmt.Println(common_type, int(common_type[0]))

		total_1 += getPriority(common_type)

		if len(group) == 3 {
			badge_1_2 := intersection(strings.Split(group[0], ""), strings.Split(group[1], ""))
			//fmt.Println(badge_1_2)
			badge_group := intersection(badge_1_2, strings.Split(group[2], ""))
			//fmt.Println(badge_group)
			total_2 += getPriority(badge_group[0])
			group = nil
		}

	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Total for Puzzle #1:", total_1)
	fmt.Println("Total for Puzzle #2:", total_2)
}
