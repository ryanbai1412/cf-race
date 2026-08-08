import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n, k = int(data[pos]), int(data[pos + 1]); pos += 2
        p = [int(v) for v in data[pos:pos + n]]; pos += n
        out.append(str(sum(1 for v in p[:k] if v > k)))
    print("\n".join(out))


main()
