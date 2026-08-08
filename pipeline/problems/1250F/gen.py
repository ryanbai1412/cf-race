import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

MAXN = 10**5


def main(outdir):
    rnd = random.Random(1250)
    w = Writer(outdir)
    fixed = [
        1,                # smallest
        MAXN,             # largest allowed
        99991,            # large prime => 1 x n
        2,                # smallest prime
        4,                # perfect square
        99856,            # 316^2, largest perfect square <= 1e5
        65536,            # power of two
        99999,            # 3 * 3 * 41 * 271
        90000,            # 300^2
        6,
        99989,            # prime
        59049,            # 3^10
    ]
    for n in fixed:
        w.add(str(n))
    for _ in range(7):
        w.add(str(rnd.randint(1, MAXN)))


if __name__ == "__main__":
    main(sys.argv[1])
