"""Alternative: per-character comparison with explicit colourblind rule."""
import sys


def same(a, b):
    return a == b or {a, b} <= {"G", "B"}


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        idx += 1
        r1 = data[idx]; r2 = data[idx + 1]; idx += 2
        out.append("YES" if all(same(a, b) for a, b in zip(r1, r2)) else "NO")
    print("\n".join(out))


main()
