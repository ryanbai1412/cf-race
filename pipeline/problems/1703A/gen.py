import itertools
import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1703)
w = Writer(sys.argv[1])

# all 8 casings of "yes"
yes_all = ["".join(c) for c in itertools.product(*[(ch.lower(), ch.upper()) for ch in "yes"])]
w.add(multi(yes_all))
# near-misses: one char off from YES
near = ["yEs", "yeS"]  # actual yes-casings; add real misses:
near = []
for i in range(3):
    for repl in "abYESyes":
        s = list("YES")
        s[i] = repl
        s = "".join(s)
        if s.upper() != "YES":
            near.append(s)
w.add(multi(near))
# tricky: sey, esy, NOO, no-like
w.add(multi(["SEY", "sey", "EYS", "yse", "YSE", "eys", "NOO", "noY", "Yno", "yyy", "eee", "sss", "YYY", "YEE", "ESS"]))
# random 3-letter strings, max t
for _ in range(3):
    w.add(multi(["".join(rng.choice(string.ascii_letters) for _ in range(3)) for _ in range(1000)]))
# random casings of yes mixed with random strings at max t
w.add(multi([rng.choice(yes_all) if rng.random() < 0.5 else
             "".join(rng.choice(string.ascii_letters) for _ in range(3)) for _ in range(1000)]))
