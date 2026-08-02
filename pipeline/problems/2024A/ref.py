import sys

def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(int(data[0])):
        a, b = map(int, data[1 + 2 * i:3 + 2 * i])
        out.append(str(a if a >= b else max(0, 2 * a - b)))
    print("\n".join(out))

main()
