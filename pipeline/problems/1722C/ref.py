import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        lists = []
        for _ in range(3):
            lists.append(data[idx:idx + n])
            idx += n
        cnt = {}
        for words in lists:
            for w in words:
                cnt[w] = cnt.get(w, 0) + 1
        pts = [0, 3, 1, 0]  # by number of writers
        scores = []
        for words in lists:
            scores.append(sum(pts[cnt[w]] for w in words))
        out.append(" ".join(map(str, scores)))
    sys.stdout.write("\n".join(out) + "\n")


main()
