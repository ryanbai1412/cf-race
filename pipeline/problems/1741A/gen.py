import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

ALL = ["M"] + ["X" * k + c for c in "SL" for k in range(50)]


def rand_size(rnd, max_x=49):
    if rnd.random() < 0.1:
        return "M"
    return "X" * rnd.randint(0, max_x) + rnd.choice("SL")


def main(outdir):
    rnd = random.Random(1741)
    w = Writer(outdir)
    # edges: equal pairs of every size, M against everything
    w.add(multi([f"{s} {s}" for s in ALL]))
    w.add(multi([f"M {s}" for s in ALL] + [f"{s} M" for s in ALL]))
    # adjacent sizes (off-by-one X counts, both letters)
    adj = []
    for k in range(49):
        for c in "SL":
            adj.append(f"{'X' * k + c} {'X' * (k + 1) + c}")
            adj.append(f"{'X' * (k + 1) + c} {'X' * k + c}")
    w.add(multi(adj))
    # S vs L with all X combos
    w.add(multi([f"{'X' * i}S {'X' * j}L"
                 for i in range(0, 50, 7) for j in range(0, 50, 7)]))
    # random small-X and full-range, max t
    w.add(multi([f"{rand_size(rnd, 3)} {rand_size(rnd, 3)}"
                 for _ in range(10**4)]))
    w.add(multi([f"{rand_size(rnd)} {rand_size(rnd)}"
                 for _ in range(10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
