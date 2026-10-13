"""Constraint-checked, additive cases for the three primary-auditor findings."""
from itertools import product

IDS = ("404A", "465B", "29A")


def answer(pid, text):
    lines = text.splitlines()
    n = int(lines[0])
    if pid == "404A":
        assert 3 <= n < 300 and n % 2 == 1 and len(lines) == n + 1
        grid = lines[1:]
        assert all(len(row) == n and all("a" <= c <= "z" for c in row) for row in grid)
        diagonal, background = grid[0][0], grid[0][1]
        valid = diagonal != background and all(
            grid[i][j] == (diagonal if i == j or i + j == n - 1 else background)
            for i in range(n) for j in range(n))
        return "YES\n" if valid else "NO\n"
    if pid == "465B":
        assert 1 <= n <= 1000 and len(lines) == 2
        values = list(map(int, lines[1].split()))
        assert len(values) == n and set(values) <= {0, 1}
        ones = sum(values)
        blocks = sum(value == 1 and (i == 0 or values[i - 1] == 0)
                     for i, value in enumerate(values))
        return f"{ones + max(0, blocks - 1)}\n"
    if pid == "29A":
        assert 1 <= n <= 100 and len(lines) == n + 1
        records = [tuple(map(int, line.split())) for line in lines[1:]]
        assert all(len(row) == 2 for row in records)
        assert len({x for x, _ in records}) == n
        assert all(-10000 <= x <= 10000 and 1 <= abs(d) <= 20000 for x, d in records)
        mutual = any(x + d == y and y + e == x
                     for i, (x, d) in enumerate(records) for y, e in records[i + 1:])
        return "YES\n" if mutual else "NO\n"
    raise ValueError(pid)


def cases(pid):
    result = []

    def add(text, reason, *categories):
        result.append({"input": text, "output": answer(pid, text),
                       "reason": reason, "categories": list(categories)})

    if pid == "404A":
        for n in (3, 5, 299):
            grid = ["".join("a" if i == j or i + j == n - 1 else "b"
                            for j in range(n)) for i in range(n)]
            text = str(n) + "\n" + "\n".join(grid) + "\n"
            add(text, f"Valid positional X at legal odd n={n}",
                "boundary" if n == 3 else "maxSize" if n == 299 else "adversarial")
            if n > 3:
                corrupted = grid.copy()
                row = list(corrupted[1])
                row[1], row[2] = row[2], row[1]
                corrupted[1] = "".join(row)
                add(str(n) + "\n" + "\n".join(corrupted) + "\n",
                    f"Row-count-preserving diagonal/off-diagonal swap at n={n}; old oracle incorrectly accepts",
                    "adversarial", *( ["maxSize"] if n == 299 else []))
        for bits in product("ab", repeat=9):
            grid = ["".join(bits[i:i + 3]) for i in (0, 3, 6)]
            add("3\n" + "\n".join(grid) + "\n", "Exhaustive binary 3x3 grid", "adversarial")
        for letter in ("a", "z"):
            grid = [letter * 299] * 299
            add("299\n" + "\n".join(grid) + "\n",
                "Maximum grid with equal diagonal/background letters must be NO", "maxSize", "adversarial")
    elif pid == "465B":
        add("6\n1 0 0 1 1 0\n", "Unread block after a gap must return once, not for every mail", "adversarial")
        for n in range(1, 9):
            for values in product((0, 1), repeat=n):
                add(f"{n}\n" + " ".join(map(str, values)) + "\n",
                    "Exhaustive binary unread-mail sequence through length eight", "adversarial", "boundary")
        for values in ([0] * 1000, [1] * 1000, [0, 1] * 500,
                       [1] + [0] * 998 + [1], [0] * 499 + [1, 1] + [0] * 499):
            add("1000\n" + " ".join(map(str, values)) + "\n",
                "Legal maximum inbox: empty/full/alternating/extreme-gap/interior contiguous block", "maxSize")
    elif pid == "29A":
        for records, reason in (
            ([(-10000, 20000), (10000, -20000)], "Mutual spit across actual maximum separation 20000"),
            ([(10000, -20000), (-10000, 20000)], "Reverse input order of maximum-separation mutual pair"),
            ([(-10000, 20000), (10000, -19999)], "Maximum-separation near miss is not mutual"),
            ([(10000, 20000)], "Positive coordinate endpoint and maximum positive distance without partner"),
            ([(10000, -20000)], "Positive coordinate endpoint and maximum negative distance without partner"),
            ([(-10000, 20000)], "Negative endpoint and maximum positive distance without partner")):
            add(str(len(records)) + "\n" + "".join(f"{x} {d}\n" for x, d in records),
                reason, "boundary", "adversarial", "maxSize")
        positions = [-10000, *range(-49, 49), 10000]
        assert len(positions) == 100
        for mutual in (True, False):
            records = [(x, 20000 if x == -10000 else -20000 if x == 10000 and mutual else 1)
                       for x in positions]
            add("100\n" + "".join(f"{x} {d}\n" for x, d in records),
                "Maximum n=100 with both coordinate endpoints and maximum distance, "
                + ("mutual endpoint pair" if mutual else "no mutual pair"), "maxSize", "adversarial")
    else:
        raise ValueError(pid)
    return result


def generator_source(pid, prior_source):
    from pathlib import Path
    module = Path(__file__).read_text()
    return ("import io,json,sys\n"
            "saved_stdout=sys.stdout\n"
            "sys.stdout=io.StringIO()\n"
            f"exec(compile({prior_source!r},'/work/prior-generator.py','exec'),{{'__name__':'__main__'}})\n"
            "pairs=json.loads(sys.stdout.getvalue())\n"
            "sys.stdout=saved_stdout\n"
            f"exec(compile({module!r},'/work/correction-cases.py','exec'))\n"
            f"pairs.extend({{'input':p['input'],'output':p['output']}} for p in cases({pid!r}))\n"
            "print(json.dumps(pairs,sort_keys=True))\n")
