import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def main(outdir):
    rnd = random.Random(1060)
    w = Writer(outdir)
    w.add(case("8"))
    w.add(case("0"))
    w.add(case("8" * 100))
    w.add(case("0" * 100))
    w.add(case("8" * 11 + "0" * 89))
    w.add(case("8" * 9 + "0" * 90))          # 9 eights, floor(100/11)=9
    w.add(case("8" * 10 + "0" * 90))         # more eights than groups
    w.add(case("0" * 10 + "8"))              # exactly one number
    w.add(case("0" * 10))                    # length 10, impossible
    w.add(case("8" * 99))                    # 99 digits, 9 numbers
    for n in (1, 2, 11, 12, 21, 22, 33, 99, 100):
        w.add(case("".join(rnd.choice("08") for _ in range(n))))
    for _ in range(3):
        n = rnd.randint(1, 100)
        w.add(case("".join(rnd.choice("0123456789") for _ in range(n))))


if __name__ == "__main__":
    main(sys.argv[1])
