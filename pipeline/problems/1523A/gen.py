import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(m, s):
    return f"{len(s)} {m}\n{s}"


def rand_string(rnd, n, p_alive):
    return "".join("1" if rnd.random() < p_alive else "0" for _ in range(n))


def main(outdir):
    rnd = random.Random(1523)
    w = Writer(outdir)
    # edges: all dead, all alive, single 1 at ends/middle, m=1, m=1e9
    w.add(multi([case(1, "00"), case(10 ** 9, "0" * 1000),
                 case(10 ** 9, "1" * 1000),
                 case(1, "1" + "0" * 999), case(10 ** 9, "0" * 999 + "1"),
                 case(3, "0" * 500 + "1" + "0" * 499),
                 case(10 ** 9, "0" * 500 + "1" + "0" * 499)]))
    # equidistant collision patterns (cells that never become alive)
    w.add(multi([case(m, "1" + "0" * (2 * k + 1) + "1")
                 for m in (1, 2, 5, 10 ** 9) for k in range(0, 20)]))
    # sparse alive, various m (sum n <= 1e4 per file)
    for seed in range(3):
        cases = []
        total = 0
        while total < 9000:
            n = rnd.randint(2, 1000)
            m = rnd.choice([1, 2, 3, rnd.randint(1, 1000), 10 ** 9])
            p = rnd.choice([0.005, 0.02, 0.1, 0.5])
            cases.append(case(m, rand_string(rnd, n, p)))
            total += n
        w.add(multi(cases))
    # small dense random
    cases = []
    for _ in range(1000):
        n = rnd.randint(2, 10)
        m = rnd.randint(1, 15)
        cases.append(case(m, rand_string(rnd, n, rnd.random())))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
