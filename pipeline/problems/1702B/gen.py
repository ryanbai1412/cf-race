import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1702 * 2)
w = Writer(sys.argv[1])


def rand_s(n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))


# edge: single chars, tiny strings
w.add(multi(["a", "z", "ab", "abc", "abcd", "aaaa", "abca"]))
# single letter long, exactly 3 distinct, 4 distinct alternating
w.add(multi(["a" * 200000]))
w.add(multi([rand_s(200000, "abc")]))
w.add(multi(["abcd" * 50000]))
# full alphabet random, max size
w.add(multi([rand_s(200000, string.ascii_lowercase)]))
# many small random with small alphabets
for k in (2, 3, 4, 5, 26):
    w.add(multi([rand_s(rng.randint(1, 50), string.ascii_lowercase[:k]) for _ in range(4000)]))
# blocks of 3-letter chunks (stresses day boundaries)
cases = []
for _ in range(2000):
    s = ""
    for _ in range(rng.randint(1, 10)):
        alpha = rng.sample(string.ascii_lowercase, 3)
        s += rand_s(rng.randint(1, 20), alpha)
    cases.append(s)
w.add(multi(cases))
# max t small strings
w.add(multi([rand_s(rng.randint(1, 20), string.ascii_lowercase[:rng.randint(1, 26)]) for _ in range(10000)]))
