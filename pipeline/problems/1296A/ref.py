import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        arr = [int(x) for x in data[idx:idx + n]]; idx += n
        odd = sum(1 for x in arr if x % 2)
        even = n - odd
        if odd == 0:
            out.append("NO")
        elif sum(arr) % 2 == 1 or even > 0:
            out.append("YES")
        else:
            out.append("NO")
    print("\n".join(out))


main()
