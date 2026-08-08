import sys
from heapq import heappush, heappop


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        a = tuple(int(x) for x in data[idx + 1: idx + 1 + n])
        idx += 1 + n
        full = 0
        for v in a:
            full |= v
        subs = [m for m in range(full + 1) if m | full == full]
        start = tuple(sorted(a))
        seen = {start}
        pq = [(sum(start), start)]
        best = sum(start)
        while pq:
            ssum, arr = heappop(pq)
            best = min(best, ssum)
            for i in range(n):
                for j in range(i + 1, n):
                    orv = arr[i] | arr[j]
                    for x in subs:
                        if x | orv != orv:
                            continue
                        y = orv  # try y covering the rest minimally
                        for y in subs:
                            if x | y == orv:
                                na = list(arr)
                                na[i], na[j] = x, y
                                na = tuple(sorted(na))
                                if na not in seen and sum(na) <= ssum:
                                    seen.add(na)
                                    heappush(pq, (sum(na), na))
        out.append(str(best))
    print("\n".join(out))


main()
