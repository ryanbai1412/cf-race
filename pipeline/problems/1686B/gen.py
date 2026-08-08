import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, sortedness=None):
    p = list(range(1, n + 1))
    if sortedness == "rev":
        p.reverse()
    elif sortedness == "sorted":
        pass
    else:
        rnd.shuffle(p)
    return f"{n}\n{' '.join(map(str, p))}"


def main(outdir):
    rnd = random.Random(16862)
    w = Writer(outdir)
    # edge: n=1, sorted, reversed
    w.add(multi(["1\n1", "2\n1 2", "2\n2 1", case(rnd, 60000, "sorted"), case(rnd, 60000, "rev")]))
    w.add(multi([case(rnd, rnd.randint(1, 8)) for _ in range(300)]))
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(1, 1000)) for _ in range(rnd.randint(1, 50))]))
    # large case (kept under 1MB input)
    w.add(multi([case(rnd, 140000)]))


if __name__ == "__main__":
    main(sys.argv[1])
