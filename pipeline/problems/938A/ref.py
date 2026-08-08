import sys

VOWELS = set("aeiouy")


def main():
    data = sys.stdin.read().split()
    s = data[1] if len(data) > 1 else ""
    out = []
    for ch in s:
        if out and ch in VOWELS and out[-1] in VOWELS:
            continue
        out.append(ch)
    print("".join(out))


main()
