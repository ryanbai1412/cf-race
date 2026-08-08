import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = [int(v) for v in data[idx : idx + n]]
        idx += n
        zeros = a.count(0)
        if zeros:
            out.append(n - zeros)
        elif len(set(a)) < n:
            out.append(n)
        else:
            out.append(n + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
