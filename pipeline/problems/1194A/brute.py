import sys


def sim(n, x):
    nums = list(range(1, n + 1))
    i = 1
    while len(nums) >= i:
        nums.pop(i - 1)
        i += 1
    return nums[x - 1]


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + 2 * i])
        x = int(data[2 + 2 * i])
        out.append(sim(n, x))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
