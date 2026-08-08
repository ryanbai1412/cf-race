import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1688)
    w = Writer(outdir)
    # edge: 1, all powers of two up to 2^30, 2^30 itself
    w.add(multi([str(1 << k) for k in range(31)]))
    w.add(multi([str((1 << k) - 1) for k in range(1, 31)] + [str((1 << k) + 1) for k in range(1, 30)]))
    w.add(multi([str(rnd.randint(1, 100)) for _ in range(100)]))
    for _ in range(3):
        w.add(multi([str(rnd.randint(1, 1 << 30)) for _ in range(rnd.randint(1, 300))]))
    # max: t = 1000
    w.add(multi([str(rnd.randint(1, 1 << 30)) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
