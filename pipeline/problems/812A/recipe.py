from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO; unique, exact token comparison."
STATEMENT = "Legend (pedestrian green with conflicting car lane), input (four lines of l s r p in {0,1}, counter-clockwise), output present."


def solve(s):
    a = ints(s)
    q = [a[4 * i:4 * i + 4] for i in range(4)]
    for i in range(4):
        if q[i][3] and (q[i][0] or q[i][1] or q[i][2] or q[(i + 1) % 4][0] or q[(i + 2) % 4][1] or q[(i + 3) % 4][2]):
            return "YES\n"
    return "NO\n"


def grid(mask):
    return fmt(*[[(mask >> (4 * i + j)) & 1 for j in range(4)] for i in range(4)])


def cases(g):
    out = [("boundary", "all red", grid(0)), ("boundary", "all green", grid(2 ** 16 - 1)),
           ("adversarial", "pedestrian only all parts", grid(sum(1 << (4 * i + 3) for i in range(4))))]
    for i in range(4):
        for j in range(3):
            for k in range(4):
                if len(out) < 40:
                    out.append(("adversarial", "one pedestrian one lane", grid((1 << (4 * i + 3)) | (1 << (4 * k + j)))))
    out.append(("maxSize", "cars only all green", grid(sum(7 << (4 * i) for i in range(4)))))
    out += fill(g, lambda g: grid(g.randrange(2 ** 16)), 80)
    return out
