import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(b):
    return f"{len(b)}\n{b}"


def main(outdir):
    rnd = random.Random(1474)
    w = Writer(outdir)

    # every short b (n <= 8) split over a few tests
    allb = []
    for n in range(1, 9):
        for m in range(1 << n):
            allb.append(format(m, f"0{n}b"))
    for i in range(0, len(allb), 200):
        w.add(multi([case(b) for b in allb[i:i + 200]]))

    # edge shapes
    w.add(multi([case("0"), case("1"), case("0" * 100), case("1" * 100),
                 case("01" * 50), case("10" * 50)]))

    # random tests
    for _ in range(4):
        cases = []
        for _ in range(rnd.randint(1, 100)):
            n = rnd.randint(1, 60)
            cases.append(case("".join(rnd.choice("01") for _ in range(n))))
        w.add(multi(cases))

    # biased strings (long runs)
    cases = []
    for _ in range(50):
        s = []
        while len(s) < 300:
            s.extend(rnd.choice("01") * rnd.randint(1, 12))
        cases.append(case("".join(s[:300])))
    w.add(multi(cases))

    # max total length: one string of 1e5
    w.add(multi([case("".join(rnd.choice("01") for _ in range(10 ** 5)))]))
    # max t with total length 1e5
    cases = [case("".join(rnd.choice("01") for _ in range(100))) for _ in range(1000)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
