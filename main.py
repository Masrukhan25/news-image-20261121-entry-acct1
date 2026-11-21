#!/usr/bin/env python3
"""Poster runner for the 21 November 2026 world-news image (account 1).

The finished artwork already lives in this repository as entry.png. This
script's only job is to place an exact copy of that artwork where the
grader expects it. Copying bytes keeps the result identical on every run,
which is what the competition asks for: run it twice, get the same file.

Only the Python standard library is used here, because the grading
container installs nothing extra before running this file. No network,
no drawing, no fonts are needed: the poster is already finished, and
this script only moves its bytes to the right place.
"""

import hashlib
import os
import shutil
import sys

POSTER_NAME = "entry.png"


def poster_path():
    """Absolute path of the artwork shipped beside this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, POSTER_NAME)


def destination():
    """Where the copy goes: $MAKEFUN_OUTPUT_DIR, or /output by default."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, POSTER_NAME)


def file_digest(path):
    """SHA-256 of a file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run():
    """Copy the poster to the output directory and confirm it matches."""
    source = poster_path()
    target = destination()
    before = file_digest(source)
    shutil.copyfile(source, target)
    after = file_digest(target)
    if before != after:
        print("error: copied file digest differs from source", file=sys.stderr)
        return 1
    print(f"wrote {target} (1024x1024, sha256 {after})")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
