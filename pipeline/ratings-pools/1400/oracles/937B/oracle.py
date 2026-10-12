import re
import sys


class Invalid(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def lines_of(data, count):
    data = data.replace(b"\r\n", b"\n")
    require(b"\r" not in data, "bare carriage return")
    lines = data.split(b"\n")
    while lines and not lines[-1].strip(b" \t"):
        lines.pop()
    require(len(lines) == count, "wrong line count")
    return lines


def integers(line, count, low, high):
    tokens = re.split(b"[ \t]+", line.strip(b" \t"))
    require(len(tokens) == count, "wrong token count")
    result = []
    for token in tokens:
        require(re.fullmatch(b"[+-]?[0-9]+", token) is not None, "invalid integer")
        digits = token[1:] if token[:1] in (b"+", b"-") else token
        digits = digits.lstrip(b"0") or b"0"
        require(len(digits) <= len(str(max(abs(low), abs(high)))), "integer out of range")
        value = int(digits) * (-1 if token[:1] == b"-" else 1)
        require(low <= value <= high, "integer out of range")
        result.append(value)
    return result


def solve(data):
    line, = lines_of(data, 1)
    p, y = integers(line, 2, 2, 1000000000)
    require(p <= y, "p exceeds y")
    if p == y:
        return "-1"
    from math import isqrt
    bound = min(p, isqrt(y))
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(bound) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:bound + 1:prime] = b"\x00" * ((bound - start) // prime + 1)
    primes = [i for i in range(2, bound + 1) if sieve[i]]
    for candidate in range(y, p, -1):
        safe = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                safe = False
                break
        if safe:
            return str(candidate)
    return "-1"


def main():
    try:
        answer = solve(sys.stdin.buffer.read())
    except (Invalid, ValueError) as error:
        print(str(error)[:160], file=sys.stderr)
        return 1
    print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
