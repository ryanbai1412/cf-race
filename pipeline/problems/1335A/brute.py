import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + i])
        cnt = 0
        for b in range(1, n):
            a = n - b
            if a > b:
                cnt += 1
        out.append(cnt)
    print("\n".join(map(str, out)))


main()
