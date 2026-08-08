import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, k1, k2, w, b):
    return f"{n} {k1} {k2}\n{w} {b}"


def main(outdir):
    rnd = random.Random(1499)
    w = Writer(outdir)
    # all tiny cases n<=3 exhaustively
    cases = []
    for n in range(1, 4):
        for k1 in range(n + 1):
            for k2 in range(n + 1):
                for ww in range(n + 1):
                    for bb in range(n + 1):
                        cases.append(case(n, k1, k2, ww, bb))
    for i in range(0, len(cases), 3000):
        w.add(multi(cases[i : i + 3000]))
    # boundary-heavy random cases
    for _ in range(5):
        cs = []
        for _ in range(3000):
            n = rnd.randint(1, 1000)
            k1, k2 = rnd.randint(0, n), rnd.randint(0, n)
            white, black = k1 + k2, 2 * n - k1 - k2
            ww = rnd.choice([rnd.randint(0, n), min(n, white // 2), min(n, white // 2 + 1)])
            bb = rnd.choice([rnd.randint(0, n), min(n, black // 2), min(n, black // 2 + 1)])
            cs.append(case(n, k1, k2, ww, bb))
        w.add(multi(cs))
    # max sizes
    w.add(multi([case(1000, 1000, 1000, 1000, 0), case(1000, 0, 0, 0, 1000), case(1000, 500, 500, 500, 500)]))


if __name__ == "__main__":
    main(sys.argv[1])
