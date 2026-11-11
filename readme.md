<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/docs/images/KLOTZ_font_dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="/docs/images/KLOTZ_font_bright.svg">
  <img alt="KLOTZ logo font" src="/docs/images/KLOTZ_font_bright.svg">
</picture>

## Keyboards and firmware

One shared 34-key keymap (`config/keymap/base.keymap`) builds for every keyboard
in `devices.yaml`:

| keyboard | controller | modes |
|---|---|---|
| KLOTZ | nice!nano | `ble`, `bledongle`, `esb` |
| Urchin | nice!nano | `ble`, `bledongle`, `esb` |
| TOTEM | XIAO BLE | `ble`, `bledongle`, `esb` |
| TC36K | Raspberry Pi Pico | `usb` (wired) |

- `ble`: the left half is the central and pairs with the host over Bluetooth.
- `bledongle`: both halves connect to a nice!nano dongle over Bluetooth; the dongle plugs in over USB.
- `esb`: both halves connect to a nice!nano dongle over ESB (lower latency); the dongle plugs in over USB.

Files are named `<keyboard>-<mode>-<part>.uf2` (for example `klotz-esb-dongle.uf2`).
Flash every part of a mode from the same release, and flash `settings_reset-<board>.uf2`
first when switching a keyboard between modes. Positions 0-33 are the same on every
keyboard; TOTEM's and TC36K's extra keys come after them and are unbound for now.

Every push to `main` builds all firmware in parallel and publishes a new GitHub release
(`fw-<date>-<time>-<sha>`); older releases are kept. Other branches build without
releasing (the files are on the Actions run); a manual run creates a pre-release.

### Adding a keyboard

1. Shield: `config/boards/shields/<shield>/`, or a west module added to both
   `config/west.yml` and `config-esb/west.yml`.
2. `config/devices/<id>/<id>.keymap` including `../../keymap/base.keymap`
   (define `KB_EXTRA_KEYS` if it has more than 34 keys, and order its matrix
   transform so the shared 34 come first).
3. For dongle modes, `config/devices/<id>/dongle.overlay`; for `esb`, also
   `config/devices/<id>/esb.overlay` with addresses no other keyboard uses.
4. An entry in `devices.yaml`. `yq -o=json devices.yaml | python3 scripts/matrix.py --check`
   lists every firmware it will build.

Shared settings live in `config/modes/` (see its README); per-keyboard settings in
`config/devices/<id>/`.

## English Colemak and Korean

The firmware starts in English Colemak and keeps the previous Korean key positions on a separate layer. Use the right thumb language key or the right-top language combo to switch both the host input language and the firmware layer. Configure the host for QWERTY English and Korean 2-set; a host-side Colemak layout would remap the firmware output again. macOS is the default and sends F18 for language switching. Toggle Windows mode from Settings (right home row, second key) to swap the modifiers and send LANG1 instead; the toggle is not saved, so the keyboard returns to macOS after a restart.

The keyboard cannot detect input-source changes made on the host. If the two layouts get out of sync, hold the outer thumb combo for Settings and tap the top-right key to toggle only the firmware layout.
