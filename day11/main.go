package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"

	"aoc2024/internal/aocutil"
)

var (
	testFile     = "day11/test/input.txt"
	stoneToCount = map[string]int{}
)

func parseData(file string) []int {
	data, err := os.ReadFile(file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}
	dataS := strings.TrimSpace(string(data))

	numsS := strings.Split(string(dataS), " ")
	nums := []int{}
	for _, numS := range numsS {
		num, err := strconv.Atoi(numS)
		if err != nil {
			panic(err)
		}
		nums = append(nums, num)
	}
	return nums
}

func parseDataV2(file string) *aocutil.LinkedList {
	data, err := os.ReadFile(file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}
	dataS := strings.TrimSpace(string(data))

	numsS := strings.Split(string(dataS), " ")
	nums := aocutil.NewLinkedList()
	for _, numS := range numsS {
		num, err := strconv.Atoi(numS)
		if err != nil {
			panic(err)
		}
		nums.Append(num)
	}
	return &nums
}

func blinkV2(data *aocutil.LinkedList, seen map[int][]int) {
	cur := data.Head
	for range data.Length() {
		val := cur.Value
		if val == 0 {
			cur.Value = 1
		} else if aocutil.IsEven(aocutil.LenOfInt(val)) {
			if mem := seen[val]; len(mem) == 2 {
				cur.Value = mem[0]
				data.Append(mem[1])
			} else {
				s := strconv.Itoa(val)
				firstHalf, err := strconv.Atoi(s[:len(s)/2])
				if err != nil {
					panic(err)
				}
				secondHalf, err := strconv.Atoi(s[len(s)/2:])
				if err != nil {
					panic(err)
				}
				cur.Value = firstHalf
				data.Append(secondHalf)
				seen[val] = []int{firstHalf, secondHalf}
			}
		} else {
			cur.Value = val * 2024
		}
		cur = cur.Next
	}
}

func blink(data []int) []int {
	for i, val := range data {
		if val == 0 {
			data[i] = 1
		} else if aocutil.IsEven(aocutil.LenOfInt(val)) {
			s := strconv.Itoa(val)
			firstHalf, err := strconv.Atoi(s[:len(s)/2])
			if err != nil {
				panic(err)
			}
			secondHalf, err := strconv.Atoi(s[len(s)/2:])
			if err != nil {
				panic(err)
			}
			data[i] = firstHalf
			data = append(data, secondHalf)
		} else {
			data[i] = val * 2024
		}
	}
	return data
}

func insert(data []int, index, newVal int) []int {
	newData := []int{}
	if index == len(data) {
		data = append(data, newVal)
		return data
	}

	for i, val := range data {
		if i == index {
			newData = append(newData, newVal)
		}
		newData = append(newData, val)
	}

	return newData
}

func blinkSingleStone(stone int) (int, int) {
	if stone == 0 {
		return 1, -1
	} else if aocutil.IsEven(aocutil.LenOfInt(stone)) {
		s := strconv.Itoa(stone)
		firstHalf, err := strconv.Atoi(s[:len(s)/2])
		if err != nil {
			panic(err)
		}
		secondHalf, err := strconv.Atoi(s[len(s)/2:])
		if err != nil {
			panic(err)
		}
		return firstHalf, secondHalf
	} else {
		return stone * 2024, -1
	}
}

func countStones(depth, stone int) int {
	if depth == 0 {
		return 1
	}
	key := strconv.Itoa(stone) + "," + strconv.Itoa(depth)
	if count := stoneToCount[key]; count != 0 {
		return count
	}
	s1, s2 := blinkSingleStone(stone)
	s1Count := countStones(depth-1, s1)
	s2Count := 0
	if s2 != -1 {
		s2Count = countStones(depth-1, s2)
	}
	count := s1Count + s2Count
	stoneToCount[key] = count
	return count
}

func part1() int {
	data := parseData(testFile)
	for i := range 25 {
		data = blink(data)
		fmt.Println("Blink complete:", i)
	}
	return len(data)
}

func part2() int {
	data := parseData(testFile)
	count := 0
	for i, stone := range data {
		count += countStones(75, stone)
		fmt.Println("Blink complete:", i)
	}
	return count
}

func main() {
	fmt.Printf("Part 1: %d\n", part1())
	fmt.Printf("Part 2: %d\n", part2())
}
