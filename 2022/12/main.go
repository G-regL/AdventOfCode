package main

import (
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/yourbasic/graph"
)

var flag_testData = flag.Bool("test", false, "Use Test dataset")

type point struct {
	x      int
	y      int
	height int
}

func toInt(in string) (out int) {
	out, _ = strconv.Atoi(in)
	return out
}

func getPoint(points []point, x, y int) (out int) {
	for id, p := range points {
		if p.x == x && p.y == y {
			return id
		}
	}
	return

}

func bfsMoves(v, start int) {

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

	// Split the file into the stack definitions, and moves
	lines := strings.Split(sfile, "\n")

	points := []point{}
	startPoint := point{}
	endPoint := point{}
	//lineLength := len(lines[0])
	minSteps := math.MaxInt

	for lineNumber, line := range lines {
		//heightMap = appendmake([]int, len([]rune(l)))
		//chars := strings.Split(line, "\n")
		chars := []rune(line)
		for charNumber, char := range chars {
			points = append(points, point{x: charNumber, y: lineNumber, height: int(char) - 96})
			if char == 'S' {
				points[len(points)-1].height = int('a') - 96
				startPoint = points[len(points)-1]
			} else if char == 'E' {
				points[len(points)-1].height = int('z') - 96
				endPoint = points[len(points)-1]
			}
		}

	}

	//fmt.Println(startPoint, endPoint)
	//fmt.Println(points)

	diffHeightCost := int64(0)
	sameHeightCost := int64(1)

	g := graph.New(len(points))
	//thisCost := int64(0)
	for id, p := range points {

		// point to the right
		right_id := getPoint(points, p.x+1, p.y)
		right_pt := points[right_id]
		if p.y == right_pt.y && !g.Edge(right_id, id) {
			right_diff := right_pt.height - p.height
			if right_diff == 0 {
				g.AddCost(id, right_id, sameHeightCost)
				fmt.Printf("adding %d cost > edge for points %d, %d\n", sameHeightCost, id, right_id)
				//thisCost = sameHeightCost
			} else if right_diff == 1 {
				g.AddCost(id, right_id, diffHeightCost)
				fmt.Printf("adding %d cost > edge for points %d, %d\n", diffHeightCost, id, right_id)
				//thisCost = diffHeightCost
			}
			//  else {
			// 	g.AddCost(id, right_id, int64(right_diff))
			// 	fmt.Printf("adding %d cost > edge for points %d, %d\n", right_diff, id, right_id)
			// }

		}

		left_id := getPoint(points, p.x-1, p.y)
		left_pt := points[left_id]
		if left_pt.y == p.y && !g.Edge(left_id, id) {
			left_diff := left_pt.height - p.height
			if left_diff == 0 {
				g.AddCost(id, left_id, sameHeightCost)
				fmt.Printf("adding %d cost < edge for points %d, %d\n", sameHeightCost, id, left_id)
				//thisCost = sameHeightCost
			} else if left_diff == 1 {
				g.AddCost(id, left_id, diffHeightCost)
				fmt.Printf("adding %d cost < edge for points %d, %d\n", diffHeightCost, id, left_id)
				//thisCost = diffHeightCost
			}
			//  else {
			// 	g.AddCost(id, left_id, int64(left_diff))
			// 	fmt.Printf("adding %d cost < edge for points %d, %d\n", left_diff, id, left_id)
			// }
		}

		up_id := getPoint(points, p.x, p.y-1)
		up_pt := points[up_id]
		if up_pt.y+1 == p.y && !g.Edge(up_id, id) {
			up_diff := up_pt.height - p.height
			if up_diff == 0 {
				g.AddCost(id, up_id, sameHeightCost)
				fmt.Printf("adding %d cost ^ edge for points %d, %d\n", sameHeightCost, id, up_id)
				//thisCost = sameHeightCost
			} else if up_diff == 1 {
				g.AddCost(id, up_id, diffHeightCost)
				fmt.Printf("adding %d cost ^ edge for points %d, %d\n", diffHeightCost, id, up_id)
				//thisCost = diffHeightCost
			}
			//  else {
			// 	g.AddCost(id, left_id, int64(up_diff))
			// 	fmt.Printf("adding %d cost ^ edge for points %d, %d\n", up_diff, id, up_id)
			// }
		}

		var (
			starts []coord
			end    coord
		)
		blah := coord{}

		down_id := getPoint(points, p.x, p.y+1)
		down_pt := points[down_id]
		if down_pt.y-1 == p.y && !g.Edge(down_id, id) {
			down_diff := down_pt.height - p.height
			if down_diff == 0 {
				g.AddCost(id, down_id, sameHeightCost)
				fmt.Printf("adding %d cost v edge for points %d, %d\n", sameHeightCost, id, down_id)
				//thisCost = sameHeightCost
			} else if down_diff == 1 {
				g.AddCost(id, down_id, diffHeightCost)
				fmt.Printf("adding %d cost v edge for points %d, %d\n", diffHeightCost, id, down_id)
				//thisCost = diffHeightCost
			}
			//  else {
			// 	g.AddCost(id, left_id, int64(down_diff))
			// 	fmt.Printf("adding %d cost v edge for points %d, %d\n", down_diff, id, down_id)
			// }
		}
		//fmt.Println(thisCost)
	}

	//fmt.Println(g)

	path, dist := graph.ShortestPath(g, getPoint(points, startPoint.x, startPoint.y), getPoint(points, endPoint.x, endPoint.y))
	fmt.Println("path:", path, "dist:", dist, "path_length:", len(path))

	// dist2 := make([]int, g.Order())
	// graph.BFS(g, 0, func(v, w int, _ int64) {
	// 	fmt.Println(v, "to", w)
	// 	dist2[w] = dist2[v] + 1
	// })
	// fmt.Println("dist2:", dist2, "dist2_length:", len(dist2))

	// Show us what we've got!
	//fmt.Println("Part 1 shortest Path:", inspectedItems_p1[len(inspectedItems_p1)-1]*inspectedItems_p1[len(inspectedItems_p1)-2])
	//fmt.Println("Part 2 Monkey Business:", inspectedItems_p2[len(inspectedItems_p2)-1]*inspectedItems_p2[len(inspectedItems_p2)-2])

	fmt.Println(minSteps)
	fmt.Printf("Took %s\n", time.Since(start))

}
