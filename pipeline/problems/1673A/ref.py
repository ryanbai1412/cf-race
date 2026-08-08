import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        total = sum(c - 96 for c in s)
        if len(s) % 2 == 0:
            out.append(f"Alice {total}")
        else:
            leave = min(s[0], s[-1]) - 96
            diff = total - 2 * leave
            if diff > 0:
                out.append(f"Alice {diff}")
            else:
                out.append(f"Bob {-diff}")
    sys.stdout.write("\n".join(out) + "\n")


main()
