import os, random, sys
out = sys.argv[1]
random.seed(1538)

def write(idx, cases):
    with open(os.path.join(out, f"{idx:02d}.in"), "w") as f:
        f.write(str(len(cases)) + "\n")
        for a in cases:
            f.write(str(len(a)) + "\n")
            f.write(" ".join(map(str, a)) + "\n")

def rand_case(nmax=100):
    n = random.randint(2, nmax)
    a = list(range(1, n + 1))
    random.shuffle(a)
    return a

write(1, [rand_case(6) for _ in range(100)])
edge = []
edge.append([1, 2])
edge.append([2, 1])
edge.append([1] + list(range(2, 100)) + [100])
edge.append([100] + list(range(2, 100)) + [1])
edge.append(list(range(1, 101)))
edge.append(list(range(100, 0, -1)))
a = list(range(3, 101)); edge.append([1] + a[:49] + [2] + a[49:])
a = list(range(2, 100)); edge.append(a[:50] + [1, 100] + a[50:])
write(2, edge)
write(3, [rand_case(10) for _ in range(100)])
write(4, [rand_case(100) for _ in range(100)])
write(5, [rand_case(100) for _ in range(100)])
