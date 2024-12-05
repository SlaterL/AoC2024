import argparse

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()

input = []

inputFile = "day5/test/input.txt"
if args.testfile:
    inputFile = "day5/test/" + args.testfile

with open(inputFile) as f:
    input = f.read().splitlines()


def parse(line):
    return line


def getRulesDict(rules):
    d = {}
    for rule in rules:
        before, after = rule.split("|")
        if before in d.keys():
            d[before].add(after)
        else:
            d[before] = set()
            d[before].add(after)
    return d


def isOrdered(update, rules):
    ordered = True
    for i in range(len(update)):
        if update[i] not in rules.keys():
            continue
        after = rules[update[i]]
        for a in after:
            if a in update[:i]:
                ordered = False
    return ordered


def reorder(update: list, rules):
    while not isOrdered(update, rules):
        for i in range(len(update)):
            if update[i] not in rules.keys():
                continue
            after = rules[update[i]]
            for a in after:
                if a in update[:i]:
                    val = update[i]
                    update.remove(val)
                    update.insert(update.index(a), val)
                    break
    return int(update[int((len(update)-1)/2)])


def part1():
    rules = getRulesDict([line for line in input if "|" in line])
    updates = [line for line in input if "|" not in line and line != ""]

    sum = 0
    for updateString in updates:
        update = updateString.split(",")
        if isOrdered(update, rules):
            sum += int(update[int((len(update)-1)/2)])
    return sum


def part2():
    rules = getRulesDict([line for line in input if "|" in line])
    updates = [line for line in input if "|" not in line and line != ""]

    sum = 0
    for updateString in updates:
        update = updateString.split(",")
        if not isOrdered(update, rules):
            sum += reorder(update, rules)
    return sum

    pass
