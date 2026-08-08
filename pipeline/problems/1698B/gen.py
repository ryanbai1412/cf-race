import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(k, a):
    return f"{len(a)} {k}\n{' '.join(map(str, a))}"


def rand_case(rnd, n, k, hi):
    return case(k, [rnd.randint(1, hi) for _ in range(n)])


def spiky(rnd, n, hi):
    """Alternating tall/short piles (many initially too-tall)."""
    return [rnd.randint(2 * hi, 3 * hi) if i % 2 else rnd.randint(1, hi)
            for i in range(n)]


def main(outdir):
    rnd = random.Random(16982)
    w = Writer(outdir)
    # edge cases
    edge = [
        case(1, [1, 1, 1]),
        case(3, [1, 1, 1]),
        case(2, [1, 10**9, 1]),
        case(1, [1, 10**9, 1]),
        case(2, [1, 1, 1, 1]),
        case(1, [5, 1, 5, 1, 5]),
        case(4, [1, 100, 1, 100, 1]),
        case(2, [1, 3, 1, 3, 1]),
    ]
    w.add(multi(edge))
    # small randoms across k values
    for _ in range(4):
        cases = []
        for _ in range(150):
            n = rnd.randint(3, 8)
            k = rnd.randint(1, n)
            cases.append(rand_case(rnd, n, k, rnd.choice([3, 10])))
        w.add(multi(cases))
    # spiky arrays (near the too-tall threshold)
    cases = []
    for _ in range(60):
        n = rnd.randint(3, 300)
        k = rnd.randint(1, n)
        cases.append(case(k, spiky(rnd, n, rnd.choice([2, 5, 100]))))
    w.add(multi(cases))
    # k = 1 on larger n (formula branch)
    cases = [rand_case(rnd, rnd.randint(3, 1000), 1, 10**9) for _ in range(30)]
    w.add(multi(cases))
    # max-size: sum n = 2*10^5, small values (file < 1MB)
    cases = []
    total = 0
    while total < 2 * 10**5 - 3000:
        n = rnd.randint(1000, 5000)
        total += n
        k = rnd.choice([1, 2, 3, n // 2, n])
        cases.append(case(k, spiky(rnd, n, 3)))
    w.add(multi(cases))
    # big values, large n (kept < 1MB)
    cases = [case(rnd.choice([1, 2]),
                  [rnd.randint(1, 10**9) for _ in range(40000)])]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
