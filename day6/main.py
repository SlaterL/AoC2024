import argparse
from copy import deepcopy

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day6/test/input.txt"
if args.testfile:
    inputFile = "day6/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()

guardSyms = ["^", ">", "v", "<"]


def parse(line):
    return line


def nextGuardDir(dir):
    return guardSyms[(guardSyms.index(dir)+1) % 4]


def getGuardPos(map):
    for row, rowVal in enumerate(map):
        for col, colVal in enumerate(rowVal):
            if colVal in guardSyms:
                return [row, col], colVal


def part1():
    map = [list(line) for line in input]
    guardPos, guardDir = getGuardPos(map)
    map[guardPos[0]][guardPos[1]] = "X"
    while True:
        nextPos = [pos for pos in guardPos]
        match guardDir:
            case "^":
                nextPos[0] -= 1
            case "v":
                nextPos[0] += 1
            case "<":
                nextPos[1] -= 1
            case ">":
                nextPos[1] += 1
        try:
            if map[nextPos[0]][nextPos[1]] == "#":
                guardDir = nextGuardDir(guardDir)
            elif map[nextPos[0]][nextPos[1]] == "." or map[nextPos[0]][nextPos[1]] == "X":
                map[nextPos[0]][nextPos[1]] = "X"
                guardPos = nextPos
        except IndexError:
            return sum([line.count("X") for line in map])


def hasLoop(map, seen, guardPos, guardDir):
    while True:

        nextPos = [pos for pos in guardPos]
        match guardDir:
            case "^":
                nextPos[0] -= 1
            case "v":
                nextPos[0] += 1
            case "<":
                nextPos[1] -= 1
            case ">":
                nextPos[1] += 1
        try:
            if map[nextPos[0]][nextPos[1]] == "#":
                guardDir = nextGuardDir(guardDir)
            elif map[nextPos[0]][nextPos[1]] == "." or map[nextPos[0]][nextPos[1]] == "X":
                map[nextPos[0]][nextPos[1]] = "X"
                guardPos = nextPos
        except IndexError:
            return 0

        gpString = ",".join([str(v)for v in guardPos])
        if gpString not in seen.keys():
            seen[gpString] = [guardDir]
        else:
            if guardDir in seen[gpString]:
                return 1
            else:
                seen[gpString].append(guardDir)


def part2():
    map = [list(line) for line in input]
    guardPos, guardDir = getGuardPos(map)
    map[guardPos[0]][guardPos[1]] = "X"
    seen = {}
    loops = 0
    while True:
        nextPos = [pos for pos in guardPos]
        match guardDir:
            case "^":
                nextPos[0] -= 1
            case "v":
                nextPos[0] += 1
            case "<":
                nextPos[1] -= 1
            case ">":
                nextPos[1] += 1
        try:
            if map[nextPos[0]][nextPos[1]] == "#":
                guardDir = nextGuardDir(guardDir)
            elif map[nextPos[0]][nextPos[1]] == "." or map[nextPos[0]][nextPos[1]] == "X":
                mapCopy = deepcopy(map)
                mapCopy[nextPos[0]][nextPos[1]] = "#"
                loops += hasLoop(mapCopy, deepcopy(seen),
                                 deepcopy(guardPos), guardDir)
                map[nextPos[0]][nextPos[1]] = "X"
                guardPos = nextPos
        except IndexError:
            return loops
        gpString = ",".join([str(v)for v in guardPos])
        if gpString not in seen.keys():
            seen[gpString] = [guardDir]
        else:
            seen[gpString].append(guardDir)
