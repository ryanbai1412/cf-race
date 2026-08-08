import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = data[idx : idx + n]
        idx += n
        b = data[idx : idx + n]
        idx += n
        diff = sum(1 for x, y in zip(a, b) if x != y)
        ones_gap = abs(a.count(b"1") - b.count(b"1"))
        out.append(str(min(diff, ones_gap + 1)))
    sys.stdout.write("\n".join(out) + "\n")


main()
