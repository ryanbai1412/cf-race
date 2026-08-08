import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

MAXN = 10 ** 5


def case(a, queries):
    n = len(a)
    lines = [f"{n} {len(queries)}", " ".join(map(str, a))]
    lines += [f"{t} {v}" for t, v in queries]
    return "\n".join(lines)


def main(outdir):
    rnd = random.Random(1491)
    w = Writer(outdir)

    # n = 1 edge cases
    w.add(case([0], [(2, 1), (1, 1), (2, 1), (1, 1), (2, 1)]))
    w.add(case([1], [(2, 1)]))
    # all zeros / all ones, k at both ends
    w.add(case([0] * 5, [(2, 1), (2, 5), (1, 3), (2, 1), (2, 2)]))
    w.add(case([1] * 5, [(2, 1), (2, 5), (1, 5), (2, 5), (2, 4)]))
    # toggle the same position many times
    w.add(case([0, 1, 0], [(1, 2), (2, 1), (1, 2), (2, 1), (1, 2), (2, 2), (2, 3)]))

    # small random tests
    for _ in range(4):
        n = rnd.randint(1, 8)
        q = rnd.randint(1, 20)
        a = [rnd.randint(0, 1) for _ in range(n)]
        qs = []
        for _ in range(q):
            if rnd.random() < 0.5:
                qs.append((1, rnd.randint(1, n)))
            else:
                qs.append((2, rnd.randint(1, n)))
        if all(t == 1 for t, _ in qs):
            qs.append((2, rnd.randint(1, n)))
        w.add(case(a, qs))

    # medium random test
    n = 1000
    a = [rnd.randint(0, 1) for _ in range(n)]
    qs = [(rnd.randint(1, 2), rnd.randint(1, n)) for _ in range(1000)]
    qs.append((2, 1))
    w.add(case(a, qs))

    # max size: n = q = 1e5, mixed queries
    a = [rnd.randint(0, 1) for _ in range(MAXN)]
    qs = [(rnd.randint(1, 2), rnd.randint(1, MAXN)) for _ in range(MAXN)]
    qs[0] = (2, MAXN)
    w.add(case(a, qs))

    # max size: all updates on one cell then queries sweeping k
    a = [0] * MAXN
    qs = [(1, 1) for _ in range(MAXN // 2)] + [(2, k % MAXN + 1) for k in range(MAXN // 2)]
    w.add(case(a, qs))


if __name__ == "__main__":
    main(sys.argv[1])
