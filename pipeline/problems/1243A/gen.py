import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1243)
    w = Writer(outdir)
    # smallest possible input
    w.add(multi([case([1])]))
    # max size: k=10, n=1000 each
    w.add(multi([case([1000] * 1000) for _ in range(10)]))
    w.add(multi([case([rnd.randint(1, 1000) for _ in range(1000)]) for _ in range(10)]))
    # all ones (answer 1) and all n (answer n)
    w.add(multi([case([1] * 1000), case([1000] * 1000), case([1] * 999 + [1000])]))
    # answer exactly at a boundary: exactly s planks of height s
    cs = []
    for s in (1, 2, 3, 500, 999, 1000):
        a = [s] * s + [1] * (1000 - s)
        cs.append(case(a))
        b = [s] * (s - 1) + [1] * (1000 - s + 1)  # one short => answer s-1 or less
        cs.append(case(b))
    w.add(multi(cs))
    # increasing / decreasing sequences
    w.add(multi([case(list(range(1, 1001))), case(list(range(1000, 0, -1)))]))
    # small exhaustive-ish random tests
    for _ in range(6):
        k = rnd.randint(1, 10)
        cs = []
        for _ in range(k):
            n = rnd.randint(1, 8)
            cs.append(case([rnd.randint(1, n) for _ in range(n)]))
        w.add(multi(cs))
    # random mid-size
    for _ in range(6):
        k = rnd.randint(1, 10)
        cs = []
        for _ in range(k):
            n = rnd.randint(1, 200)
            cs.append(case([rnd.randint(1, n) for _ in range(n)]))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
