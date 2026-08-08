import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MX = 10**8


def case(a, b, c):
    return f"{a} {b} {c}"


def main(outdir):
    rnd = random.Random(1622)
    w = Writer(outdir)

    # edges: all ones, minimal YES/NO shapes, max values
    w.add(
        multi(
            [
                case(1, 1, 1),
                case(1, 1, 2),
                case(2, 1, 1),
                case(1, 2, 1),
                case(MX, MX, MX),
                case(MX, MX - 1, 1),
                case(MX, MX, 2 * 10**7),
                case(1, 1, MX),
                case(MX - 1, MX, MX),
                case(3, 3, 3),
            ]
        )
    )

    # small exhaustive-ish random (l <= 10)
    for _ in range(3):
        w.add(multi([case(*[rnd.randint(1, 10) for _ in range(3)]) for _ in range(10**4)]))

    # structured: sum cases, equal-pair cases (even/odd third), shuffled
    cases = []
    for _ in range(10**4):
        kind = rnd.randrange(4)
        if kind == 0:
            a, b = rnd.randint(1, MX // 2), rnd.randint(1, MX // 2)
            ls = [a, b, a + b]
        elif kind == 1:
            a = rnd.randint(1, MX)
            ls = [a, a, rnd.randint(1, MX)]
        elif kind == 2:
            a = rnd.randint(1, MX)
            ls = [a, a, 2 * rnd.randint(1, MX // 2)]
        else:
            ls = [rnd.randint(1, MX) for _ in range(3)]
        rnd.shuffle(ls)
        cases.append(case(*ls))
    w.add(multi(cases))

    # pure large random, max t
    w.add(multi([case(*[rnd.randint(1, MX) for _ in range(3)]) for _ in range(10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
