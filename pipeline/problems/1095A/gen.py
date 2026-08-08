import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

AB = "abcdefghijklmnopqrstuvwxyz"


def encrypt(s):
    return "".join(c * (i + 1) for i, c in enumerate(s))


def case(s):
    t = encrypt(s)
    return f"{len(t)}\n{t}\n"


def main(outdir):
    rnd = random.Random(1095)
    w = Writer(outdir)
    # every valid length of s (n = m(m+1)/2 <= 55 => m <= 10)
    for m in range(1, 11):
        w.add(case("".join(rnd.choice(AB) for _ in range(m))))
    # all same letter, maximum size
    w.add(case("a" * 10))
    w.add(case("z" * 10))
    # first ten distinct letters
    w.add(case(AB[:10]))
    w.add(case(AB[-10:]))
    # a few extra randoms at max length
    for _ in range(5):
        w.add(case("".join(rnd.choice("ab") for _ in range(10))))


if __name__ == "__main__":
    main(sys.argv[1])
