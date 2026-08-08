import sys


def solve(s: str) -> int:
    total = sum(int(c) for c in s)
    swaps = sum(1 for c in s[:-1] if c != "0")
    return total + swaps


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        idx += 1  # n
        out.append(str(solve(data[idx])))
        idx += 1
    print("\n".join(out))


main()
