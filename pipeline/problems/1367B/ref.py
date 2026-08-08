import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos:pos + n]; pos += n
        bad_even_idx = 0  # even index holding an odd value
        bad_odd_idx = 0   # odd index holding an even value
        for i in range(n):
            v = int(a[i]) & 1
            if i % 2 == 0 and v == 1:
                bad_even_idx += 1
            elif i % 2 == 1 and v == 0:
                bad_odd_idx += 1
        out.append(bad_even_idx if bad_even_idx == bad_odd_idx else -1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
