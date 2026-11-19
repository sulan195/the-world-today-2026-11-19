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
    # white field first: without it the white stripes are just the sky
    # showing through, and the flag reads as red bars on blue-grey
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    stripe = h / 7
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=(178, 34, 52))
    draw.rectangle([x, y, x + w, y + h], outline=(40, 40, 40), width=1)
    draw.rectangle([x, y, x + w * 0.45, y + stripe * 4], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            cx = x + 12 + c * (w * 0.45 - 20) / 4
            cy = y + 8 + r * (stripe * 4 - 14) / 3
            star(draw, cx, cy, 5, (255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=(40, 40, 40), width=1)
    star(draw, x + w * 0.22, y + h * 0.28, 17, (255, 222, 0))
    for dx, dy in [(0.42, 0.14), (0.47, 0.30), (0.47, 0.47), (0.42, 0.62)]:
        star(draw, x + w * dx, y + h * dy, 7, (255, 222, 0))


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))
    draw.rectangle([x, y, x + w, y + h], outline=(40, 40, 40), width=1)


def hero(draw, x0, y0, x1, y1):
    """The summit itself: three leaders at one long table, flags behind."""
    draw.rectangle([x0, y0, x1, y1], fill=(228, 231, 233))
    w = x1 - x0
    # the three flags on stands along the back wall
    fw, fh = 138, 84
    flags = [flag_us, flag_cn, flag_ru]
    names = ["TRUMP", "XI JINPING", "PUTIN"]
    suits = [(35, 42, 60), (24, 24, 28), (48, 50, 56)]
    centers = []
    for i, draw_flag in enumerate(flags):
        cx = x0 + w * (0.27 + 0.23 * i)
        centers.append(cx)
        draw.line([cx - fw / 2 - 8, y0 + 10, cx - fw / 2 - 8, y1 - 26],
                  fill=(90, 90, 90), width=3)
        draw_flag(draw, cx - fw / 2, y0 + 10, fw, fh)
    # the long table
    table_top = y1 - 34
    draw.polygon([(x0 + 60, table_top), (x1 - 60, table_top),
                  (x1 - 30, y1), (x0 + 30, y1)], fill=(104, 78, 54))
    draw.rectangle([x0 + 30, y1 - 12, x1 - 30, y1], fill=(84, 62, 42))
    # the three leaders, seated at the table under their flags
    for i, cx in enumerate(centers):
        # shoulders and suit
        draw.pieslice([cx - 34, table_top - 40, cx + 34, table_top + 28],
                      180, 360, fill=suits[i])
        draw.rectangle([cx - 34, table_top - 6, cx + 34, table_top + 2],
                       fill=suits[i])
        # head, with a thin cap of hair rather than a helmet
        draw.ellipse([cx - 13, table_top - 62, cx + 13, table_top - 36],
                     fill=(233, 198, 165))
        draw.pieslice([cx - 13, table_top - 63, cx + 13, table_top - 47],
                      180, 360, fill=(52, 46, 40))
        # microphone
        draw.line([cx + 20, table_top, cx + 12, table_top - 22],
                  fill=(30, 30, 30), width=2)
        draw.ellipse([cx + 9, table_top - 27, cx + 15, table_top - 21],
                     fill=(30, 30, 30))
        # name card on the table
        draw.rectangle([cx - 37, table_top + 8, cx + 37, table_top + 24],
                       fill=(255, 255, 255), outline=(120, 120, 120))
        f = sans("Bold", 11)
        tw = draw.textlength(names[i], font=f)
        draw.text((cx - tw / 2, table_top + 10), names[i], font=f, fill=INK)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def panel(draw, x, y, w, h, tag, tag_color, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=(150, 144, 128), width=2)
    draw.rectangle([x, y, x + w, y + 26], fill=tag_color)
    draw.text((x + 12, y + 3), tag, font=sans("Bold", 17), fill=(255, 255, 255))
    hy = wrapped(draw, x + 12, y + 33, headline, serif("Bold", 23), w - 24, 1.12)
    # shrink the body until it fits the space the headline left
    size = 16
    while size > 12:
        f = sans("Regular", size)
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        end = wrapped(probe, 0, 0, body, f, w - 24, 1.2)
        if hy + 3 + end <= y + h - 6:
            break
        size -= 1
    wrapped(draw, x + 12, hy + 3, body, sans("Regular", size), w - 24, 1.2)


def brief(draw, x, y, w, lead, body):
    """One short item in the IN BRIEF strip: a bold place line, then the news."""
    draw.text((x, y), lead, font=sans("Bold", 15), fill=ACCENT)
    wrapped(draw, x, y + 21, body, sans("Regular", 14), w, 1.25)


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
    centered(draw, 70, "THE WORLD TODAY", serif("Bold", 80))

    # date bar: names the day, as the judge asks
    draw.rectangle([MARGIN, 160, W - MARGIN, 206], fill=INK)
    centered(draw, 167, "THURSDAY, 19 NOVEMBER 2026", sans("Bold", 36),
             fill=(255, 255, 255))

    # main headline: the trilateral summit in Shenzhen
    centered(draw, 218,
             "SHENZHEN \u00b7 APEC SUMMIT \u00b7 THE FIRST U.S.\u2013CHINA\u2013RUSSIA SUMMIT IN HISTORY",
             sans("Bold", 19), fill=ACCENT)
    centered(draw, 244, "TRUMP, XI AND PUTIN HOLD", serif("Bold", 48))
    centered(draw, 296, "FIRST THREE-WAY SUMMIT", serif("Bold", 48))
    centered(draw, 356,
             "Xi hosts the two presidents at Kylin Villa: 90 minutes of talks, nine months",
             sans("Regular", 20), fill=GREY)
    centered(draw, 381,
             "after New START expired \u2014 then a four-point \u201cDeclaration toward Peace.\u201d",
             sans("Regular", 20), fill=GREY)

    hero(draw, MARGIN, 412, W - MARGIN, 520)
    centered(draw, 528,
             "Kylin Villa, Shenzhen, on Thursday. None of the three leaders spoke to the press afterwards.",
             sans("Regular", 16), fill=GREY)

    # the declaration's four points, as a strip under the picture
    dy = 552
    draw.text((MARGIN, dy), "THE DECLARATION \u2014 FOUR POINTS",
              font=sans("Bold", 16), fill=INK)
    note = "NOT IN THE TEXT: UKRAINE \u00b7 IRAN \u00b7 NORTH KOREA"
    draw.text((W - MARGIN - draw.textlength(note, font=sans("Bold", 16)), dy),
              note, font=sans("Bold", 16), fill=ACCENT)
    points = ["1  Reform the United Nations",
              "2  Raise refined-fuel supply \u201cfor all nations\u201d",
              "3  Uphold state officials' immunity; the ICC warned",
              "4  Nuclear-risk dialogue: \u201ca war that must never be fought\u201d"]
    colw = (W - 2 * MARGIN - 3 * 14) // 4
    for i, p in enumerate(points):
        wrapped(draw, MARGIN + i * (colw + 14), dy + 24, p,
                sans("Regular", 15), colw, 1.2)
    draw.line([MARGIN, dy + 70, W - MARGIN, dy + 70], fill=INK, width=2)

    # four more of the day's stories, each with its key numbers
    pw = (W - 2 * MARGIN - 16) // 2
    ph = 124
    gy = 634
    panel(draw, MARGIN, gy, pw, ph, "WORLD COURT \u00b7 THE HAGUE", (44, 84, 126),
          "Genocide Verdict on Myanmar",
          "The U.N.'s top court rules 9\u20136 that Myanmar's 2017 campaign "
          "against the Rohingya was genocide \u2014 its first such verdict on a "
          "state. Some 10,000 were killed; reparations are ordered.")
    panel(draw, MARGIN + pw + 16, gy, pw, ph, "UKRAINE WAR \u00b7 KERCH STRAIT", (150, 96, 30),
          "Crimean Bridge Hit a Third Time",
          "Neptune missiles hit the 19 km bridge's railway section hours "
          "before the summit, halting trains. Tuesday's strike felled a "
          "227-metre road span. Putin threatens retaliation.")
    gy2 = gy + ph + 12
    panel(draw, MARGIN, gy2, pw, ph, "MIDDLE EAST \u00b7 KHAN YOUNIS", (120, 44, 44),
          "Six Killed at Nasser Hospital",
          "A strike just after midnight hits the surgical wing, killing "
          "surgeon Rizk Abu Shaira and a boy of 13 among the six. Israel "
          "says it aimed at a Hamas commander.")
    panel(draw, MARGIN + pw + 16, gy2, pw, ph, "CLIMATE \u00b7 ANTALYA", (46, 110, 70),
          "COP31 Stalls on Fossil Fuels",
          "Ministers enter the final stretch split over how fast to exit "
          "fossil fuels \u2014 a second straight COP stalled there. The IEA sees "
          "\u201cno credible pathway back\u201d for energy.")

    # three shorter items across the foot of the page
    by = 906
    draw.text((MARGIN, by), "IN BRIEF", font=sans("Bold", 16), fill=INK)
    draw.line([MARGIN, by + 22, W - MARGIN, by + 22], fill=INK, width=1)
    bw = (W - 2 * MARGIN - 2 * 16) // 3
    brief(draw, MARGIN, by + 30, bw, "STRAIT OF HORMUZ",
          "Iran drones target U.S. bases in Kuwait and Bahrain after U.S. "
          "jets hit Qeshm Island. An ADNOC tanker burns: one missing, 11 hurt.")
    brief(draw, MARGIN + bw + 16, by + 30, bw, "VIENNA \u00b7 NORTH KOREA",
          "The IAEA says Pyongyang has completed a new uranium-enrichment "
          "hall at Yongbyon \u2014 \u201ca cause for serious concern.\u201d")
    brief(draw, MARGIN + 2 * (bw + 16), by + 30, bw, "COPENHAGEN \u00b7 THE ARCTIC",
          "Parliament votes 109\u20130 to ratify the Greenland security pact: "
          "new U.S. defence areas at Narsarsuaq and Mestersvig.")

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
