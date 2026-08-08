import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

PERMS = ["abc", "acb", "bac", "bca", "cab", "cba"]


def case(rnd, n, alpha):
    s = "".join(rnd.choice(alpha) for _ in range(n))
    return s + "\n" + rnd.choice(PERMS)


def main(outdir):
    rnd = random.Random(1617)
    w = Writer(outdir)
    # edges: missing letters, single char, all-abc combos with T=abc
    w.add(multi([
        "a\nabc",
        "z\ncba",
        "abc\nabc",
        "abc\nacb",
        "aabbcc\nabc",
        "cba\nabc",
        "ab\nabc",
        "bc\nabc",
        "ac\nabc",
        "aaa\nabc",
        "abcz\nabc",
        "zzzabc\nabc",
    ]))
    # random abc-only strings (stress the special case)
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(1, 100), "abc")
                     for _ in range(250)]))
    # random abcd strings
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(1, 100), "abcd")
                     for _ in range(250)]))
    # random full alphabet
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(1, 100),
                          "abcdefghijklmnopqrstuvwxyz")
                     for _ in range(250)]))
    # max size
    w.add(multi([case(rnd, 100, "abc") for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
