import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10**16


def case(rnd, lo, hi):
    return f"{rnd.randint(lo, hi)} {rnd.randint(lo, hi)} {rnd.randint(lo, hi)}"


def main(outdir):
    rnd = random.Random(1196)
    w = Writer(outdir)
    # edges: all minimal, all maximal, mixed extremes
    w.add(multi(["1 1 1", f"{MAX} {MAX} {MAX}", f"1 1 {MAX}", f"{MAX} 1 1",
                 f"1 {MAX} 1", "1 2 3", "2 2 2", "1 1 2"]))
    # small randoms (parity coverage)
    for _ in range(4):
        w.add(multi([case(rnd, 1, 10) for _ in range(rnd.randint(1, 50))]))
    # medium randoms
    for _ in range(3):
        w.add(multi([case(rnd, 1, 10**6) for _ in range(rnd.randint(1, 200))]))
    # max-size: q=1000 with huge values
    w.add(multi([case(rnd, 1, MAX) for _ in range(1000)]))
    w.add(multi([case(rnd, MAX - 5, MAX) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
