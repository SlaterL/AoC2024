import argparse

parser = argparse.ArgumentParser(description="This script does something.")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
args = parser.parse_args()

input = []

inputFile = "day2/test/input.txt"
if args.testfile:
    inputFile = "day2/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    return [int(i) for i in line.split()]


def isSorted(report):
    for i in range(1, len(report)):
        if report[i] <= report[i-1] or abs(report[i]-report[i-1]) > 3:
            return False
    return True


def isSafe(report):
    return isSorted(report) or isSorted(list(reversed(report)))


def part1():
    reports = [parse(line) for line in input]
    count = 0
    for report in reports:
        if isSafe(report):
            count += 1
    return count


def part2():
    reports = [parse(line) for line in input]
    count = 0
    for report in reports:
        if isSafe(report):
            count += 1
        else:
            for i in range(len(report)):
                if isSafe(report[:i]+report[i+1:]):
                    count += 1
                    break
    return count


def main():
    if not args.part:
        print("Part 1:", part1())
        print("Part 2:", part2())
    elif args.part == "1":
        print("Part 1:", part1())
    elif args.part == "2":
        print("Part 2:", part2())


if __name__ == "__main__":
    main()
