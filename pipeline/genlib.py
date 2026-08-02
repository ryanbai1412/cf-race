"""Tiny helpers shared by per-problem test generators."""
import os


class Writer:
    def __init__(self, outdir):
        self.outdir = outdir
        self.n = 0
        os.makedirs(outdir, exist_ok=True)

    def add(self, content: str):
        self.n += 1
        with open(os.path.join(self.outdir, f"{self.n:02d}.in"), "w") as f:
            f.write(content if content.endswith("\n") else content + "\n")


def multi(cases) -> str:
    """Join a list of per-testcase strings into one multi-test input."""
    return f"{len(cases)}\n" + "\n".join(c.rstrip("\n") for c in cases) + "\n"
