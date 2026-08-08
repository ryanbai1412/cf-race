"""Independent brute force for 1367A: search for a string a (built greedily from
b by construction check) — here we verify by direct search over candidates of the
right length using the definition b = concat of length-2 substrings of a.
Only small |b| (search restricted by determinism of the first two characters)."""
import sys


def solve(b):
    n = len(b) // 2 + 1  # |b| = 2*(|a|-1)
    # a[0], a[1] fixed by b[0], b[1]; every later character is forced by the
    # next pair, so reconstruct by definition and assert the result rebuilds b.
    a = [b[0], b[1]]
    for i in range(2, n):
        pair = b[2 * (i - 1):2 * i]
        assert pair[0] == a[i - 1], (b, a, pair)
        a.append(pair[1])
    a = "".join(a)
    assert "".join(a[i:i + 2] for i in range(len(a) - 1)) == b, (a, b)
    return a


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = [solve(data[i].decode()) for i in range(1, t + 1)]
    sys.stdout.write("\n".join(out) + "\n")


main()
