import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos:pos + n]; pos += n
        a = list(map(int, a))
        cnt = Counter(a)
        uniq = [v for v in cnt if cnt[v] == 1]
        if not uniq:
            out.append("-1")
        else:
            best = min(uniq)
            out.append(str(a.index(best) + 1))
    sys.stdout.write("\n".join(out) + "\n")


main()
