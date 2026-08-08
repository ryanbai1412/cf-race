import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAXLEN = 50
MAXT = 1000
rng = random.Random(15511)
w = Writer(sys.argv[1])


def rand_str(n, alpha=string.ascii_lowercase):
    return "".join(rng.choice(alpha) for _ in range(n))


# edge: single characters, all same character
w.add(multi(list(string.ascii_lowercase) + ["x" * n for n in range(1, 51)]))
# all-distinct strings of every length (odd/even single counts)
w.add(multi([string.ascii_lowercase[:n] for n in range(1, 27)]))
# exactly two of each letter
w.add(multi([string.ascii_lowercase[:n] * 2 for n in range(1, 26)]))
# one letter with high count plus distinct singles
cases = []
for k in range(1, 26):
    cases.append("a" * (MAXLEN - k) + string.ascii_lowercase[1:1 + k][:k])
w.add(multi(cases))
# random over small alphabets (many duplicates)
for alpha in ("ab", "abc", "abcde", "abcdefghij"):
    w.add(multi([rand_str(rng.randint(1, MAXLEN), alpha) for _ in range(MAXT)]))
# random over full alphabet
for _ in range(4):
    w.add(multi([rand_str(rng.randint(1, MAXLEN)) for _ in range(MAXT)]))
# max size: t=1000 strings of length 50
w.add(multi([rand_str(MAXLEN) for _ in range(MAXT)]))
w.add(multi([rand_str(MAXLEN, "abcdefghijklm") for _ in range(MAXT)]))
