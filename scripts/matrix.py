#!/usr/bin/env python3
"""Expand devices.yaml (passed as JSON on stdin) into the CI build matrix.

    yq -o=json devices.yaml | python3 scripts/matrix.py          # matrix JSON
    yq -o=json devices.yaml | python3 scripts/matrix.py --check  # validate only

Every firmware = shield/board defaults + mode files (config/modes) + the
device's own files (config/devices/<id>). Paths in the output are relative to
the repo root; the workflow makes them absolute.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = {"ble": "config", "bledongle": "config", "usb": "config", "esb": "config-esb"}
NO_BLE = {"esb", "usb"}  # builds without the &bt behavior


def mode(*names):
    return [f"config/modes/{n}.conf" for n in names]


def optional(*paths):
    return [p for p in paths if (ROOT / p).exists()]


def targets(dev_id, dev, dongle_board):
    d = f"config/devices/{dev_id}"
    board, shield = dev["board"], dev["shield"]
    half = optional(f"{d}/half.conf")
    dongle = optional(f"{d}/dongle.conf")
    for m in dev["modes"]:
        if m == "ble":
            yield m, "left", board, f"{shield}_left", mode("half", "ble", "ble_central") + half, []
            yield m, "right", board, f"{shield}_right", mode("half", "ble") + half, []
        elif m == "bledongle":
            yield m, "left", board, f"{shield}_left", mode("half", "ble", "peripheral") + half, []
            yield m, "right", board, f"{shield}_right", mode("half", "ble") + half, []
            yield (m, "dongle", dongle_board, "kb_dongle",
                   mode("ble", "ble_central", "ble_dongle") + dongle, [f"{d}/dongle.overlay"])
        elif m == "esb":
            esb = [f"{d}/esb.overlay"]
            yield m, "left", board, f"{shield}_left", mode("half", "esb", "esb_left", "peripheral") + half, esb
            yield m, "right", board, f"{shield}_right", mode("half", "esb", "esb_right") + half, esb
            yield (m, "dongle", dongle_board, "kb_dongle",
                   mode("esb", "esb_dongle") + dongle, [f"{d}/dongle.overlay"] + esb)
        elif m == "usb":
            yield m, None, board, shield, optional(f"{d}/usb.conf"), []
        else:
            raise SystemExit(f"{dev_id}: unknown mode {m!r}")


def main():
    cfg = json.load(sys.stdin)
    include, missing = [], []
    for dev_id, dev in cfg["keyboards"].items():
        keymap = f"config/devices/{dev_id}/{dev_id}.keymap"
        for m, part, board, shield, confs, overlays in targets(dev_id, dev, cfg["dongle_board"]):
            missing += [p for p in [keymap, *confs, *overlays] if not (ROOT / p).exists()]
            include.append({
                "name": "-".join(x for x in (dev_id, m, part) if x),
                "device": dev_id,
                "mode": m,
                "board": board,
                "shield": shield,
                "manifest": MANIFEST[m],
                "keymap": keymap,
                "confs": ";".join(confs),
                "overlays": ";".join(overlays),
                "cppflags": "-DKB_NO_BLE" if m in NO_BLE else "",
            })
    for board in cfg.get("settings_reset", []):
        include.append({
            "name": f"settings_reset-{board.split('/')[0]}", "device": "settings_reset",
            "mode": "reset", "board": board, "shield": "settings_reset", "manifest": "config",
            "keymap": "", "confs": "", "overlays": "", "cppflags": "",
        })
    names = [t["name"] for t in include]
    dupes = {n for n in names if names.count(n) > 1}
    if missing or dupes:
        for p in sorted(set(missing)):
            print(f"missing file: {p}", file=sys.stderr)
        for n in sorted(dupes):
            print(f"duplicate artifact name: {n}", file=sys.stderr)
        raise SystemExit(1)
    if "--check" in sys.argv:
        print(f"{len(include)} firmware targets OK", file=sys.stderr)
        for t in include:
            print(f"  {t['name']:28} {t['manifest']:10} {t['board']:16} {t['shield']}", file=sys.stderr)
        return
    print(json.dumps({"include": include}))


if __name__ == "__main__":
    main()
