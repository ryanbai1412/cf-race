import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10 ** 9


def main(outdir):
    rnd = random.Random(1611)
    w = Writer(outdir)
    # small exhaustive-ish edge grid
    edge = []
    for a in range(0, 9):
        for b in range(0, 9):
            edge.append(f"{a} {b}")
    w.add(multi(edge))
    # extremes
    w.add(multi(["0 0", f"0 {M}", f"{M} 0", f"{M} {M}", f"1 {M}",
                 f"{M} 1", f"3 {M}", f"{M} 3", "1 3", "3 1"]))
    # random small
    for _ in range(3):
        cases = [f"{rnd.randint(0, 100)} {rnd.randint(0, 100)}"
                 for _ in range(1000)]
        w.add(multi(cases))
    # random large + max t
    for _ in range(3):
        cases = [f"{rnd.randint(0, M)} {rnd.randint(0, M)}"
                 for _ in range(10000)]
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
