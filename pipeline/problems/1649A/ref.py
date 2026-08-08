import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = data[idx:idx + n]; idx += n
        zeros = [i for i, v in enumerate(a) if v == "0"]
        out.append(str(zeros[-1] - zeros[0] + 2) if zeros else "0")
    sys.stdout.write("\n".join(out) + "\n")


main()
