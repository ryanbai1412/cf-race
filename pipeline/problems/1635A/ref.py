import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        acc = 0
        for v in data[idx + 1: idx + 1 + n]:
            acc |= int(v)
        idx += 1 + n
        out.append(str(acc))
    print("\n".join(out))


main()
