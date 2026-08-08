import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, a):
    """a = first player's cards; the rest go to the second player."""
    sa = set(a)
    b = [v for v in range(1, n + 1) if v not in sa]
    return (f"{n} {len(a)} {len(b)}\n{' '.join(map(str, a))}\n"
            f"{' '.join(map(str, b))}")


def main(outdir):
    rnd = random.Random(1270)
    w = Writer(outdir)
    # minimum n both ways; n held by a huge-minority / huge-majority player
    w.add(multi([case(2, [2]), case(2, [1]),
                 case(100, [100]), case(100, [1]),
                 case(100, list(range(1, 100))),
                 case(100, list(range(2, 101)))]))
    # first player has everything but one card, yet loses (missing card is n)
    cs = []
    for n in (3, 4, 10, 99, 100):
        cs.append(case(n, [v for v in range(1, n + 1) if v != n]))
        cs.append(case(n, [n]))
        cs.append(case(n, [n - 1]))
    w.add(multi(cs))
    # exhaustive small n = 2..5, every proper non-empty subset for player 1
    small = []
    for n in range(2, 6):
        for mask in range(1, (1 << n) - 1):
            small.append(case(n, [i + 1 for i in range(n) if mask >> i & 1]))
    for i in range(0, len(small), 100):
        w.add(multi(small[i:i + 100]))
    # shuffled card order within each hand
    cs = []
    for _ in range(50):
        n = rnd.randint(2, 100)
        k1 = rnd.randint(1, n - 1)
        a = rnd.sample(range(1, n + 1), k1)
        cs.append(case(n, a))
    w.add(multi(cs))
    # max t random, biased splits
    for _ in range(8):
        cs = []
        for _ in range(100):
            n = rnd.randint(2, 100)
            k1 = rnd.choice([1, n - 1, rnd.randint(1, n - 1)])
            cs.append(case(n, rnd.sample(range(1, n + 1), k1)))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
