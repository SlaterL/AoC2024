import argparse

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day8/test/input.txt"
if args.testfile:
    inputFile = "day8/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, pos):
        if pos.x == self.x and pos.y == self.y:
            return True
        return False

    def __str__(self):
        return f"{self.x},{self.y}"


def parse(line):
    return line


def getFreqLocations(map: list) -> dict:
    freqToLoc = {}
    for x in range(len(map)):
        for y, yVal in enumerate(map[x]):
            if yVal == ".":
                continue
            if yVal in freqToLoc.keys():
                freqToLoc[yVal].append(Position(x, y))
            else:
                freqToLoc[yVal] = [Position(x, y)]

    return freqToLoc


def getAntinodes(tower1: Position, tower2: Position):
    xDiff = tower1.x - tower2.x
    yDiff = tower1.y - tower2.y

    n1 = Position(tower1.x + xDiff, tower1.y + yDiff)
    n2 = Position(tower1.x - xDiff, tower1.y - yDiff)
    n3 = Position(tower2.x + xDiff, tower2.y + yDiff)
    n4 = Position(tower2.x - xDiff, tower2.y - yDiff)

    antinodes = [n for n in [n1, n2, n3, n4] if n != tower1 and n != tower2]

    return antinodes


def getAntinodesV2(tower1: Position, tower2: Position, xMax: int, yMax: int):
    xDiff = tower1.x - tower2.x
    yDiff = tower1.y - tower2.y
    antinodes = []
    last = Position(tower1.x, tower1.y)
    while last.x <= xMax+1 and last.y <= yMax+1 and last.x >= 0 and last.y >= 0:
        antinodes.append(last)
        last = Position(last.x-xDiff, last.y-yDiff)

    last = Position(tower1.x, tower1.y)
    while last.x <= xMax+1 and last.y <= yMax+1 and last.x >= 0 and last.y >= 0:
        if last not in antinodes:
            antinodes.append(last)
        last = Position(last.x+xDiff, last.y+yDiff)

    return antinodes


def removeDupes(nodes):
    res = []
    for node in nodes:
        if node not in res:
            res.append(node)
    return res


def part1():
    map = [line for line in input]
    freqToLoc = getFreqLocations(map)

    antinodes = []
    for freq, locs in freqToLoc.items():
        if len(locs) == 1:
            continue
        for i, loc in enumerate(locs):
            for otherLoc in locs[:i]+locs[i+1:]:
                antinodes.extend(getAntinodes(loc, otherLoc))

    res = 0
    antinodes = removeDupes(antinodes)
    for node in antinodes:
        if node.x < len(map) and node.x >= 0 and node.y < len(map[0]) and node.y >= 0:
            res += 1
    return res


def part2():
    map = [line for line in input]
    freqToLoc = getFreqLocations(map)

    antinodes = []
    for freq, locs in freqToLoc.items():
        if len(locs) == 1:
            continue
        for i, loc in enumerate(locs):
            for otherLoc in locs[:i]+locs[i+1:]:
                antinodes.extend(getAntinodesV2(
                    loc, otherLoc, len(map), len(map[0])))

    res = 0
    antinodes = removeDupes(antinodes)
    for node in antinodes:
        if node.x < len(map) and node.x >= 0 and node.y < len(map[0]) and node.y >= 0:
            res += 1
    return res
