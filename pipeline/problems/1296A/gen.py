import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(arr):
    return f"{len(arr)}\n" + " ".join(map(str, arr))


def main(outdir):
    rnd = random.Random(1296)
    w = Writer(outdir)
    w.add(multi([case([1]), case([2]), case([2000]), case([1999])]))
    w.add(multi([case([2] * 2000)]))
    w.add(multi([case([1] * 2000)]))
    w.add(multi([case([1] * 1999)]))
    w.add(multi([case([1] * 1999 + [2])]))
    # max t with n=1 each
    w.add(multi([case([rnd.randint(1, 2000)]) for _ in range(2000)]))
    for _ in range(8):
        cases = []
        budget = 2000
        while budget > 0 and len(cases) < 2000:
            n = rnd.randint(1, min(20, budget))
            budget -= n
            cases.append(case([rnd.randint(1, 2000) for _ in range(n)]))
        w.add(multi(cases))
    # all-even / all-odd mixes
    for par in (0, 1):
        cases = []
        for _ in range(50):
            n = rnd.randint(1, 10)
            cases.append(case([rnd.randint(1, 1000) * 2 - par
                               for _ in range(n)]))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
