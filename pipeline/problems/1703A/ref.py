import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        out.append("YES" if data[i].decode().upper() == "YES" else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
