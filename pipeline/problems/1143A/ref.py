import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    last0 = max(i for i in range(n) if a[i] == b"0")
    last1 = max(i for i in range(n) if a[i] == b"1")
    print(min(last0, last1) + 1)


main()
