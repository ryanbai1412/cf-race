import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def rand_s(rnd, k):
    return "".join(rnd.choice("AP") for _ in range(k))


def main(outdir):
    rnd = random.Random(1287)
    w = Writer(outdir)
    w.add(multi([case("P")]))
    w.add(multi([case("A")]))
    w.add(multi([case("A" + "P" * 99)]))
    w.add(multi([case("P" * 100)]))
    w.add(multi([case("A" * 100)]))
    w.add(multi([case("P" * 99 + "A")]))
    # max: 100 groups of 100
    w.add(multi([case(rand_s(rnd, 100)) for _ in range(100)]))
    w.add(multi([case("A" + "P" * 50 + "A" + "P" * 48)]))
    for _ in range(8):
        t = rnd.randint(1, 100)
        w.add(multi([case(rand_s(rnd, rnd.randint(1, 100)))
                     for _ in range(t)]))
    # sparse A strings
    for _ in range(3):
        t = rnd.randint(1, 50)
        cases = []
        for _ in range(t):
            k = rnd.randint(1, 100)
            s = ["P"] * k
            for _ in range(rnd.randint(0, 2)):
                s[rnd.randrange(k)] = "A"
            cases.append(case("".join(s)))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
