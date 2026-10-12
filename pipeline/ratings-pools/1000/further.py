"""Additional exact-rating candidates; independent semantic/checker audit still required."""
from itertools import permutations
import json
from pathlib import Path
import random

from additional import require
from recipes import within

IDS = ("143A", "452A")
REVIEW = json.loads(Path(__file__).with_name("final-statement-review.json").read_text())
RULES = {pid: REVIEW[pid]["input_format"] for pid in IDS}
RULES["143A"] += " At most one grid: 2*a=r1+c1-d2 then b=r1-a,c=c1-a,d=r2-c. Audit this uniqueness despite statement allowing any solution."
RULES["452A"] += " Exactly one of the eight named evolutions must match; lowercase token output."
POKEMON = tuple("vaporeon jolteon flareon espeon umbreon leafeon glaceon sylveon".split())


def output(pid, text):
    rows = text.splitlines()
    if pid == "452A":
        require(len(rows) == 2 and len(rows[0].split()) == 1 and len(rows[1].split()) == 1)
        n, pattern = int(rows[0]), rows[1]
        within(n, 6, 8)
        require(len(pattern) == n and all(c == "." or "a" <= c <= "z" for c in pattern))
        matches = [p for p in POKEMON if len(p) == n and all(x == "." or x == y for x, y in zip(pattern, p))]
        require(len(matches) == 1)
        return matches[0] + "\n"
    require(pid == "143A" and len(rows) == 3 and all(len(r.split()) == 2 for r in rows))
    values = list(map(int, text.split()))
    for v in values:
        within(v, 1, 20)
    r1, r2, c1, c2, d1, d2 = values
    if (r1 + c1 - d2) % 2:
        return "-1\n"
    a = (r1 + c1 - d2) // 2
    b, c = r1 - a, c1 - a
    d = r2 - c
    if not all(1 <= x <= 9 for x in (a, b, c, d)) or len({a, b, c, d}) != 4 or b + d != c2 or a + d != d1 or b + c != d2:
        return "-1\n"
    return f"{a} {b}\n{c} {d}\n"


def sums(grid):
    a, b, c, d = grid
    return (a + b, c + d, a + c, b + d, a + d, b + c)


def grid_input(values):
    return "".join(f"{values[i]} {values[i+1]}\n" for i in (0, 2, 4))


def patterns():
    candidates = set()
    for pokemon in POKEMON:
        for mask in range(1 << len(pokemon)):
            pattern = "".join(c if mask & (1 << i) else "." for i, c in enumerate(pokemon))
            matches = [p for p in POKEMON if len(p) == len(pattern) and all(x == "." or x == y for x, y in zip(pattern, p))]
            if len(matches) == 1:
                candidates.add((len(pattern), pattern))
    return sorted(candidates)


def extras(pid):
    if pid == "452A":
        inputs = [f"{n}\n{pattern}\n" for n, pattern in patterns()]
        return [{"input": text, "output": output(pid, text), "caseKind": "max-size" if int(text.splitlines()[0]) == 8 else "boundary" if int(text.splitlines()[0]) == 6 else "adversarial"} for text in inputs]
    rng = random.Random(1000143)
    grids = list(permutations(range(1, 10), 4))
    rng.shuffle(grids)
    values = [(1,) * 6, (20,) * 6] + [sums(g) for g in grids[:100]] + [tuple(rng.randint(1, 20) for _ in range(6)) for _ in range(100)]
    inputs = list(dict.fromkeys(grid_input(v) for v in values))
    return [{"input": text, "output": output(pid, text), "caseKind": "max-size" if "20" in text.split() else "boundary" if i == 0 else "adversarial"} for i, text in enumerate(inputs)]
