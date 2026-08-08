import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_ticket(rnd):
    return "".join(str(rnd.randint(0, 9)) for _ in range(6))


def lucky_ticket(rnd):
    while True:
        s = rand_ticket(rnd)
        d = [int(c) for c in s]
        if d[0] + d[1] + d[2] == d[3] + d[4] + d[5]:
            return s


def main(outdir):
    rnd = random.Random(1676)
    w = Writer(outdir)
    # edges: all zeros, all nines, leading zeros, off-by-one sums
    w.add(multi(["000000", "999999", "000001", "100000", "011010", "999998", "899999"]))
    # half lucky / half not, random
    for _ in range(6):
        t = rnd.randint(1, 1000)
        cs = [lucky_ticket(rnd) if rnd.random() < 0.5 else rand_ticket(rnd) for _ in range(t)]
        w.add(multi(cs))
    # max t, fully random
    w.add(multi([rand_ticket(rnd) for _ in range(1000)]))
    # max t, all lucky
    w.add(multi([lucky_ticket(rnd) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
