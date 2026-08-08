import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def word(rnd, m, alpha=string.ascii_lowercase):
    return "".join(rnd.choice(alpha) for _ in range(m))


def case(n, m, words):
    return f"{n} {m}\n" + "\n".join(words)


def main(outdir):
    rnd = random.Random(16763)
    w = Writer(outdir)
    # edges: duplicates (answer 0), extreme distance, m=1, n=2
    edge = [
        case(2, 8, ["a" * 8, "z" * 8]),
        case(2, 1, ["a", "z"]),
        case(3, 4, ["abcd", "abcd", "zzzz"]),
        case(2, 8, ["abcdefgh", "abcdefgh"]),
        case(50, 1, [string.ascii_lowercase[i % 26] for i in range(50)]),
    ]
    w.add(multi(edge))
    # random small alphabets (ties/near-ties likely)
    for _ in range(4):
        cs = []
        for _ in range(rnd.randint(1, 20)):
            n, m = rnd.randint(2, 8), rnd.randint(1, 4)
            cs.append(case(n, m, [word(rnd, m, "abc") for _ in range(n)]))
        w.add(multi(cs))
    # fully random
    for _ in range(4):
        cs = []
        for _ in range(rnd.randint(1, 50)):
            n, m = rnd.randint(2, 50), rnd.randint(1, 8)
            cs.append(case(n, m, [word(rnd, m) for _ in range(n)]))
        w.add(multi(cs))
    # max size: t=100, n=50, m=8
    cs = [case(50, 8, [word(rnd, 8) for _ in range(50)]) for _ in range(100)]
    w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
