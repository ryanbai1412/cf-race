import os, random, sys
out = sys.argv[1]
random.seed(1535)

def write(idx, cases):
    with open(os.path.join(out, f"{idx:02d}.in"), "w") as f:
        f.write(str(len(cases)) + "\n")
        for s in cases:
            f.write(" ".join(map(str, s)) + "\n")

def rand_case():
    return random.sample(range(1, 101), 4)

write(1, [rand_case() for _ in range(100)])
import itertools
perms = [list(p) for p in itertools.permutations([1, 2, 3, 4])]
write(2, perms)
write(3, [random.sample(range(1, 5), 4) for _ in range(1000)])
write(4, [rand_case() for _ in range(10000)])
write(5, [random.sample(range(97, 101), 4) for _ in range(10000)])
