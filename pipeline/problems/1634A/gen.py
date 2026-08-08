import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s, k):
    return f"{len(s)} {k}\n{s}"


def rand_str(rnd, n, alpha):
    return "".join(rnd.choice(alpha) for _ in range(n))


def pal(rnd, n, alpha):
    half = rand_str(rnd, (n + 1) // 2, alpha)
    return half + half[: n // 2][::-1]


def main(outdir):
    rnd = random.Random(1634)
    w = Writer(outdir)
    # edge: k=0, n=1, palindromes, max sizes
    w.add(multi([case("a", 0), case("a", 1000), case("ab", 0), case("ab", 1),
                 case("ab", 1000), case("aba", 5), case("z" * 100, 1000)]))
    w.add(multi([case(pal(rnd, 100, "ab"), 1000), case(rand_str(rnd, 100, "ab"), 1000)]))
    # random mixes: palindromes, near-palindromes, random strings; k in {0,1,big}
    for seed in range(6):
        cases = []
        for _ in range(100):
            n = rnd.randint(1, 100)
            k = rnd.choice([0, 1, 2, rnd.randint(0, 1000), 1000])
            kind = rnd.randrange(3)
            alpha = rnd.choice(["ab", "abc", string.ascii_lowercase])
            if kind == 0:
                s = pal(rnd, n, alpha)
            elif kind == 1:
                s = list(pal(rnd, n, alpha))
                s[rnd.randrange(n)] = rnd.choice(alpha)
                s = "".join(s)
            else:
                s = rand_str(rnd, n, alpha)
            cases.append(case(s, k))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
