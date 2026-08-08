import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10**5


def main(outdir):
    rnd = random.Random(1715)
    w = Writer(outdir)
    # all small grids
    w.add(multi([f"{n} {m}" for n in range(1, 8) for m in range(1, 8)]))
    # extremes
    w.add(multi(["1 1", f"1 {M}", f"{M} 1", f"{M} {M}", f"1 2", f"2 1", f"2 2"]))
    # random mix of small/large
    for _ in range(5):
        cases = []
        for _ in range(1000):
            if rnd.random() < 0.5:
                cases.append(f"{rnd.randint(1, 20)} {rnd.randint(1, 20)}")
            else:
                cases.append(f"{rnd.randint(1, M)} {rnd.randint(1, M)}")
        w.add(multi(cases))
    # max-size test
    w.add(multi([f"{M} {M}" for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
