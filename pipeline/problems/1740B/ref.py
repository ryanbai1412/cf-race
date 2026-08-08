import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        width_sum = 0
        max_h = 0
        for _ in range(n):
            a, b = int(data[idx]), int(data[idx + 1])
            idx += 2
            if a > b:
                a, b = b, a
            width_sum += a
            if b > max_h:
                max_h = b
        out.append(str(2 * (width_sum + max_h)))
    sys.stdout.write("\n".join(out) + "\n")


main()
