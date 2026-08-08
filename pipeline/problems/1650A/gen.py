import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s, c):
    return f"{s}\n{c}"


def rand_case(rnd, n, alpha):
    s = "".join(rnd.choice(alpha) for _ in range(n))
    c = rnd.choice(alpha if rnd.random() < 0.7 else string.ascii_lowercase)
    return case(s, c)


def main(outdir):
    rnd = random.Random(1650)
    w = Writer(outdir)
    # edge: length 1, present / absent
    w.add(multi([case("a", "a"), case("a", "b"), case("z", "z")]))
    # c only at even (0-based odd) positions -> NO
    w.add(multi([case("aba", "b"), case("ababa", "b"), case("xax", "a")]))
    # c only at odd (0-based even) positions -> YES
    w.add(multi([case("bab", "b"), case("babab", "b"), case("axaxa", "a")]))
    # small alphabets, small lengths (tricky parity cases)
    for alpha in ("ab", "abc"):
        w.add(multi([rand_case(rnd, rnd.randrange(1, 10, 2), alpha)
                     for _ in range(500)]))
    # random full alphabet
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randrange(1, 50, 2),
                               string.ascii_lowercase) for _ in range(500)]))
    # max size
    w.add(multi([rand_case(rnd, 49, "ab") for _ in range(1000)]))
    w.add(multi([rand_case(rnd, 49, string.ascii_lowercase)
                 for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
