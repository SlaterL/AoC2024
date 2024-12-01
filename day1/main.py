from sys import argv

input = []

inputFile = "test/input.txt"
if "-t" in argv:
    testInputIndex = argv.index("-t")
    inputFile = "test/" + argv[testInputIndex+1]

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    return line.split()


def part1():
    l1 = [int(parse(line)[0]) for line in input]
    l2 = [int(parse(line)[1]) for line in input]
    l1.sort()
    l2.sort()

    sum = 0
    for i in range(len(l1)):
        sum += abs(l1[i]-l2[i])
    return sum


def part2():
    l1 = [int(parse(line)[0]) for line in input]
    l2 = [int(parse(line)[1]) for line in input]
    sum = 0
    for val in l1:
        sum += val * l2.count(val)
    return sum


def main():
    if "-p1" in argv:
        print("Part 1:", part1())
    elif "-p2" in argv:
        print("Part 2:", part2())
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())


if __name__ == "__main__":
    main()
