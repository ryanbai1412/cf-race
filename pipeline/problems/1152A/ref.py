import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    a = data[2:2 + n]
    b = data[2 + n:2 + n + m]
    ao = sum(1 for v in a if v[-1] in b"13579")
    bo = sum(1 for v in b if v[-1] in b"13579")
    print(min(ao, m - bo) + min(n - ao, bo))


main()
