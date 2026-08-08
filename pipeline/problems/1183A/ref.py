import sys

a = int(sys.stdin.read().split()[0])
n = a
while sum(int(c) for c in str(n)) % 4 != 0:
    n += 1
print(n)
