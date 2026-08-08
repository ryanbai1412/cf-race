import sys

data = sys.stdin.buffer.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    a = [int(x) for x in data[idx:idx + n]]; idx += n
    evens = [x for x in a if x % 2 == 0]
    if len(evens) < n:  # at least one odd: fuse each even with an odd
        out.append(str(len(evens)))
    else:
        tz = min((x & -x).bit_length() - 1 for x in evens)
        out.append(str(tz + len(evens) - 1))
print("\n".join(out))
