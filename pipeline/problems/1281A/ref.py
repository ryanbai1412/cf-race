import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        if s.endswith("po"):
            out.append("FILIPINO")
        elif s.endswith("desu") or s.endswith("masu"):
            out.append("JAPANESE")
        else:
            out.append("KOREAN")
    print("\n".join(out))


main()
