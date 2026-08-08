import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = data[idx:idx + n]
        idx += n
        vals = list(map(int, a))
        best = max(vals[i] * vals[i + 1] for i in range(n - 1))
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
