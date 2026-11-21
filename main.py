#!/usr/bin/env python3
"""Publish this entry's image for grading.

The graded program: it takes the entry image that ships with this
repository (entry.png, 1024x1024, next to this file) and places an
exact copy at $MAKEFUN_OUTPUT_DIR/entry.png (default /output). It
uses only the Python standard library, writes nothing to the current
directory, and refuses to hand over anything that is not a PNG of
the expected size. No network, no third-party packages: the copy is
verified byte for byte before the program reports success.
"""
import hashlib
import os
import shutil
import struct
import sys

ENTRY_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)


def _repo_dir():
    return os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _png_dimensions(path):
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        return None
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return (width, height)


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def run():
    source = os.path.join(_repo_dir(), ENTRY_NAME)
    if not os.path.isfile(source):
        return _fail(f"entry image missing: {source}")
    dims = _png_dimensions(source)
    if dims is None:
        return _fail(f"{source} is not a PNG file")
    if dims != EXPECTED_SIZE:
        return _fail(f"{source} is {dims[0]}x{dims[1]}, expected "
                      f"{EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output") or "/output"
    # The output directory is created by the program itself, so a
    # fresh grading container needs no setup step before the run.
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, ENTRY_NAME)
    if os.path.abspath(target) == os.path.abspath(source):
        print(f"output is the repository file itself: {target}")
    else:
        shutil.copyfile(source, target)
    if os.path.getsize(source) != os.path.getsize(target):
        return _fail("size changed while copying")
    if _sha256(source) != _sha256(target):
        return _fail("sha256 changed while copying")
    if _png_dimensions(target) != EXPECTED_SIZE:
        return _fail("copied file is not the expected 1024x1024 PNG")
    print(f"wrote {target} "
          f"({os.path.getsize(target)} bytes, sha256 {_sha256(target)})")
    return 0


if __name__ == "__main__":
    sys.exit(run())
