import os, random, sys
out = sys.argv[1]
random.seed(1537)

def write(idx, cases):
    with open(os.path.join(out, f"{idx:02d}.in"), "w") as f:
        f.write(str(len(cases)) + "\n")
        for a in cases:
            f.write(str(len(a)) + "\n")
            f.write(" ".join(map(str, a)) + "\n")

def rand_case(nmax=50, lo=-10000, hi=10000):
    n = random.randint(1, nmax)
    return [random.randint(lo, hi) for _ in range(n)]

write(1, [rand_case(5, -3, 3) for _ in range(1000)])
edge = [[1], [0], [-10000], [10000], [10000]*50, [-10000]*50,
        [1]*50, [0]*50, [2], [-1], [1, 1], [3, -1]]
write(2, edge)
write(3, [rand_case() for _ in range(1000)])
write(4, [rand_case(50, -10, 10) for _ in range(1000)])
write(5, [rand_case(50, 9000, 10000) for _ in range(1000)])
