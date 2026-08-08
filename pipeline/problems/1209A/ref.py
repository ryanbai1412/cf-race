import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = sorted(int(x) for x in data[1:1 + n])
    leaders = []
    for v in a:
        if not any(v % m == 0 for m in leaders):
            leaders.append(v)
    print(len(leaders))


main()
