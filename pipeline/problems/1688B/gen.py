import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, hi=10**9, all_even=False):
    if all_even:
        a = [rnd.randint(1, hi // 2) * 2 for _ in range(n)]
    else:
        a = [rnd.randint(1, hi) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(16882)
    w = Writer(outdir)
    # edge: n=1 odd, n=1 even (large power of two), all odd
    w.add(multi(["1\n1", "1\n536870912", "1\n1000000000", "3\n1 3 5", "2\n2 2"]))
    w.add(multi([case(rnd, rnd.randint(1, 8), 16) for _ in range(200)]))
    w.add(multi([case(rnd, rnd.randint(1, 8), 16, all_even=True) for _ in range(200)]))
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(1, 1000), all_even=rnd.random() < 0.5) for _ in range(rnd.randint(1, 50))]))
    # large all-even case with big trailing zero counts (kept under 1MB input)
    w.add(multi([f"{120000}\n" + " ".join(str(rnd.randint(1, 1953) * 512) for _ in range(120000))]))
    w.add(multi([case(rnd, 90000, hi=10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
