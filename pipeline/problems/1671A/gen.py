import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_str(rnd, n):
    return "".join(rnd.choice("ab") for _ in range(n))


def run_str(rnd, n):
    # build from runs of random lengths 1..4
    s = []
    c = rnd.choice("ab")
    while len("".join(s)) < n:
        L = rnd.randint(1, 4)
        s.append(c * L)
        c = "a" if c == "b" else "b"
    return "".join(s)[:n]


def main(outdir):
    rnd = random.Random(1671)
    w = Writer(outdir)
    # edges: single chars, alternating, all same
    w.add(multi(["a", "b", "aa", "ab", "ba", "bb", "aba", "bab", "a" * 50, "ab" * 25]))
    # run length 1 hidden at start/middle/end
    w.add(multi(["abb", "aab", "aaba", "abaa", "bbab", "aabaa", "bbabb", "aabbb" * 10]))
    # small random exhaustive-ish
    w.add(multi([rand_str(rnd, rnd.randint(1, 8)) for _ in range(500)]))
    # run-structured strings
    w.add(multi([run_str(rnd, rnd.randint(1, 50)) for _ in range(500)]))
    # random long
    for _ in range(2):
        w.add(multi([rand_str(rnd, rnd.randint(1, 50)) for _ in range(500)]))
    # max t
    w.add(multi([run_str(rnd, 50) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
