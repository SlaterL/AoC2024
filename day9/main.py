import argparse
from itertools import groupby

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day9/test/input.txt"
if args.testfile:
    inputFile = "day9/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def getBlocks(disk: str) -> list:
    curId = 0
    blocks: list = []
    isFile = True
    for char in disk:
        i = int(char)
        if isFile:
            for v in range(i):
                blocks.append(curId)
            curId += 1
        else:
            for v in range(i):
                blocks.append(".")
        isFile = not isFile
    return blocks


def getChecksum(blocks: list) -> int:
    sum = 0
    for i in range(len(blocks)):
        if blocks[i] == ".":
            continue
        sum += i*blocks[i]
    return sum


def part1():
    disk = input[0]
    blocks: list = getBlocks(disk)
    nextDot = blocks.index(".")
    while True:
        try:
            nextDot = blocks.index(".", nextDot)
        except ValueError:
            break
        blocks.pop(nextDot)
        lastFile = "."
        while lastFile == ".":
            lastFile = blocks.pop()
        blocks.insert(nextDot, lastFile)

    return getChecksum(blocks)


def part2():
    disk = input[0]
    blocks: list = getBlocks(disk)
    groupMoved = []
    blocksGrouped: list = [list(group) for key, group in groupby(blocks)]
    i = len(blocksGrouped)
    while i > 0:
        i -= 1
        blocks = []
        [blocks.extend(v) for v in blocksGrouped]

        blocksGrouped = [list(group) for key, group in groupby(blocks)]

        if blocksGrouped[i][0] == "." or blocksGrouped[i][0] in groupMoved:
            continue
        for ii in range(len(blocksGrouped)):
            if ii > i:
                break
            if blocksGrouped[ii][0] != ".":
                continue
            if len(blocksGrouped[ii]) >= len(blocksGrouped[i]):
                id = blocksGrouped[i][0]
                for iii in range(len(blocksGrouped[i])):
                    blocksGrouped[ii][iii] = id
                    blocksGrouped[i][iii] = "."
                dots = ["."] * blocksGrouped[ii].count(".")
                ids = [id] * blocksGrouped[ii].count(id)
                blocksGrouped.pop(ii)
                blocksGrouped.insert(ii, ids)
                if len(dots) > 0:
                    blocksGrouped.insert(ii+1, dots)

                groupMoved.append(id)
                break

    blocks = []
    for i in blocksGrouped:
        blocks.extend(i)

    return getChecksum(blocks)
