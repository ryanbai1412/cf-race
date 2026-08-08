import itertools
import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def main(outdir):
    rnd = random.Random(1722)
    w = Writer(outdir)
    # all 120 permutations of "Timur" (all YES)
    w.add(multi([case("".join(p)) for p in itertools.permutations("Timur")]))
    # tricky NO cases: wrong case, wrong letters, wrong length
    tricky = ["timur", "TIMUR", "TimuR", "Timur" + "r", "Timu", "T", "t",
              "Timur"[::-1].lower(), "Tiimur", "Timmur", "Timur".replace("u", "v"),
              "murTi", "imurT", "aaaaa", "TTTTT", "iiiii"]
    w.add(multi([case(s) for s in tricky]))
    # near-misses: one char changed in a random permutation
    cases = []
    for _ in range(300):
        s = list(rnd.choice(list(itertools.permutations("Timur"))))
        i = rnd.randrange(5)
        s[i] = rnd.choice(string.ascii_letters)
        cases.append(case("".join(s)))
    w.add(multi(cases))
    # random strings, lengths 1..10 (max-size: t=1000)
    for _ in range(2):
        cases = []
        for _ in range(1000):
            n = rnd.randint(1, 10)
            cases.append(case("".join(rnd.choice("TimurTIMURtimurab")
                                      for _ in range(n))))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
