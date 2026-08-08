import sys


def solve(s: str) -> str:
    lt, gt = "<" in s, ">" in s
    if lt and gt:
        return "?"
    if lt:
        return "<"
    if gt:
        return ">"
    return "="


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    print("\n".join(solve(data[i]) for i in range(1, t + 1)))


main()
