import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    i = 1
    out = []
    for _ in range(t):
        n = int(data[i])
        i += 1
        s = list(map(int, data[i : i + n]))
        i += n
        srt = sorted(s, reverse=True)
        m1, m2 = srt[0], srt[1]
        out.append(" ".join(str(x - (m2 if x == m1 else m1)) for x in s))
    sys.stdout.write("\n".join(out) + "\n")


main()
