# Build modes

Each firmware is `shield/board defaults` + the mode files below (applied in the
order listed in `scripts/matrix.py`) + the device's own files in
`config/devices/<device>/`. Later files win.

| file | used by |
|---|---|
| `half.conf` | every battery-powered half, all modes |
| `ble.conf` | everything that talks Bluetooth (BLE halves, BLE dongle) |
| `ble_central.conf` | whatever is the BLE split central (left half in `ble`, dongle in `bledongle`) |
| `peripheral.conf` | left half when a dongle is the central (`bledongle`, `esb`) |
| `ble_dongle.conf` | BLE dongle |
| `esb.conf` | every ESB build (halves and dongle) - radio settings must match |
| `esb_left.conf` / `esb_right.conf` | ESB peripheral IDs |
| `esb_dongle.conf` | ESB dongle |
