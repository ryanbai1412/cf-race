import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        b, p, f = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        h, c = int(data[idx + 3]), int(data[idx + 4])
        idx += 5
        pairs = b // 2
        profit = 0
        for price, stock in sorted(((h, p), (c, f)), reverse=True):
            k = min(pairs, stock)
            profit += k * price
            pairs -= k
        out.append(str(profit))
    print("\n".join(out))


main()
