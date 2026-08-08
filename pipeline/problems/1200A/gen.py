import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def gen_events(rnd, n, p_leave):
    """Generate a valid event string of length n."""
    occ = set()
    s = []
    for _ in range(n):
        if occ and (len(occ) == 10 or rnd.random() < p_leave):
            x = rnd.choice(sorted(occ))
            occ.discard(x)
            s.append(str(x))
        else:
            if rnd.random() < 0.5:
                r = min(i for i in range(10) if i not in occ)
                s.append("L")
            else:
                r = max(i for i in range(10) if i not in occ)
                s.append("R")
            occ.add(r)
    return "".join(s)


def case(s):
    return f"{len(s)}\n{s}\n"


def main(outdir):
    rnd = random.Random(1200)
    w = Writer(outdir)
    w.add(case("L"))
    w.add(case("R"))
    w.add(case("L" * 10))
    w.add(case("R" * 10))
    w.add(case("LRLRLRLRLR"))
    # fill fully, empty fully, refill
    w.add(case("L" * 10 + "0123456789" + "R" * 10))
    # small randoms with varying leave probability
    for p in (0.2, 0.4, 0.5):
        for _ in range(3):
            w.add(case(gen_events(rnd, rnd.randint(1, 60), p)))
    # max-size tests
    w.add(case(gen_events(rnd, 10**5, 0.45)))
    w.add(case(gen_events(rnd, 10**5, 0.05)))


if __name__ == "__main__":
    main(sys.argv[1])
