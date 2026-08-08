import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        arr = [int(x) for x in data[idx:idx + n]]; idx += n
        z = sum(1 for x in arr if x == 0)
        steps = z
        if sum(arr) + z == 0:
            steps += 1
        out.append(steps)
    print("\n".join(map(str, out)))


main()
