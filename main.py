#!/usr/bin/env python3
"""make.fun news-image-20261119 entry program (stdlib only).

Copies ./entry.png to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
The image itself is a pre-built asset in this repo; it was drawn by
draw.py (a build-time script, not part of the run) with PIL.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
