import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_str(rnd, n, alpha=string.ascii_lowercase):
    return "".join(rnd.choice(alpha) for _ in range(n))


def main(outdir):
    rnd = random.Random(1673)
    w = Writer(outdir)
    # single chars (Bob wins), tiny odd/even strings
    w.add(multi(["a", "z", "aa", "az", "za", "aba", "zaz", "abz", "zba"]))
    # odd length where the end choice matters
    w.add(multi(["zzza", "azzz"[::-1], "azz", "zza", "bab", "yzy"]))
    # small random over a tiny alphabet (ties on ends)
    w.add(multi([rand_str(rnd, rnd.randint(1, 7), "ab") for _ in range(300)]))
    # small random full alphabet
    w.add(multi([rand_str(rnd, rnd.randint(1, 10)) for _ in range(300)]))
    # medium random
    w.add(multi([rand_str(rnd, rnd.randint(1, 200)) for _ in range(200)]))
    # max: sum |s| = 2e5 as one big string (odd and even variants)
    w.add(multi([rand_str(rnd, 200000)]))
    w.add(multi([rand_str(rnd, 199999)]))
    # max t: 5e4 strings, sum length <= 2e5
    w.add(multi([rand_str(rnd, rnd.randint(1, 3)) for _ in range(50000)]))


if __name__ == "__main__":
    main(sys.argv[1])
