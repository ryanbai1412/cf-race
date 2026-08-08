import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    for i in range(1, t + 1):
        s = data[i]
        if s[-5:] == "mnida":
            print("KOREAN")
        elif s[-4:] in ("desu", "masu"):
            print("JAPANESE")
        else:
            print("FILIPINO")


main()
