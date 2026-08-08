import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


M = 10 ** 9


def main(outdir):
    rnd = random.Random(1185)
    w = Writer(outdir)
    fixed = [(5, 2, 6, 3), (3, 1, 5, 6), (8, 3, 3, 2), (2, 3, 10, 4),
             (1, 1, 1, 1), (1, 1, 1, M), (M, M, M, M), (1, M, M // 2, M),
             (1, 2, 3, 1), (7, 7, 7, 1), (1, 1, M, 1)]
    for t in fixed:
        w.add(" ".join(map(str, t)))
    for _ in range(5):
        w.add(" ".join(str(rnd.randint(1, M)) for _ in range(4)))
    for _ in range(4):
        base = rnd.randint(1, M - 10)
        vals = [base + rnd.randint(0, 10) for _ in range(3)] + [rnd.randint(1, M)]
        w.add(" ".join(map(str, vals)))


if __name__ == "__main__":
    main(sys.argv[1])
