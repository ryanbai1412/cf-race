"""Generate full test data for a problem.

Per-problem assets live in pipeline/problems/<id>/:
  gen.py   — writes NN.in files into a directory given as argv[1]
  ref.py or ref.cpp — reference solution (stdin -> stdout)

This script runs gen.py to produce inputs into problems/<id>/tests/,
copies the sample inputs in as the first tests, then runs the reference
solution to produce the .out files.

Usage: python3 pipeline/gen_tests.py 1927A [...]
"""
import glob
import os
import shutil
import subprocess
import sys

from common import PIPELINE_DIR, PROBLEMS_DIR, load_meta


def build_ref(problem_id: str) -> list:
    """Returns the command to run the reference solution."""
    pdir = os.path.join(PIPELINE_DIR, "problems", problem_id)
    cpp = os.path.join(pdir, "ref.cpp")
    py = os.path.join(pdir, "ref.py")
    if os.path.exists(cpp):
        binary = os.path.join(pdir, "ref")
        subprocess.run(["g++", "-O2", "-std=c++20", "-o", binary, cpp], check=True)
        return [binary]
    if os.path.exists(py):
        return ["python3", py]
    raise RuntimeError(f"no reference solution for {problem_id}")


def gen(problem_id: str) -> None:
    pdir = os.path.join(PIPELINE_DIR, "problems", problem_id)
    tests_dir = os.path.join(PROBLEMS_DIR, problem_id, "tests")
    samples_dir = os.path.join(PROBLEMS_DIR, problem_id, "samples")
    shutil.rmtree(tests_dir, ignore_errors=True)
    os.makedirs(tests_dir)

    # samples become the first tests (like CF), then generated tests
    tmp = tests_dir + ".gen"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    subprocess.run(["python3", os.path.join(pdir, "gen.py"), tmp], check=True)

    inputs = []
    for f in sorted(glob.glob(os.path.join(samples_dir, "*.in"))):
        inputs.append(f)
    for f in sorted(glob.glob(os.path.join(tmp, "*.in"))):
        inputs.append(f)

    ref_cmd = build_ref(problem_id)
    for i, src in enumerate(inputs, 1):
        dst = os.path.join(tests_dir, f"{i:02d}.in")
        shutil.copyfile(src, dst)
        with open(dst) as fin, open(os.path.join(tests_dir, f"{i:02d}.out"), "w") as fout:
            subprocess.run(ref_cmd, stdin=fin, stdout=fout, check=True, timeout=60)
    shutil.rmtree(tmp)

    meta = load_meta(problem_id)
    total = sum(os.path.getsize(f) for f in glob.glob(os.path.join(tests_dir, "*")))
    print(f"{problem_id}: {len(inputs)} tests, {total/1e6:.2f} MB  ({meta['name']})")


if __name__ == "__main__":
    for pid in sys.argv[1:]:
        gen(pid)
