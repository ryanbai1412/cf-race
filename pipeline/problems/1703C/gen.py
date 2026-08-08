import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1703 * 3)
w = Writer(sys.argv[1])


def case(n):
    a = [rng.randint(0, 9) for _ in range(n)]
    lines = [str(n), " ".join(map(str, a))]
    for _ in range(n):
        b = rng.randint(1, 10)
        moves = "".join(rng.choice("UD") for _ in range(b))
        lines.append(f"{b} {moves}")
    return "\n".join(lines)


def fixed_case(a, moves_list):
    lines = [str(len(a)), " ".join(map(str, a))]
    for m in moves_list:
        lines.append(f"{len(m)} {m}")
    return "\n".join(lines)


# edge: n=1, wraparound cases
w.add(multi([
    fixed_case([0], ["U"]),
    fixed_case([9], ["D"]),
    fixed_case([0], ["D"]),
    fixed_case([9], ["U"]),
    fixed_case([5], ["UUUUUUUUUU"]),
    fixed_case([5], ["DDDDDDDDDD"]),
    fixed_case([0, 9], ["UUUUU", "DDDDD"]),
]))
# all-U and all-D max-length moves on each digit
w.add(multi([fixed_case(list(range(10)), ["U" * 10] * 10),
             fixed_case(list(range(10)), ["D" * 10] * 10)]))
# random small
for _ in range(3):
    w.add(multi([case(rng.randint(1, 10)) for _ in range(100)]))
# random max: t=100, n=100
for _ in range(3):
    w.add(multi([case(100) for _ in range(100)]))
