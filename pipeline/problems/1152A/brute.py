"""Independent brute force: greedy pairing simulation over key lists."""
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    b = list(map(int, data[2 + n:2 + n + m]))
    keys = list(b)
    cnt = 0
    for ch in a:
        for i, k in enumerate(keys):
            if (ch + k) % 2 == 1:
                keys.pop(i)
                cnt += 1
                break
    print(cnt)


main()
