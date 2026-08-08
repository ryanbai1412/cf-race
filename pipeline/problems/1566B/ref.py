import sys


def solve(s: str) -> int:
    if "0" not in s:
        return 0
    blocks = len([b for b in s.split("1") if b])
    return 1 if blocks == 1 else 2


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        out.append(str(solve(data[i])))
    print("\n".join(out))


main()
