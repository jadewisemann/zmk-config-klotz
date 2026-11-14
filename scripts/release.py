#!/usr/bin/env python3
"""Prepare a release: versioned file names in dist/ and notes.md with download links.

    yq -o=json devices.yaml | python3 scripts/release.py firmware/ <tag> <suffix> "<message>"

firmware/klotz-esb-left.uf2 -> dist/klotz-esb-left-<suffix>.uf2
The suffix keeps downloads from different releases apart.
"""
import json
import os
import shutil
import sys
from pathlib import Path

fw_dir, tag, suffix, message = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4].strip()
cfg = json.load(sys.stdin)
repo = os.environ.get("GITHUB_REPOSITORY", "jadewisemann/zmk-config-klotz")
base = f"https://github.com/{repo}/releases/download/{tag}"

MODES = {"ble": "BLE", "bledongle": "BLE dongle", "esb": "ESB dongle", "usb": "Wired"}
PARTS = ["left", "right", "dongle"]

dist = Path("dist")
dist.mkdir(exist_ok=True)
built = {}  # stem -> link
for f in sorted(fw_dir.glob("*.uf2")):
    name = f"{f.stem}-{suffix}.uf2"
    shutil.copy(f, dist / name)
    built[f.stem] = f"{base}/{name}"


def link(stem, label):
    return f"[{label}]({built[stem]})" if stem in built else ""


subject, _, body = message.partition("\n")
out = [f"**{subject}**", ""]
if body.strip():
    out += [body.strip(), ""]

for kb_id, kb in cfg["keyboards"].items():
    rows = []
    for m in kb["modes"]:
        if m == "usb":
            rows.append(f"| {MODES[m]} | {link(f'{kb_id}-usb', 'firmware')} | | |")
        else:
            rows.append(f"| {MODES[m]} | " + " | ".join(link(f"{kb_id}-{m}-{p}", p) for p in PARTS) + " |")
    out += [f"### {kb_id}", "", "| mode | left | right | dongle |", "|---|---|---|---|", *rows]
    resets = [link(f"reset-{kb['board'].split('/')[0]}", "reset")]
    if kb["board"] != cfg["dongle_board"] and {"bledongle", "esb"} & set(kb["modes"]):
        resets.append(link(f"reset-{cfg['dongle_board'].split('/')[0]}", "reset (dongle)"))
    resets = [r for r in resets if r]
    if resets:
        out += ["", "Settings reset: " + " · ".join(resets)]
    out.append("")

out += ["Flash every part of a mode from the same release. Flash the reset on every part "
        "before switching a keyboard between modes."]
Path("notes.md").write_text("\n".join(out) + "\n")
