import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, h, a):
    return f"{n} {h}\n" + " ".join(map(str, a))


def rand_case(rnd, n_max, h_max, a_max):
    n = rnd.randint(2, n_max)
    h = rnd.randint(1, h_max)
    a = [rnd.randint(1, a_max) for _ in range(n)]
    return case(n, h, a)


def main(outdir):
    rnd = random.Random(1592)
    w = Writer(outdir)
    # edge: minimal
    w.add(multi([case(2, 1, [1, 1])]))
    # edge: one-shot kill, exact-pair kill, remainder needs 1 or 2 hits
    w.add(multi([
        case(2, 10, [10, 1]),
        case(2, 10, [7, 3]),
        case(2, 10, [7, 2]),
        case(2, 10, [4, 4]),
        case(3, 11, [2, 1, 7]),
    ]))
    # edge: huge H with tiny damage (max pair count)
    w.add(multi([case(2, 10**9, [1, 1]), case(2, 10**9, [10**9, 10**9])]))
    # duplicates of the max weapon
    w.add(multi([case(5, 999999937, [5, 5, 5, 1, 2])]))
    # random small
    for _ in range(6):
        w.add(multi([rand_case(rnd, 6, 30, 8) for _ in range(200)]))
    # random large values
    for _ in range(4):
        w.add(multi([rand_case(rnd, 50, 10**9, 10**9) for _ in range(100)]))
    # max-size: sum n = 2*10^5, t = 10^5 with n=2
    big = [rand_case(rnd, 2, 10**9, 10**9) for _ in range(10**5)]
    w.add(multi(big))
    # one test with n = 10^3
    w.add(multi([rand_case(rnd, 1000, 10**9, 10**9) for _ in range(200)]))


if __name__ == "__main__":
    main(sys.argv[1])
