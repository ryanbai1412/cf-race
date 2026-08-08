import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        kb = data[1 + 2 * i]
        s = data[2 + 2 * i]
        pos = {ch: j for j, ch in enumerate(kb)}
        total = sum(abs(pos[a] - pos[b]) for a, b in zip(s, s[1:]))
        out.append(total)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
