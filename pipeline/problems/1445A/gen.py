import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

MAXX = 1000
MAXN = 50


def case(n, x, a, b):
    return f"{n} {x}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b))


def multi_blank(cases):
    """Test cases separated by a blank line, like the original input."""
    return f"{len(cases)}\n\n" + "\n\n".join(c.rstrip("\n") for c in cases) + "\n"


def main(outdir):
    rnd = random.Random(1445)
    w = Writer(outdir)

    # edges: n=1, x=1, exact fit, off by one
    w.add(multi_blank([
        case(1, 1, [1], [1]),
        case(1, 2, [1], [1]),
        case(1, MAXX, [MAXX], [MAXX]),
        case(2, 2, [1, 1], [1, 1]),
        case(2, 3, [1, 2], [1, 2]),
        case(3, 4, [1, 2, 3], [1, 1, 2]),
    ]))

    # max-size: t=100 blocks of n=50 with exact-fit pairs (all Yes)
    cases = []
    for _ in range(100):
        n = MAXN
        a = sorted(rnd.randint(1, MAXX // 2) for _ in range(n))
        b = sorted(MAXX - a[n - 1 - i] for i in range(n))
        cases.append(case(n, MAXX, a, b))
    w.add(multi_blank(cases))

    # max-size: exact fit broken in exactly one place (all No)
    cases = []
    for _ in range(100):
        n = MAXN
        a = sorted(rnd.randint(1, MAXX // 2) for _ in range(n))
        b = sorted(MAXX - a[n - 1 - i] for i in range(n))
        j = rnd.randrange(n)
        b[j] = min(MAXX, b[j] + 1)
        b.sort()
        cases.append(case(n, MAXX, a, b))
    w.add(multi_blank(cases))

    # random mixes
    for _ in range(12):
        t = rnd.randint(1, 100)
        cases = []
        for _ in range(t):
            n = rnd.randint(1, MAXN)
            x = rnd.randint(2, 30)
            a = sorted(rnd.randint(1, x) for _ in range(n))
            b = sorted(rnd.randint(1, x) for _ in range(n))
            cases.append(case(n, x, a, b))
        w.add(multi_blank(cases))


if __name__ == "__main__":
    main(sys.argv[1])
