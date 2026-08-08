"""Independent implementation using a set of occupied rooms."""
import sys


def main():
    data = sys.stdin.read().split()
    s = data[1]
    occ = set()
    for ch in s:
        if ch == "L":
            occ.add(min(i for i in range(10) if i not in occ))
        elif ch == "R":
            occ.add(max(i for i in range(10) if i not in occ))
        else:
            occ.remove(int(ch))
    print("".join("1" if i in occ else "0" for i in range(10)))


main()
