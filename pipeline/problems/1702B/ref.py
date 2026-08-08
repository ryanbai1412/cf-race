import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i].decode()
        days = 0
        cur = set()
        for ch in s:
            if ch not in cur:
                if len(cur) == 3:
                    days += 1
                    cur = set()
                cur.add(ch)
        if cur:
            days += 1
        out.append(str(days))
    sys.stdout.write("\n".join(out) + "\n")


main()
