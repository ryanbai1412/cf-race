import os
import random
import string
import sys

out = sys.argv[1]
random.seed(978)

cases = [
    "abc",
    "xxx",
    "x" * 100,
    "xx" + "a" + "xx" + "b" + "xx",
    "xxxaxxxbxxx",
]
for _ in range(10):
    n = random.randint(3, 100)
    s = "".join(random.choice("xya") for _ in range(n))
    cases.append(s)
n = 100
cases.append("".join(random.choice(string.ascii_lowercase) for _ in range(n)))

for i, s in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(s)}\n{s}\n")
