import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        x, y, a = map(int, data[1 + 3 * i:4 + 3 * i])
        r = a % (x + y)
        out.append("NO" if x > r else "YES")
    print("\n".join(out))

main()
