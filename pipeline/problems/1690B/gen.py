import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b):
    return f"{len(a)}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}"


def rand_case(rnd, n, hi):
    a = [rnd.randint(0, hi) for _ in range(n)]
    mode = rnd.randint(0, 3)
    if mode == 0:  # valid: b derived from a with a fixed k
        k = rnd.randint(0, hi + 1)
        b = [max(x - k, 0) for x in a]
    elif mode == 1:  # near-valid: derive then perturb one element
        k = rnd.randint(0, hi + 1)
        b = [max(x - k, 0) for x in a]
        i = rnd.randrange(n)
        b[i] = max(0, b[i] + rnd.choice([-1, 1]))
    elif mode == 2:  # b == a
        b = list(a)
    else:  # fully random b
        b = [rnd.randint(0, hi) for _ in range(n)]
    return case(a, b)


def main(outdir):
    rnd = random.Random(16902)
    w = Writer(outdir)
    # hand-picked edge cases
    edge = [
        case([0], [0]),
        case([5], [0]),
        case([0], [5]),  # b > a -> NO
        case([1000000000], [0]),
        case([1000000000], [1000000000]),
        case([3, 0], [1, 0]),
        case([3, 1], [1, 0]),  # k=2, a2=1 -> 0 ok? max(1-2,0)=0 yes
        case([3, 3], [1, 0]),  # b2=0 but a2=3 > k=2 -> NO
        case([0, 0, 0], [0, 0, 0]),
        case([7, 7, 7], [7, 7, 7]),
        case([5, 4], [3, 3]),  # different k -> NO
    ]
    w.add(multi(edge))
    # small random cases, many per file
    for seed in range(6):
        cases = [rand_case(rnd, rnd.randint(1, 8), rnd.randint(1, 6)) for _ in range(150)]
        w.add(multi(cases))
    # medium random with large values
    for _ in range(3):
        cases = [rand_case(rnd, rnd.randint(1, 200), 10**9) for _ in range(30)]
        w.add(multi(cases))
    # max-size: sum n = 2*10^5 with small values (keeps file < 1MB)
    cases = []
    total = 0
    while total < 2 * 10**5 - 1000:
        n = rnd.randint(500, 2000)
        total += n
        cases.append(rand_case(rnd, n, 9))
    w.add(multi(cases))
    # large values, big n (kept under 1MB)
    cases = [rand_case(rnd, 20000, 10**9) for _ in range(2)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
