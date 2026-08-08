import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def main(outdir):
    rnd = random.Random(1167)
    w = Writer(outdir)
    # edge: minimal length strings
    w.add(multi(["1\n8", "1\n0", "11\n80000000000", "11\n00000000000", "11\n88888888888"]))
    # exactly boundary: 8 at last possible position / one past
    w.add(multi([case("0" * 89 + "8" + "0" * 10), case("0" * 90 + "8" + "0" * 9)]))
    # all eights, max size
    w.add(multi([case("8" * 100)] * 100))
    # no eights at all
    w.add(multi([case("".join(rnd.choice("01234567 9".replace(" ", "")) for _ in range(100))) for _ in range(100)]))
    # random with sparse eights
    for _ in range(8):
        t = rnd.randint(1, 100)
        cases = []
        for _ in range(t):
            n = rnd.randint(1, 100)
            s = "".join(rnd.choice("0123456789") if rnd.random() < 0.85 else "8" for _ in range(n))
            cases.append(case(s))
        w.add(multi(cases))
    # short strings only (1..15)
    for _ in range(4):
        t = rnd.randint(1, 100)
        cases = []
        for _ in range(t):
            n = rnd.randint(1, 15)
            cases.append(case("".join(rnd.choice("08") for _ in range(n))))
        w.add(multi(cases))
    # length exactly 11 with 8 in random spot
    cases = []
    for i in range(11):
        s = list("0" * 11)
        s[i] = "8"
        cases.append(case("".join(s)))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
