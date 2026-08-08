import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1742)
    w = Writer(outdir)
    # edges: n=1, all equal, all distinct, one duplicate pair at max n
    w.add(multi([case([1]), case([10**9]), case([5] * 100), case(list(range(1, 101)))]))
    perm = list(range(1, 101))
    rnd.shuffle(perm)
    dup = perm[:]
    dup[50] = dup[10]
    w.add(multi([case(perm), case(dup)]))
    # max size: t=100, n=100 each
    big = []
    for _ in range(100):
        if rnd.random() < 0.5:
            a = rnd.sample(range(1, 10**9), 100)
        else:
            a = [rnd.randint(1, 10**9) for _ in range(100)]
            a[rnd.randrange(100)] = a[rnd.randrange(100)]
        big.append(case(a))
    w.add(multi(big))
    # random small, mixed dup probability
    for _ in range(8):
        t = rnd.randint(1, 30)
        cases = []
        for _ in range(t):
            n = rnd.randint(1, 12)
            a = [rnd.randint(1, rnd.choice([3, 10, 10**9])) for _ in range(n)]
            cases.append(case(a))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
