import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(2171)
w = Writer(sys.argv[1])

# full exhaustive coverage of the domain (n in 1..100), split across tests
w.add(multi([str(n) for n in range(1, 101)]))
w.add(multi([str(n) for n in (1, 2, 3, 4, 99, 100)]))
w.add(multi([str(n) for n in range(2, 101, 2)]))
w.add(multi([str(n) for n in range(1, 100, 2)]))
# randoms
for _ in range(10):
    w.add(multi([str(rng.randint(1, 100)) for _ in range(rng.randint(10, 100))]))
# max-size: t = 100
for _ in range(3):
    w.add(multi([str(rng.randint(1, 100)) for _ in range(100)]))
w.add(multi(["100"] * 100))
w.add(multi(["1"] * 100))
