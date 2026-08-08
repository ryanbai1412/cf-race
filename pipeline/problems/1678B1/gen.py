import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

N_MAX = 2 * 10**5


def case(s):
    return f"{len(s)}\n{s}"


def rand_str(rnd, n):
    return "".join(rnd.choice("01") for _ in range(n))


def main(outdir):
    rnd = random.Random(16781)
    w = Writer(outdir)
    # edges: n=2, alternating (worst), already good, all same
    edge = [
        case("00"),
        case("01"),
        case("10"),
        case("11"),
        case("01" * 100),
        case("10" * 100),
        case("0" * 200),
        case("0011" * 50),
    ]
    w.add(multi(edge))
    # random small
    for _ in range(5):
        cs = []
        for _ in range(rnd.randint(1, 100)):
            n = rnd.randrange(2, 21, 2)
            cs.append(case(rand_str(rnd, n)))
        w.add(multi(cs))
    # random medium, block-structured strings
    for _ in range(3):
        cs = []
        total = 0
        while total < 10**5:
            n = rnd.randrange(2, 2001, 2)
            total += n
            s = ""
            while len(s) < n:
                s += rnd.choice("01") * rnd.randint(1, 10)
            cs.append(case(s[:n]))
        w.add(multi(cs))
    # max single string: alternating (max answer), random
    w.add(multi([case("01" * (N_MAX // 2))]))
    w.add(multi([case(rand_str(rnd, N_MAX))]))
    # many tiny tests (t = 10000)
    cs = [case(rand_str(rnd, rnd.randrange(2, 21, 2))) for _ in range(10000)]
    w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
