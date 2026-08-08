import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1552)
w = Writer(sys.argv[1])
MAXT = 1000
MAXN = 40


def case(s):
    return f"{len(s)}\n{s}"


def rand_str(n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))


# tiny edge cases: n=1, single letters, two-letter strings
w.add(multi([case(c) for c in string.ascii_lowercase]
            + [case(a + b) for a in "abc" for b in "abc"]))
# already sorted / reverse sorted / all equal at max n
w.add(multi([case("a" * MAXN), case("".join(sorted(rand_str(MAXN, "abcdefghij")))),
             case("".join(sorted(rand_str(MAXN, string.ascii_lowercase), reverse=True))),
             case("z" * 20 + "a" * 20), case("ab" * 20), case("ba" * 20),
             case("z" + "a" * 39), case("b" * 39 + "a")]))
# max t with random strings over full alphabet, max length
w.add(multi([case(rand_str(MAXN, string.ascii_lowercase)) for _ in range(MAXT)]))
# max t with tiny alphabet (many ties)
w.add(multi([case(rand_str(MAXN, "ab")) for _ in range(MAXT)]))
w.add(multi([case(rand_str(MAXN, "abc")) for _ in range(MAXT)]))
# max t with random lengths
for _ in range(3):
    w.add(multi([case(rand_str(rng.randint(1, MAXN),
                               rng.choice(["ab", "abc", "abcde",
                                           string.ascii_lowercase])))
                 for _ in range(MAXT)]))
# nearly-sorted strings (few swaps)
cases = []
for _ in range(MAXT):
    n = rng.randint(2, MAXN)
    s = sorted(rand_str(n, "abcdefgh"))
    for _ in range(rng.randint(0, 3)):
        i, j = rng.randrange(n), rng.randrange(n)
        s[i], s[j] = s[j], s[i]
    cases.append(case("".join(s)))
w.add(multi(cases))
# single-case inputs
w.add(multi([case("codeforces")]))
w.add(multi([case(rand_str(MAXN, string.ascii_lowercase))]))
