import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    g = data[1:1 + n]
    cnt = 0
    for i in range(1, n - 1):
        row, up, dn = g[i], g[i - 1], g[i + 1]
        for j in range(1, n - 1):
            if (row[j] == 'X' and up[j - 1] == 'X' and up[j + 1] == 'X'
                    and dn[j - 1] == 'X' and dn[j + 1] == 'X'):
                cnt += 1
    print(cnt)


main()
