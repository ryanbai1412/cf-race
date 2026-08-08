import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1547)
w = Writer(sys.argv[1])
MAXT = 10000


def alphabetical(n):
    """build a valid alphabetical string of length n"""
    dq = []
    for c in range(1, n + 1):
        ch = chr(96 + c)
        if rng.random() < 0.5:
            dq.insert(0, ch)
        else:
            dq.append(ch)
    return "".join(dq)


def mutate(s):
    s = list(s)
    k = rng.randint(1, 2)
    for _ in range(k):
        i = rng.randrange(len(s))
        op = rng.randrange(3)
        if op == 0:
            s[i] = rng.choice(string.ascii_lowercase)
        elif op == 1 and len(s) > 1:
            j = rng.randrange(len(s))
            s[i], s[j] = s[j], s[i]
        else:
            s[i] = chr(96 + rng.randint(1, 26))
    return "".join(s)


# edge: single letters
w.add(multi(list(string.ascii_lowercase)))
# all valid, every length
w.add(multi([alphabetical(n) for n in range(1, 27)]))
# max length 26 valid strings
w.add(multi([alphabetical(26) for _ in range(MAXT)]))
# mutated near-valid strings (mostly NO, occasionally YES)
w.add(multi([mutate(alphabetical(rng.randint(1, 26))) for _ in range(MAXT)]))
# repeated letters / degenerate
w.add(multi(["a" * n for n in range(1, 27)] + ["z" * n for n in range(1, 27)] +
            ["ba", "ab", "ca", "acb", "ddcba", "xyz", "aa", "z"]))
# reversed / sorted alphabet prefixes
w.add(multi([string.ascii_lowercase[:n] for n in range(1, 27)] +
            [string.ascii_lowercase[:n][::-1] for n in range(1, 27)]))
# random garbage strings
for _ in range(4):
    w.add(multi(["".join(rng.choice(string.ascii_lowercase)
                         for _ in range(rng.randint(1, 26)))
                 for _ in range(MAXT)]))
# random garbage over a small alphabet (more near-misses)
for _ in range(2):
    w.add(multi(["".join(rng.choice("abcde")
                         for _ in range(rng.randint(1, 6)))
                 for _ in range(MAXT)]))
# max size: t=1e4 mixed valid/invalid length-26
w.add(multi([alphabetical(26) if i % 2 else mutate(alphabetical(26))
             for i in range(MAXT)]))
