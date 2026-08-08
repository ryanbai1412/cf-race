import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        k = int(data[idx + 1])
        s = data[idx + 2]
        idx += 3
        out.append("1" if k == 0 or s == s[::-1] else "2")
    print("\n".join(out))


main()
