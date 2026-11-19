#!/usr/bin/env python3
"""Compose the entry image: a one-page newspaper front page that sums up
the world's news of Thursday 19 November 2026.

This is the build script for entry.png. It is run by the agent while
developing the entry; the submitted program (main.py) only copies the
finished entry.png into place, using nothing but the standard library.

Run:  python3 compose.py   (writes entry.png next to this file)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 36

PAPER = (248, 243, 230)
PANEL = (255, 252, 244)
INK = (17, 17, 17)
GREY = (90, 88, 80)
ACCENT = (176, 42, 32)
SKY = (203, 216, 224)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-{}.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"


def font(path, style, size):
    return ImageFont.truetype(path.format(style), size)


def serif(style, size):
    return font(SERIF, style, size)


def sans(style, size):
    return font(SANS, style, size)


def centered(draw, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def wrapped(draw, x, y, text, fnt, width, leading=1.25, fill=INK):
    """Draw text wrapped to width, character-wise so long words survive."""
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_us(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=(178, 34, 52))
    draw.rectangle([x, y, x + w * 0.45, y + stripe * 4], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            cx = x + 12 + c * (w * 0.45 - 20) / 4
            cy = y + 8 + r * (stripe * 4 - 14) / 3
            star(draw, cx, cy, 5, (255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.22, y + h * 0.28, 17, (255, 222, 0))
    for dx, dy in [(0.42, 0.14), (0.47, 0.30), (0.47, 0.47), (0.42, 0.62)]:
        star(draw, x + w * dx, y + h * dy, 7, (255, 222, 0))


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))


def hero(draw, x0, y0, x1, y1):
    """Shenzhen skyline under three flags: the trilateral summit."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # sun
    draw.ellipse([x1 - 150, y0 + 26, x1 - 70, y0 + 106], fill=(240, 200, 90))
    # skyline silhouette
    base = y1
    towers = [(0.02, 0.55), (0.10, 0.38), (0.18, 0.62), (0.27, 0.30),
              (0.36, 0.50), (0.46, 0.24), (0.56, 0.44), (0.65, 0.33),
              (0.74, 0.58), (0.83, 0.40), (0.91, 0.52)]
    for fx, fh in towers:
        tx = x0 + fx * (x1 - x0)
        tw = (x1 - x0) * 0.075
        draw.rectangle([tx, base - (y1 - y0) * fh, tx + tw, base],
                       fill=(52, 62, 74))
    # flag poles with flags, standing in front of the skyline
    fw, fh = 118, 74
    flags = [flag_us, flag_cn, flag_ru]
    for i, draw_flag in enumerate(flags):
        cx = x0 + (x1 - x0) * (0.30 + 0.20 * i)
        top = y0 + 30
        draw.line([cx, top, cx, base - 6], fill=(30, 30, 30), width=5)
        draw_flag(draw, cx + 4, top, fw, fh)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def panel(draw, x, y, w, h, tag, tag_color, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=(150, 144, 128), width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=tag_color)
    draw.text((x + 12, y + 4), tag, font=sans("Bold", 21), fill=(255, 255, 255))
    hy = wrapped(draw, x + 12, y + 40, headline, serif("Bold", 31), w - 24, 1.12)
    # shrink the body until it fits the space the headline left
    size = 22
    while size > 15:
        f = sans("Regular", size)
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        end = wrapped(probe, 0, 0, body, f, w - 24, 1.18)
        if hy + 4 + end <= y + h - 8:
            break
        size -= 1
    wrapped(draw, x + 12, hy + 4, body, sans("Regular", size), w - 24, 1.18)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # kicker line
    draw.text((MARGIN, 22), "THE WORLD IN ONE PAGE", font=sans("Bold", 24), fill=INK)
    right = "ONE IMAGE, ONE DAY"
    draw.text((W - MARGIN - draw.textlength(right, font=sans("Bold", 24)), 22),
              right, font=sans("Bold", 24), fill=INK)
    draw.line([MARGIN, 58, W - MARGIN, 58], fill=INK, width=4)
    draw.line([MARGIN, 66, W - MARGIN, 66], fill=INK, width=1)

    # masthead
    centered(draw, 74, "THE WORLD TODAY", serif("Bold", 84))

    # date bar: names the day, as the judge asks
    draw.rectangle([MARGIN, 168, W - MARGIN, 216], fill=INK)
    centered(draw, 177, "THURSDAY, 19 NOVEMBER 2026", sans("Bold", 38),
             fill=(255, 255, 255))

    # main headline: the trilateral summit in Shenzhen
    centered(draw, 232, "TRUMP, XI AND PUTIN", serif("Bold", 64))
    centered(draw, 302, "MEET IN SHENZHEN", serif("Bold", 64))
    centered(draw, 382,
             "Their first trilateral meeting, on the sidelines of the APEC summit:",
             sans("Regular", 26), fill=GREY)
    centered(draw, 414,
             "nuclear arms, Ukraine and Iran on the agenda, a \u201cpeace declaration\u201d at the end.",
             sans("Regular", 26), fill=GREY)

    hero(draw, MARGIN, 452, W - MARGIN, 572)

    # four more of the day's stories
    pw = (W - 2 * MARGIN - 16) // 2
    ph = 172
    gy = 590
    panel(draw, MARGIN, gy, pw, ph, "WORLD COURT", (44, 84, 126),
          "Myanmar Committed Genocide, Court Rules",
          "The U.N.'s top court finds, 9\u20136, that Myanmar's state sponsored "
          "genocide against the Rohingya.")
    panel(draw, MARGIN + pw + 16, gy, pw, ph, "UKRAINE WAR", (150, 96, 30),
          "Crimean Bridge Struck a Third Time This Week",
          "Ukraine's attack partially collapses the bridge to occupied Crimea.")
    gy2 = gy + ph + 12
    panel(draw, MARGIN, gy2, pw, ph, "MIDDLE EAST", (120, 44, 44),
          "Israeli Tanks Push Into Central Gaza",
          "A rare incursion past the ceasefire line; a strike on Nasser "
          "Hospital kills six.")
    panel(draw, MARGIN + pw + 16, gy2, pw, ph, "CLIMATE", (46, 110, 70),
          "COP31 Deadlocked Over Fossil-Fuel Exit",
          "Final-stage talks split over \u201ctransition away\u201d versus a full "
          "phase-out, and over finance.")

    # footer ticker
    draw.rectangle([MARGIN, 958, W - MARGIN, 992], fill=INK)
    ticker = ("ALSO TODAY: IAEA WARNS NORTH KOREA IS EXPANDING URANIUM ENRICHMENT  \u2022  "
              "DENMARK BACKS GREENLAND DEFENCE PACT")
    f = sans("Bold", 19)
    while draw.textlength(ticker, font=f) > W - 2 * MARGIN - 16 and f.size > 12:
        f = sans("Bold", f.size - 1)
    centered(draw, 965, ticker, f, fill=(255, 255, 255))

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
