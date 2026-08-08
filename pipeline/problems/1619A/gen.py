import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_str(rnd, n, alpha):
    return "".join(rnd.choice(alpha) for _ in range(n))


def case(rnd, alpha):
    kind = rnd.randint(0, 2)
    if kind == 0:  # square
        h = rand_str(rnd, rnd.randint(1, 50), alpha)
        return h + h
    if kind == 1:  # near-square: mutate one char of a square
        h = rand_str(rnd, rnd.randint(1, 50), alpha)
        s = list(h + h)
        i = rnd.randrange(len(s))
        s[i] = rnd.choice(alpha)
        return "".join(s)
    return rand_str(rnd, rnd.randint(1, 100), alpha)


def main(outdir):
    rnd = random.Random(1619)
    w = Writer(outdir)
    # edges
    w.add(multi([
        "a", "aa", "ab", "aba", "abab", "aaa", "zz",
        "a" * 100, "a" * 99, ("ab" * 25) * 2, "ab" * 49 + "ba",
    ]))
    # random binary alphabet (many squares)
    for _ in range(4):
        w.add(multi([case(rnd, "ab") for _ in range(100)]))
    # random small alphabet
    for _ in range(3):
        w.add(multi([case(rnd, "abc") for _ in range(100)]))
    # random full alphabet
    for _ in range(3):
        w.add(multi([case(rnd, "abcdefghijklmnopqrstuvwxyz")
                     for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
