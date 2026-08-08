import sys


def main():
    data = sys.stdin.read().split()
    s = data[1]
    cur = 0
    for ch in s:
        if ch == "+":
            cur += 1
        else:
            cur = max(cur - 1, 0)
    print(cur)


main()
