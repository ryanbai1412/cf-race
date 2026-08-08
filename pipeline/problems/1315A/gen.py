import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1315)
    w = Writer(outdir)
    # edges: 1-wide screens, corners, center
    w.add(multi(["1 2 0 0", "1 2 0 1", "2 1 0 0", "2 1 1 0",
                 "10000 10000 0 0", "10000 10000 9999 9999",
                 "10000 10000 5000 5000", "1 10000 0 5000",
                 "10000 1 5000 0"]))
    # small random
    for _ in range(4):
        cases = []
        for _ in range(1000):
            a = rnd.randint(1, 8)
            b = rnd.randint(1, 8)
            if a == 1 and b == 1:
                b = 2
            cases.append(f"{a} {b} {rnd.randint(0, a - 1)} {rnd.randint(0, b - 1)}")
        w.add(multi(cases))
    # max-size random
    for _ in range(4):
        cases = []
        for _ in range(10000):
            a = rnd.randint(1, 10000)
            b = rnd.randint(1, 10000)
            if a == 1 and b == 1:
                b = 2
            cases.append(f"{a} {b} {rnd.randint(0, a - 1)} {rnd.randint(0, b - 1)}")
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
