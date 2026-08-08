import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1454)
    w = Writer(outdir)
    # edge: n=1
    w.add(multi([case([1])]))
    # all same value -> -1
    w.add(multi([case([3] * 5), case([1, 1]), case([2, 2, 2, 2])]))
    # small randoms, many cases
    for _ in range(5):
        cases = []
        for _ in range(rnd.randint(50, 200)):
            n = rnd.randint(1, 10)
            cases.append(case([rnd.randint(1, n) for _ in range(n)]))
        w.add(multi(cases))
    # medium randoms with varying value ranges
    for hi_frac in (0.1, 0.5, 1.0):
        cases = []
        tot = 0
        while tot < 50000:
            n = rnd.randint(1, 2000)
            tot += n
            hi = max(1, int(n * hi_frac))
            cases.append(case([rnd.randint(1, hi) for _ in range(n)]))
        w.add(multi(cases))
    # max-size: one big n = 2e5
    n = 200000
    w.add(multi([case([rnd.randint(1, n) for _ in range(n)])]))
    # max-size: values from tiny range (lots of dups)
    w.add(multi([case([rnd.randint(1, 3) for _ in range(n)])]))
    # max t = 2e4 tiny cases
    cases = [case([rnd.randint(1, 5) for _ in range(rnd.randint(1, 10))])
             for _ in range(20000)]
    w.add(multi(cases))
    # unique winner at last index
    a = list(range(2, 1001)) + list(range(2, 1001)) + [1]
    rnd.shuffle(a)
    w.add(multi([case(a)]))


if __name__ == "__main__":
    main(sys.argv[1])
