import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, hi=26):
    s = "".join(rnd.choice(string.ascii_lowercase[:hi]) for _ in range(n))
    return f"{n}\n{s}"


def main(outdir):
    rnd = random.Random(17602)
    w = Writer(outdir)
    # edges: single letters a and z, all same letter, max n
    w.add(multi(["1\na", "1\nz", "100\n" + "a" * 100, "100\n" + "z" * 100, "100\n" + "a" * 99 + "b"]))
    # each letter as the max, once
    w.add(multi([f"2\n{ch}a" for ch in string.ascii_lowercase]))
    # random small alphabets and full alphabet
    for hi in (1, 2, 5, 26):
        w.add(multi([case(rnd, rnd.randint(1, 100), hi) for _ in range(rnd.randint(1, 1000))]))
    # max t
    w.add(multi([case(rnd, rnd.randint(1, 100)) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
