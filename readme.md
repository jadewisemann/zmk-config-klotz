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
