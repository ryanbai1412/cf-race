import sys

a = int(sys.stdin.read().split()[0])
n = a
while True:
    s = 0
    m = n
    while m:
        s += m % 10
        m //= 10
    if s % 4 == 0:
        print(n)
        break
    n += 1
