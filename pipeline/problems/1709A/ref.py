import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        x = int(data[pos]); pos += 1
        abc = [int(v) for v in data[pos:pos + 3]]; pos += 3
        opened = set()
        key = x
        while key != 0 and key not in opened:
            opened.add(key)
            key = abc[key - 1]
        out.append("YES" if len(opened) == 3 else "NO")
    print("\n".join(out))


main()
