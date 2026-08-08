import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


LIM = 10 ** 18


def rand_smooth(rnd):
    n = 1
    while True:
        p = rnd.choice([2, 3, 5])
        if n * p > LIM:
            return n
        n *= p
        if rnd.random() < 0.05:
            return n


def main(outdir):
    rnd = random.Random(1176)
    w = Writer(outdir)
    w.add(multi(["1", "10", "25", "30", "14", "27", str(10 ** 18)]))
    w.add(multi(["1"] * 1000))
    w.add(multi([str(2 ** 59), str(3 ** 37), str(5 ** 25), str(2 ** 59 * 3), "999999999999999989", str(LIM)]))
    # all pure powers
    cases = []
    for p in (2, 3, 5):
        v = 1
        while v * p <= LIM:
            v *= p
            cases.append(str(v))
    w.add(multi(cases))
    # impossible numbers (contain other prime factors)
    w.add(multi([str(rnd.randint(1, LIM)) for _ in range(1000)]))
    for _ in range(8):
        q = rnd.randint(1, 1000)
        cases = []
        for _ in range(q):
            if rnd.random() < 0.7:
                cases.append(str(rand_smooth(rnd)))
            else:
                cases.append(str(rnd.randint(1, LIM)))
        w.add(multi(cases))
    # small exhaustive-ish
    w.add(multi([str(v) for v in range(1, 1001)]))


if __name__ == "__main__":
    main(sys.argv[1])
