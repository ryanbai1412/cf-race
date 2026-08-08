import sys

data = sys.stdin.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    a = data[idx:idx + n]; idx += n
    m = int(data[idx]); idx += 1
    b = data[idx:idx + m]; idx += m
    ma = max(int(x) for x in a)
    mb = max(int(x) for x in b)
    out.append("Alice" if ma >= mb else "Bob")
    out.append("Bob" if mb >= ma else "Alice")
print("\n".join(out))
