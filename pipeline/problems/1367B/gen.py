import os
import random
import sys

out_dir = sys.argv[1]
rnd = random.Random(13672)
tests = []


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}\n"


def make(cases):
    return f"{len(cases)}\n" + "".join(case(a) for a in cases)


# edge cases
edge = [[0], [1], [1000], [999], [0, 1], [1, 0], [0, 0], [1, 1],
        [i for i in range(40)], [i + 1 for i in range(40)],
        [0] * 40, [1] * 40, [1000] * 40, [999] * 40,
        [3, 2, 7, 6], [3, 2, 6], [7], [4, 9, 2, 1, 18, 3, 0]]
tests.append(make(edge))

# already-good arrays of every length
cs = []
for n in range(1, 41):
    cs.append([rnd.randrange(i % 2, 1001, 2) for i in range(n)])
tests.append(make(cs))

# fully swapped-parity arrays of every length
cs = []
for n in range(1, 41):
    cs.append([rnd.randrange(1 - i % 2, 1001, 2) for i in range(n)])
tests.append(make(cs))

# random, max t = 1000
for _ in range(5):
    cs = []
    for _ in range(1000):
        n = rnd.randint(1, 40)
        cs.append([rnd.randint(0, 1000) for _ in range(n)])
    tests.append(make(cs))

# random but always solvable (equal parity counts), max t
for _ in range(3):
    cs = []
    for _ in range(1000):
        n = rnd.randint(1, 40)
        need_odd = n // 2
        vals = ([rnd.randrange(1, 1001, 2) for _ in range(need_odd)]
                + [rnd.randrange(0, 1001, 2) for _ in range(n - need_odd)])
        rnd.shuffle(vals)
        cs.append(vals)
    tests.append(make(cs))

# max t, max n
cs = [[rnd.randint(0, 1000) for _ in range(40)] for _ in range(1000)]
tests.append(make(cs))

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
