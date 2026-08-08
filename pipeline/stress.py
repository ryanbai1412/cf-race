"""Stress-test ref.py against brute.py on small random inputs.

Each per-problem directory may provide small.py with a `case(rnd)` function
returning one small multi-test input string; otherwise stress.py is skipped.

Usage: python3 pipeline/stress.py <id> [iters]
"""
import importlib.util
import os
import random
import subprocess
import sys

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd, data):
    r = subprocess.run(cmd, input=data, capture_output=True, text=True,
                       timeout=120, check=True)
    return r.stdout.split()


def main(pid, iters):
    pdir = os.path.join(PIPELINE_DIR, "problems", pid)
    small = load(os.path.join(pdir, "small.py"), f"small_{pid}")
    ref = ["python3", os.path.join(pdir, "ref.py")]
    brute = ["python3", os.path.join(pdir, "brute.py")]
    rnd = random.Random(12345)
    for it in range(iters):
        data = small.case(rnd)
        a, b = run(ref, data), run(brute, data)
        if a != b:
            print(f"MISMATCH on iteration {it}:\n{data}\nref:   {a}\nbrute: {b}")
            sys.exit(1)
    print(f"{pid}: {iters} stress iterations OK")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 300)
