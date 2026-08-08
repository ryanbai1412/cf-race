import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def win(state):
    # state: sorted tuple of log lengths > 1 (length-1 logs are dead)
    for i, x in enumerate(state):
        for y in range(1, x // 2 + 1):
            z = x - y
            nxt = list(state[:i]) + list(state[i + 1:])
            if y > 1:
                nxt.append(y)
            if z > 1:
                nxt.append(z)
            if not win(tuple(sorted(nxt))):
                return True
    return False


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        state = tuple(sorted(x for x in a if x > 1))
        out.append("errorgorn" if win(state) else "maomao90")
    sys.stdout.write("\n".join(out) + "\n")


main()
