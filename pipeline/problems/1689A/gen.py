import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, m, k, nalpha=26):
    letters = list(string.ascii_lowercase[:nalpha])
    rnd.shuffle(letters)
    cut = rnd.randint(1, len(letters) - 1)
    sa, sb = letters[:cut], letters[cut:]
    a = "".join(rnd.choice(sa) for _ in range(n))
    b = "".join(rnd.choice(sb) for _ in range(m))
    return f"{n} {m} {k}\n{a}\n{b}"


def main(outdir):
    rnd = random.Random(1689)
    w = Writer(outdir)
    # edge: sizes 1, k=1, single letters
    w.add(multi(["1 1 1\na\nb", "1 1 100\nz\na", "3 1 1\naaa\nb", "1 3 1\nb\naaa"]))
    # tiny alphabets force long runs hitting k
    w.add(multi([case(rnd, rnd.randint(1, 10), rnd.randint(1, 10), rnd.randint(1, 3), 2) for _ in range(200)]))
    w.add(multi([case(rnd, rnd.randint(1, 30), rnd.randint(1, 30), rnd.randint(1, 5), 4) for _ in range(200)]))
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(1, 100), rnd.randint(1, 100), rnd.randint(1, 100)) for _ in range(rnd.randint(1, 50))]))
    # max: t=100 full-size, small k
    w.add(multi([case(rnd, 100, 100, rnd.randint(1, 3), rnd.randint(2, 6)) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
