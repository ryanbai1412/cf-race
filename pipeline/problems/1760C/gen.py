import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, lo=1, hi=10**9):
    return f"{n}\n{' '.join(str(rnd.randint(lo, hi)) for _ in range(n))}"


def main(outdir):
    rnd = random.Random(17603)
    w = Writer(outdir)
    # edges: n=2, duplicates, all equal, extreme values
    w.add(
        multi(
            [
                "2\n1 1",
                "2\n1 1000000000",
                "2\n1000000000 1",
                "3\n5 5 5",
                "4\n7 7 1 7",
                "5\n1000000000 1000000000 999999999 1 2",
            ]
        )
    )
    # random small with duplicates
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(2, 10), 1, 5) for _ in range(rnd.randint(1, 200))]))
    # random medium
    w.add(multi([case(rnd, rnd.randint(2, 1000)) for _ in range(100)]))
    # max n with small values (keeps input <1MB), and many medium cases with big values
    w.add(multi([case(rnd, 200000, 1, 999)]))
    w.add(multi(["2\n1000000000 1000000000"] + [case(rnd, 1998) for _ in range(30)]))
    # all-equal large
    w.add(multi([f"200000\n{' '.join(['999'] * 200000)}"]))


if __name__ == "__main__":
    main(sys.argv[1])
