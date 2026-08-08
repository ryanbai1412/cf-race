"""Independent brute force: explicit character counting from the end."""
import sys


def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); s = data[pos + 1]; pos += 2
        tail = 0
        for ch in reversed(s):
            if ch == ")":
                tail += 1
            else:
                break
        rest = 0
        for i in range(n - tail):
            rest += 1
        out.append("Yes" if tail > rest else "No")
    print("\n".join(out))


main()
