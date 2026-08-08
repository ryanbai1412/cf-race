"""Independent solution: smallest k such that the sequence can be split into k
strictly increasing subsequences, found by greedy feasibility check
(place each element on the first color whose last value is smaller)."""
import sys


def feasible(a, k):
    last = [None] * k
    for v in a:
        for i in range(k):
            if last[i] is None or last[i] < v:
                last[i] = v
                break
        else:
            return False
    return True


def solve(a):
    k = 1
    while not feasible(a, k):
        k += 1
    return k


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = list(map(int, data[p:p + n])); p += n
        out.append(str(solve(a)))
    sys.stdout.write("\n".join(out) + "\n")


main()
