"""Shared helpers for authored rating-800 recipes."""
import random
import re

INT = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")


def need(cond, msg="constraint violated"):
    if not cond:
        raise AssertionError(msg)


def toks(inp):
    return inp.split()


def lines(inp):
    """Input lines without the final newline."""
    body = inp[:-1] if inp.endswith("\n") else inp
    return body.split("\n")


def num(token, lo, hi):
    need(INT.match(token) is not None, f"not an integer: {token!r}")
    value = int(token)
    need(lo <= value <= hi, f"{value} outside [{lo}, {hi}]")
    return value


def nums(tokens, lo, hi):
    return [num(t, lo, hi) for t in tokens]


def word(s, alphabet, lo, hi):
    need(lo <= len(s) <= hi, f"length {len(s)} outside [{lo}, {hi}]")
    need(all(c in alphabet for c in s), f"bad characters in {s[:20]!r}")
    return s


def exact_tokens(inp, count):
    t = toks(inp)
    need(len(t) == count, f"expected {count} tokens, got {len(t)}")
    return t


def rng(seed):
    return random.Random(seed)


LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = LOWER.upper()
LETTERS = LOWER + UPPER
DIGITS = "0123456789"


def joined(values):
    return " ".join(map(str, values))


def yn(flag):
    return "YES" if flag else "NO"
