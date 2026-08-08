import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_yes(rnd, half):
    """B count == A+C count -> YES."""
    other = [rnd.choice("AC") for _ in range(half)]
    s = list("B" * half) + other
    rnd.shuffle(s)
    return "".join(s)


def rand_any(rnd, n):
    return "".join(rnd.choices("ABC", k=n))


def main(outdir):
    rnd = random.Random(1579)
    w = Writer(outdir)

    # edges: single letters, tiny strings, extremes
    w.add(multi(["A", "B", "C", "AB", "BC", "BA", "CB", "AC", "BB",
                 "ABC", "BBB", "AAB", "BBC"]))
    w.add(multi(["B" * 50, "A" * 50, "C" * 50, "AB" * 25, "BC" * 25,
                 "B" * 25 + "A" * 13 + "C" * 12]))
    # guaranteed YES cases of all sizes
    w.add(multi([rand_yes(rnd, h) for h in range(1, 26)]))
    # random (mostly NO) and near-balanced
    w.add(multi([rand_any(rnd, rnd.randint(1, 50)) for _ in range(300)]))
    # max: t=1000 len 50, mix of YES and random
    w.add(multi([rand_yes(rnd, 25) if i % 2 else rand_any(rnd, 50)
                 for i in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
