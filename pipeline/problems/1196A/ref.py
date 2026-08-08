import sys


def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    out = []
    idx = 1
    for _ in range(q):
        a, b, c = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        idx += 3
        out.append(str((a + b + c) // 2))
    print("\n".join(out))


main()
