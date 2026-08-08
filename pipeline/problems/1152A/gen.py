import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

N = 10**5
V = 10**9


def case(a, b):
    return (f"{len(a)} {len(b)}\n" + " ".join(map(str, a)) + "\n"
            + " ".join(map(str, b)) + "\n")


def main(outdir):
    rnd = random.Random(1152)
    w = Writer(outdir)
    # minimal
    w.add(case([1], [1]))
    w.add(case([1], [2]))
    w.add(case([V], [V - 1]))
    # all even chests / all odd keys and vice versa
    w.add(case([2] * N, [1] * N))
    w.add(case([1] * N, [1] * N))
    w.add(case([2] * N, [2] * N))
    # lopsided sizes
    w.add(case([2] * N, [1]))
    w.add(case([2], [1] * N))
    # max values, max sizes, random parity
    w.add(case([rnd.randint(1, V) for _ in range(N)],
               [rnd.randint(1, V) for _ in range(N)]))
    w.add(case([rnd.randrange(1, V, 2) for _ in range(N)],
               [rnd.randrange(2, V, 2) for _ in range(N)]))
    # small randoms
    for _ in range(6):
        n = rnd.randint(1, 8)
        m = rnd.randint(1, 8)
        w.add(case([rnd.randint(1, 20) for _ in range(n)],
                   [rnd.randint(1, 20) for _ in range(m)]))


if __name__ == "__main__":
    main(sys.argv[1])
