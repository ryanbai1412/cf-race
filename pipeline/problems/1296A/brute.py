import sys
from itertools import product


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        n = int(data[idx]); idx += 1
        arr = [int(x) % 2 for x in data[idx:idx + n]]; idx += n
        # reachable arrays: BFS over parity tuples via a_i := a_j
        seen = {tuple(arr)}
        stack = [tuple(arr)]
        ok = False
        while stack:
            cur = stack.pop()
            if sum(cur) % 2 == 1:
                ok = True
                break
            for i in range(n):
                for j in range(n):
                    if i != j and cur[i] != cur[j]:
                        nxt = list(cur)
                        nxt[i] = cur[j]
                        tn = tuple(nxt)
                        if tn not in seen:
                            seen.add(tn)
                            stack.append(tn)
        print("YES" if ok else "NO")


main()
