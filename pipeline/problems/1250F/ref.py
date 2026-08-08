import sys


def main():
    n = int(sys.stdin.buffer.read().split()[0])
    best = None
    i = 1
    while i * i <= n:
        if n % i == 0:
            best = 2 * (i + n // i)
        i += 1
    sys.stdout.write(f"{best}\n")


main()
