import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def wins(n, mahmoud_turn):
    """True if the player to move wins."""
    moves = range(2, n + 1, 2) if mahmoud_turn else range(1, n + 1, 2)
    for a in moves:
        if not wins(n - a, not mahmoud_turn):
            return True
    return False


def main():
    n = int(sys.stdin.read().split()[0])
    print("Mahmoud" if wins(n, True) else "Ehab")


main()
