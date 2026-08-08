import sys
from itertools import combinations


def contiguous(s):
    t = s.replace("0", " ").split()
    return len(t) <= 1


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    for i in range(1, t + 1):
        s = data[i]
        zeros = [j for j, ch in enumerate(s) if ch == "0"]
        ans = None
        for k in range(len(zeros) + 1):
            found = False
            for rem in combinations(zeros, k):
                r = set(rem)
                ns = "".join(ch for j, ch in enumerate(s) if j not in r)
                if contiguous(ns):
                    found = True
                    break
            if found:
                ans = k
                break
        print(ans)


main()
