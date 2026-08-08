import sys


def main():
    data = sys.stdin.read().split()
    s = data[1]
    occ = [0] * 10
    for ch in s:
        if ch == "L":
            occ[occ.index(0)] = 1
        elif ch == "R":
            for i in range(9, -1, -1):
                if occ[i] == 0:
                    occ[i] = 1
                    break
        else:
            occ[int(ch)] = 0
    print("".join(map(str, occ)))


main()
