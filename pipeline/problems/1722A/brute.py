"""Alternative: compare against the explicit set of all permutations."""
import itertools
import sys

VALID = {"".join(p) for p in itertools.permutations("Timur")}


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s = data[2 + 2 * i]
        out.append("YES" if s in VALID else "NO")
    print("\n".join(out))


main()
