"""Independent implementation: greedily remove letters of "one"/"zero"."""
import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    s = data[1] if len(data) > 1 else ""
    cnt = Counter(s)
    digits = []
    while cnt["n"] > 0:
        for ch in "one":
            cnt[ch] -= 1
        digits.append("1")
    while cnt["z"] > 0:
        for ch in "zero":
            cnt[ch] -= 1
        digits.append("0")
    assert all(v == 0 for v in cnt.values()), cnt
    print(" ".join(sorted(digits, reverse=True)))


main()
