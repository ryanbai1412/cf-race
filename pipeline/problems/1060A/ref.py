import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1] if len(data) > 1 else ""
    print(min(s.count("8"), n // 11))


main()
