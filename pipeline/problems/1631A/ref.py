import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = [int(x) for x in data[idx : idx + n]]
        idx += n
        b = [int(x) for x in data[idx : idx + n]]
        idx += n
        hi = max(max(ai, bi) for ai, bi in zip(a, b))
        lo = max(min(ai, bi) for ai, bi in zip(a, b))
        out.append(str(hi * lo))
    print("\n".join(out))


main()
