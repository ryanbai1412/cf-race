"""Build a self-contained sandboxed generator: genlib + recipe + deterministic JSON emitter."""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEMS = HERE.parents[2] / "problems"
IMPORT = "from genlib import *  # noqa: F401,F403\n"
MAIN = '''

def _emit():
    seed = int(sys.stdin.read().split()[0])
    seen, out = set(), []
    for _kind, _reason, text in cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append({"input": text, "output": solve(text)})
    sys.stdout.write(json.dumps(out))


_emit()
'''


def source(pid):
    recipe = (PROBLEMS / pid / "recipe.py").read_text()
    if IMPORT not in recipe:
        raise ValueError("recipe must import genlib with the canonical line")
    return "import json\n" + (HERE / "genlib.py").read_text() + "\n\n" + recipe.replace(IMPORT, "") + MAIN


def build(pid):
    path = PROBLEMS / pid / "generator.py"
    path.write_text(source(pid))
    return path


def labelled(recipe, seed):
    seen, out = set(), []
    for kind, reason, text in recipe.cases(random.Random(seed)):
        if text not in seen:
            seen.add(text)
            out.append((kind, reason, text))
    return out


if __name__ == "__main__":
    for pid in sys.argv[1:]:
        print(build(pid))
