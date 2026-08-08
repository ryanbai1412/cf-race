import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1549)
w = Writer(sys.argv[1])
SUMN = 200000


def case(enemy, mine):
    return f"{len(enemy)}\n{enemy}\n{mine}"


def rand_bits(n, p):
    return "".join("1" if rng.random() < p else "0" for _ in range(n))


def rand_case(n, pe=None, pm=None):
    pe = rng.random() if pe is None else pe
    pm = rng.random() if pm is None else pm
    return case(rand_bits(n, pe), rand_bits(n, pm))


def pack(sizes, maker):
    """build a multi-test input with the given per-case sizes"""
    return multi([maker(n) for n in sizes])


# edge: n=2, all combinations
w.add(multi([case(f"{a}{b}", f"{c}{d}")
             for a in "01" for b in "01" for c in "01" for d in "01"]))
# n=3 exhaustive-ish
w.add(multi([case(e, m)
             for e in ("000", "001", "010", "011", "100", "101", "110", "111")
             for m in ("000", "001", "010", "011", "100", "101", "110", "111")]))
# extremes: no enemies / all enemies / no pawns / all pawns
w.add(multi([case("0" * 1000, "1" * 1000), case("1" * 1000, "1" * 1000),
             case("1" * 1000, "0" * 1000), case("0" * 1000, "0" * 1000),
             case("10" * 500, "01" * 500), case("01" * 500, "10" * 500),
             case("110" * 333 + "1", "011" * 333 + "0")]))
# alternating / blocked patterns at max single n
n = SUMN
w.add(multi([case("1" * n, "1" * n)]))
w.add(multi([case("0" * n, "1" * n)]))
w.add(multi([case("10" * (n // 2), "01" * (n // 2))]))
w.add(multi([case("101" * (n // 3), "010" * (n // 3))]))
# sparse enemies with dense pawns (contention for capture squares)
w.add(multi([case(rand_bits(n, 0.1), rand_bits(n, 0.9))]))
w.add(multi([case(rand_bits(n, 0.9), rand_bits(n, 0.1))]))
w.add(multi([case(rand_bits(n, 0.5), rand_bits(n, 0.5))]))
# many small random cases (sum n <= 2e5)
for _ in range(4):
    sizes = []
    left = SUMN
    while left >= 2 and len(sizes) < 20000:
        k = rng.randint(2, min(20, left))
        sizes.append(k)
        left -= k
    w.add(pack(sizes, rand_case))
# max t with n=2 each
w.add(pack([2] * 20000, rand_case))
# medium random cases
for _ in range(2):
    sizes = []
    left = SUMN
    while left >= 2 and len(sizes) < 200:
        k = rng.randint(2, min(1000, left))
        sizes.append(k)
        left -= k
    w.add(pack(sizes, rand_case))
