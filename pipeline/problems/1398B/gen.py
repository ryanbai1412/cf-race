import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1398)
w = Writer(sys.argv[1])


def rand_str(n, p1=0.5):
    return "".join("1" if rng.random() < p1 else "0" for _ in range(n))


# edges: tiny strings, all-ones, all-zeros, max length
w.add(multi(["0", "1", "01", "10", "11", "00", "1" * 100, "0" * 100,
             "10" * 50, "01" * 50]))
# all strings of length <= 8 (exhaustive-ish, chunked)
small = [bin(m)[2:].zfill(L) for L in range(1, 9) for m in range(2 ** L)]
for i in range(0, len(small), 500):
    w.add(multi(small[i:i + 500]))
# random densities
for p in (0.1, 0.3, 0.5, 0.7, 0.9):
    w.add(multi([rand_str(rng.randint(1, 100), p) for _ in range(500)]))
# blocky strings (long runs)
def blocky():
    out = []
    while len(out) < 100:
        ch = "1" if len(out) % 2 == 0 else "0"
        out.extend(ch * rng.randint(1, 12))
    return "".join(out[:100])


for _ in range(2):
    w.add(multi([blocky() for _ in range(500)]))
# max size: 500 strings of length 100
w.add(multi([rand_str(100) for _ in range(500)]))
w.add(multi(["1" * 100 for _ in range(500)]))
