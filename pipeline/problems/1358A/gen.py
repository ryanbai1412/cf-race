import os
import random
import sys

out_dir = sys.argv[1]
rnd = random.Random(1358)
tests = []

# edge cases
cs = []
for n, m in [(1, 1), (1, 2), (2, 1), (1, 10000), (10000, 1), (2, 2), (3, 3),
             (10000, 10000), (9999, 9999), (10000, 9999), (1, 9999), (9999, 1),
             (2, 10000), (10000, 2), (5, 3), (3, 5)]:
    cs.append(f"{n} {m}")
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# all small pairs 1..30 x 1..30
cs = [f"{n} {m}" for n in range(1, 31) for m in range(1, 31)]
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# random, max t
for _ in range(6):
    cs = [f"{rnd.randint(1, 10000)} {rnd.randint(1, 10000)}" for _ in range(10000)]
    tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# max t of maximum values
cs = ["10000 10000"] * 10000
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# max t of thin parks
cs = []
for _ in range(10000):
    if rnd.random() < 0.5:
        cs.append(f"1 {rnd.randint(1, 10000)}")
    else:
        cs.append(f"{rnd.randint(1, 10000)} 1")
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
