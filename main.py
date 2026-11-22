#!/usr/bin/env python3
"""news-image-20261121 v2 — acct1 (Masrukhan25).

Copies the pre-built entry.png (in this repository's root) into
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).

v2: flat-vector broadsheet following the winning top-1 formula (koran krem,
THE DAY IN UTC strip, THE DAY IN NUMBERS, 3 numbered heroes, 10-story grid,
world map with numbered dots, ALSO TODAY list, DATE CHECK bar, date
guarantee footer). All artwork drawn in code — no AI photos. 33 verified
stories from 21 November 2026. Entry image: 1024x1024 JPEG, 424,305 bytes.

Standard library only: no third-party imports, no network.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1048576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print("entry.png too large: %d bytes (limit %d)" % (size, MAX_BYTES),
              file=sys.stderr)
        return 1
    sha = hashlib.sha256(open(src, "rb").read()).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy byte-for-byte before reporting success, and never
    # write anything into the current working directory.
    dst_sha = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    if dst_sha != sha:
        print("copy mismatch: %s != %s" % (dst_sha, sha), file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dst, size, sha))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
