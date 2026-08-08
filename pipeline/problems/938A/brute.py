"""Independent solution: literal simulation of the deletion rule."""
import sys

VOWELS = set("aeiouy")


def main():
    data = sys.stdin.read().split()
    s = list(data[1]) if len(data) > 1 else []
    while True:
        idx = None
        for i in range(1, len(s)):
            if s[i] in VOWELS and s[i - 1] in VOWELS:
                idx = i
                break
        if idx is None:
            break
        del s[idx]
    print("".join(s))


main()
