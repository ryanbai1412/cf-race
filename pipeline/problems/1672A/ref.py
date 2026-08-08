import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        moves = sum(a) - n
        out.append("errorgorn" if moves % 2 == 1 else "maomao90")
    sys.stdout.write("\n".join(out) + "\n")


main()
