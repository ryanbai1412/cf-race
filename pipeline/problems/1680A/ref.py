import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        l1, r1, l2, r2 = (int(v) for v in data[idx : idx + 4])
        idx += 4
        if max(l1, l2) <= min(r1, r2):
            out.append(max(l1, l2))
        else:
            out.append(l1 + l2)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
