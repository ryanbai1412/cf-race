import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXN = 10**18


def main(outdir):
    rnd = random.Random(1498)
    w = Writer(outdir)
    # edge values (distinct within each test)
    w.add(multi(["1", "2", "3"]))
    w.add(multi([str(MAXN), str(MAXN - 1), str(MAXN - 2)]))
    # small values 1..300
    w.add(multi([str(x) for x in range(1, 301)]))
    # numbers just below multiples of 3 across magnitudes
    cases = []
    for e in range(1, 19):
        base = 10**e
        for d in (-2, -1, 0, 1, 2):
            v = base + d
            if 1 <= v <= MAXN:
                cases.append(str(v))
    w.add(multi(sorted(set(cases), key=int)))
    # random across magnitudes
    for _ in range(4):
        seen = set()
        while len(seen) < 2000:
            e = rnd.randint(0, 17)
            seen.add(rnd.randint(10**e, min(MAXN, 10 ** (e + 1))))
        w.add(multi([str(x) for x in seen]))
    # max t with random huge values
    seen = set()
    while len(seen) < 10000:
        seen.add(rnd.randint(1, MAXN))
    w.add(multi([str(x) for x in seen]))


if __name__ == "__main__":
    main(sys.argv[1])
