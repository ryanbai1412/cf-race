import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        idx += 1  # n
        s = data[idx].decode()
        idx += 1
        seen = set()
        total = 0
        for ch in s:
            total += 1
            if ch not in seen:
                seen.add(ch)
                total += 1
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


main()
