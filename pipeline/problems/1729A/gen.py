import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10**8


def rand_case(rnd, lo, hi):
    a = rnd.randint(lo, hi)
    while True:
        b, c = rnd.randint(lo, hi), rnd.randint(lo, hi)
        if b != c:
            return f"{a} {b} {c}"


def tie_case(rnd, hi):
    while True:
        b, c = rnd.randint(1, hi), rnd.randint(1, hi)
        if b == c:
            continue
        a = abs(b - c) + (c - 1) + 1
        if 1 <= a <= MAX:
            return f"{a} {b} {c}"


def main(outdir):
    rnd = random.Random(1729)
    w = Writer(outdir)
    # edge: elevator 1 already on floor 1, elevator 2 heading to floor 1
    w.add(multi(["1 2 3", "1 3 2", f"1 {MAX} 1", f"{MAX} 1 2", f"{MAX} 2 1",
                 f"1 1 {MAX}", "2 1 2", "2 2 1", f"{MAX} {MAX} 1",
                 f"{MAX} 1 {MAX}", f"{MAX} {MAX - 1} {MAX}"]))
    # exact ties
    w.add(multi([tie_case(rnd, 10**8 // 2) for _ in range(1000)]))
    # small random (many ties/near-ties)
    w.add(multi([rand_case(rnd, 1, 5) for _ in range(10**4)]))
    w.add(multi([rand_case(rnd, 1, 30) for _ in range(10**4)]))
    # large random, max t
    w.add(multi([rand_case(rnd, 1, MAX) for _ in range(10**4)]))
    w.add(multi([rand_case(rnd, MAX // 2, MAX) for _ in range(10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
