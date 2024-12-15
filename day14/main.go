package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var (
	testFile = "day14/test/input.txt"
	// rowMax   = 11
	// colMax   = 7
	rowMax = 101
	colMax = 103
)

type Robot struct {
	Row     int
	Col     int
	RowDiff int
	ColDiff int
}

func (r *Robot) next() {
	r.Row = (r.Row + r.RowDiff) % rowMax
	r.Col = (r.Col + r.ColDiff) % colMax
	if r.Row < 0 {
		r.Row += rowMax
	}
	if r.Col < 0 {
		r.Col += colMax
	}
}

func parseData(file string) []*Robot {
	robots := []*Robot{}
	data, err := os.ReadFile(file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}
	lines := strings.Split(strings.TrimSpace(string(data)), "\n")
	for _, line := range lines {
		robotData := strings.Split(line, " ")
		pos := strings.Split(robotData[0][2:], ",")
		vel := strings.Split(robotData[1][2:], ",")
		row, rowErr := strconv.Atoi(pos[0])
		if rowErr != nil {
			panic(rowErr)
		}
		col, colErr := strconv.Atoi(pos[1])
		if colErr != nil {
			panic(colErr)
		}
		rowDiff, rowDiffErr := strconv.Atoi(vel[0])
		if rowDiffErr != nil {
			panic(rowDiffErr)
		}
		colDiff, colDiffErr := strconv.Atoi(vel[1])
		if colDiffErr != nil {
			panic(colDiffErr)
		}

		robot := &Robot{
			Row:     row,
			Col:     col,
			RowDiff: rowDiff,
			ColDiff: colDiff,
		}
		robots = append(robots, robot)
	}

	return robots
}

func safetyFactor(robots []*Robot) int {
	rowMid := rowMax / 2
	colMid := colMax / 2
	q1Robots := []*Robot{}
	q2Robots := []*Robot{}
	q3Robots := []*Robot{}
	q4Robots := []*Robot{}
	for _, robot := range robots {
		if robot.Row < rowMid && robot.Col < colMid {
			q1Robots = append(q1Robots, robot)
		} else if robot.Row > rowMid && robot.Col < colMid {
			q2Robots = append(q2Robots, robot)
		} else if robot.Row < rowMid && robot.Col > colMid {
			q3Robots = append(q3Robots, robot)
		} else if robot.Row > rowMid && robot.Col > colMid {
			q4Robots = append(q4Robots, robot)
		}
	}

	return len(q1Robots) * len(q2Robots) * len(q3Robots) * len(q4Robots)
}

func printGrid(g [][]int) {
	for y := range g[0] {
		for x := range g {
			fmt.Printf("%d", g[x][y])
		}
		fmt.Printf("\n")
	}
}

func part1() int {
	robots := parseData(testFile)
	for range 100 {
		for _, robot := range robots {
			robot.next()
		}
	}
	grid := make([][]int, rowMax)
	for i := range grid {
		grid[i] = make([]int, colMax)
	}
	for _, robot := range robots {
		grid[robot.Row][robot.Col]++
	}
	// printGrid(grid)

	return safetyFactor(robots)
}

func part2() int {
	robots := parseData(testFile)
	reader := bufio.NewReader(os.Stdin)
	count := 0
	for {
		count++
		grid := make([][]int, rowMax)
		for i := range grid {
			grid[i] = make([]int, colMax)
		}
		for _, robot := range robots {
			grid[robot.Row][robot.Col]++
		}
		inARow := 0
		inARowMax := 0
		for x := range grid {
			for y := range grid[0] {
				if grid[x][y] == 1 {
					inARow++
				} else {
					inARowMax = max(inARow, inARowMax)
					inARow = 0
				}
			}
		}
		if inARowMax > 5 {
			printGrid(grid)
			fmt.Printf("Enter for next iter (%d): ", count)
			input, _ := reader.ReadString('\n')
			input = strings.TrimSpace(input)
			if input == "q" {
				break
			}
		}
		for _, robot := range robots {
			robot.next()
		}
	}

	return safetyFactor(robots)
}

func main() {
	fmt.Printf("Part 1: %d\n", part1())
	fmt.Printf("Part 2: %d\n", part2())
}
