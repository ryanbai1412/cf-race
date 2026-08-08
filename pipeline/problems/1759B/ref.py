import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    i = 1
    out = []
    for _ in range(t):
        m, s = int(data[i]), int(data[i + 1])
        i += 2
        present = set(map(int, data[i : i + m]))
        i += m
        x = 1
        while s > 0:
            while x in present:
                x += 1
            if x > s:
                break
            present.add(x)
            s -= x
        ok = s == 0 and max(present) == len(present)
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
