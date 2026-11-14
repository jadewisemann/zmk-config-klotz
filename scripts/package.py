#!/usr/bin/env python3
"""Pack built .uf2 files into one zip per keyboard for a release.

    yq -o=json devices.yaml | python3 scripts/package.py firmware/ <suffix> dist/

firmware/klotz-esb-left.uf2  -> dist/klotz-<suffix>.zip : klotz-<suffix>/esb/left.uf2
firmware/tc36k-usb.uf2       -> dist/tc36k-<suffix>.zip : tc36k-<suffix>/usb.uf2
firmware/reset-<board>.uf2   -> reset.uf2 in each zip whose keyboard uses that board,
                                plus reset-dongle.uf2 when the dongle is a different board
"""
import json
import sys
import zipfile
from pathlib import Path

fw_dir, suffix, out_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
cfg = json.load(sys.stdin)
keyboards, dongle_board = cfg["keyboards"], cfg["dongle_board"]
DONGLE_MODES = {"bledongle", "esb"}
out_dir.mkdir(parents=True, exist_ok=True)

files = {}  # device -> [(source, path inside its folder)]
for f in sorted(fw_dir.glob("*.uf2")):
    device, _, rest = f.stem.partition("-")
    if device != "reset":
        files.setdefault(device, []).append((f, rest.replace("-", "/", 1) + ".uf2"))

for device, entries in files.items():
    reset = lambda board: fw_dir / f"reset-{board.split('/')[0]}.uf2"
    kb = keyboards[device]
    if kb["board"] != dongle_board and DONGLE_MODES & set(kb["modes"]) and reset(dongle_board).exists():
        entries.insert(0, (reset(dongle_board), "reset-dongle.uf2"))
    if reset(kb["board"]).exists():
        entries.insert(0, (reset(kb["board"]), "reset.uf2"))
    folder = f"{device}-{suffix}"
    with zipfile.ZipFile(out_dir / f"{folder}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for src, inner in entries:
            z.write(src, f"{folder}/{inner}")
    print(f"{folder}.zip")
