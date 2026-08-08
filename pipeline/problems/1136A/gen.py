import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(lens, k):
    lines = [str(len(lens))]
    p = 1
    for L in lens:
        lines.append(f"{p} {p + L - 1}")
        p += L
    lines.append(str(k))
    return "\n".join(lines) + "\n"


def main(outdir):
    rnd = random.Random(1136)
    w = Writer(outdir)
    # single chapter, k on first / last page
    w.add(case([1], 1))
    w.add(case([100], 1))
    w.add(case([100], 100))
    # k = 1 (nothing read) and k on the very last page
    w.add(case([1] * 100, 1))
    w.add(case([1] * 100, 100))
    w.add(case([100] * 100, 10000))
    # k exactly at a chapter boundary (last page of chapter 3)
    w.add(case([5, 5, 5, 5, 5], 15))
    w.add(case([5, 5, 5, 5, 5], 16))
    w.add(case([5, 5, 5, 5, 5], 11))
    # random
    for _ in range(8):
        n = rnd.randint(1, 100)
        lens = [rnd.randint(1, 100) for _ in range(n)]
        w.add(case(lens, rnd.randint(1, sum(lens))))


if __name__ == "__main__":
    main(sys.argv[1])
