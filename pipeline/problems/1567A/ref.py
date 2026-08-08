import sys

MAP = {"L": "L", "R": "R", "U": "D", "D": "U"}


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        idx += 1  # n
        s = data[idx]
        idx += 1
        out.append("".join(MAP[c] for c in s))
    print("\n".join(out))


main()
