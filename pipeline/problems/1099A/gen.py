import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(w, h, u1, d1, u2, d2):
    return f"{w} {h}\n{u1} {d1}\n{u2} {d2}\n"


def main(outdir):
    rnd = random.Random(1099)
    w = Writer(outdir)
    # minimum height: both stones must sit at h=1, but heights must differ -> h>=2
    w.add(case(0, 2, 0, 1, 0, 2))
    w.add(case(0, 1, 100, 1, 100, 1)) if False else None
    # zero weight, heavy stones (clamping to zero happens twice)
    w.add(case(0, 100, 100, 100, 100, 99))
    # maximum weight/height, no stone effect
    w.add(case(100, 100, 0, 1, 0, 2))
    w.add(case(100, 100, 100, 1, 100, 2))
    # stones high up so weight regrows afterwards
    w.add(case(0, 100, 100, 100, 100, 50))
    # stones at the very bottom (clamp near the end)
    w.add(case(5, 5, 100, 1, 100, 2))
    # h=1 edge: only possible with d1=d2=1 which is forbidden, so use h=2
    w.add(case(1, 2, 100, 2, 0, 1))
    w.add(case(1, 2, 0, 2, 100, 1))
    for _ in range(11):
        h = rnd.randint(2, 100)
        d1 = rnd.randint(1, h)
        d2 = rnd.choice([d for d in range(1, h + 1) if d != d1])
        w.add(case(rnd.randint(0, 100), h, rnd.randint(0, 100), d1,
                   rnd.randint(0, 100), d2))


if __name__ == "__main__":
    main(sys.argv[1])
