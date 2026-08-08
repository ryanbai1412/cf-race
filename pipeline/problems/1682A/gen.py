import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def pal(rnd, n, alpha):
    half = [rnd.choice(alpha) for _ in range(n // 2)]
    mid = [rnd.choice(alpha)] if n % 2 else []
    s = half + mid + half[::-1]
    return f"{n}\n{''.join(s)}"


def main(outdir):
    rnd = random.Random(1682)
    w = Writer(outdir)
    # edge: n=2, all-same strings
    w.add(multi(["2\naa", "3\naaa", f"{100000}\n" + "a" * 100000]))
    # small alphabet => long central runs
    w.add(multi([pal(rnd, rnd.randint(2, 30), "ab") for _ in range(300)]))
    w.add(multi([pal(rnd, rnd.randint(2, 100), "abc") for _ in range(200)]))
    w.add(multi([pal(rnd, rnd.randint(2, 50), string.ascii_lowercase) for _ in range(200)]))
    # max size: sum n = 2e5
    w.add(multi([pal(rnd, 100000, "ab"), pal(rnd, 99999, "ab")]))
    w.add(multi([pal(rnd, 1000, "abcd") for _ in range(200)]))


if __name__ == "__main__":
    main(sys.argv[1])
