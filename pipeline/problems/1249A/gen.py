import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1249)
    w = Writer(outdir)
    # single student, and the two smallest consecutive/non-consecutive pairs
    w.add(multi([case([1]), case([100]), case([1, 2]), case([1, 3]),
                 case([99, 100]), case([2, 100])]))
    # max size: q=100, n=100 (must use all of 1..100 => consecutive => 2)
    w.add(multi([case(rnd.sample(range(1, 101), 100)) for _ in range(100)]))
    # all-even and all-odd sets (answer 1)
    w.add(multi([case(list(range(2, 101, 2))), case(list(range(1, 100, 2))),
                 case(list(range(1, 101, 3)))]))
    # exactly one consecutive pair hidden in an otherwise spread set
    cs = []
    for v in (1, 2, 50, 98, 99):
        base = [x for x in range(1, 101, 4)]
        s = set(base)
        s.add(v)
        s.add(v + 1)
        cs.append(case(sorted(s)))
    w.add(multi(cs))
    # shuffled input order (answer must not depend on order)
    w.add(multi([case(rnd.sample([5, 6, 20, 40], 4)) for _ in range(20)]))
    # random small tests
    for _ in range(7):
        q = rnd.randint(1, 100)
        cs = []
        for _ in range(q):
            n = rnd.randint(1, 6)
            cs.append(case(rnd.sample(range(1, 13), n)))
        w.add(multi(cs))
    # random mid tests over the full value range
    for _ in range(5):
        q = rnd.randint(1, 30)
        cs = []
        for _ in range(q):
            n = rnd.randint(1, 100)
            cs.append(case(rnd.sample(range(1, 101), n)))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
