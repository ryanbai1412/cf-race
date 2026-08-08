import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_case(rnd):
    m = rnd.randint(1, 50)
    b = rnd.sample(range(1, 51), m)
    if rnd.random() < 0.5:
        # solvable-ish: complete to a permutation of 1..n, s = missing sum
        n = max(max(b), rnd.randint(1, 60))
        missing = [x for x in range(1, n + 1) if x not in b]
        s = sum(missing)
        if not 1 <= s <= 1000:
            s = rnd.randint(1, 1000)
    else:
        s = rnd.randint(1, 1000)
    return f"{m} {s}\n{' '.join(map(str, b))}"


def main(outdir):
    rnd = random.Random(1759)
    w = Writer(outdir)
    # edge cases
    w.add(
        multi(
            [
                "1 1\n2",  # append 1 -> [2,1] YES
                "1 1\n1",  # need sum 1 but 1 taken -> NO
                "1 1000\n50",
                "1 2\n1",  # 2 -> YES
                "1 3\n1",  # 2+? 3=3 taken? add 2 then s=1 left, 3>1 -> NO? actually 2,3? 2+3=5 no; s=3: add 2 (s=1), stop -> NO
                "50 1000\n" + " ".join(map(str, range(1, 51))),
            ]
        )
    )
    # full permutation prefix cases
    cases = []
    for n in range(2, 51):
        b = list(range(1, n + 1))
        rnd.shuffle(b)
        k = rnd.randint(1, n - 1)
        kept = b[:k]
        s = sum(b[k:])
        cases.append(f"{len(kept)} {s}\n{' '.join(map(str, kept))}")
    w.add(multi(cases))
    # random, max t
    for _ in range(6):
        w.add(multi([rand_case(rnd) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
