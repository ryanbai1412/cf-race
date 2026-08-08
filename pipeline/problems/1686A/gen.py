import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, hi=100):
    a = [rnd.randint(0, hi) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}"


def yes_case(rnd, n, hi=100):
    # force sum = n * a_i for some i
    while True:
        a = [rnd.randint(0, hi) for _ in range(n - 1)]
        s = sum(a)
        # choose target value v with v*n - s in [0, hi]
        vs = [v for v in range(0, hi + 1) if 0 <= v * n - s <= hi]
        if vs:
            v = rnd.choice(vs)
            a.append(v * n - s)
            i = rnd.randrange(n)
            a[i], a[-1] = a[-1], a[i]
            return f"{n}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1686)
    w = Writer(outdir)
    # edge: all zeros, all equal, n=3 minimal
    w.add(multi(["3\n0 0 0", "3\n100 100 100", "3\n0 0 1", "3\n1 2 3", "3\n0 1 2"]))
    w.add(multi([case(rnd, rnd.randint(3, 50), 5) for _ in range(60)]))
    w.add(multi([yes_case(rnd, rnd.randint(3, 50)) for _ in range(60)]))
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(3, 50)) for _ in range(rnd.randint(1, 100))]))
    # max: t=200 full-size
    w.add(multi([(yes_case if rnd.random() < 0.5 else case)(rnd, 50) for _ in range(200)]))


if __name__ == "__main__":
    main(sys.argv[1])
