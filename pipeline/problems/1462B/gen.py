import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(s):
    return f"{len(s)}\n{s}"


def rand_digits(rnd, n):
    return "".join(str(rnd.randint(0, 9)) for _ in range(n))


def yes_case(rnd, n):
    k = rnd.randint(0, 4)
    pre, suf = "2020"[:k], "2020"[k:]
    return case(pre + rand_digits(rnd, n - 4) + suf)


def main(outdir):
    rnd = random.Random(14622)
    w = Writer(outdir)
    # edge: n=4 exact and near-misses
    w.add(multi([case("2020"), case("2021"), case("0202"), case("2200"),
                 case("0000"), case("2002")]))
    # tricky: contains 2020 in the middle only -> NO unless prefix/suffix works
    w.add(multi([case("12020"), case("20201"), case("120201"),
                 case("22020"), case("20200"), case("02020"), case("20202")]))
    # constructed YES cases of all split types
    w.add(multi([yes_case(rnd, rnd.randint(4, 200)) for _ in range(200)]))
    # random digit strings (mostly NO)
    w.add(multi([case(rand_digits(rnd, rnd.randint(4, 200)))
                 for _ in range(500)]))
    # random strings over {0,2} (more near-misses)
    w.add(multi([case("".join(rnd.choice("02") for _ in range(rnd.randint(4, 30))))
                 for _ in range(500)]))
    # max: t=1000, n=200
    cases = []
    for i in range(1000):
        if i % 2 == 0:
            cases.append(yes_case(rnd, 200))
        else:
            cases.append(case(rand_digits(rnd, 200)))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
