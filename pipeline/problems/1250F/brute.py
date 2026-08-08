"""Independent brute force: try every width from 1 to n."""
import sys


def main():
    n = int(sys.stdin.buffer.read().split()[0])
    best = min(2 * (h + n // h) for h in range(1, n + 1) if n % h == 0)
    sys.stdout.write(f"{best}\n")


main()
