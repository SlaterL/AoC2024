import argparse

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day11/test/input.txt"
if args.testfile:
    inputFile = "day11/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    return line


def part1():
    pass


def part2():
    pass

