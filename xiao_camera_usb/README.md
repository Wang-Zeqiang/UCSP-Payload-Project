# XIAO ESP32S3 Sense Camera

Take a JPEG photo over USB and save it on your Mac. No microSD card or `boot.py` changes are needed.

Keep this `README.md` beside `code.py` and `receive_photo.py` in the repository's `xiao_camera_usb` folder.

## Run

Connect the board and confirm that `CIRCUITPY` appears in Finder. Close other serial monitors; exit Miniterm with **Control + ]**.

Run these commands in Mac Terminal:

```bash
cd "/Users/zeqiang/Desktop/UCSP/UCSP-Payload-Project/xiao_camera_usb"
cp code.py /Volumes/CIRCUITPY/code.py
/opt/homebrew/bin/python3 receive_photo.py
```

The copy command replaces the board's current program. The ESP32 runs `code.py`; your Mac runs `receive_photo.py` to restart the board, request a photo, and receive it.

The photo is saved as `xiao_photo_....jpg` on your Desktop and opens automatically.

To take another photo, run again:

```bash
/opt/homebrew/bin/python3 receive_photo.py
```

Copy `code.py` again only after editing it or switching from the sensor program. Do not run the board's `code.py` with Mac Python or VS Code's Python Run button.

## Functions

These run automatically; no manual function calls are needed.

| Function | Purpose |
| --- | --- |
| Board `main()` | Initializes the camera and handles capture requests using `camera.take(2)`. |
| Mac `choose_port()` | Finds the board's USB serial port. |
| Mac `receive_image()` | Requests a photo, receives it, and checks the JPEG. |
| Mac `main()` | Connects to the board, receives the photo, and saves it. |

## Troubleshooting

- **Port busy:** close Miniterm, `screen`, and other serial monitors.
- **Timeout:** confirm the camera program is saved as `CIRCUITPY/code.py`. The receiver must send `b"CAPTURE\r"`.
- **No USB port:** check the data cable and board connection.
- **No module named `serial`:** install the Mac dependency once:

```bash
/opt/homebrew/bin/python3 -m pip install --user --break-system-packages pyserial
```

For higher resolution, change `FrameSize.QVGA` (320 × 240) to `FrameSize.VGA` (640 × 480) in `code.py`, copy it to the board again, and rerun the receiver.
