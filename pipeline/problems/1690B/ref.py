import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        b = [int(x) for x in data[pos:pos + n]]; pos += n
        ok = True
        k = -1
        for ai, bi in zip(a, b):
            if bi > ai:
                ok = False
                break
            if bi > 0:
                if k == -1:
                    k = ai - bi
                elif ai - bi != k:
                    ok = False
                    break
        if ok and k != -1:
            for ai, bi in zip(a, b):
                if bi == 0 and ai > k:
                    ok = False
                    break
        out.append("YES" if ok else "NO")
    sys.stdout.write("\n".join(out) + "\n")


main()
