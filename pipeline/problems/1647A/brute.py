import sys


def best_number(n):
    best = None

    def dfs(prefix, last, rem):
        nonlocal best
        if rem == 0:
            v = int(prefix)
            if best is None or v > best:
                best = v
            return
        for d in range(1, min(9, rem) + 1):
            if d != last:
                dfs(prefix + str(d), d, rem - d)

    dfs("", 0, n)
    return best


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = [str(best_number(int(data[i]))) for i in range(1, t + 1)]
    print("\n".join(out))


main()
