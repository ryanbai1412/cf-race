import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    out = []
    for s in data[1:1 + n]:
        cs = sorted(s)
        ok = len(set(cs)) == len(cs) and ord(cs[-1]) - ord(cs[0]) == len(cs) - 1
        out.append("Yes" if ok else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
