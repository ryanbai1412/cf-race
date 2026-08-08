import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        ab = []
        for _ in range(n):
            ab.append((int(data[pos]), int(data[pos + 1])))
            pos += 2
        tm = [int(data[pos + i]) for i in range(n)]
        pos += n
        depart_prev = 0
        b_prev = 0
        arrive = 0
        for i in range(n):
            a, b = ab[i]
            arrive = depart_prev + (a - b_prev + tm[i])
            stay = (b - a + 1) // 2
            depart_prev = max(b, arrive + stay)
            b_prev = b
        out.append(arrive)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
