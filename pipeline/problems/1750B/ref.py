import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        idx += 1  # n
        s = data[idx].decode()
        idx += 1
        ones = s.count("1")
        zeros = len(s) - ones
        run = best = 1
        for i in range(1, len(s)):
            run = run + 1 if s[i] == s[i - 1] else 1
            best = max(best, run)
        ans = best * best
        if ones and zeros:
            ans = max(ans, ones * zeros)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
