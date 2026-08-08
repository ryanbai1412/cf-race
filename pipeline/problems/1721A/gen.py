import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(px):
    return f"{px[0]}{px[1]}\n{px[2]}{px[3]}"


def main(outdir):
    rnd = random.Random(1721)
    w = Writer(outdir)
    # every pattern of equalities over a 4-letter alphabet (covers 1-4 distinct)
    letters = "abcd"
    cases = []
    for a in letters:
        for b in letters:
            for c in letters:
                for d in letters:
                    cases.append(case([a, b, c, d]))
    w.add(multi(cases[:1000]))
    # remaining patterns + z boundary
    w.add(multi(cases[1000:] + [case(["z"] * 4), case(["w", "x", "y", "z"])]))
    # random over full alphabet
    for _ in range(3):
        w.add(multi([case([rnd.choice(string.ascii_lowercase) for _ in range(4)])
                     for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
