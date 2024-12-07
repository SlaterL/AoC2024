import argparse

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day7/test/input.txt"
if args.testfile:
    inputFile = "day7/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    target, inputs = line.split(":")
    inputs = [int(val) for val in inputs.split()]
    return (int(target), inputs)


def isValid(inputs: list, target: int, cur: int) -> bool:
    if len(inputs) == 0:
        return target == cur
    nextVal = inputs[0]
    return isValid(inputs[1:], target, cur+nextVal) or isValid(inputs[1:], target, cur*nextVal)


def isValidV2(inputs: list, target: int, cur: int) -> bool:
    if len(inputs) == 0:
        return target == cur
    nextVal = inputs[0]
    concat = int(str(cur)+str(nextVal))
    return isValidV2(inputs[1:], target, cur+nextVal) or isValidV2(inputs[1:], target, cur*nextVal) or isValidV2(inputs[1:], target, concat)


def part1():
    tests = [parse(line) for line in input]
    sum = 0
    for test in tests:
        if isValid(test[1][1:], test[0], test[1][0]):
            sum += test[0]
    return sum


def part2():
    tests = [parse(line) for line in input]
    sum = 0
    for test in tests:
        if isValidV2(test[1][1:], test[0], test[1][0]):
            sum += test[0]
    return sum
