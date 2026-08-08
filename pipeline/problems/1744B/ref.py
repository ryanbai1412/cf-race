import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n, q = int(data[idx]), int(data[idx + 1])
        idx += 2
        a = [int(x) for x in data[idx:idx + n]]
        idx += n
        total = sum(a)
        even = sum(1 for x in a if x % 2 == 0)
        odd = n - even
        for _ in range(q):
            typ, x = int(data[idx]), int(data[idx + 1])
            idx += 2
            if typ == 0:
                total += even * x
                if x % 2 == 1:
                    odd += even
                    even = 0
            else:
                total += odd * x
                if x % 2 == 1:
                    even += odd
                    odd = 0
            out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
