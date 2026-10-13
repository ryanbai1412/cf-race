from genlib import *  # noqa: F401,F403

CHECKER = "Three fixed-phrase lines; names in input order; unique, exact token comparison."
STATEMENT = "Legend (taxi = six equal digits, pizza = six strictly decreasing digits, rest girls; duplicates counted), input (1<=n<=100, 0<=si<=100, names <=20 letters), output present."
PH = ["If you want to call a taxi, you should call: ", "If you want to order a pizza, you should call: ",
      "If you want to go to a cafe with a wonderful girl, you should call: "]


def kind(num):
    d = num.replace("-", "")
    if len(set(d)) == 1:
        return 0
    if all(d[i] > d[i + 1] for i in range(5)):
        return 1
    return 2


def solve(s):
    t = s.split()
    n, i, rows = int(t[0]), 1, []
    for _ in range(n):
        k, name = int(t[i]), t[i + 1]
        c = [0, 0, 0]
        for num in t[i + 2:i + 2 + k]:
            c[kind(num)] += 1
        rows.append((name, c))
        i += 2 + k
    out = []
    for j in range(3):
        m = max(c[j] for _, c in rows)
        out.append(PH[j] + ", ".join(name for name, c in rows if c[j] == m) + ".")
    return "\n".join(out) + "\n"


def number(g):
    r = g.random()
    if r < 0.25:
        d = [str(g.randint(0, 9))] * 6
    elif r < 0.5:
        d = sorted(map(str, g.sample(range(10), 6)), reverse=True)
    else:
        d = [str(g.randint(0, 9)) for _ in range(6)]
    return "".join(d[0:2]) + "-" + "".join(d[2:4]) + "-" + "".join(d[4:6])


def name(g):
    return "".join(g.choice("abcXYZ") for _ in range(g.randint(1, 20)))


def make(g, n, smax):
    rows = [n]
    for _ in range(n):
        k = g.randint(0, smax)
        rows.append(f"{k} {name(g)}")
        rows += [number(g) for _ in range(k)]
    return fmt(*rows)


def cases(g):
    out = [("boundary", "n=1 empty book", fmt(1, "0 A")), ("boundary", "all empty ties", fmt(3, "0 A", "0 bb", "0 Ccc")),
           ("adversarial", "123456 is not pizza; 98-76-54 is", fmt(2, "2 Ann", "12-34-56", "98-76-54", "1 Bob", "11-11-11")),
           ("adversarial", "duplicate numbers counted twice", fmt(2, "2 X", "22-22-22", "22-22-22", "1 Y", "33-33-33")),
           ("adversarial", "non-strict decreasing 99-87-65 is girl", fmt(1, "1 Z", "99-87-65")),
           ("maxSize", "n=100 s=100", make(g, 100, 100)), ("maxSize", "n=100 max names", fmt(100, *["100 " + "q" * 20 + "\n" + "\n".join(["98-76-54"] * 100)] * 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 4), 4), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(5, 100), 30), 25)
    return out
