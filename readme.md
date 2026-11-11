<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/docs/images/KLOTZ_font_dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="/docs/images/KLOTZ_font_bright.svg">
  <img alt="KLOTZ logo font" src="/docs/images/KLOTZ_font_bright.svg">
</picture>

## Firmware builds

GitHub Actions builds both connection modes:

- `klotz_ble_left.uf2` and `klotz_ble_right.uf2`: standard ZMK Bluetooth split
- `klotz_esb_left.uf2` and `klotz_esb_right.uf2`: ESB peripherals
- `klotz_esb_dongle.uf2`: USB ESB central for a nice!nano
- `settings_reset.uf2`: clears stored settings before changing modes

The BLE and ESB firmwares are separate. Flash both halves with the matching pair; ESB mode also requires the dongle firmware on a third nice!nano.

## English Colemak and Korean

The firmware starts in English Colemak and keeps the previous Korean key positions on a separate layer. Use the right thumb language key or the right-top language combo to switch both the host input language and the firmware layer. Configure the host for QWERTY English and Korean 2-set; a host-side Colemak layout would remap the firmware output again. macOS is the default and sends F18 for language switching. Toggle Windows mode from Settings (right home row, second key) to swap the modifiers and send LANG1 instead; the toggle is not saved, so the keyboard returns to macOS after a restart.

The keyboard cannot detect input-source changes made on the host. If the two layouts get out of sync, hold the outer thumb combo for Settings and tap the top-right key to toggle only the firmware layout.
