import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1604)
    w = Writer(outdir)
    # edge: n=1, already satisfied, huge values
    w.add(multi([
        case([1]),
        case([10**9]),
        case(list(range(1, 101))),
        case([10**9] * 100),
        case([1] * 100),
    ]))
    # random small
    for _ in range(5):
        w.add(multi([
            case([rnd.randint(1, 8) for _ in range(rnd.randint(1, 6))])
            for _ in range(200)
        ]))
    # random medium values
    for _ in range(4):
        w.add(multi([
            case([rnd.randint(1, 200) for _ in range(rnd.randint(1, 100))])
            for _ in range(200)
        ]))
    # random huge values
    for _ in range(3):
        w.add(multi([
            case([rnd.randint(1, 10**9) for _ in range(rnd.randint(1, 100))])
            for _ in range(200)
        ]))
    # max-size: t = 200, n = 100
    w.add(multi([
        case([rnd.randint(1, 10**9) for _ in range(100)])
        for _ in range(200)
    ]))


if __name__ == "__main__":
    main(sys.argv[1])
