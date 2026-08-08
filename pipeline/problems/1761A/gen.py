import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1761)
    w = Writer(outdir)
    # exhaustive small: all (n, a, b) with n <= 12
    cases = [f"{n} {a} {b}" for n in range(1, 13) for a in range(1, n + 1) for b in range(1, n + 1)]
    w.add(multi(cases))
    # edges around n=100
    w.add(
        multi(
            [
                "100 100 100",
                "100 99 100",
                "100 100 99",
                "100 99 99",
                "100 1 97",
                "100 97 1",
                "100 1 98",
                "100 98 1",
                "100 49 49",
                "100 50 49",
                "100 49 50",
                "1 1 1",
            ]
        )
    )
    # random, max t
    for _ in range(3):
        cases = []
        for _ in range(10000):
            n = rnd.randint(1, 100)
            cases.append(f"{n} {rnd.randint(1, n)} {rnd.randint(1, n)}")
        w.add(multi(cases))
    # biased near-boundary random
    cases = []
    for _ in range(10000):
        n = rnd.randint(2, 100)
        a = rnd.randint(1, n)
        b = max(1, min(n, n - a + rnd.randint(-3, 3)))
        cases.append(f"{n} {a} {b}")
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
