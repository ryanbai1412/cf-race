import os
import random
import string
import sys

out_dir = sys.argv[1]
rnd = random.Random(1367)
tests = []


def build(a):
    return "".join(a[i:i + 2] for i in range(len(a) - 1))


def make(strings):
    return f"{len(strings)}\n" + "\n".join(build(a) for a in strings) + "\n"


# edge cases: shortest, longest, single-letter, alternating
edge = ["ab", "aa", "z" * 2, "a" * 51, "z" * 51, "ab" * 25 + "a",
        "abac", "bcdaf", "abcdefghijklmnopqrstuvwxyz",
        string.ascii_lowercase[:25] + "a" * 26]
tests.append(make(edge))

# all lengths 2..51 over a 2-letter alphabet
cs = ["".join(rnd.choice("ab") for _ in range(n)) for n in range(2, 52)]
tests.append(make(cs))

# all lengths 2..51 over the full alphabet
cs = ["".join(rnd.choice(string.ascii_lowercase) for _ in range(n))
      for n in range(2, 52)]
tests.append(make(cs))

# random, max t = 1000
for _ in range(5):
    cs = []
    for _ in range(1000):
        n = rnd.randint(2, 51)
        alpha = rnd.choice(["a", "ab", "abc", string.ascii_lowercase])
        cs.append("".join(rnd.choice(alpha) for _ in range(n)))
    tests.append(make(cs))

# max t of maximum-length strings
for _ in range(2):
    cs = ["".join(rnd.choice(string.ascii_lowercase) for _ in range(51))
          for _ in range(1000)]
    tests.append(make(cs))

# max t of minimum-length strings
cs = ["".join(rnd.choice(string.ascii_lowercase) for _ in range(2))
      for _ in range(1000)]
tests.append(make(cs))

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
