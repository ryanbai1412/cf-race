import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

N = 200000


def case(seq):
    return f"{len(seq)}\n" + " ".join(map(str, seq)) + "\n"


def main(outdir):
    rnd = random.Random(1143)
    w = Writer(outdir)
    # minimum n
    w.add(case([0, 1]))
    w.add(case([1, 0]))
    # all lefts then the single right at the end (answer n)
    w.add(case([0] * (N - 1) + [1]))
    w.add(case([1] + [0] * (N - 1)))
    # blocks
    w.add(case([0] * (N // 2) + [1] * (N // 2)))
    w.add(case([1] * (N // 2) + [0] * (N // 2)))
    # alternating, max size
    w.add(case([i % 2 for i in range(N)]))
    # small randoms
    for _ in range(5):
        n = rnd.randint(2, 12)
        while True:
            s = [rnd.randint(0, 1) for _ in range(n)]
            if 0 in s and 1 in s:
                break
        w.add(case(s))
    # large randoms with skewed ratios
    for p in (0.5, 0.1, 0.9, 0.98):
        s = [0 if rnd.random() < p else 1 for _ in range(N)]
        s[rnd.randrange(N)], s[rnd.randrange(N)] = 0, 1
        if 0 not in s or 1 not in s:
            s[0], s[1] = 0, 1
        w.add(case(s))


if __name__ == "__main__":
    main(sys.argv[1])
