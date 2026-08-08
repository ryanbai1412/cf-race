import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    s = data[idx:idx + n]; idx += n
    t = data[idx:idx + m]; idx += m
    q = int(data[idx]); idx += 1
    out = []
    for i in range(q):
        y = int(data[idx + i])
        out.append(s[(y - 1) % n] + t[(y - 1) % m])
    print("\n".join(out))


main()
