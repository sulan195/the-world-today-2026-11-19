#!/usr/bin/env python3
"""Entry program for make.fun's "Sum up 19 November's world news in one
image" competition (news-image-20261119).

The entry image (entry.png, a one-page newspaper front page of Thursday
19 November 2026) is stored in this repository; this program copies it
to the output location the harness gives it. Standard library only, no
network, and byte-for-byte deterministic: it runs twice and both runs
write the same bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.png")


def main():
    dest = output_path()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    # Copy in chunks and verify the copy, so a truncated write can never
    # pass silently: the gate reads exactly the bytes of this file.
    written = 0
    with open(SOURCE, "rb") as src, open(dest, "wb") as dst:
        while True:
            chunk = src.read(65536)
            if not chunk:
                break
            dst.write(chunk)
            written += len(chunk)
    if written != os.path.getsize(SOURCE):
        raise IOError("short copy: wrote %d bytes" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
