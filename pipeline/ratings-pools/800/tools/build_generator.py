"""Assemble a self-contained deterministic generator for the generated qualification basis.

The generator inlines rlib plus genrecipes/<ID>.py, reads an integer seed on stdin and prints a JSON
list of {input, output} pairs: the recipe's authored extras first, then random cases from gen(rng)
until TARGET distinct inputs exist. Every input passes validate() before it is emitted.
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = 150

MAIN = f'''

def _main():
    import json, random, sys
    seed = int(sys.stdin.read().split()[0])
    rng = random.Random(seed)
    seen, out = set(), []

    def add(inp):
        if inp in seen:
            return
        validate(inp)
        seen.add(inp)
        out.append({{"input": inp, "output": solve(inp) + "\\n"}})

    for _, _, inp in extra():
        add(inp)
    attempts = 0
    while len(seen) < {TARGET}:
        attempts += 1
        if attempts > 200000:
            raise SystemExit("could not reach target distinct inputs")
        add(gen(rng))
    sys.stdout.write(json.dumps(out))


_main()
'''


def build(pid):
    lib = (HERE / "rlib.py").read_text()
    recipe = (HERE.parent / "genrecipes" / f"{pid}.py").read_text()
    recipe = re.sub(r"^from rlib import \*\n", "", recipe, flags=re.M)
    return f'"""Deterministic generator for Codeforces {pid} (rated-800 worker)."""\n' + lib + "\n\n" + recipe + MAIN


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(build(args.id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
