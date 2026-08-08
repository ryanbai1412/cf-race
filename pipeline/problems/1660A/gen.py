import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10 ** 8


def main(outdir):
    rnd = random.Random(1660)
    w = Writer(outdir)
    # edge cases
    w.add(multi(["0 0", "1 0", "0 1", "1 1", f"{MAX} {MAX}",
                 f"0 {MAX}", f"{MAX} 0", "1 " + str(MAX), f"{MAX} 1"]))
    # small exhaustive
    w.add(multi([f"{a} {b}" for a in range(20) for b in range(20)]))
    # random, max t
    for _ in range(3):
        w.add(multi([f"{rnd.randint(0, MAX)} {rnd.randint(0, MAX)}"
                     for _ in range(10000)]))
    # many zeros of one kind
    w.add(multi([f"0 {rnd.randint(0, MAX)}" for _ in range(5000)] +
                [f"{rnd.randint(0, MAX)} 0" for _ in range(5000)]))


if __name__ == "__main__":
    main(sys.argv[1])
