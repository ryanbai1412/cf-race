import sys


def main():
    data = sys.stdin.read().split()
    s = data[1] if len(data) > 1 else ""
    ones = s.count("n")
    zeros = s.count("z")
    print(" ".join(["1"] * ones + ["0"] * zeros))


main()
