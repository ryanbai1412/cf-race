import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        a, b, c = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        idx += 3
        t1 = a - 1
        t2 = abs(b - c) + (c - 1)
        out.append("1" if t1 < t2 else "2" if t2 < t1 else "3")
    sys.stdout.write("\n".join(out) + "\n")


main()
