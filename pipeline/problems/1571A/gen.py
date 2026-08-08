import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

CH = "<>="


def rand_s(rnd, n, weights):
    return "".join(rnd.choices(CH, weights=weights, k=n))


def main(outdir):
    rnd = random.Random(1571)
    w = Writer(outdir)

    # edges: single chars, pure strings, boundary mixes
    w.add(multi(["<", ">", "=", "<>", "><", "<=", "=>", "==",
                 "=" * 100, "<" * 100, ">" * 100,
                 "=" * 99 + "<", ">" + "=" * 99]))
    # random with varying composition (some without '<' or '>')
    for weights in ((1, 1, 1), (5, 1, 1), (1, 5, 1), (1, 1, 5), (1, 0, 5), (0, 1, 5)):
        w.add(multi([rand_s(rnd, rnd.randint(1, 100), weights) for _ in range(100)]))
    # max: t=500, len 100
    w.add(multi([rand_s(rnd, 100, (1, 1, 1)) for _ in range(500)]))


if __name__ == "__main__":
    main(sys.argv[1])
