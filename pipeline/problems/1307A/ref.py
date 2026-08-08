import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n, d = int(data[idx]), int(data[idx + 1]); idx += 2
        a = [int(data[idx + i]) for i in range(n)]; idx += n
        res = a[0]
        for j in range(1, n):
            cost = j
            take = min(a[j], d // cost)
            res += take
            d -= take * cost
        out.append(res)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
