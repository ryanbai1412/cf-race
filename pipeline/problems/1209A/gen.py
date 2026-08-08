import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}\n"


def main(outdir):
    rnd = random.Random(1209)
    w = Writer(outdir)
    w.add(case([1]))
    w.add(case([100]))
    w.add(case([1] * 100))
    w.add(case([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]))  # primes: all colors
    w.add(case(list(range(1, 101))))  # contains 1: one color
    w.add(case(list(range(2, 102))[:100]))
    w.add(case([97] * 50 + [89] * 50))
    # small randoms
    for hi in (5, 10, 30):
        for _ in range(3):
            n = rnd.randint(1, 20)
            w.add(case([rnd.randint(1, hi) for _ in range(n)]))
    # max-size randoms
    for _ in range(4):
        w.add(case([rnd.randint(2, 100) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
