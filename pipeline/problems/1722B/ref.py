import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        idx += 1  # n
        r1 = data[idx]; r2 = data[idx + 1]; idx += 2
        out.append("YES" if r1.replace("G", "B") == r2.replace("G", "B") else "NO")
    print("\n".join(out))


main()
