# Image to QR

Turn an image into one QR code that contains the picture itself. Scan it with a normal phone camera and the image opens. No server stores the image.

## How it works

1. The image is shrunk and compressed (WebP, or JPEG where WebP is not available) until it fits in one QR code. A QR holds about 2.9 KB at most.
2. The QR holds a link to the hosted `index.html` plus the image data after a `#`:
   `https://your-site/#webp;<base64 image>`
3. A phone camera opens the link. The page reads the data after the `#` and shows the image.

The part of a URL after `#` is never sent to a server, so the image only exists in the QR code and in the browser that scans it.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The whole site. Generator when opened normally, image viewer when opened from a QR link. Stays in the root so GitHub Pages serves it. |
| `cli/img2qr.py` | Command line version (single image, compact only). Needs `pillow` and `qrcode`. |
| `legacy/viewer.html` | Old viewer-only page. `index.html` replaces it, so it can be deleted. |
| `examples/` | Sample QR and screenshot. |
| `README.md` | This file. |

## Use the website

1. Open the hosted page.
2. Choose or drop an image. The page shows the original next to the version stored in the QR.
3. Pick a mode and a density, then download or print the QR.
4. Scan with a phone camera and tap the link.

Modes:

- **Compact**: works for any image. It is shrunk (up to 320 px on the long side) so some quality is lost.
- **Maximum**: the whole photo in one QR, with uneven detail. About 30% of the bytes go to a very small, blurry copy of the full photo (the edges). The rest go to a sharp circle cut from the middle of the photo. The viewer draws the blurry photo first and the sharp circle on top, with a soft edge. A slider sets the circle's diameter, kept between 20% and 70% of the photo's shorter side: smaller than that is pointless, bigger leaves the edges nothing. Link format: `#c;<fmt>;<percent>;<base64 whole photo>;<base64 center>`.
- **Original, no loss**: the exact bytes of your file. Only works if the whole file fits in one QR (about 2 KB), so think tiny icons. Bigger files get a message telling you to use Compact.

Density:

- **Easy to scan**: simpler QR, smaller image. Best for print.
- **Balanced**: default.
- **Dense**: biggest image, very dense QR. Needs a large print or a full screen display.

## Host it (GitHub Pages)

1. Push this repo to GitHub. It must be public on a free account.
2. Go to **Settings, Pages**.
3. Source: **Deploy from a branch**. Pick your branch and `/ (root)`. Save.
4. After about a minute the site is at `https://USER.github.io/REPO/`.

## Command line

```
pip install pillow qrcode
python cli/img2qr.py photo.jpg -o qr.png --viewer-url https://USER.github.io/REPO/
```

Options: `-f jpeg|webp`, `--limit N` (max payload bytes).

## Limits

- One QR code holds about 2.9 KB, so a full photo (millions of bytes) can never fit in it with its quality intact. That is a property of QR codes, not of this tool. Compact mode gives you a small, lossy version of the photo.
- To get a full-quality photo from a QR you need the photo hosted somewhere and a QR that links to it. This tool does not do that, because it keeps everything serverless.
- The scanning phone needs internet to load the page.
- Very dense QR codes are hard to scan from small prints or low resolution screens.
- The page loads the QR library from cdnjs, so generating also needs internet.

## Privacy

Everything runs in the browser. Images are not uploaded. The hosted page is a static file with no tracking.
