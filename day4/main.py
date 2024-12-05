import argparse
import regex as re
import numpy as np

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day4/test/input.txt"
if args.testfile:
    inputFile = "day4/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    return line


def part1():
    h = np.array([list(line) for line in input])
    v = []
    for i in list(zip(*input[::-1])):
        st = ""
        for ii in i:
            st += ii
        v.append(st)
    v = np.array([list(line) for line in v])
    d1 = []
    d2 = []
    cur = 0-(len(v)-1)
    cur = int(cur)
    for i in range(len(v)*2-1):
        d1.append(np.diag(h, cur))
        d2.append(np.diag(v, cur))
        cur += 1

    lines = []
    lines.extend(h)
    lines.extend(v)
    lines.extend(d1)
    lines.extend(d2)
    lines = ["".join(i) for i in lines]

    pattern = r"XMAS|SAMX"
    count = 0
    for i in range(len(lines)):
        count += len(re.findall(pattern, lines[i], overlapped=True))
    return count


def part2():
    grid = [line for line in input]

    count = 0
    for line in range(len(grid)):
        for c in range(len(grid[line])):
            if grid[line][c] == "A":
                try:
                    lDiag = [grid[line-1][c-1], grid[line+1][c+1]]
                    rDiag = [grid[line-1][c+1], grid[line+1][c-1]]
                    if "M" in lDiag and "S" in lDiag and "M" in rDiag and "S" in rDiag:
                        count += 1
                except IndexError:
                    pass
    return count
