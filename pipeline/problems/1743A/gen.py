import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(forbidden):
    return f"{len(forbidden)}\n" + " ".join(map(str, sorted(forbidden)))


def main(outdir):
    rnd = random.Random(1743)
    w = Writer(outdir)
    # every n from 1..8 with prefix digits
    w.add(multi([case(list(range(n))) for n in range(1, 9)]))
    # every n with suffix digits
    w.add(multi([case(list(range(10 - n, 10))) for n in range(1, 9)]))
    # max t=200 random
    for _ in range(5):
        cases = []
        for _ in range(200):
            n = rnd.randint(1, 8)
            cases.append(case(rnd.sample(range(10), n)))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
