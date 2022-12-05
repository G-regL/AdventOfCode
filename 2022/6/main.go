package main

import (
	"flag"
	"fmt"
	"log"
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

	// Read in file as bytes, and convert to a string.
	bfile, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	sfile := string(bfile)

	// Split the file into the stack definitions, and moves
	parts := strings.Split(sfile, "\n\n")

	stacktops_1 := ""
	stacktops_2 := ""

	// Show us what we've got!
	fmt.Println("\n-----------------------")
	fmt.Println("Stack tops for CrateMover 9000:", stacktops_1)
	fmt.Println("Stack tops for CrateMover 9001:", stacktops_2)
}
