import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def rand_case(rnd, n):
    a = [rnd.randint(0, 1) for _ in range(n)]
    a[0] = a[-1] = 1
    return a


def main(outdir):
    rnd = random.Random(1649)
    w = Writer(outdir)
    # edge cases
    w.add(multi([case([1, 1]), case([1, 0, 1]), case([1] * 100)]))
    # one big water block spanning almost everything
    w.add(multi([case([1] + [0] * 98 + [1])]))
    # water at very start / very end of the interior
    w.add(multi([case([1, 0] + [1] * 98), case([1] * 98 + [0, 1]),
                 case([1, 0] + [1] * 96 + [0, 1])]))
    # small exhaustive-ish random
    for _ in range(4):
        w.add(multi([case(rand_case(rnd, rnd.randint(2, 10)))
                     for _ in range(100)]))
    # max size
    for _ in range(3):
        w.add(multi([case(rand_case(rnd, 100)) for _ in range(100)]))
    # sparse water
    w.add(multi([case([1] * i + [0] + [1] * (99 - i)) for i in range(1, 99, 10)]))


if __name__ == "__main__":
    main(sys.argv[1])
