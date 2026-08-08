import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        s = data[idx].decode(); idx += 1
        target = sorted(s)
        out.append(sum(1 for i in range(n) if s[i] != target[i]))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
