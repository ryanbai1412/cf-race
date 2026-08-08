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
        m = min(a)
        out.append(sum(a) - m * n)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
