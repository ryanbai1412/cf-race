import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(p):
    return f"{len(p)}\n" + " ".join(map(str, p))


def rand_perm(rnd, n):
    p = list(range(1, n + 1))
    rnd.shuffle(p)
    return p


def near_identity(rnd, n, swaps):
    p = list(range(1, n + 1))
    for _ in range(swaps):
        i, j = rnd.randrange(n), rnd.randrange(n)
        p[i], p[j] = p[j], p[i]
    return p


def main(outdir):
    rnd = random.Random(1638)
    w = Writer(outdir)
    # edges: n=1, identity, reversed, max n
    w.add(multi([case([1]), case([1, 2]), case([2, 1]),
                 case(list(range(1, 501))), case(list(range(500, 0, -1)))]))
    # near-identity permutations (prefix already sorted)
    w.add(multi([case(near_identity(rnd, 500, s)) for s in (1, 2, 3, 5, 10)]))
    # random small permutations
    for seed in range(6):
        w.add(multi([case(rand_perm(rnd, rnd.randint(1, 12))) for _ in range(80)]))
    # random larger permutations
    w.add(multi([case(rand_perm(rnd, rnd.randint(100, 500))) for _ in range(20)]))


if __name__ == "__main__":
    main(sys.argv[1])
