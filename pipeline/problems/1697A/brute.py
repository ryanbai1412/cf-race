"""Independent alternative: simulate walking, restoring lazily at each bench."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        energy = m
        restored = 0
        for x in data[pos:pos + n]:
            d = int(x)
            if energy < d:
                restored += d - energy
                energy = d
            energy -= d
        pos += n
        out.append(restored)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
