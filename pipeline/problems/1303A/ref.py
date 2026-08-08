import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        if "1" in s:
            core = s[s.index("1"):s.rindex("1") + 1]
            out.append(core.count("0"))
        else:
            out.append(0)
    print("\n".join(map(str, out)))


main()
