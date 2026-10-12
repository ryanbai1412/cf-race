"""Shared strict-ish input reader for 1200 recipes (line-structured, token validated)."""
import random


class Reader:
    def __init__(self, text):
        assert "\r" not in text.replace("\r\n", "\n"), "stray CR"
        self.lines = [l.split() for l in text.replace("\r\n", "\n").split("\n")]
        while self.lines and not self.lines[-1]:
            self.lines.pop()
        self.pos = 0

    def line(self, count=None):
        assert self.pos < len(self.lines), "missing line"
        tokens = self.lines[self.pos]
        self.pos += 1
        assert tokens, "empty line"
        assert count is None or len(tokens) == count, f"expected {count} tokens, got {len(tokens)}"
        return tokens

    def ints(self, count=None, lo=None, hi=None):
        values = [int(t) for t in self.line(count)]
        for v in values:
            assert (lo is None or v >= lo) and (hi is None or v <= hi), f"{v} outside [{lo},{hi}]"
        return values

    def int(self, lo=None, hi=None):
        return self.ints(1, lo, hi)[0]

    def word(self, alphabet=None, lo=1, hi=None):
        (w,) = self.line(1)
        assert lo <= len(w) and (hi is None or len(w) <= hi), f"length {len(w)}"
        assert alphabet is None or set(w) <= set(alphabet), "bad alphabet"
        return w

    def end(self):
        assert self.pos == len(self.lines), "trailing data"


def rng(seed):
    return random.Random(seed)


def fmt(*rows):
    return "\n".join(" ".join(map(str, r)) if isinstance(r, (list, tuple)) else str(r) for r in rows) + "\n"
