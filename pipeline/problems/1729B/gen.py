import random
import string
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def encode(s: str) -> str:
    out = []
    for ch in s:
        num = ord(ch) - ord("a") + 1
        out.append(str(num))
        if num >= 10:
            out.append("0")
    return "".join(out)


def rand_string(rnd, alphabet, max_code_len=50):
    s = ""
    while True:
        ch = rnd.choice(alphabet)
        if len(encode(s + ch)) > max_code_len:
            return s
        s += ch
        if rnd.random() < 0.05 and s:
            return s


def case(s: str) -> str:
    t = encode(s)
    return f"{len(t)}\n{t}"


def main(outdir):
    rnd = random.Random(172902)
    w = Writer(outdir)
    low = string.ascii_lowercase
    # every single letter
    w.add(multi([case(ch) for ch in low]))
    # edge: max-length codes of tricky letters (j=10 -> "100", t=20 -> "200")
    w.add(multi([case("a" * 50), case("z" * 16), case("j" * 16),
                 case("t" * 16), case("aj" * 12), case("ja" * 12),
                 case("e" * 50), case("jt" * 12)]))
    # random over full alphabet
    w.add(multi([case(rand_string(rnd, low)) for _ in range(10**4)]))
    # random over ambiguity-prone letters (codes containing 0/1/2 digits)
    tricky = "abjklmnopqrst"
    w.add(multi([case(rand_string(rnd, tricky)) for _ in range(10**4)]))
    # random over two-digit letters only
    w.add(multi([case(rand_string(rnd, low[9:])) for _ in range(10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
