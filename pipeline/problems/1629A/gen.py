import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(k, a, b):
    return f"{len(a)} {k}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}"


def rand_case(rnd, nmax=100, amax=1000, bmax=1000, kmax=1000):
    n = rnd.randint(1, nmax)
    return case(
        rnd.randint(1, kmax),
        [rnd.randint(1, amax) for _ in range(n)],
        [rnd.randint(1, bmax) for _ in range(n)],
    )


def main(outdir):
    rnd = random.Random(1629)
    w = Writer(outdir)

    # edges: n=1 usable/unusable, chains, max everything
    chain_a = list(range(1, 101))
    w.add(
        multi(
            [
                case(1, [1], [1]),
                case(1, [2], [1000]),
                case(1000, [1000] * 100, [1000] * 100),
                case(1, [1] * 100, [1000] * 100),
                case(1, chain_a, [1] * 100),
                case(1, chain_a[::-1], [1] * 100),
                case(1000, [1000], [1]),
                case(999, [1000], [1000]),
            ]
        )
    )

    # tiny values: forces careful ordering
    for _ in range(2):
        w.add(
            multi(
                [rand_case(rnd, nmax=6, amax=6, bmax=3, kmax=4) for _ in range(50)]
            )
        )
    # chain-like: a_i close to reachable frontier
    cases = []
    for _ in range(100):
        n = rnd.randint(1, 100)
        k = rnd.randint(1, 20)
        cur = k
        a, b = [], []
        for _ in range(n):
            ai = rnd.randint(max(1, cur - 3), cur + 3)
            bi = rnd.randint(1, 5)
            a.append(ai)
            b.append(bi)
            if ai <= cur:
                cur += bi
        order = list(range(n))
        rnd.shuffle(order)
        cases.append(case(k, [a[i] for i in order], [b[i] for i in order]))
    w.add(multi(cases))
    # general random, max t
    w.add(multi([rand_case(rnd) for _ in range(100)]))
    w.add(multi([rand_case(rnd, nmax=100, amax=1000, bmax=1000, kmax=10) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
