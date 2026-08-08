import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


N = 10 ** 9


def main(outdir):
    rnd = random.Random(1194)
    w = Writer(outdir)
    w.add(multi(["3 1", "4 2", "69 6"]))
    w.add(multi(["2 1"]))
    w.add(multi([f"{N} {N // 2}", f"{N} 1", f"{N} {N // 2 - 1}", "2 1", "3 1"]))
    # x at max allowed: 2x <= n
    w.add(multi([f"{n} {n // 2}" for n in range(2, 102)]))
    w.add(multi([f"{n} 1" for n in range(2, 102)]))
    for _ in range(10):
        t = rnd.randint(1, 100)
        cases = []
        for _ in range(t):
            n = rnd.randint(2, N)
            x = rnd.randint(1, n // 2)
            cases.append(f"{n} {x}")
        w.add(multi(cases))
    # small n exhaustive
    cases = []
    for n in range(2, 30):
        for x in range(1, n // 2 + 1):
            cases.append(f"{n} {x}")
    w.add(multi(cases[:100]))


if __name__ == "__main__":
    main(sys.argv[1])
