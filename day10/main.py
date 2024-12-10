import argparse

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day10/test/input.txt"
if args.testfile:
    inputFile = "day10/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    return [int(i) for i in line]


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return f"{self.row},{self.col}"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def next(self) -> list:
        ret = [
            Position(self.row-1, self.col),
            Position(self.row+1, self.col),
            Position(self.row, self.col-1),
            Position(self.row, self.col+1),
        ]
        return [pos for pos in ret if pos.row >= 0 and pos.col >= 0]


class Path:
    def __init__(self, startPos: Position = None):
        self.path = []
        if startPos:
            self.path.append(startPos)

    def copy(self):
        p = Path(self.path[0])
        p.path = [pos for pos in self.path]
        return p

    def hike(self, pos: Position):
        self.path.append(pos)

    def curPos(self) -> Position:
        return self.path[-1]

    def __eq__(self, o):
        if len(self.path) != len(o.path):
            return False
        for i in range(len(self.path)):
            if self.path[i] != o.path[i]:
                return False
        return True

    def __str__(self):
        path = ""
        for pos in self.path:
            path += str(pos) + " "
        return f"{path}"


def count9sV2(map: list, curPath: Path) -> (list):
    retPaths = []
    try:
        curElevation = map[curPath.curPos().row][curPath.curPos().col]
    except IndexError:
        return []

    if curElevation == 9:
        return [curPath]

    for pos in curPath.curPos().next():
        try:
            posElevation = map[pos.row][pos.col]
        except IndexError:
            continue

        if posElevation == curElevation + 1:
            newPath = curPath.copy()
            newPath.hike(pos)
            retPaths.extend(count9sV2(map, newPath))

    return retPaths


def count9s(map: list, curPos: Position) -> (list):
    retPositions = []
    try:
        curElevation = map[curPos.row][curPos.col]
    except IndexError:
        return []

    if curElevation == 9:
        return [curPos]

    for pos in curPos.next():
        try:
            posElevation = map[pos.row][pos.col]
        except IndexError:
            continue

        if posElevation == curElevation + 1:
            retPositions.extend(count9s(map, pos))

    return retPositions


def part1():
    map = [parse(line) for line in input]
    sum = 0
    for rowI, row in enumerate(map):
        for colI, col in enumerate(row):
            if col == 0:
                nines = count9s(map, Position(rowI, colI))
                final = []
                for nine in nines:
                    if nine not in final:
                        final.append(nine)
                sum += len(final)
    return sum


def part2():
    map = [parse(line) for line in input]
    sum = 0
    for rowI, row in enumerate(map):
        for colI, col in enumerate(row):
            if col == 0:
                nines = count9sV2(map, Path(Position(rowI, colI)))
                final = []
                for nine in nines:
                    if nine not in final:
                        final.append(nine)
                sum += len(final)
                # [print(x) for x in final]
                # print(len(final))
    return sum
