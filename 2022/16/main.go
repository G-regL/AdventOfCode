package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/yourbasic/graph"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

type valve struct {
	name      string
	rate      int
	connected []string
}

func toInt(in string) (out int) {
	out, _ = strconv.Atoi(in)
	return out
}

func getValveByName(valves []valve, search string) (out int) {
	for out, v := range valves {
		if v.name == search {
			return out
		}
	}

	return -1
}

func getValveByRate(valves []valve, search int) (out int) {
	for out, v := range valves {
		if v.rate == search {
			return out
		}
	}

	return -1
}

func min(a, b int) (min int) {
	if a < b {
		return a
	}
	return b
}

func RemoveIndex(s []int, index int) []int {
	return append(s[:index], s[index+1:]...)
}

func contains(elems []int, search int) bool {
	for _, item := range elems {
		if item == search {
			return true
		}
	}
	return false
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

	valves := map[string]valve{}
	valves_s := []valve{}

	scanner := regexp.MustCompile(`^Valve ([A-Z][A-Z]) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z, ]+)$`)

	paths := []map[string]string{}

	rates := []int{}

	for _, line := range strings.Split(sfile, "\n") {

		matches := scanner.FindAllStringSubmatch(line, 1)

		connected := strings.Split(matches[0][3], ", ")
		rate := toInt(matches[0][2])
		valveName := matches[0][1]
		valves[valveName] = valve{name: valveName, rate: rate, connected: connected}
		valves_s = append(valves_s, valve{name: valveName, rate: rate, connected: connected})

		if rate > 0 {
			rates = append(rates, rate)
		}

		for _, cv := range connected {
			paths = append(paths, map[string]string{valveName: cv})
		}
	}

	for i, v := range valves_s {
		fmt.Printf("id:%2d {name:%2s rate:%2d con:%v}\n", i, v.name, v.rate, v.connected)
	}
	fmt.Println("--")
	sort.Sort(sort.Reverse(sort.IntSlice(rates)))

	g := graph.New(len(paths))

	for id, v := range valves_s {
		for _, c := range v.connected {
			g.Add(id, getValveByName(valves_s, c))
			//fmt.Println("adding", id, getValveByName(valves_s, c))
		}
	}

	current := 0
	next := valve{}
	min := 0
	visited := []int{current}
	for minute := 0; minute < 30; {
		path := []int{}
		for _, r := range rates {
			if contains(visited, getValveByRate(valves_s, r)) {
				continue
			}
			path, _ = graph.ShortestPath(g, current, getValveByRate(valves_s, r))
			//fmt.Println("path:", path, "len:", len(path), "dist:", dist)
			if min == 0 {
				min = len(path)
			}
			//fmt.Println("min check", len(path) <= min, ";rate check", valves_s[current].rate < valves_s[getValveByRate(valves_s, r)].rate)
			if len(path) <= min && valves_s[current].rate < valves_s[getValveByRate(valves_s, r)].rate {
				next = valves_s[getValveByRate(valves_s, r)]

				break
			}
		}

		fmt.Println("next:", next, path)

		minute += len(path)
		current = getValveByName(valves_s, next.name)
		visited = append(visited, current)
		fmt.Println("minute:", minute, "current:", current)
	}

	//path, dist := graph.ShortestPath(g, 0, getValveByName(valves_s, "NQ"))
	//fmt.Println("path:", path, "length:", dist)

	totalP1 := 0

	// ------------ end borrowed

	fmt.Println("Part 1 Pressure released:", totalP1)

	fmt.Printf("Took %s\n", time.Since(start))
}
