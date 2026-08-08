import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    pref = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref[i + 1] = pref[i] + (ord(ch) - 96)
    out = []
    idx = 3
    for _ in range(q):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        out.append(pref[r] - pref[l - 1])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
