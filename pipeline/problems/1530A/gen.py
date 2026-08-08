import os, random, sys
out = sys.argv[1]
random.seed(1530)

def write(idx, cases):
    with open(os.path.join(out, f"{idx:02d}.in"), "w") as f:
        f.write(str(len(cases)) + "\n")
        for n in cases:
            f.write(str(n) + "\n")

write(1, [random.randint(1, 100) for _ in range(1000)])
write(2, [random.randint(1, 10**9) for _ in range(1000)])
edge = [1, 9, 10, 11, 99, 100, 101, 10**9, 999999999, 111111111,
        1000000000, 123456789, 987654321, 2, 5, 20, 900000000, 101010101]
write(3, edge)
write(4, [int("".join(random.choice("01") for _ in range(random.randint(1,9))).lstrip("0") or "1") for _ in range(1000)])
write(5, [random.randint(10**8, 10**9) for _ in range(1000)])
