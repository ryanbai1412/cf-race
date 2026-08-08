import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, maxv=10**6, maxtm=10**6, tight=False):
    # build n pairs a_i < b_i with b_i < a_{i+1}, all <= maxv
    cuts = sorted(rnd.sample(range(1, maxv + 1), 2 * n))
    if tight:
        cuts = list(range(1, 2 * n + 1))
    lines = [f"{cuts[2 * i]} {cuts[2 * i + 1]}" for i in range(n)]
    tms = [rnd.choice([0, 1, rnd.randint(0, maxtm)]) for _ in range(n)]
    return f"{n}\n" + "\n".join(lines) + "\n" + " ".join(map(str, tms))


def main(outdir):
    rnd = random.Random(1501)
    w = Writer(outdir)
    # minimal cases
    w.add(multi(["1\n1 2\n0", "1\n1 2\n1000000", "1\n999999 1000000\n1000000"]))
    # tiny n, tight schedules
    w.add(multi([case(rnd, rnd.randint(1, 3), tight=True) for _ in range(50)]))
    # small random
    for _ in range(5):
        w.add(multi([case(rnd, rnd.randint(1, 10), maxv=100, maxtm=10) for _ in range(60)]))
    # medium random
    for _ in range(5):
        w.add(multi([case(rnd, rnd.randint(1, 100)) for _ in range(30)]))
    # max size: t=100, n=100, extreme values
    w.add(multi([case(rnd, 100) for _ in range(100)]))
    w.add(multi([case(rnd, 100, maxtm=0) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
