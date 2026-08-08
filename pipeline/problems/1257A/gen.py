import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, x, a, b):
    return f"{n} {x} {a} {b}"


def main(outdir):
    rnd = random.Random(1257)
    w = Writer(outdir)
    # minimal n, no swaps, already maximal distance, huge x
    w.add(multi([case(2, 0, 1, 2), case(2, 100, 2, 1), case(2, 0, 2, 1),
                 case(100, 0, 1, 100), case(100, 100, 1, 100),
                 case(100, 100, 50, 51), case(100, 0, 50, 51)]))
    # x exactly reaches / just misses the maximum
    cs = []
    for n in (2, 3, 50, 100):
        for a, b in ((1, 2), (n - 1, n), (n // 2, n // 2 + 1)):
            if a == b or not (1 <= a <= n and 1 <= b <= n):
                continue
            need = (n - 1) - abs(a - b)
            for x in {max(0, need - 1), need, need + 1, 100}:
                if 0 <= x <= 100:
                    cs.append(case(n, x, a, b))
                    cs.append(case(n, x, b, a))
    w.add(multi(cs[:100]))
    # a > b and a < b symmetry over all adjacent pairs of a small row
    w.add(multi([case(10, 3, a, a + 1) for a in range(1, 10)]
                + [case(10, 3, a + 1, a) for a in range(1, 10)]))
    # exhaustive small: n=2..5, all a!=b, x=0..4
    small = [case(n, x, a, b) for n in range(2, 6) for a in range(1, n + 1)
             for b in range(1, n + 1) if a != b for x in range(5)]
    for i in range(0, len(small), 100):
        w.add(multi(small[i:i + 100]))
    # max t random
    for _ in range(8):
        cs = []
        for _ in range(100):
            n = rnd.randint(2, 100)
            a = rnd.randint(1, n)
            b = rnd.randint(1, n)
            while b == a:
                b = rnd.randint(1, n)
            cs.append(case(n, rnd.randint(0, 100), a, b))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
