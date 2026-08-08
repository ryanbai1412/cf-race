"""Independent check: bitmask of used letters must be a gapless run."""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    out = []
    for s in data[1:1 + n]:
        mask = 0
        dup = False
        for ch in s:
            bit = 1 << (ord(ch) - 97)
            if mask & bit:
                dup = True
            mask |= bit
        ok = not dup and bin(mask)[2:].strip("0").count("0") == 0
        out.append("Yes" if ok else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
