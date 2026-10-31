"""Run on the Mac with Homebrew Python and pyserial; not on CIRCUITPY."""

import argparse
import base64
from datetime import datetime
from pathlib import Path
import subprocess
import sys
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    raise SystemExit(
        "pyserial is missing from this interpreter. Use your Homebrew Python: "
        "/opt/homebrew/bin/python3 receive_photo.py"
    )


def choose_port():
    candidates = [p.device for p in list_ports.comports()
                  if "usbmodem" in p.device]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise RuntimeError("No USB modem port found. Connect the XIAO using its USB data cable.")
    raise RuntimeError("Multiple USB modem ports found. Use --port PATH. Found: "
                       + ", ".join(candidates))


def receive_image(connection, timeout=45):
    """Receive one bounded, length-checked JPEG from code.py's text protocol."""
    deadline = time.monotonic() + timeout
    expected = None
    image = bytearray()
    capture_sent = False

    while time.monotonic() < deadline:
        line = connection.readline().strip()
        if not line:
            continue
        if line.startswith(b"CAMERA_ERROR:"):
            raise RuntimeError(line.decode("utf-8", errors="replace"))
        if line == b"CAMERA_READY" and expected is None:
            if not capture_sent:
                print("Camera ready. Taking photo...")
                connection.write(b"CAPTURE\r")
                capture_sent = True
            continue
        if expected is None:
            if line.startswith(b"JPEG_BEGIN "):
                expected = int(line.split()[1])
                if not 0 < expected <= 8_000_000:
                    raise RuntimeError("Invalid image size received")
                print("Receiving {} bytes...".format(expected))
            else:
                print("Board:", line.decode("utf-8", errors="replace"))
            continue
        if line == b"JPEG_END":
            if len(image) != expected:
                raise RuntimeError("Incomplete transfer: expected {}, received {} bytes".
                                   format(expected, len(image)))
            if not image.startswith(b"\xff\xd8") or b"\xff\xd9" not in image[-64:]:
                raise RuntimeError("Transferred data does not contain a complete JPEG")
            return bytes(image)
        image.extend(base64.b64decode(line, validate=True))
        if len(image) > expected:
            raise RuntimeError("Received more image data than expected")

    raise TimeoutError(
        "No complete photo arrived within {} seconds. Confirm the supplied code.py "
        "is on CIRCUITPY and close other serial consoles.".format(timeout)
    )


def main():
    parser = argparse.ArgumentParser(description="Take one Sense camera photo over USB.")
    parser.add_argument("--port", help="Serial port; automatically found if omitted")
    parser.add_argument("--output", type=Path, help="New JPEG path; existing files are never overwritten")
    parser.add_argument("--no-open", action="store_true", help="Do not open the saved JPEG")
    args = parser.parse_args()

    port = args.port or choose_port()
    print("Connecting to", port)
    with serial.Serial(port, 115200, timeout=0.5, write_timeout=2) as connection:
        time.sleep(0.5)
        # Interrupt the old program and restart the saved board-side code.py.
        connection.write(b"\x03")
        time.sleep(0.3)
        connection.reset_input_buffer()
        connection.write(b"\x04")
        photo = receive_image(connection)

    output = args.output or (
        Path.home() / "Desktop" /
        ("xiao_photo_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg")
    )
    output = output.expanduser().resolve()
    with output.open("xb") as image_file:
        image_file.write(photo)
    print("Saved:", output)
    if sys.platform == "darwin" and not args.no_open:
        subprocess.run(["open", str(output)], check=False)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, TimeoutError) as error:
        raise SystemExit("Error: " + str(error))
