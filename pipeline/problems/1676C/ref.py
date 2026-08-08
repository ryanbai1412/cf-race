import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx])
    idx += 1
    out = []
    for _ in range(t):
        n, m = int(data[idx]), int(data[idx + 1])
        idx += 2
        words = data[idx : idx + n]
        idx += n
        best = None
        for i in range(n):
            for j in range(i + 1, n):
                d = sum(abs(ord(a) - ord(b)) for a, b in zip(words[i], words[j]))
                if best is None or d < best:
                    best = d
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
