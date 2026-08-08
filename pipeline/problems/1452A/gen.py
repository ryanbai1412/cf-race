import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10**4


def main(outdir):
    rnd = random.Random(1452)
    w = Writer(outdir)
    # edges
    w.add(multi([
        "0 0", "0 1", "1 0", "1 1",
        f"0 {MAX}", f"{MAX} 0", f"{MAX} {MAX}",
        f"{MAX} {MAX - 1}", f"{MAX - 1} {MAX}",
    ]))
    # all small pairs 0..9
    w.add(multi([f"{x} {y}" for x in range(10) for y in range(10)]))
    # random, max t
    for _ in range(4):
        w.add(multi([f"{rnd.randint(0, MAX)} {rnd.randint(0, MAX)}"
                     for _ in range(100)]))
    # near-diagonal cases
    cases = []
    for _ in range(100):
        x = rnd.randint(0, MAX)
        y = min(MAX, max(0, x + rnd.randint(-2, 2)))
        cases.append(f"{x} {y}")
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
