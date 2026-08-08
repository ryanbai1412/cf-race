import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXA = 10**7


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1234)
    w = Writer(outdir)
    # single good, extremes
    w.add(multi([case([1]), case([MAXA])]))
    # all equal (sum divisible), and off-by-one above/below
    w.add(multi([case([7] * 100), case([7] * 99 + [8]), case([8] * 99 + [7])]))
    # max size: q=100, n=100, max values
    w.add(multi([case([MAXA] * 100) for _ in range(100)]))
    w.add(multi([case([rnd.randint(1, MAXA) for _ in range(100)]) for _ in range(100)]))
    # remainder-boundary cases: sum = n*k + r for each r
    cs = []
    for n in range(1, 11):
        for r in range(n):
            a = [5] * n
            for i in range(r):
                a[i] += 1
            cs.append(case(a))
    w.add(multi(cs))
    # small random with small values (many ties / exact divisions)
    for _ in range(8):
        q = rnd.randint(1, 100)
        cs = []
        for _ in range(q):
            n = rnd.randint(1, 10)
            cs.append(case([rnd.randint(1, 12) for _ in range(n)]))
        w.add(multi(cs))
    # random mid-size values
    for _ in range(5):
        q = rnd.randint(1, 20)
        cs = []
        for _ in range(q):
            n = rnd.randint(1, 100)
            hi = rnd.choice([10, 1000, 10**6, MAXA])
            cs.append(case([rnd.randint(1, hi) for _ in range(n)]))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
