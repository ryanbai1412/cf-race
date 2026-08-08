import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    s = data[idx:idx + n]; idx += n
    t = data[idx:idx + m]; idx += m
    q = int(data[idx]); idx += 1
    for k in range(q):
        y = int(data[idx + k])
        i = j = 0
        for _ in range(y - 1):
            i = (i + 1) % n
            j = (j + 1) % m
        print(s[i] + t[j])


main()
