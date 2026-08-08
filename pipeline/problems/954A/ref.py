import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    res = 0
    i = 0
    while i < n:
        if i + 1 < n and s[i] != s[i + 1]:
            i += 2
        else:
            i += 1
        res += 1
    print(res)


main()
