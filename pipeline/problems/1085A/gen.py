import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def encrypt(s):
    res = ""
    for i, ch in enumerate(s, 1):
        if i == 1 or i % 2 == 0:
            res = res + ch
        else:
            res = ch + res
    return res


def main(outdir):
    rnd = random.Random(1085)
    w = Writer(outdir)
    w.add(encrypt("a"))
    w.add(encrypt("ab"))
    w.add(encrypt("abc"))
    w.add(encrypt("a" * 50))
    w.add(encrypt("z" * 49))
    w.add(encrypt("abcdefghijklmnopqrstuvwxyz"))
    w.add(encrypt("abcdefghijklmnopqrstuvwxyz" * 2)[:50] if False else encrypt(
        ("abcdefghijklmnopqrstuvwxyz" * 2)[:50]))
    w.add(encrypt("ab" * 25))
    w.add(encrypt("racecar"))
    for n in (2, 3, 4, 5, 49, 50):
        w.add(encrypt("".join(rnd.choice("ab") for _ in range(n))))
    for _ in range(5):
        n = rnd.randint(1, 50)
        w.add(encrypt("".join(rnd.choice("abcdefghijklmnopqrstuvwxyz")
                              for _ in range(n))))


if __name__ == "__main__":
    main(sys.argv[1])
