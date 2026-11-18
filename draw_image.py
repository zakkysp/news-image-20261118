#!/usr/bin/env python3
"""Draw the news image for Wednesday 18 November 2026.

One 1024x1024 PNG infographic: a header naming the day, six story
cards (headline + one-line summary + a simple drawn icon), and a
footer strip with the day's other headlines and sources. Everything
is drawn with PIL primitives; no photos, no stock art, no network.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (10, 37, 64)
GOLD = (253, 176, 34)
PAPER = (247, 244, 236)
INK = (16, 24, 40)
GREY = (52, 64, 84)
CARD_LINE = (208, 213, 221)
WHITE = (255, 255, 255)
FOOT_GREY = (152, 162, 179)

F_TITLE = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 74)
F_DATE = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 31)
F_TAG = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 18)
F_HEAD = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 28)
F_BODY = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 20)
F_FOOT = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 20)
F_FOOT_B = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 20)
F_SRC = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 15)


def wrap(text, font, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=color, width=3)


def draw_burst(d, cx, cy, r, color):
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22],
              fill=GOLD)


def draw_summit(d, cx, cy, r, color):
    d.ellipse([cx - r - 26, cy - 8, cx - r + 26, cy + 44], fill=color)
    d.ellipse([cx - 26, cy - 30, cx + 26, cy + 22], fill=GOLD)
    d.ellipse([cx + r - 26, cy - 8, cx + r + 26, cy + 44], fill=(23, 92, 211))
    d.line([cx - r, cy + 58, cx + r, cy + 58], fill=color, width=4)


def draw_bridge(d, cx, cy, r, color):
    d.line([cx - r, cy + 20, cx + r, cy + 20], fill=color, width=6)
    d.arc([cx - r, cy - 30, cx + r, cy + 40], 180, 360, fill=color, width=5)
    d.line([cx - r + 8, cy + 20, cx - r + 8, cy + 52], fill=color, width=5)
    d.line([cx + r - 8, cy + 20, cx + r - 8, cy + 52], fill=color, width=5)
    d.line([cx - 6, cy + 20, cx + 4, cy + 6, cx - 2, cy - 6, cx + 8, cy - 18],
           fill=(180, 35, 24), width=4)


def draw_ballot(d, cx, cy, r, color):
    d.rounded_rectangle([cx - r, cy - r + 12, cx + r, cy + r - 6],
                        radius=8, outline=color, width=5)
    d.line([cx - r + 14, cy + 2, cx - 8, cy + 22, cx + r - 10, cy - 26],
           fill=(6, 118, 71), width=7)


def draw_cross(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 245, 232))
    d.rectangle([cx - 11, cy - r + 14, cx + 11, cy + r - 14], fill=color)
    d.rectangle([cx - r + 14, cy - 11, cx + r - 14, cy + 11], fill=color)


def draw_voyager(d, cx, cy, r, color):
    for i in range(5):
        t = i / 4
        x = cx - r + 8 + t * (2 * r - 30)
        y = cy + 26 - t * 46
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=color)
    d.polygon([(cx + r - 18, cy - 34), (cx + r - 6, cy - 22),
               (cx + r - 18, cy - 10), (cx + r - 30, cy - 22)], fill=GOLD)
    d.rectangle([cx - r + 2, cy + 18, cx - r + 22, cy + 38], fill=color)


STORIES = [
    ("MIDDLE EAST", (180, 35, 24), draw_burst,
     "Iran strikes US bases in Kuwait and Bahrain",
     "US jets hit a missile site on Qeshm Island; Iran fires on bases hosting US forces."),
    ("DIPLOMACY", (23, 92, 211), draw_summit,
     "Xi and Putin meet in Shenzhen ahead of Trump talks",
     "The three leaders are set for a rare three-way summit as Xi denounces protectionism."),
    ("WAR IN UKRAINE", (105, 65, 198), draw_bridge,
     "Ukraine hits the Crimea bridge a second day",
     "Part of the Kerch road span falls into the strait after drone and missile strikes."),
    ("UNITED STATES", (14, 116, 144), draw_ballot,
     "Peltola wins Alaska; Democrats take Senate 56-44",
     "Democrat Mary Peltola unseats Dan Sullivan in the final Senate race of the midterms."),
    ("HEALTH", (6, 118, 71), draw_cross,
     "US loses measles-free status after 26 years",
     "More than 5,400 cases and 10 deaths in 2026, the worst US year since 1991."),
    ("SCIENCE", (181, 71, 8), draw_voyager,
     "Voyager 1 reaches one light-day from Earth",
     "16 billion miles out, its signals now take a full day to reach home."),
]


def draw_card(d, x, y, w, h, tag, color, icon, headline, summary):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=WHITE,
                        outline=CARD_LINE, width=2)
    pad = 18
    chip_w = F_TAG.getlength(tag) + 22
    chip_h = 30
    d.rounded_rectangle([x + pad, y + 14, x + pad + chip_w, y + 14 + chip_h],
                        radius=15, fill=color)
    d.text((x + pad + 11, y + 14 + 6), tag, font=F_TAG, fill=WHITE)
    icon(d, x + w - pad - 40, y + 52, 38, color)
    head_lines = wrap(headline, F_HEAD, w - 2 * pad - 96)
    body_lines = wrap(summary, F_BODY, w - 2 * pad)
    block_h = len(head_lines) * 33 + 4 + len(body_lines) * 27
    hy = y + 52 + max(0, (h - 52 - block_h) // 2)
    for line in head_lines:
        d.text((x + pad, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    sy = hy + 4
    for line in body_lines:
        d.text((x + pad, sy), line, font=F_BODY, fill=GREY)
        sy += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header band naming the day.
    d.rectangle([0, 0, W, 146], fill=NAVY)
    d.text((24, 22), "WORLD NEWS", font=F_TITLE, fill=WHITE)
    d.text((26, 104), "WEDNESDAY  ·  18 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    draw_globe(d, 948, 73, 46, GOLD)
    d.rectangle([0, 146, W, 150], fill=GOLD)

    # Six story cards, 2 columns x 3 rows.
    cw, ch, gx, gy = 484, 244, 16, 12
    x0, y0 = 20, 162
    for i, (tag, color, icon, headline, summary) in enumerate(STORIES):
        cx = x0 + (i % 2) * (cw + gx)
        cy = y0 + (i // 2) * (ch + gy)
        draw_card(d, cx, cy, cw, ch, tag, color, icon, headline, summary)

    # Footer band: other headlines of the day + sources.
    d.rectangle([0, 930, W, H], fill=NAVY)
    d.text((24, 940), "ALSO TODAY:", font=F_FOOT_B, fill=GOLD)
    d.text((24, 964),
           "Nvidia revenue doubles to $115.8B  ·  Cyclone Xavier, Category 5, hits the Cook Islands",
           font=F_FOOT, fill=WHITE)
    d.text((24, 988),
           "Russian military plane crashes in Siberia — 19 dead",
           font=F_FOOT, fill=WHITE)
    d.text((1024 - 24 - F_SRC.getlength("Sources: Reuters · AP · AFP · NASA · PAHO"),
            940), "Sources: Reuters · AP · AFP · NASA · PAHO",
           font=F_SRC, fill=FOOT_GREY)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
