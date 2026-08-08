import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        s = data[2 + 2 * i]
        zeros = [j for j, ch in enumerate(s) if ch == "0"]
        ans = 0
        for a, b in zip(zeros, zeros[1:]):
            gap = b - a - 1
            if gap < 2:
                ans += 2 - gap
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
