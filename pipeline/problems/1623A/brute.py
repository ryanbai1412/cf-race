"""Independent check: closed-form via 1D triangle-wave meeting times.

The row coordinate follows a triangle wave of period 2(n-1); find the first
time each coordinate matches the dirt, take the minimum.
"""
import sys


def first_hit(size, start, target):
    """First t >= 0 with pos(t) == target for a bouncing point in [1, size]."""
    if size == 1:
        return 0 if target == 1 else None
    period = 2 * (size - 1)
    best = None
    # position at time t: derived from unfolding; check one full period
    pos, d = start, 1
    for t in range(period + 1):
        if pos == target:
            best = t
            break
        if pos + d < 1 or pos + d > size:
            d = -d
        pos += d
    return best


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, m, rb, cb, rd, cd = (int(x) for x in data[idx : idx + 6])
        idx += 6
        a = first_hit(n, rb, rd)
        b = first_hit(m, cb, cd)
        cands = [x for x in (a, b) if x is not None]
        out.append(str(min(cands)))
    print("\n".join(out))


main()
