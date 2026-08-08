import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

AB = string.ascii_lowercase


def case(strs):
    return f"{len(strs)}\n" + "\n".join(strs) + "\n"


def diverse(rnd, L):
    start = rnd.randint(0, 26 - L)
    s = list(AB[start:start + L])
    rnd.shuffle(s)
    return "".join(s)


def main(outdir):
    rnd = random.Random(1144)
    w = Writer(outdir)
    # single-letter strings (all diverse)
    w.add(case([c for c in AB]))
    # whole alphabet shuffled + a-z + z-a
    w.add(case([AB, AB[::-1], diverse(rnd, 26)]))
    # duplicates only
    w.add(case([c * 100 for c in AB]))
    # contiguous letters but one duplicate -> No
    w.add(case(["abcda", "aab", "bcdb", "zyxwz"]))
    # contiguous set except a single gap -> No
    w.add(case(["ac", "abd", "xz", "acb", "bdc", "aczb"]))
    # a/z non-adjacency trap
    w.add(case(["az", "za", "zab", "abz"]))
    # max size: 100 strings of length 100
    w.add(case([diverse(rnd, 26) * 4 if False else (AB * 4)[:100] for _ in range(100)]))
    w.add(case([("".join(rnd.choice(AB) for _ in range(100))) for _ in range(100)]))
    # random small mixes (diverse-biased)
    for _ in range(8):
        n = rnd.randint(1, 20)
        strs = []
        for _ in range(n):
            if rnd.random() < 0.5:
                strs.append(diverse(rnd, rnd.randint(1, 26)))
            else:
                L = rnd.randint(1, 6)
                strs.append("".join(rnd.choice(AB[:8]) for _ in range(L)))
        w.add(case(strs))


if __name__ == "__main__":
    main(sys.argv[1])
