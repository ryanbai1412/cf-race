import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1191)
    w = Writer(outdir)
    for x in (30, 31, 32, 33, 97, 98, 99, 100):
        w.add(str(x))
    seen = set()
    while len(seen) < 12:
        v = rnd.randint(30, 100)
        if v in seen:
            continue
        seen.add(v)
        w.add(str(v))


if __name__ == "__main__":
    main(sys.argv[1])
