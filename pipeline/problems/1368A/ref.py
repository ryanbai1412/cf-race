import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        a = int(data[1 + 3 * i]); b = int(data[2 + 3 * i]); n = int(data[3 + 3 * i])
        steps = 0
        while a <= n and b <= n:
            if a < b:
                a += b
            else:
                b += a
            steps += 1
        out.append(steps)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
