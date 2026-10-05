#!/usr/bin/env python3
"""Build the BWHS Reels icon: official BWHS mark plus a red R badge."""
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://raw.githubusercontent.com/HumbleKidd/BWHS/main/android-chrome-512x512.png"
SRC = os.path.join(ROOT, "tools", "bwhs-source.png")
OUT = os.path.join(ROOT, "icons")

def load_logo():
    os.makedirs(os.path.dirname(SRC), exist_ok=True)
    if not os.path.exists(SRC):
        urllib.request.urlretrieve(URL, SRC)
    im = Image.open(SRC).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r < 18 and g < 18 and b < 18:
                px[x, y] = (0, 0, 0, 0)
    return im.crop(im.getbbox())

def font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def make(size):
    mark = load_logo()
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.22), fill=(244, 248, 255, 255))
    wash = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    wd.ellipse((-int(size * 0.16), int(size * 0.55), int(size * 0.7), int(size * 1.5)), fill=(255, 59, 107, 46))
    wd.ellipse((int(size * 0.42), -int(size * 0.16), int(size * 1.25), int(size * 0.66)), fill=(47, 128, 255, 40))
    bg = Image.alpha_composite(bg, wash)
    canvas = Image.alpha_composite(canvas, bg)
    scale = (size * 0.66) / max(mark.size)
    nw, nh = int(mark.size[0] * scale), int(mark.size[1] * scale)
    mark = mark.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.alpha_composite(mark, ((size - nw) // 2, (size - nh) // 2 - int(size * 0.035)))
    badge = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    cx = cy = int(size * 0.765)
    rad = int(size * 0.152)
    bd.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=(255, 45, 78, 255))
    bd.ellipse((cx - rad + 6, cy - rad + 6, cx + rad - 6, cy + rad - 6), outline=(255, 255, 255, 230), width=max(4, size // 86))
    f = font(int(size * 0.18))
    box = bd.textbbox((0, 0), "R", font=f)
    tw, th = box[2] - box[0], box[3] - box[1]
    bd.text((cx - tw / 2 - box[0], cy - th / 2 - box[1] - size * 0.008), "R", font=f, fill=(255, 255, 255, 255))
    return Image.alpha_composite(canvas, badge)

def main():
    os.makedirs(OUT, exist_ok=True)
    for size, name in ((512, "icon-512.png"), (192, "icon-192.png"), (48, "icon-48.png")):
        make(size).save(os.path.join(OUT, name), "PNG")
        print("wrote", name)

if __name__ == "__main__":
    main()
