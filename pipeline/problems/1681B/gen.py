import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, m):
    a = list(range(1, n + 1))
    rnd.shuffle(a)
    b = [rnd.randint(1, n - 1) for _ in range(m)]
    return f"{n}\n{' '.join(map(str, a))}\n{m}\n{' '.join(map(str, b))}"


def main(outdir):
    rnd = random.Random(16812)
    w = Writer(outdir)
    # edge: n=2
    w.add(multi(["2\n1 2\n1\n1", "2\n2 1\n3\n1 1 1"]))
    # random small
    w.add(multi([case(rnd, rnd.randint(2, 10), rnd.randint(1, 10)) for _ in range(100)]))
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(2, 1000), rnd.randint(1, 1000)) for _ in range(rnd.randint(1, 50))]))
    # large case (kept under 1MB input)
    w.add(multi([case(rnd, 70000, 70000)]))
    # many small cases
    w.add(multi([case(rnd, 2, 2) for _ in range(5000)]))


if __name__ == "__main__":
    main(sys.argv[1])
