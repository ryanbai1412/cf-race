import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1303)
    w = Writer(outdir)
    w.add(multi(["0", "1", "01", "10", "101", "010"]))
    w.add(multi(["0" * 100, "1" * 100,
                 "1" + "0" * 98 + "1",
                 "0" * 49 + "1" + "0" * 50]))
    for _ in range(8):
        t = rnd.randint(1, 100)
        cases = []
        for _ in range(t):
            n = rnd.randint(1, 100)
            p = rnd.random()
            cases.append("".join("1" if rnd.random() < p else "0"
                                 for _ in range(n)))
        w.add(multi(cases))
    # sparse ones
    cases = []
    for _ in range(100):
        n = rnd.randint(2, 100)
        s = ["0"] * n
        for _ in range(rnd.randint(1, 3)):
            s[rnd.randrange(n)] = "1"
        cases.append("".join(s))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
