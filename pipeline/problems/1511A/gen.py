import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, weights=(1, 1, 1)):
    r = rnd.choices([1, 2, 3], weights=weights, k=n)
    return f"{n}\n" + " ".join(map(str, r))


def main(outdir):
    rnd = random.Random(1511)
    w = Writer(outdir)
    # single-reviewer cases
    w.add(multi(["1\n1", "1\n2", "1\n3"]))
    # all same type, max n
    w.add(multi([f"50\n" + " ".join([str(v)] * 50) for v in (1, 2, 3)]))
    # random small
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(1, 10)) for _ in range(200)]))
    # skewed distributions
    for wt in [(5, 1, 1), (1, 5, 1), (1, 1, 5)]:
        w.add(multi([case(rnd, rnd.randint(1, 50), wt) for _ in range(500)]))
    # max t
    for _ in range(2):
        w.add(multi([case(rnd, rnd.randint(1, 50)) for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
