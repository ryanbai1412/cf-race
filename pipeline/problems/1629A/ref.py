import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, k = int(data[idx]), int(data[idx + 1])
        idx += 2
        a = [int(x) for x in data[idx : idx + n]]
        idx += n
        b = [int(x) for x in data[idx : idx + n]]
        idx += n
        for ai, bi in sorted(zip(a, b)):
            if ai <= k:
                k += bi
            else:
                break
        out.append(str(k))
    print("\n".join(out))


main()
