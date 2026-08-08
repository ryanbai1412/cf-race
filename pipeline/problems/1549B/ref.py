import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        enemy = data[idx].decode(); idx += 1
        mine = data[idx].decode(); idx += 1
        used = bytearray(n)
        cnt = 0
        for j in range(n):
            if mine[j] != '1':
                continue
            if enemy[j] == '0' and not used[j]:
                used[j] = 1
                cnt += 1
            elif j > 0 and enemy[j - 1] == '1' and not used[j - 1]:
                used[j - 1] = 1
                cnt += 1
            elif j + 1 < n and enemy[j + 1] == '1' and not used[j + 1]:
                used[j + 1] = 1
                cnt += 1
        out.append(cnt)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
