"""Shared helpers for rating-1400 authored validators, oracles and generators."""
import math
import random

REG = {}


class Bad(Exception):
    pass


def need(cond, msg="constraint violated"):
    if not cond:
        raise Bad(msg)


def lines(s):
    rows = s.replace("\r\n", "\n").split("\n")
    while rows and rows[-1].strip() == "":
        rows.pop()
    need(rows, "empty input")
    return rows


def toks(line):
    return line.split()


def intok(t, lo, hi):
    need(t.lstrip("-").isdigit() and (t == "0" or not t.lstrip("-").startswith("0")) and t != "-0", f"bad integer {t!r}")
    v = int(t)
    need(lo <= v <= hi, f"{v} not in [{lo},{hi}]")
    return v


def ints_line(line, bounds):
    ts = toks(line)
    need(len(ts) == len(bounds), f"expected {len(bounds)} tokens, got {len(ts)}")
    return [intok(t, lo, hi) for t, (lo, hi) in zip(ts, bounds)]


def single_ints(s, bounds, one_line=True):
    rows = lines(s)
    if one_line:
        need(len(rows) == 1, "expected one line")
        return ints_line(rows[0], bounds)
    need(len(rows) == len(bounds), "expected one value per line")
    return [ints_line(r, [b])[0] for r, b in zip(rows, bounds)]


def problem(pid, rules, brute_cases=0):
    def wrap(cls):
        cls.pid, cls.rules, cls.brute_cases = pid, rules, brute_cases
        REG[pid] = cls
        return cls
    return wrap


def rng(pid):
    return random.Random("cf-race-1400-" + pid)


def isqrt(n):
    return math.isqrt(n)


class LR:
    """Line-structured strict reader."""

    def __init__(self, s):
        self.rows = lines(s)
        self.i = 0

    def line(self):
        need(self.i < len(self.rows), "missing line")
        self.i += 1
        return self.rows[self.i - 1].rstrip("\r")

    def ints(self, bounds):
        return ints_line(self.line(), bounds)

    def same(self, k, lo, hi):
        return ints_line(self.line(), [(lo, hi)] * k)

    def word(self, alphabet=None, lo=1, hi=10 ** 9):
        w = self.line().strip()
        need(lo <= len(w) <= hi, "length")
        if alphabet is not None:
            need(set(w) <= set(alphabet), "alphabet")
        return w

    def done(self):
        need(self.i == len(self.rows), "trailing lines")


LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = LOWER.upper()
