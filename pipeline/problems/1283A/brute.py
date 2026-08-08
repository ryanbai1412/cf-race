import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    for i in range(t):
        h = int(data[1 + 2 * i])
        m = int(data[2 + 2 * i])
        cnt = 0
        while h != 0 or m != 0:
            m += 1
            if m == 60:
                m = 0
                h = (h + 1) % 24
            cnt += 1
        print(cnt)


main()
