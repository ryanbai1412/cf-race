import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

LET = "abcdefghijklmnopqrstuvwxyz"


def case(a, b, c):
    return f"{a}\n{b}\n{c}"


def rand_word(rnd, n, alpha=LET):
    return "".join(rnd.choice(alpha) for _ in range(n))


def main(outdir):
    rnd = random.Random(1301)
    w = Writer(outdir)
    w.add(multi([case("a", "a", "a"), case("a", "b", "a"),
                 case("a", "b", "b"), case("a", "b", "c")]))
    # max length YES and NO
    a = rand_word(rnd, 100)
    b = rand_word(rnd, 100)
    c = "".join(rnd.choice([x, y]) for x, y in zip(a, b))
    w.add(multi([case(a, b, c)]))
    w.add(multi([case(rand_word(rnd, 100), rand_word(rnd, 100),
                      rand_word(rnd, 100))]))
    # t=100 random small alphabet (forces both YES/NO)
    for alpha in ("ab", "abc", LET):
        for _ in range(3):
            cases = []
            for _ in range(100):
                n = rnd.randint(1, 20)
                aa = rand_word(rnd, n, alpha)
                bb = rand_word(rnd, n, alpha)
                if rnd.random() < 0.5:
                    cc = "".join(rnd.choice([x, y])
                                 for x, y in zip(aa, bb))
                else:
                    cc = rand_word(rnd, n, alpha)
                cases.append(case(aa, bb, cc))
            w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
