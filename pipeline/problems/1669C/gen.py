import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, lo=1, hi=1000):
    a = [rnd.randint(lo, hi) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}"


def yes_case(rnd, n):
    # both index-parity groups internally consistent
    po = rnd.randint(0, 1)
    pe = rnd.randint(0, 1)
    a = []
    for i in range(n):
        p = po if i % 2 == 0 else pe
        v = rnd.randint(1, 500) * 2
        a.append(v + p if v + p <= 1000 else v - 2 + p)
    return f"{n}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(16693)
    w = Writer(outdir)
    # minimal and edge cases
    w.add(multi(["2\n1 2", "2\n2 2", "2\n1 1", "2\n1000 1000", "2\n999 1000"]))
    # small random (mix of YES/NO)
    w.add(multi([case(rnd, rnd.randint(2, 6), 1, 4) for _ in range(100)]))
    # constructed YES cases
    w.add(multi([yes_case(rnd, rnd.randint(2, 50)) for _ in range(100)]))
    # random full range
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(2, 50)) for _ in range(100)]))
    # max size
    w.add(multi([case(rnd, 50) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
