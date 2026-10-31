"""Run on the XIAO ESP32S3 Sense. Send a JPEG to the Mac over USB.

Requires the Sense camera expansion board. No SD card or boot.py edits.
"""

import binascii
import time
import board
import busio
import espcamera


def main():
    print("Starting Sense camera...")
    camera_i2c = busio.I2C(board.CAM_SCL, board.CAM_SDA)
    camera = espcamera.Camera(
        data_pins=board.CAM_DATA,
        external_clock_pin=board.CAM_XCLK,
        pixel_clock_pin=board.CAM_PCLK,
        vsync_pin=board.CAM_VSYNC,
        href_pin=board.CAM_HREF,
        i2c=camera_i2c,
        external_clock_frequency=20_000_000,
        pixel_format=espcamera.PixelFormat.JPEG,
        frame_size=espcamera.FrameSize.QSXGA,
        framebuffer_count=1,
    )

    try:
        while True:
            print("CAMERA_READY")
            if input().strip() != "CAPTURE":
                continue

            # Refresh several frames so automatic exposure can settle.
            for _ in range(5):
                frame = camera.take(2)
                time.sleep(0.2)

            if frame is None:
                raise RuntimeError("Camera capture timed out")

            # Short base64 lines preserve the JPEG through a text console.
            print("JPEG_BEGIN", len(frame))
            for offset in range(0, len(frame), 48):
                encoded = binascii.b2a_base64(frame[offset:offset + 48])
                print(encoded.decode("ascii").strip())
            print("JPEG_END")
    finally:
        camera.deinit()
        camera_i2c.deinit()


try:
    main()
except Exception as error:
    print("CAMERA_ERROR:", repr(error))
    raise
