import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = data[idx : idx + n]
        idx += n
        b = [int(x) for x in data[idx : idx + n]]
        idx += n
        fire = sorted((v for ty, v in zip(a, b) if ty == b"0"), reverse=True)
        frost = sorted((v for ty, v in zip(a, b) if ty == b"1"), reverse=True)
        total = sum(fire) + sum(frost)
        if not fire or not frost:
            ans = total
        elif len(fire) == len(frost):
            # alternate everything; only the very first skill is undoubled
            ans = 2 * total - min(fire[-1], frost[-1])
        else:
            big, small = (fire, frost) if len(fire) > len(frost) else (frost, fire)
            k = len(small)
            # double all of the minority type and the top k of the majority
            ans = total + sum(small) + sum(big[:k])
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
