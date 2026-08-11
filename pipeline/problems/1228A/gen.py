"""Tests for 1228A (Distinct Digits).

The answer is "print any", so every generated window [l, r] contains either
exactly one distinct-digit number or none at all — that makes token comparison
against the reference output correct for every valid solution. The CF samples
are intentionally NOT included as tests (sample 1 has many valid answers).
"""
import os
import random
import sys

LIMIT = 10**5


def distinct(x: int) -> bool:
    s = str(x)
    return len(set(s)) == len(s)


def main(outdir):
    rnd = random.Random(1228)
    ok = [distinct(x) for x in range(LIMIT + 2)]

    def window(x):
        """Maximal window around x containing no other distinct-digit number."""
        l = x
        while l - 1 >= 1 and not ok[l - 1]:
            l -= 1
        r = x
        while r + 1 <= LIMIT and not ok[r + 1]:
            r += 1
        return l, r

    cases = []
    # unique-answer windows around distinct-digit numbers, biased to wide ones
    xs = [x for x in range(1, LIMIT + 1) if ok[x]]
    wide = sorted(xs, key=lambda x: window(x)[0] - window(x)[1])[:400]
    for x in rnd.sample(wide, 18):
        l, r = window(x)
        # shrink randomly but keep x inside
        l = rnd.randint(l, x)
        r = rnd.randint(x, r)
        cases.append((l, r))
    # -1 windows: gaps with no distinct-digit numbers
    gaps = []
    run = None
    for x in range(1, LIMIT + 1):
        if not ok[x]:
            run = x if run is None else run
        elif run is not None:
            gaps.append((run, x - 1))
            run = None
    if run is not None:
        gaps.append((run, LIMIT))
    gaps.sort(key=lambda g: g[0] - g[1])
    for l, r in gaps[:8]:
        cases.append((rnd.randint(l, r), r) if l == r else (l, r))
    # single-point cases
    for _ in range(4):
        x = rnd.randint(1, LIMIT)
        cases.append((x, x))

    rnd.shuffle(cases)
    for i, (l, r) in enumerate(cases, 1):
        with open(os.path.join(outdir, f"{i:02d}.in"), "w") as f:
            f.write(f"{l} {r}\n")


if __name__ == "__main__":
    main(sys.argv[1])
