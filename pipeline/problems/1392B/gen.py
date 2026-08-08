import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

LIM = 10**9
KMAX = 10**18


def case(a, k):
    return f"{len(a)} {k}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1392)
    w = Writer(outdir)

    # minimal input, k = 1 and k = 2 on a single element
    w.add(multi([case([0], 1), case([0], 2), case([-LIM], 1), case([LIM], KMAX)]))
    # large arrays with extreme k parities
    # N is capped so each input file stays under 1 MB
    N = 70000
    big = [rnd.randint(-LIM, LIM) for _ in range(N)]
    w.add(multi([case(big, KMAX)]))
    w.add(multi([case(big, KMAX - 1)]))
    w.add(multi([case([-LIM if i % 2 else LIM for i in range(N)], 1)]))
    w.add(multi([case([-LIM if i % 2 else LIM for i in range(N)], 2)]))
    # all-equal arrays (max/min collapse)
    w.add(multi([case([5] * N, 1), case([5] * (N // 2), 10**17)]))
    # 100 test cases summing to N
    cases = []
    rem = N
    for i in range(100):
        n = rem // (100 - i)
        cases.append(case([rnd.randint(-LIM, LIM) for _ in range(n)],
                          rnd.randint(1, KMAX)))
        rem -= n
    w.add(multi(cases))
    # small random tests with small k
    for _ in range(10):
        t = rnd.randint(1, 100)
        cs = []
        for _ in range(t):
            n = rnd.randint(1, 6)
            hi = rnd.choice([3, 10, LIM])
            cs.append(case([rnd.randint(-hi, hi) for _ in range(n)],
                           rnd.randint(1, 8)))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
