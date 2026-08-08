import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(r1, r2):
    return f"{len(r1)}\n{r1}\n{r2}"


def main(outdir):
    rnd = random.Random(17222)
    w = Writer(outdir)
    # n=1: all 9 combinations
    w.add(multi([case(a, b) for a in "RGB" for b in "RGB"]))
    # equal-looking rows (G/B swapped), and rows differing only at the ends
    cases = []
    for _ in range(30):
        n = rnd.randint(1, 100)
        r1 = "".join(rnd.choice("RGB") for _ in range(n))
        r2 = "".join(c if c == "R" else rnd.choice("GB") for c in r1)
        cases.append(case(r1, r2))
    for _ in range(10):
        n = rnd.randint(2, 100)
        r1 = "".join(rnd.choice("RGB") for _ in range(n))
        r2 = ("R" if r1[0] != "R" else "G") + r1[1:]
        cases.append(case(r1, r2))
        r2 = r1[:-1] + ("R" if r1[-1] != "R" else "B")
        cases.append(case(r1, r2))
    w.add(multi(cases))
    # random rows
    for _ in range(3):
        cases = []
        for _ in range(100):
            n = rnd.randint(1, 100)
            r1 = "".join(rnd.choice("RGB") for _ in range(n))
            if rnd.random() < 0.5:
                r2 = "".join(rnd.choice("RGB") for _ in range(n))
            else:
                r2 = "".join(c if c == "R" else rnd.choice("GB") for c in r1)
            cases.append(case(r1, r2))
        w.add(multi(cases))
    # max-size test: t=100, n=100
    w.add(multi([case("".join(rnd.choice("RGB") for _ in range(100)),
                      "".join(rnd.choice("RGB") for _ in range(100)))
                 for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
