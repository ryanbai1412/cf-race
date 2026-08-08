"""Independent brute force: DP over liters (small n only)."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    out = []
    for i in range(q):
        n, a, b = (int(v) for v in data[1 + 3 * i:4 + 3 * i])
        dp = [0] * (n + 1)
        for k in range(1, n + 1):
            dp[k] = dp[k - 1] + a
            if k >= 2:
                dp[k] = min(dp[k], dp[k - 2] + b)
        out.append(dp[n])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
