import sys

def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(int(data[0])):
        a, b, c = map(int, data[1 + 3 * i:4 + 3 * i])
        s = a + b + c
        out.append("YES" if s % 3 == 0 and b <= s // 3 else "NO")
    print("\n".join(out))

main()
