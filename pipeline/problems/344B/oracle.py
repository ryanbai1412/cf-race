import re
import sys

INPUT = re.compile(
    rb"[ \t]*([+-]?[0-9]+)[ \t]+([+-]?[0-9]+)[ \t]+([+-]?[0-9]+)[ \t]*(?:\r?\n)?"
)


def parse(data):
    match = INPUT.fullmatch(data)
    if match is None:
        raise ValueError("expected one line with exactly three integers")
    values = []
    for token in match.groups():
        if token.startswith(b"-"):
            raise ValueError("valence must be positive")
        digits = token.lstrip(b"+").lstrip(b"0")
        if not digits or len(digits) > 7:
            raise ValueError("valence outside [1, 1000000]")
        value = int(digits)
        if value > 1_000_000:
            raise ValueError("valence outside [1, 1000000]")
        values.append(value)
    return tuple(values)


def solve(a, b, c):
    total = a + b + c
    if total % 2:
        return "Impossible"
    half = total // 2
    bonds = (half - c, half - a, half - b)
    if min(bonds) < 0:
        return "Impossible"
    return " ".join(map(str, bonds))


def main():
    try:
        values = parse(sys.stdin.buffer.read())
    except ValueError:
        sys.exit(3)
    sys.stdout.write(solve(*values) + "\n")


if __name__ == "__main__":
    main()
