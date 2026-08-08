import itertools
import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

ALL_WORDS = ["".join(p) for p in itertools.product(string.ascii_lowercase, repeat=3)]


def case(rnd, n, alphabet_words):
    rows = [rnd.sample(alphabet_words, n) for _ in range(3)]
    return f"{n}\n" + "\n".join(" ".join(r) for r in rows)


def main(outdir):
    rnd = random.Random(17223)
    w = Writer(outdir)
    # n=1 hand cases: all same, all distinct, two share
    w.add(multi(["1\naaa\naaa\naaa", "1\naaa\nbbb\nccc", "1\naaa\naaa\nbbb"]))
    # small pool -> lots of overlaps
    pool = ALL_WORDS[:8]
    w.add(multi([case(rnd, rnd.randint(1, 6), pool) for _ in range(100)]))
    # medium random
    for _ in range(3):
        cases = []
        for _ in range(50):
            n = rnd.randint(1, 50)
            pool = rnd.sample(ALL_WORDS, min(len(ALL_WORDS), n * 2))
            cases.append(case(rnd, n, pool))
        w.add(multi(cases))
    # identical lists (everyone 0), fully disjoint lists (everyone 3n)
    row = rnd.sample(ALL_WORDS, 1000)
    w.add(multi([f"1000\n" + "\n".join(" ".join(row) for _ in range(3))]))
    disj = rnd.sample(ALL_WORDS, 3000)
    w.add(multi([f"1000\n" + "\n".join(
        " ".join(disj[i * 1000:(i + 1) * 1000]) for i in range(3))]))
    # large: 60 cases with n=1000 (~750KB, under the 1MB cap)
    w.add(multi([case(rnd, 1000, ALL_WORDS) for _ in range(60)]))


if __name__ == "__main__":
    main(sys.argv[1])
