import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

ALL = [a + b for a in string.ascii_lowercase for b in string.ascii_lowercase if a != b]


def main(outdir):
    rnd = random.Random(1674)
    w = Writer(outdir)
    # all 650 words (t = 650 = max)
    w.add(multi(ALL))
    # extremes
    w.add(multi(["ab"]))
    w.add(multi(["zy"]))
    w.add(multi(["az", "ba", "yz", "za"]))
    # random selections
    for _ in range(8):
        t = rnd.randint(1, 650)
        w.add(multi([rnd.choice(ALL) for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
