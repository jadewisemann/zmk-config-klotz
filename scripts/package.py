#!/usr/bin/env python3
"""Pack built .uf2 files into one zip per keyboard for a release.

    python3 scripts/package.py firmware/ <suffix> dist/

firmware/klotz-esb-left.uf2 -> dist/klotz-<suffix>.zip : klotz-<suffix>/esb/left.uf2
firmware/tc36k-usb.uf2      -> dist/tc36k-<suffix>.zip : tc36k-<suffix>/usb.uf2
firmware/reset-nice_nano.uf2 -> dist/reset-<suffix>.zip : reset-<suffix>/nice_nano.uf2
"""
import sys
import zipfile
from pathlib import Path

fw_dir, suffix, out_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
out_dir.mkdir(parents=True, exist_ok=True)

zips = {}
for f in sorted(fw_dir.glob("*.uf2")):
    device, _, rest = f.stem.partition("-")
    inner = rest.replace("-", "/", 1) + ".uf2"
    folder = f"{device}-{suffix}"
    if device not in zips:
        zips[device] = zipfile.ZipFile(out_dir / f"{folder}.zip", "w", zipfile.ZIP_DEFLATED)
    zips[device].write(f, f"{folder}/{inner}")

for z in zips.values():
    print(z.filename)
    z.close()
