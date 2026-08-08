import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, s):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n" + s


def rand_case(rnd, n, valid):
    a = [rnd.randint(1, rnd.choice([3, 8, 50])) for _ in range(n)]
    if valid:
        mp = {v: rnd.choice(string.ascii_lowercase) for v in set(a)}
        s = "".join(mp[v] for v in a)
    else:
        s = "".join(rnd.choice("ab") for _ in range(n))
    return case(a, s)


def main(outdir):
    rnd = random.Random(1744)
    w = Writer(outdir)
    # edges: n=1; all same number same letter; all same number diff letters
    w.add(multi([case([1], "z"), case([50] * 50, "q" * 50),
                 case([7] * 50, "a" * 49 + "b"),
                 case(list(range(1, 51)), "".join(rnd.choice(string.ascii_lowercase) for _ in range(50)))]))
    # max t=1000 mixed
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randint(1, 50), rnd.random() < 0.5) for _ in range(1000)]))
    # random small
    for _ in range(6):
        w.add(multi([rand_case(rnd, rnd.randint(1, 10), rnd.random() < 0.5) for _ in range(rnd.randint(1, 30))]))


if __name__ == "__main__":
    main(sys.argv[1])
