import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

ALPHA = string.ascii_lowercase


def case(kb, s):
    return f"{kb}\n{s}"


def rand_kb(rnd):
    letters = list(ALPHA)
    rnd.shuffle(letters)
    return "".join(letters)


def rand_case(rnd, max_len):
    kb = rand_kb(rnd)
    s = "".join(rnd.choice(ALPHA) for _ in range(rnd.randint(1, max_len)))
    return case(kb, s)


def main(outdir):
    rnd = random.Random(1607)
    w = Writer(outdir)
    # edge: single-letter word, same-letter word, maximum-distance jumps
    w.add(multi([
        case(ALPHA, "a"),
        case(ALPHA, "z"),
        case(ALPHA, "aaaaaaaaaa"),
        case(ALPHA, "az" * 25),
        case(ALPHA[::-1], "az" * 25),
    ]))
    # random short words
    for _ in range(5):
        w.add(multi([rand_case(rnd, 5) for _ in range(200)]))
    # random long words
    for _ in range(5):
        w.add(multi([rand_case(rnd, 50) for _ in range(200)]))
    # max-size: t = 1000, |s| = 50
    w.add(multi([
        case(rand_kb(rnd), "".join(rnd.choice(ALPHA) for _ in range(50)))
        for _ in range(1000)
    ]))


if __name__ == "__main__":
    main(sys.argv[1])
