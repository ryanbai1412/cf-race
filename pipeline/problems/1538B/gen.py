import os, random, sys
out = sys.argv[1]
random.seed(15382)

def write(idx, cases):
    with open(os.path.join(out, f"{idx:02d}.in"), "w") as f:
        f.write(str(len(cases)) + "\n")
        for a in cases:
            f.write(str(len(a)) + "\n")
            f.write(" ".join(map(str, a)) + "\n")

def rand_case(nmax, vmax=10000, divisible=False):
    n = random.randint(1, nmax)
    a = [random.randint(0, vmax) for _ in range(n)]
    if divisible:
        r = sum(a) % n
        if r:
            need = n - r
            while need > 0:
                i = random.randrange(n)
                add = min(need, vmax - a[i])
                a[i] += add
                need -= add
    return a

write(1, [rand_case(6, 5) for _ in range(500)])
write(2, [rand_case(6, 5, divisible=True) for _ in range(500)])
edge = [[0], [10000], [0, 0], [0]*100, [10000]*100, [0, 10000], [1, 3], [1, 2]]
write(3, edge)
# max: sum n = 2e5 as one big case
big = rand_case(1, 10000); big = [random.randint(0, 10000) for _ in range(200000)]
write(4, [big])
big2 = [random.randint(0, 10000) for _ in range(200000)]
r = sum(big2) % 200000
if r: big2[0] += (200000 - r) if big2[0] + (200000 - r) <= 10000 else 0
# ensure valid range: instead adjust by distributing
need = (200000 - sum(big2) % 200000) % 200000
i = 0
while need > 0:
    add = min(need, 10000 - big2[i])
    big2[i] += add; need -= add; i += 1
write(5, [big2])
# many small cases, t = 1e4, total n <= 2e5
cases = [rand_case(10, 10000, divisible=random.random() < 0.5) for _ in range(10000)]
write(6, cases)
