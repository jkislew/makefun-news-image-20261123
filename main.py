#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261123.

Writes one image — a newspaper front page summing up the world news of
Monday 23 November 2026 — to <output>/entry.png. The picture is drawn by
make_image.py, which lives beside this file in the repository root; this
program only finds that module relative to its own location (never the
working directory) and hands it the output directory.

The output directory is MAKEFUN_OUTPUT_DIR when set, else /output, the
directory the sealed scorer reads. No network is used, nothing is read
from the clock or the environment beyond that one directory variable, so
two runs write byte-identical files.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import make_image  # noqa: E402


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    make_image.build(target)
    size = os.path.getsize(target)
    print("wrote", target, "(%d bytes)" % size)


if __name__ == "__main__":
    main()
