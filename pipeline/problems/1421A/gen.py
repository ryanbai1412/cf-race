import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10**9


def main(outdir):
    rnd = random.Random(1421)
    w = Writer(outdir)
    # edge values
    edges = [1, 2, 3, MAX, MAX - 1, 2**29, 2**30 - 1, 536870912, 999999999]
    w.add(multi([f"{a} {b}" for a in edges for b in edges][:81]))
    # a == b cases
    w.add(multi([f"{v} {v}" for v in [1, 7, 12345, MAX]]))
    # small random
    for _ in range(3):
        cases = [f"{rnd.randint(1, 100)} {rnd.randint(1, 100)}" for _ in range(1000)]
        w.add(multi(cases))
    # large random, max t
    for _ in range(4):
        cases = [f"{rnd.randint(1, MAX)} {rnd.randint(1, MAX)}" for _ in range(10000)]
        w.add(multi(cases))
    # bit-pattern heavy
    cases = []
    for _ in range(10000):
        a = rnd.getrandbits(rnd.randint(1, 30)) | 1
        b = rnd.getrandbits(rnd.randint(1, 30)) | 1
        cases.append(f"{min(a, MAX)} {min(b, MAX)}")
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
