#!/usr/bin/env python3
"""Build the firmware targets of one CI job (JSON list in $TARGETS) into out/."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(os.environ.get("GITHUB_WORKSPACE", Path(__file__).resolve().parents[1]))
out = root / "out"
out.mkdir(exist_ok=True)
failed = []

for t in json.loads(os.environ["TARGETS"]):
    absl = lambda paths: ";".join(str(root / p) for p in paths.split(";"))
    args = [f"-DZMK_CONFIG={root / 'config'}", f"-DSHIELD={t['shield']}"]
    if t["keymap"]:
        args.append(f"-DKEYMAP_FILE={root / t['keymap']}")
    if t["confs"]:
        args.append(f"-DEXTRA_CONF_FILE={absl(t['confs'])}")
    if t["overlays"]:
        args.append(f"-DEXTRA_DTC_OVERLAY_FILE={absl(t['overlays'])}")
    if t["cppflags"]:
        args.append(f"-DDTS_EXTRA_CPPFLAGS={t['cppflags']}")
    build_dir = root / "build" / t["name"]
    print(f"::group::{t['name']}", flush=True)
    rc = subprocess.call(["west", "build", "-s", "zmk/app", "-d", str(build_dir),
                          "-b", t["board"], "--", *args])
    config = build_dir / "zephyr" / ".config"
    if config.exists():
        print("--- Kconfig ---")
        print("\n".join(sorted(l for l in config.read_text().splitlines()
                                if l and not l.startswith("#"))))
    print("::endgroup::", flush=True)
    if rc == 0:
        shutil.copy(build_dir / "zephyr" / "zmk.uf2", out / f"{t['name']}.uf2")
    else:
        print(f"::error title={t['name']}::build failed", flush=True)
        failed.append(t["name"])

sys.exit(1 if failed else 0)
