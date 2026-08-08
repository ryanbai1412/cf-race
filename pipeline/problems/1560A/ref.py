import sys


def main():
    liked = [x for x in range(1, 4000) if x % 3 != 0 and x % 10 != 3]
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = [str(liked[int(data[i + 1]) - 1]) for i in range(t)]
    sys.stdout.write("\n".join(out) + "\n")


main()
