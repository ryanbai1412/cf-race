import os, random, sys
out = sys.argv[1]
random.seed(1529)

def write(idx, cases):
    with open(os.path.join(out, f"{idx:02d}.in"), "w") as f:
        f.write(str(len(cases)) + "\n")
        for a in cases:
            f.write(str(len(a)) + "\n")
            f.write(" ".join(map(str, a)) + "\n")

def rand_case(nmax=100, vmax=100):
    n = random.randint(1, nmax)
    return [random.randint(1, vmax) for _ in range(n)]

# small random
write(1, [rand_case(8, 5) for _ in range(100)])
write(2, [rand_case(20, 3) for _ in range(100)])
# edge cases
write(3, [[1], [100], [1]*100, [100]*100, [1]+[100]*99, [100]*99+[1],
          list(range(1,101)), [1,2], [2,1], [50]*50+[49]*50])
# random medium
write(4, [rand_case(100, 100) for _ in range(100)])
# max size, all equal heavy
write(5, [[random.choice([1,2]) for _ in range(100)] for _ in range(100)])
write(6, [rand_case(100, 2) for _ in range(100)])
write(7, [rand_case(100, 100) for _ in range(100)])
