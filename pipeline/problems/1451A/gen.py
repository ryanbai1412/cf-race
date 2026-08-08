import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXN = 10 ** 9


def main(outdir):
    rnd = random.Random(1451)
    w = Writer(outdir)

    # all small n (covers every special case: 1, 2, 3, 4, odd, even)
    w.add(multi([str(n) for n in range(1, 31)]))
    # extremes
    w.add(multi([str(MAXN), str(MAXN - 1), "1", "2", "3", "4", "5", "999999999"]))
    # max t of large random values
    w.add(multi([str(rnd.randint(1, MAXN)) for _ in range(1000)]))
    # max t of large odd values only
    w.add(multi([str(rnd.randrange(1, MAXN, 2)) for _ in range(1000)]))
    # max t of large even values only
    w.add(multi([str(rnd.randrange(2, MAXN, 2)) for _ in range(1000)]))
    # max t of powers of two and primes-ish
    w.add(multi([str(2 ** rnd.randint(0, 29)) for _ in range(1000)]))
    # random small
    for _ in range(10):
        t = rnd.randint(1, 100)
        w.add(multi([str(rnd.randint(1, 12)) for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
