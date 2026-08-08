import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1712)
    w = Writer(outdir)
    # every tiny n
    w.add(multi([str(n) for n in range(1, 21)]))
    # extremes
    w.add(multi(["1"]))
    w.add(multi(["2"]))
    w.add(multi(["100000"]))
    w.add(multi(["99999"]))
    # random ns summing to <= 1e5
    for _ in range(4):
        ns, total = [], 0
        while total < 90000 and len(ns) < 1000:
            n = rnd.randint(1, 5000)
            if total + n > 100000:
                break
            ns.append(n)
            total += n
        w.add(multi([str(n) for n in ns]))


if __name__ == "__main__":
    main(sys.argv[1])
