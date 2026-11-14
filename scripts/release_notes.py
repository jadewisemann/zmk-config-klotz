#!/usr/bin/env python3
"""Write release notes for a directory of built .uf2 files.

    python3 scripts/release_notes.py firmware/ "<commit message>" > notes.md
"""
import sys
from collections import defaultdict
from pathlib import Path

MODES = {
    "ble": "BLE: left half is the central, pairs with the host directly",
    "bledongle": "BLE dongle: both halves + `dongle` (USB to the host)",
    "esb": "ESB dongle: both halves + `dongle` (USB to the host)",
    "usb": "Wired",
}

fw_dir, message = Path(sys.argv[1]), sys.argv[2].strip()
subject, _, body = message.partition("\n")

by_device = defaultdict(lambda: defaultdict(list))
for f in sorted(fw_dir.glob("*.uf2")):
    device, mode, *_ = f.stem.split("-") + [""]
    by_device[device][mode].append(f.name)

out = [f"**{subject}**", ""]
if body.strip():
    out += [body.strip(), ""]
out += ["| keyboard | mode | files |", "|---|---|---|"]
for device in sorted(d for d in by_device if d != "reset"):
    for mode in MODES:
        if mode in by_device[device]:
            files = " ".join(f"`{n}`" for n in by_device[device][mode])
            out.append(f"| {device} | {MODES[mode]} | {files} |")
resets = [n for files in by_device.get("reset", {}).values() for n in files]
if resets:
    out.append(f"| settings reset | flash before switching modes | {' '.join(f'`{n}`' for n in resets)} |")
out += ["", "Flash every part of a mode from the same release; the halves and the dongle must match."]
print("\n".join(out))
