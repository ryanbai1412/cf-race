import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1657)
    w = Writer(outdir)
    # edge cases: origin, axis points, pythagorean pairs
    w.add(multi(["0 0", "0 1", "1 0", "0 50", "50 0", "3 4", "4 3",
                 "6 8", "5 12", "50 50", "1 1", "49 49"]))
    # exhaustive: every possible (x, y) pair — covers the whole input space
    pairs = [f"{x} {y}" for x in range(51) for y in range(51)]
    w.add(multi(pairs))
    # max t with random pairs
    for _ in range(2):
        w.add(multi([f"{rnd.randint(0, 50)} {rnd.randint(0, 50)}"
                     for _ in range(3000)]))


if __name__ == "__main__":
    main(sys.argv[1])
