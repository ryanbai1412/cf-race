import sys


def main():
    data = sys.stdin.read().split()
    s = data[1]
    # BFS over all reachable strings via replacing UR/RU with D
    seen = {s}
    frontier = [s]
    best = len(s)
    while frontier:
        nxt = []
        for cur in frontier:
            best = min(best, len(cur))
            for i in range(len(cur) - 1):
                pair = cur[i : i + 2]
                if pair in ("UR", "RU"):
                    t = cur[:i] + "D" + cur[i + 2 :]
                    if t not in seen:
                        seen.add(t)
                        nxt.append(t)
        frontier = nxt
    print(best)


main()
