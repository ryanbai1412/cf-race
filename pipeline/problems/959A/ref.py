import sys


def main():
    n = int(sys.stdin.read().split()[0])
    print("Mahmoud" if n % 2 == 0 else "Ehab")


main()
