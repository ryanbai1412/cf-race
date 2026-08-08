import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1312)
    w = Writer(outdir)
    # all valid (n, m) pairs with 3 <= m < n <= 100 where n % m == 0
    yes = [f"{n} {m}" for n in range(4, 101)
           for m in range(3, n) if n % m == 0]
    w.add(multi(yes))
    # edges
    w.add(multi(["4 3", "100 99", "100 50", "6 3", "99 33"]))
    # random mixes, including a max-size t
    all_pairs = [(n, m) for n in range(4, 101) for m in range(3, n)]
    for _ in range(4):
        t = rnd.randint(50, 500)
        cases = [f"{n} {m}" for n, m in (rnd.choice(all_pairs) for _ in range(t))]
        w.add(multi(cases))
    w.add(multi([f"{n} {m}" for n, m in (rnd.choice(all_pairs)
                                         for _ in range(10000))]))


if __name__ == "__main__":
    main(sys.argv[1])
