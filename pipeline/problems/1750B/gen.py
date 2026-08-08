import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def main(outdir):
    rnd = random.Random(1750)
    N = 2 * 10**5
    w = Writer(outdir)
    # edges: single chars, all-same max, half/half blocks, alternating
    w.add(multi([case("0"), case("1"), case("01"), case("10")]))
    w.add(multi([case("1" * N)]))
    w.add(multi([case("0" * (N // 2) + "1" * (N // 2))]))
    w.add(multi([case("01" * (N // 2))]))
    # long run inside mixed string (run^2 vs x*y trap)
    s = ("01" * 100) + "1" * 1000 + ("10" * 100)
    w.add(multi([case(s)]))
    # max t with tiny strings
    w.add(multi([case("".join(rnd.choice("01") for _ in range(rnd.randint(1, 3)))) for _ in range(10**5)]))
    # random mixed
    for _ in range(6):
        cases = []
        for _ in range(rnd.randint(1, 50)):
            n = rnd.randint(1, 300)
            p = rnd.random()
            cases.append(case("".join("1" if rnd.random() < p else "0" for _ in range(n))))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
