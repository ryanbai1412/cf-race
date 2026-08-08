import sys
from functools import lru_cache


def val(c):
    return ord(c) - 96


@lru_cache(maxsize=None)
def best_diff(s, turn):
    # returns max (current player's score - opponent's score) achievable
    if s == "":
        return 0
    parity = 0 if turn == 0 else 1  # Alice even, Bob odd
    best = None
    k = len(s)
    for l in range(k):
        for r in range(l - 1, k):  # r = l-1 means empty removal
            length = r - l + 1
            if length % 2 != parity:
                continue
            gain = sum(val(c) for c in s[l:r + 1])
            rest = s[:l] + s[r + 1:]
            if length == 0 and rest == s:
                # empty move allowed only for Alice (even, possibly empty)
                if turn != 0:
                    continue
            cand = gain - best_diff(rest, 1 - turn)
            if best is None or cand > best:
                best = cand
    if best is None:  # no legal move: statement implies game continues until empty
        # player must skip? Alice can remove empty substring; Bob cannot.
        # If Bob cannot move on nonempty string... he always can (odd length >=1 exists).
        return -best_diff(s, 1 - turn) if turn == 0 else 0
    return best


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i].decode()
        d = best_diff(s, 0)
        if d > 0:
            out.append(f"Alice {d}")
        else:
            out.append(f"Bob {-d}")
    sys.stdout.write("\n".join(out) + "\n")


main()
