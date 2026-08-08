import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

LET = "abcdefghijklmnopqrstuvwxyz"


def word(rnd, lo=1, hi=10):
    return "".join(rnd.choice(LET) for _ in range(rnd.randint(lo, hi)))


def case(rnd, n, m, q, maxy=10**9, wl=(1, 10)):
    s = [word(rnd, *wl) for _ in range(n)]
    t = [word(rnd, *wl) for _ in range(m)]
    ys = [rnd.randint(1, maxy) for _ in range(q)]
    return "{} {}\n{}\n{}\n{}\n{}".format(
        n, m, " ".join(s), " ".join(t), q, "\n".join(map(str, ys)))


def main(outdir):
    rnd = random.Random(1284)
    w = Writer(outdir)
    # max everything
    w.add(case(rnd, 20, 20, 2020, wl=(10, 10)))
    # minimal
    w.add(case(rnd, 1, 1, 1, maxy=1))
    # y = 10^9 exactly and boundary years
    s = ["ab", "cd", "ef"]
    t = ["x", "y", "z", "w"]
    ys = [1, 2, 3, 4, 11, 12, 13, 10**9, 10**9 - 1, 999999937]
    w.add("3 4\n" + " ".join(s) + "\n" + " ".join(t) + "\n" +
          str(len(ys)) + "\n" + "\n".join(map(str, ys)))
    # duplicates among strings
    w.add("2 3\naa aa\nbb bb bb\n4\n1\n2\n3\n1000000000")
    for _ in range(6):
        w.add(case(rnd, rnd.randint(1, 20), rnd.randint(1, 20),
                   rnd.randint(1, 100)))


if __name__ == "__main__":
    main(sys.argv[1])
