"""Independent brute force for 1374A: scan k downwards from n. Small n only."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        x = int(data[1 + 3 * i]); y = int(data[2 + 3 * i]); n = int(data[3 + 3 * i])
        for k in range(n, -1, -1):
            if k % x == y:
                out.append(k)
                break
        else:
            raise RuntimeError("no answer")
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
