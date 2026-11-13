#!/usr/bin/env python3
"""Embed an image inside a QR code (no per-image server needed).

Modes:
  default       QR holds a data: URI (many phones will NOT open it).
  --viewer-url  QR holds https://<viewer>#<fmt>;<base64>. Any phone camera
                opens the link; the hosted index.html shows the image.
                The part after '#' is never sent to a server.

A QR code holds at most 2953 bytes (version 40, level L), so the image is
shrunk until the payload fits.
"""
import argparse
import base64
import io
import sys

import qrcode
from PIL import Image

QR_MAX_BYTES = 2953  # version 40, error correction L, byte mode


def b64(img: Image.Image, fmt: str, quality: int) -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt.upper(), quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def make_payload(data: str, fmt: str, viewer_url: str | None) -> str:
    if viewer_url:
        return f"{viewer_url.split('#')[0]}#{fmt};{data}"
    return f"data:image/{fmt};base64,{data}"


def fit_image(path: str, fmt: str, limit: int, viewer_url: str | None):
    src = Image.open(path).convert("RGB")
    for side in range(256, 15, -8):
        img = src.copy()
        img.thumbnail((side, side), Image.LANCZOS)
        for q in (70, 50, 35, 25, 15):
            payload = make_payload(b64(img, fmt, q), fmt, viewer_url)
            if len(payload) <= limit:
                return payload, img.size, q
    sys.exit("Image cannot fit in a QR code, even at 16px.")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input")
    p.add_argument("-o", "--output", default="qr.png")
    p.add_argument("-f", "--format", choices=["webp", "jpeg"], default="jpeg")
    p.add_argument("--viewer-url",
                   help="public URL of the hosted site, e.g. https://you.github.io/REPO/")
    p.add_argument("--limit", type=int, default=QR_MAX_BYTES - 20,
                   help="max payload length in bytes")
    a = p.parse_args()

    payload, size, q = fit_image(a.input, a.format, a.limit, a.viewer_url)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=6, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(a.output)
    print(f"saved {a.output}: image {size[0]}x{size[1]} q={q}, "
          f"{len(payload)} bytes, QR version {qr.version}")


if __name__ == "__main__":
    main()
