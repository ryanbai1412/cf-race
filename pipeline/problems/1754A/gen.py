import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_case(rnd, n):
    s = ["Q"]
    for _ in range(n - 1):
        s.append(rnd.choice("QA"))
    return f"{len(s)}\n{''.join(s)}"


def main(outdir):
    rnd = random.Random(1754)
    w = Writer(outdir)
    # edge: minimal cases
    w.add(multi(["1\nQ", "2\nQA", "2\nQQ", "3\nQAQ", "3\nQAA", "3\nQQA"]))
    # all-Q and Q followed by all A
    w.add(multi(["100\n" + "Q" * 100, "100\nQ" + "A" * 99, "100\n" + "QA" * 50]))
    # random small
    for _ in range(4):
        w.add(multi([rand_case(rnd, rnd.randint(1, 12)) for _ in range(rnd.randint(1, 50))]))
    # random large, max t
    for _ in range(4):
        w.add(multi([rand_case(rnd, rnd.randint(1, 100)) for _ in range(500)]))
    # biased: mostly-A strings (usually Yes)
    for _ in range(2):
        cases = []
        for _ in range(500):
            n = rnd.randint(1, 100)
            s = ["Q"] + [("Q" if rnd.random() < 0.25 else "A") for _ in range(n - 1)]
            cases.append(f"{n}\n{''.join(s)}")
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
