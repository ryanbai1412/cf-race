import sys


def can(s, memo):
    if s == "":
        return True
    if s in memo:
        return memo[s]
    res = False
    for p in ("aa", "aaa", "bb", "bbb"):
        if s.startswith(p) and can(s[len(p):], memo):
            res = True
            break
    memo[s] = res
    return res


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i].decode()
        out.append("YES" if can(s, {}) else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
