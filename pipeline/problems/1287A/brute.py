import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        idx += 1
        s = list(data[idx]); idx += 1
        minute = 0
        while True:
            ns = s[:]
            changed = False
            for i, ch in enumerate(s):
                if ch == "A" and i + 1 < len(s) and s[i + 1] == "P":
                    ns[i + 1] = "A"
                    changed = True
            if not changed:
                break
            s = ns
            minute += 1
        print(minute)


main()
