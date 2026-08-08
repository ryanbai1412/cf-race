import sys
from itertools import combinations_with_replacement


def solve(arr):
    # try increasing numbers of total steps
    n = len(arr)
    for total in range(0, 2 * n + 2):
        # distribute `total` +1 steps among indices
        def ok(add):
            b = [arr[i] + add[i] for i in range(n)]
            if sum(b) == 0:
                return False
            for x in b:
                if x == 0:
                    return False
            return True
        # enumerate distributions
        def rec(i, rem, add):
            if i == n:
                return rem == 0 and ok(add)
            for k in range(rem + 1):
                add[i] = k
                if rec(i + 1, rem - k, add):
                    return True
            add[i] = 0
            return False
        if rec(0, total, [0] * n):
            return total
    return -1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        n = int(data[idx]); idx += 1
        arr = [int(x) for x in data[idx:idx + n]]; idx += n
        print(solve(arr))


main()
