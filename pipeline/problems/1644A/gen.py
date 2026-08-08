import itertools
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    w = Writer(outdir)
    # exhaustive: all 720 permutations of RGBrgb (covers every possible input)
    perms = ["".join(p) for p in itertools.permutations("RGBrgb")]
    w.add(multi(perms))
    # a couple of small hand-picked splits
    w.add(multi(["rgbRGB", "RGBrgb", "rRgGbB", "bBrRgG"]))


if __name__ == "__main__":
    main(sys.argv[1])
