import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def fmt(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1672)
    w = Writer(outdir)
    # edges: all-ones (no moves), single logs
    w.add(multi(["1\n1", "1\n2", "1\n50", "2\n1 1", f"50\n{' '.join(['1'] * 50)}"]))
    # parity boundary cases
    w.add(multi([fmt([2] * k) for k in range(1, 11)]))
    # small random
    w.add(multi([fmt([rnd.randint(1, 5) for _ in range(rnd.randint(1, 5))]) for _ in range(100)]))
    # random full range
    for _ in range(3):
        w.add(multi([fmt([rnd.randint(1, 50) for _ in range(rnd.randint(1, 50))]) for _ in range(100)]))
    # max size
    w.add(multi([fmt([rnd.randint(1, 50) for _ in range(50)]) for _ in range(100)]))
    w.add(multi([fmt([50] * 50) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
