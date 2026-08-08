import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b):
    n = len(a)
    return f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b))


def rand_case(rnd, max_n=100):
    n = rnd.randint(1, max_n)
    a = [rnd.randint(0, 1) for _ in range(n)]
    b = [rnd.randint(0, 1) for _ in range(n)]
    return case(a, b)


def perm_case(rnd, max_n=100):
    # b is a shuffle of a: rearrange-only should win
    n = rnd.randint(1, max_n)
    a = [rnd.randint(0, 1) for _ in range(n)]
    b = a[:]
    rnd.shuffle(b)
    return case(a, b)


def main(outdir):
    rnd = random.Random(1736)
    w = Writer(outdir)
    # edges: n=1, equal arrays, complements, all-0 vs all-1
    w.add(multi([case([0], [0]), case([0], [1]), case([1], [1]),
                 case([0] * 100, [1] * 100), case([1] * 100, [1] * 100),
                 case([0, 1] * 50, [1, 0] * 50),
                 case([1] * 50 + [0] * 50, [0] * 50 + [1] * 50)]))
    # shuffles (answer <= 1)
    w.add(multi([perm_case(rnd) for _ in range(200)]))
    w.add(multi([perm_case(rnd, max_n=5) for _ in range(400)]))
    # small random (flip-only vs rearrange trade-off)
    w.add(multi([rand_case(rnd, max_n=4) for _ in range(400)]))
    w.add(multi([rand_case(rnd, max_n=10) for _ in range(400)]))
    # max size random
    w.add(multi([rand_case(rnd) for _ in range(400)]))


if __name__ == "__main__":
    main(sys.argv[1])
