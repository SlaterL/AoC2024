import importlib
import argparse

parser = argparse.ArgumentParser(description="Run a day of Advent of Code")
parser.add_argument("-t", "--testfile", help="Name of the test file")
parser.add_argument("-p", "--part", help="Specify only one part to run")
parser.add_argument("-d", "--day", help="What day will be used", required=True)
args = parser.parse_args()


def main():
    day = importlib.import_module("day"+args.day+".main")
    if not args.part:
        print("Part 1:", day.part1())
        print("Part 2:", day.part2())
    elif args.part == "1":
        print("Part 1:", day.part1())
    elif args.part == "2":
        print("Part 2:", day.part2())


if __name__ == "__main__":
    main()
