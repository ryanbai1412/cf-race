import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def rand_valid(rnd, n):
    letters = rnd.sample(string.ascii_uppercase, rnd.randint(1, min(26, n)))
    parts = []
    left = n
    for i, ch in enumerate(letters):
        take = left - (len(letters) - 1 - i) if i == len(letters) - 1 \
            else rnd.randint(1, left - (len(letters) - 1 - i))
        parts.append(ch * take)
        left -= take
    return "".join(parts)


def main(outdir):
    rnd = random.Random(1520)
    w = Writer(outdir)
    # edges
    w.add(multi([case("A"), case("A" * 50), case("AB"), case("ABA"),
                 case("BAB"), case("AABBCCDDEEBZZ"), case("AAAAZAAAAA"),
                 case("".join(string.ascii_uppercase[:26]) * 1)[0:0] or
                 case(string.ascii_uppercase)]))
    # valid block strings
    w.add(multi([case(rand_valid(rnd, rnd.randint(1, 50)))
                 for _ in range(1000)]))
    # valid with one corruption (swap two positions)
    cases = []
    for _ in range(1000):
        s = list(rand_valid(rnd, rnd.randint(2, 50)))
        i, j = rnd.randrange(len(s)), rnd.randrange(len(s))
        s[i], s[j] = s[j], s[i]
        cases.append(case("".join(s)))
    w.add(multi(cases))
    # random small alphabet (lots of NOs)
    for k in (1, 2, 3):
        w.add(multi([case("".join(rnd.choice(string.ascii_uppercase[:k])
                                  for _ in range(rnd.randint(1, 50))))
                     for _ in range(1000)]))
    # fully random
    w.add(multi([case("".join(rnd.choice(string.ascii_uppercase)
                              for _ in range(rnd.randint(1, 50))))
                 for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
