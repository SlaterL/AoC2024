import argparse
from copy import deepcopy
from enum import Enum

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


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def next(self) -> :
        if self == Direction.LEFT:
            return Direction.UP
        else:
            return Direction(self.value + 1)

    def turn(self):
        self = self.next()

    def symbol(self):
        match self:
            case Direction.UP:
                return "^"
            case Direction.RIGHT:
                return ">"
            case Direction.DOWN:
                return "v"
            case Direction.LEFT:
                return "<"


class Guard:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x: int = x
        self.y: int = y
        self.direction: Direction = direction

    def nextPosition(self, map: list):
        match self.direction:
            case Direction.UP:
                self.y -= 1
            case Direction.RIGHT:
                self.x += 1
            case Direction.DOWN:
                self.y += 1
            case Direction.LEFT:
                self.x -= 1

    def testForLoop(self, map: list) -> bool:
        pass


def parse(line):
    return line


def part1():
    pass


def part2():
    pass
