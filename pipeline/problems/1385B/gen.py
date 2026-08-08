import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def merge(p, rnd):
    """Interleave two copies of p keeping relative order."""
    i = j = 0
    out = []
    while i < len(p) or j < len(p):
        if i < len(p) and (j >= len(p) or rnd.random() < 0.5):
            out.append(p[i])
            i += 1
        else:
            out.append(p[j])
            j += 1
    return out


def case(p, rnd):
    a = merge(p, rnd)
    return f"{len(p)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1385)
    w = Writer(outdir)

    # smallest possible input
    w.add(multi(["1\n1 1"]))
    # all n = 50 (max), max t
    w.add(multi([case(rnd.sample(range(1, 51), 50), rnd) for _ in range(400)]))
    # identity and reversed permutations at max n
    ident = list(range(1, 51))
    w.add(multi([case(ident, rnd) for _ in range(400)]))
    w.add(multi([case(ident[::-1], rnd) for _ in range(400)]))
    # concatenated copies (p then p) and fully blocked (each element twice)
    w.add(multi([f"{n}\n" + " ".join(map(str, list(range(1, n + 1)) * 2))
                 for n in range(1, 51)]))
    w.add(multi([f"{n}\n" + " ".join(str(x) for x in range(1, n + 1) for _ in range(2))
                 for n in range(1, 51)]))
    # every small n once
    w.add(multi([case(rnd.sample(range(1, n + 1), n), rnd) for n in range(1, 21)]))
    # random mixed sizes
    for _ in range(10):
        t = rnd.randint(1, 400)
        cases = []
        for _ in range(t):
            n = rnd.randint(1, 50)
            cases.append(case(rnd.sample(range(1, n + 1), n), rnd))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
