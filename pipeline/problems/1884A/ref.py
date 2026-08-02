import sys

def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(int(data[0])):
        x, k = map(int, data[1 + 2 * i:3 + 2 * i])
        y = x
        while sum(map(int, str(y))) % k != 0:
            y += 1
        out.append(str(y))
    print("\n".join(out))

main()
