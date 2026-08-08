import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1328)
    w = Writer(outdir)
    M = 10 ** 9
    # edges
    w.add(multi(["1 1", f"{M} {M}", f"1 {M}", f"{M} 1",
                 f"{M - 1} {M}", f"{M} {M - 1}", "999999999 2",
                 "1000000000 999999937"]))
    # small random
    for _ in range(4):
        cases = [f"{rnd.randint(1, 30)} {rnd.randint(1, 30)}"
                 for _ in range(2000)]
        w.add(multi(cases))
    # max-size random
    for _ in range(4):
        cases = [f"{rnd.randint(1, M)} {rnd.randint(1, M)}"
                 for _ in range(10000)]
        w.add(multi(cases))
    # divisible-heavy cases
    cases = []
    for _ in range(5000):
        b = rnd.randint(1, 10 ** 4)
        a = b * rnd.randint(1, 10 ** 5)
        cases.append(f"{a} {b}")
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
