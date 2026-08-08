import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1353)
    w = Writer(outdir)
    M = 10 ** 9
    # edges: n = 1, 2, 3 with min/max m
    w.add(multi(["1 1", f"1 {M}", "2 1", f"2 {M}", "3 1", f"3 {M}",
                 f"{M} 1", f"{M} {M}", "2 2", "3 2"]))
    # small random
    for _ in range(3):
        w.add(multi([f"{rnd.randint(1, 5)} {rnd.randint(1, 6)}"
                     for _ in range(1000)]))
    # max-size random
    for _ in range(4):
        w.add(multi([f"{rnd.randint(1, M)} {rnd.randint(1, M)}"
                     for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
