import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

TOTAL = 1000  # sum of |s_i| over all test cases


def case(strs):
    return f"{len(strs)}\n" + "\n".join(strs)


def rand_str(rnd, n, alpha="abc"):
    return "".join(rnd.choice(alpha) for _ in range(n))


def main(outdir):
    rnd = random.Random(1397)
    w = Writer(outdir)

    # minimal: single string of length 1 (always YES)
    w.add(multi([case(["a"])]))
    # one test case with n = 1000 strings of length 1 (max n, max total length)
    w.add(multi([case(["a"] * 1000)]))
    # n = 1000 with a single mismatching letter -> NO
    strs = ["a"] * 999 + ["b"]
    w.add(multi([case(strs)]))
    # one long string of length 1000 with n = 1 (always YES)
    w.add(multi([case([rand_str(rnd, 1000, string.ascii_lowercase)])]))
    # one string of length 999 plus one of length 1
    w.add(multi([case(["a" * 999, "a"])]))
    # 10 test cases, total length 1000, counts made divisible by n (all YES)
    cases = []
    for i in range(10):
        n = rnd.randint(2, 5)
        per = TOTAL // 10 // n
        letters = rand_str(rnd, per, string.ascii_lowercase)
        pool = list(letters * n)
        rnd.shuffle(pool)
        cases.append(case(["".join(pool[k::n]) for k in range(n)]))
    w.add(multi(cases))
    # hand-made small cases
    w.add(multi([case(["ab", "ba"]), case(["ab", "ab", "ab"]),
                 case(["a", "b"]), case(["abc", "abc", "abd"]),
                 case(["zz", "zz"]), case(["ba", "ab", "ab"])]))
    # random tests over a 2-letter alphabet (many YES/NO mixes)
    for _ in range(7):
        t = rnd.randint(1, 10)
        cs = []
        budget = TOTAL
        for j in range(t):
            n = rnd.randint(1, 5)
            cs.append(case([rand_str(rnd, rnd.randint(1, max(1, min(6, budget // 10))),
                                     rnd.choice(["ab", "abc", "a"]))
                            for _ in range(n)]))
        w.add(multi(cs))
    # random tests over the full alphabet, short strings
    for _ in range(5):
        t = rnd.randint(1, 10)
        cs = []
        for _ in range(t):
            n = rnd.randint(1, 6)
            cs.append(case([rand_str(rnd, rnd.randint(1, 8), string.ascii_lowercase)
                            for _ in range(n)]))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
