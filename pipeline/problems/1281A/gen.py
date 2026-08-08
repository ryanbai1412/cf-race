import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

SUF = ["po", "desu", "masu", "mnida"]
LET = "abcdefghijklmnopqrstuvwxyz"


def sentence(rnd, suffix, maxlen):
    L = rnd.randint(len(suffix), max(len(suffix), maxlen))
    extra = L - len(suffix)
    parts = []
    while extra > 0:
        wl = rnd.randint(1, min(8, extra))
        parts.append("".join(rnd.choice(LET) for _ in range(wl)))
        extra -= wl + 1
    body = "_".join(parts)
    if body:
        return body + "_" + suffix if extra == -1 else body + suffix
    return suffix


def main(outdir):
    rnd = random.Random(1281)
    w = Writer(outdir)
    # bare suffixes
    w.add(multi(SUF))
    # max length, each suffix
    w.add(multi([sentence(rnd, s, 1000) for s in SUF]))
    # tricky: words containing other suffixes mid-sentence
    w.add(multi(["po_desu_masu_mnida_po", "mnida_po_desu",
                 "desupo_masu", "masudesu_mnida"]))
    for _ in range(8):
        t = rnd.randint(1, 30)
        w.add(multi([sentence(rnd, rnd.choice(SUF), rnd.randint(2, 60))
                     for _ in range(t)]))
    for _ in range(4):
        t = rnd.randint(1, 30)
        w.add(multi([sentence(rnd, rnd.choice(SUF), 1000)
                     for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
