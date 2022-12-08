package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

func main() {

	flag.Parse()
	filename := "input.txt"

	// Detect the --test flag and use test data if needed
	if *flag_testData {
		fmt.Println("***** USING TEST DATA *****")
		filename = "test.txt"
	}

	// Open file for reading
	f, _ := os.Open(filename)
	defer f.Close()

	scanner := bufio.NewScanner(f)

	structure := map[string]int{}
	currentWorkingDir := []string{}
	for scanner.Scan() {
		line := string(scanner.Text())

		if strings.HasPrefix(line, "$ cd") {
			// command (cd/ls)
			newdir := ""
			_, _ = fmt.Sscanf(line, "$ cd %s", &newdir)

			if newdir == ".." {
				currentWorkingDir = currentWorkingDir[:len(currentWorkingDir)-1]
			} else {
				currentWorkingDir = append(currentWorkingDir, newdir)
			}

		} else {
			//listing
			if strings.HasPrefix(line, "dir") {
				dir := ""
				_, _ = fmt.Sscanf(line, "dir %s", &dir)

				dirpath := strings.Join(append(currentWorkingDir, dir), "/")

				if _, ok := structure[dirpath]; !ok {
					structure[dirpath] = 0
				}
			} else {
				size := 0
				file := ""
				_, _ = fmt.Sscanf(line, "%d %s", &size, &file)
				for i := len(currentWorkingDir); i != 0; i-- {
					structure[strings.Join(currentWorkingDir[:i], "/")] += size
				}

			}
		}
	}

	sumP1 := 0
	for _, v := range structure {
		//fmt.Println(k, v)
		if v <= 100000 {
			sumP1 += v
		}
	}

	fmt.Println("Part 1 sum:", sumP1)
	//fmt.Println("Free Space:", 70000000-structure["/"])
	//fmt.Println("Needed Space:", 30000000-(70000000-structure["/"]))

	delete := 30000000
	for _, v := range structure {
		//fmt.Println(k, v)
		if v >= 30000000-(70000000-structure["/"]) && v <= delete {
			delete = v
		}
	}
	fmt.Println("Part 2 directory size:", delete)

}
