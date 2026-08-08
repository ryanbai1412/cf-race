"""Stress-test ref.py against brute.py on small random inputs.

Usage: python3 pipeline/problems/stress.py <id> [iters]
Each problem supplies a small-input generator below.
"""
import random
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def small_1767A(rng):
    def tri():
        while True:
            p = [(rng.randint(1, 4), rng.randint(1, 4)) for _ in range(3)]
            if (p[1][0] - p[0][0]) * (p[2][1] - p[0][1]) - (p[2][0] - p[0][0]) * (p[1][1] - p[0][1]) != 0:
                return p
    cases = [tri() for _ in range(rng.randint(1, 8))]
    s = f"{len(cases)}\n"
    for c in cases:
        s += "\n" + "\n".join(f"{x} {y}" for x, y in c) + "\n"
    return s


def small_1769A(rng):
    n = rng.randint(1, 10)
    a = sorted(rng.sample(range(1, 30), n))
    return f"{n}\n" + "\n".join(map(str, a)) + "\n"


def small_1772B(rng):
    cases = [rng.sample(range(1, 8), 4) for _ in range(rng.randint(1, 10))]
    return f"{len(cases)}\n" + "".join(f"{c[0]} {c[1]}\n{c[2]} {c[3]}\n" for c in cases)


def small_912A(rng):
    return (f"{rng.randint(0, 8)} {rng.randint(0, 8)}\n"
            f"{rng.randint(0, 4)} {rng.randint(0, 4)} {rng.randint(0, 4)}\n")


def small_935A(rng):
    return f"{rng.randint(2, 3000)}\n"


def small_937A(rng):
    n = rng.randint(1, 12)
    a = [rng.randint(0, 6) for _ in range(n)]
    if not any(a):
        a[rng.randrange(n)] = 3
    return f"{n}\n" + " ".join(map(str, a)) + "\n"


def small_938A(rng):
    n = rng.randint(1, 12)
    s = "".join(rng.choice("aeiouybcd") for _ in range(n))
    return f"{n}\n{s}\n"


GENS = {k[6:]: v for k, v in list(globals().items()) if k.startswith("small_")}


def main():
    pid = sys.argv[1]
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    rng = random.Random(12345)
    gen = GENS[pid]
    ref = os.path.join(HERE, pid, "ref.py")
    brute = os.path.join(HERE, pid, "brute.py")
    for i in range(iters):
        inp = gen(rng)
        a = subprocess.run(["python3", ref], input=inp, capture_output=True, text=True, check=True)
        b = subprocess.run(["python3", brute], input=inp, capture_output=True, text=True, check=True)
        if a.stdout.split() != b.stdout.split():
            print("MISMATCH on input:\n" + inp)
            print("ref:", a.stdout)
            print("brute:", b.stdout)
            sys.exit(1)
    print(f"{pid}: {iters} random tests OK")


main()
