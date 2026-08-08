import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10 ** 9


def main(outdir):
    rnd = random.Random(1527)
    w = Writer(outdir)
    # edges: 1, 2, powers of two and neighbors, max n
    vals = ["1", "2", "3", str(M)]
    for k in range(1, 30):
        for d in (-1, 0, 1):
            v = (1 << k) + d
            if 1 <= v <= M:
                vals.append(str(v))
    w.add(multi(vals))
    # max size: t = 3*10^4 random
    for seed in range(3):
        w.add(multi([str(rnd.randint(1, M)) for _ in range(30000)]))
    # small exhaustive 1..300
    w.add(multi([str(v) for v in range(1, 301)]))


if __name__ == "__main__":
    main(sys.argv[1])
