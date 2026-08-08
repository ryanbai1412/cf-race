import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def num(rnd, ndigits):
    return "".join(rnd.choice("123456789") for _ in range(ndigits))


def main(outdir):
    rnd = random.Random(1684)
    w = Writer(outdir)
    # edge: all two-digit numbers, min/max values
    w.add(multi([f"{a}{b}" for a in "123456789" for b in "123456789"]))
    w.add(multi(["10" if False else "11", "99", "111", "999999999", "1000000000".replace("0", "9")]))
    # random lengths 2..10 (n <= 1e9 has up to 10 digits: 1000000000 has a zero, so max 9 nines... use <=9 digits, plus 10-digit not possible without zeros except none <= 1e9)
    for _ in range(6):
        w.add(multi([num(rnd, rnd.randint(2, 9)) for _ in range(rnd.randint(1, 200))]))
    # max: t = 1e4
    w.add(multi([num(rnd, rnd.randint(2, 9)) for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
