import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        n = int(data[1 + 2 * i])
        s = int(data[2 + 2 * i])
        answers = []
        for k in range(n + 2):
            r = s - k * n * n
            if 0 <= r <= (n + 1 - k) * (n - 1):
                answers.append(k)
        assert len(answers) == 1, (n, s, answers)
        out.append(str(answers[0]))
    print("\n".join(out))


main()
