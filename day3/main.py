import argparse
import re

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day3/test/input.txt"
if args.testfile:
    inputFile = "day3/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    return line


def getNums(mul):
    paren1 = mul.index("(")
    paren2 = mul.index(")")
    numsString = mul[paren1+1:paren2]
    nums = numsString.split(",")
    return [int(num) for num in nums]


def part1():
    p1Input = [line for line in input]
    pattern = r"mul\(\d{1,3},\d{1,3}\)"
    total = 0
    for line in p1Input:
        muls = re.findall(pattern, line)
        for mul in muls:
            nums = getNums(mul)
            total += nums[0]*nums[1]
    return total


def part2():
    p2String = "do()"
    for line in input:
        p2String += line.strip()
    pattern = r"mul\(\d{1,3},\d{1,3}\)"
    total = 0
    lastDo = 0
    nextDont = 0
    while True:
        lastDo = p2String.find("do()", lastDo)
        nextDont = p2String.find("don't()", lastDo)
        if lastDo == -1:
            break
        if nextDont < lastDo and nextDont != -1:
            lastDo = nextDont
            continue
        if nextDont == -1:
            muls = re.findall(pattern, p2String[lastDo:])
        else:
            muls = re.findall(pattern, p2String[lastDo:nextDont])

        for mul in muls:
            nums = getNums(mul)
            total += nums[0]*nums[1]
        lastDo = nextDont

    return total
