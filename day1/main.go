package main

import (
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

func parseData(data []byte) ([]int, []int) {
	stringList := strings.Split(string(data), "\n")
	var l1 []int
	var l2 []int

	for _, line := range stringList {
		if line == "" {
			continue
		}
		stringLine := strings.Split(line, "   ")
		i1, err := strconv.Atoi(stringLine[0])
		if err != nil {
			panic(err)
		}
		i2, err := strconv.Atoi(stringLine[1])
		if err != nil {
			panic(err)
		}
		l1 = append(l1, i1)
		l2 = append(l2, i2)
	}

	return l1, l2
}

func part1(input1, input2 []int) int {
	slices.SortFunc(input1, func(a, b int) int {
		if a > b {
			return 1
		}
		if b > a {
			return -1
		}
		return 0
	})
	slices.SortFunc(input2, func(a, b int) int {
		if a > b {
			return 1
		}
		if b > a {
			return -1
		}
		return 0
	})

	sum := 0.0
	for i := range input1 {
		sum += math.Abs(float64(input1[i] - input2[i]))
	}
	return int(sum)
}

func count(l []int, t int) int {
	count := 0
	for _, v := range l {
		if t == v {
			count++
		}
	}
	return count
}

func part2(input1, input2 []int) int {
	sum := 0
	for _, v := range input1 {
		sum += v * count(input2, v)
	}
	return int(sum)
}
func main() {
	data, err := os.ReadFile("day1/test/input.txt")
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}
	input1, input2 := parseData(data)

	fmt.Printf("Part 1: %v\n", part1(input1, input2))
	fmt.Printf("Part 2: %v\n", part2(input1, input2))
}
