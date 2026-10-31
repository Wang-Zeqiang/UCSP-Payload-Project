# XIAO ESP32S3 Sense Camera

Take a JPEG photo over USB and save it on a computer. Requires the Sense camera and CircuitPython firmware with `espcamera`. No microSD card or `boot.py` changes are needed.

## Setup

Connect the board using a USB data cable and confirm that `CIRCUITPY` appears. Install the computer dependency if needed:

```bash
python3 -m pip install --user pyserial
```

On Windows, use `py` instead of `python3` throughout. If Homebrew Python reports `externally-managed-environment`, append `--break-system-packages` to the install command while keeping `--user`.

## Run

1. Close other serial monitors; exit Miniterm with **Control + ]**.
2. Copy this folder's `code.py` to the root of `CIRCUITPY`, replacing the board's current program. Back it up first if needed.
3. Open a terminal in this repository's `xiao_camera_usb` folder and list the ports:

```bash
python3 -m serial.tools.list_ports
```

Take a photo, replacing `PORT` with the XIAO's port:

```bash
python3 receive_photo.py --port PORT --output photo.jpg
```

Typical port names are `/dev/cu.usbmodem...` on macOS, `/dev/ttyACM0` on Linux, or `COM3` on Windows. Use the actual port shown on your computer.

The ESP32 runs `code.py`. The computer runs `receive_photo.py`, which restarts the board, requests a photo, and saves `photo.jpg` in the current folder. Open that file to view it; macOS also opens it automatically.

Run again with a new filename, such as `photo2.jpg`, for another photo. Existing files are never overwritten. Copy `code.py` again only after changing it or switching from the sensor program. Do not run the board's `code.py` with computer Python or VS Code's Python Run button.

On macOS, the shorter command below automatically finds a single USB modem port and saves a uniquely named photo to the Desktop:

```bash
python3 receive_photo.py
```

## Functions

These run automatically; no manual function calls are needed.

| Function | Purpose |
| --- | --- |
| Board `main()` | Initializes the camera and handles capture requests using `camera.take(2)`. |
| Computer `choose_port()` | Finds a single `usbmodem` port when `--port` is omitted. |
| Computer `receive_image()` | Requests, receives, and checks the JPEG. |
| Computer `main()` | Connects to the board and saves the photo. |

## Troubleshooting

- **Port busy:** close Miniterm, `screen`, and other serial monitors.
- **Timeout:** confirm the camera program is on `CIRCUITPY`. The receiver must send `b"CAPTURE\r"`.
- **No USB port:** check the data cable and connection.
- **Camera error:** disconnect power before checking the camera expansion board or ribbon connection.

For 640 × 480 photos, change `FrameSize.QVGA` to `FrameSize.VGA` in `code.py`, copy it to the board, and rerun the receiver. Keep this README beside both scripts in `xiao_camera_usb`.
