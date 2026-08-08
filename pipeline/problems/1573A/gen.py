import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def rand_s(rnd, n, p0=0.3):
    return "".join("0" if rnd.random() < p0 else str(rnd.randint(1, 9))
                   for _ in range(n))


def main(outdir):
    rnd = random.Random(1573)
    w = Writer(outdir)

    # edges: n=1 all digits, leading zeros, trailing zeros
    w.add(multi([case(str(d)) for d in range(10)]))
    w.add(multi([case("0" * 100), case("9" * 100), case("0" * 99 + "1"),
                 case("1" + "0" * 99), case("10"), case("01"), case("90"), case("09")]))
    # sparse / dense nonzero digits
    for p0 in (0.9, 0.5, 0.05):
        w.add(multi([case(rand_s(rnd, rnd.randint(1, 100), p0)) for _ in range(200)]))
    # max: t=1000, n=100
    w.add(multi([case(rand_s(rnd, 100, rnd.random())) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
