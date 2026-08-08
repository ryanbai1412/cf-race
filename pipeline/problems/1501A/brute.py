"""Independent second implementation: event-by-event simulation."""
import sys


def main():
    inp = sys.stdin.read().split("\n")
    ptr = 0

    def line():
        nonlocal ptr
        while inp[ptr].strip() == "":
            ptr += 1
        ptr += 1
        return inp[ptr - 1]

    t = int(line())
    res = []
    for _ in range(t):
        n = int(line())
        pairs = [tuple(map(int, line().split())) for _ in range(n)]
        tm = list(map(int, line().split()))
        cur = 0  # current time; train departing previous station
        prev_b = 0
        for i in range(n):
            a, b = pairs[i]
            travel = a - prev_b + tm[i]
            cur = cur + travel  # arrival time at station i
            if i == n - 1:
                res.append(cur)
                break
            # departure: waited >= ceil((b-a)/2) and time >= b
            need = -(-(b - a) // 2)
            dep = cur + need
            if dep < b:
                dep = b
            cur = dep
            prev_b = b
    print("\n".join(map(str, res)))


main()
