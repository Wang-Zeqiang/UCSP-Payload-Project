# BMP280 Temperature and Pressure Sensor

Reads temperature (°C) and pressure (hPa) every second using I2C address `0x77`.

Keep this `README.md`, `code.py`, and `assets/` together in the repository's `temperature and pressure sensor` folder.

## Wiring

Disconnect USB before changing wires.

| XIAO ESP32S3 Sense | BMP280 |
| --- | --- |
| 3V3 | VIN / VCC |
| GND | GND |
| D4 / SDA / GPIO5 | SDA / SDI |
| D5 / SCL / GPIO6 | SCL / SCK |

![XIAO ESP32S3 Sense pinout](assets/xiao_esp32s3_sense_pinout.png)

## Run

Connect the board and confirm that `CIRCUITPY` appears in Finder. Exit any existing Miniterm session with **Control + ]**.

Run these commands in Mac Terminal:

```bash
cd "/Users/zeqiang/Desktop/UCSP/UCSP-Payload-Project/temperature and pressure sensor"
cp code.py /Volumes/CIRCUITPY/code.py
/opt/homebrew/bin/python3 -m serial.tools.miniterm --raw /dev/cu.usbmodemC7F4DAE196801 115200
```

The copy command replaces the board's current program. The ESP32 runs `code.py`; Miniterm displays its readings on the Mac. Do not run this file with Mac Python or VS Code's Python Run button.

- **Control + C**, then **Control + D**: stop and restart the board program.
- **Control + ]**: exit Miniterm.
- After editing the repository's `code.py`, copy it to the board again.

## Libraries

Already installed on your board. For a fresh board, run once:

```bash
circup --path /Volumes/CIRCUITPY install adafruit_bmp280
```

This installs the sensor library and its dependencies into the ESP32's `CIRCUITPY/lib/`.

## Troubleshooting

- **No pull up found:** check power, ground, and SDA/SCL wiring.
- **Port missing:** run `ls /dev/cu.usbmodem*` and use the returned port in the Miniterm command.
- **Port busy:** close other serial monitors or the camera receiver.
- **No readings:** press Control + C, then Control + D and check the error output.
