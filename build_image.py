#!/usr/bin/env python3
"""Build entry.png: a 1024x1024 infographic summing up world news of Wed 18 Nov 2026.
Drawn with PIL (sharp vector text, no AI image generation, so no garbled words).
Deterministic: same input -> same bytes every run.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

INK = (20, 33, 61)          # dark navy text
NAVY = (16, 42, 67)         # header background
RED = (192, 57, 43)         # date band / lead accent
PAPER = (251, 248, 242)     # warm paper background
CARD = (255, 255, 255)
BORDER = (214, 219, 224)
MUTED = (90, 100, 114)
LEAD_BG = (253, 236, 234)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max width in pixels; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------- icons (simple geometric pictograms, drawn in accent colour) ----------
def icon_rocket(d, box, c):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    # flame
    d.polygon([(cx - 9, y1 - 8), (cx + 9, y1 - 8), (cx, y1 + 2)], fill=(245, 158, 11))
    # body
    d.rounded_rectangle([cx - 13, y0 + 14, cx + 13, y1 - 12], radius=10, fill=c)
    # nose
    d.polygon([(cx - 13, y0 + 16), (cx + 13, y0 + 16), (cx, y0)], fill=c)
    # window
    d.ellipse([cx - 6, y0 + 30, cx + 6, y0 + 42], fill=(255, 255, 255))
    # fins
    d.polygon([(cx - 13, y1 - 26), (cx - 26, y1 - 6), (cx - 13, y1 - 12)], fill=c)
    d.polygon([(cx + 13, y1 - 26), (cx + 26, y1 - 6), (cx + 13, y1 - 12)], fill=c)


def icon_bridge(d, box, c):
    x0, y0, x1, y1 = box
    d.line([(x0 + 4, y1 - 16), (x1 - 4, y1 - 16)], fill=c, width=7)
    d.arc([x0 + 6, y0 + 6, x1 - 6, y1 - 2], start=180, end=360, fill=c, width=7)
    d.line([(x0 + 12, y1 - 16), (x0 + 12, y1 - 2)], fill=c, width=6)
    d.line([(x1 - 12, y1 - 16), (x1 - 12, y1 - 2)], fill=c, width=6)
    d.line([(x0 + 4, y1 - 2), (x1 - 4, y1 - 2)], fill=c, width=5)


def icon_flags(d, box, c):
    x0, y0, x1, y1 = box
    for i, col in enumerate([(192, 57, 43), (37, 99, 235), (21, 128, 61)]):
        px = x0 + 10 + i * 18
        d.line([(px, y0 + 8), (px, y1 - 4)], fill=INK, width=4)
        d.polygon([(px, y0 + 8), (px + 17, y0 + 14), (px, y0 + 20)], fill=col)


def icon_dome(d, box, c):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    d.pieslice([cx - 22, y0 + 4, cx + 22, y0 + 44], start=180, end=360, fill=c)
    d.rectangle([cx - 24, y0 + 42, cx + 24, y0 + 48], fill=c)
    for i in range(4):
        px = x0 + 8 + i * 14
        d.rectangle([px, y0 + 50, px + 7, y1 - 6], fill=c)
    d.rectangle([x0 + 4, y1 - 8, x1 - 4, y1 - 2], fill=c)


def icon_virus(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    import math
    for k in range(8):
        a = math.pi * k / 4
        x2, y2 = cx + int(24 * math.cos(a)), cy + int(24 * math.sin(a))
        x3, y3 = cx + int(32 * math.cos(a)), cy + int(32 * math.sin(a))
        d.line([(x2, y2), (x3, y3)], fill=c, width=5)
        d.ellipse([x3 - 4, y3 - 4, x3 + 4, y3 + 4], fill=c)
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=c)
    d.ellipse([cx - 12, cy - 14, cx - 2, cy - 4], fill=(255, 255, 255))
    d.ellipse([cx + 4, cy + 2, cx + 12, cy + 10], fill=(255, 255, 255))


def icon_shield(d, box, c):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    d.polygon([(cx, y0 + 2), (x1 - 4, y0 + 12), (x1 - 4, y0 + 34),
               (cx, y1 - 2), (x0 + 4, y0 + 34), (x0 + 4, y0 + 12)], fill=c)
    d.rectangle([cx - 4, y0 + 18, cx + 4, y0 + 38], fill=(255, 255, 255))
    d.rectangle([cx - 11, y0 + 25, cx + 11, y0 + 33], fill=(255, 255, 255))


def icon_chip(d, box, c):
    x0, y0, x1, y1 = box
    for i in range(3):
        px = x0 + 14 + i * 16
        d.line([(px, y0 + 2), (px, y0 + 10)], fill=c, width=4)
        d.line([(px, y1 - 10), (px, y1 - 2)], fill=c, width=4)
        py = y0 + 14 + i * 16
        d.line([(x0 + 2, py), (x0 + 10, py)], fill=c, width=4)
        d.line([(x1 - 10, py), (x1 - 2, py)], fill=c, width=4)
    d.rounded_rectangle([x0 + 10, y0 + 10, x1 - 10, y1 - 10], radius=6, fill=c)
    d.rounded_rectangle([x0 + 22, y0 + 22, x1 - 22, y1 - 22], radius=4,
                        outline=(255, 255, 255), width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer border
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---------- masthead ----------
    d.rectangle([MARGIN, MARGIN, W - MARGIN, MARGIN + 92], fill=NAVY)
    # globe glyph
    gx, gy = MARGIN + 18, MARGIN + 16
    d.ellipse([gx, gy, gx + 60, gy + 60], outline=(255, 255, 255), width=4)
    d.ellipse([gx + 18, gy, gx + 42, gy + 60], outline=(255, 255, 255), width=3)
    d.line([(gx, gy + 30), (gx + 60, gy + 30)], fill=(255, 255, 255), width=3)
    d.arc([gx - 6, gy + 8, gx + 66, gy + 52], start=200, end=340, fill=(255, 255, 255), width=3)
    f_mast = font(SERIF_B, 58)
    d.text((MARGIN + 96, MARGIN + 16), "WORLD NEWS", font=f_mast, fill=(255, 255, 255))
    f_sub = font(SANS_B, 21)
    d.text((MARGIN + 98, MARGIN + 66), "THE DAY IN ONE IMAGE", font=f_sub, fill=(180, 200, 220))

    # ---------- date band ----------
    y = MARGIN + 92 + 10
    d.rectangle([MARGIN, y, W - MARGIN, y + 52], fill=RED)
    f_date = font(SANS_B, 30)
    date_txt = "WEDNESDAY, 18 NOVEMBER 2026"
    tw = d.textlength(date_txt, font=f_date)
    d.text(((W - tw) / 2, y + 10), date_txt, font=f_date, fill=(255, 255, 255))

    # ---------- lead story ----------
    y = y + 52 + 12
    lead_h = 210
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + lead_h], radius=10, fill=LEAD_BG,
                        outline=RED, width=2)
    # icon panel
    ix0, iy0, ix1, iy1 = MARGIN + 16, y + 16, MARGIN + 132, y + lead_h - 16
    d.rounded_rectangle([ix0, iy0, ix1, iy1], radius=8, fill=(255, 255, 255))
    icon_rocket(d, (ix0 + 18, iy0 + 14, ix1 - 18, iy1 - 14), RED)
    tx = MARGIN + 152
    f_kick = font(SANS_B, 20)
    d.text((tx, y + 18), "MIDDLE EAST  ·  GULF WAR", font=f_kick, fill=RED)
    f_lead = font(SANS_B, 34)
    lead_head = "Iran strikes Kuwait and Bahrain after U.S. hits Qeshm Island"
    lines = wrap(d, lead_head, f_lead, W - MARGIN - tx - 18)
    ly = draw_lines(d, lines, tx, y + 48, f_lead, INK, 42)
    f_body = font(SANS, 24)
    lead_sum = ("Tehran fired drones at U.S. bases in Kuwait and Bahrain, hours after "
                "U.S. jets struck a missile site on Qeshm Island in the Strait of Hormuz.")
    lines = wrap(d, lead_sum, f_body, W - MARGIN - tx - 18)
    draw_lines(d, lines, tx, ly + 6, f_body, (60, 68, 80), 31)

    # ---------- grid of six stories ----------
    stories = [
        ("UKRAINE WAR", "Ukraine hits Kerch Bridge again — road span falls",
         "A second day of strikes partly collapsed the bridge linking Russia to Crimea.",
         (37, 99, 235), icon_bridge),
        ("DIPLOMACY", "Xi and Putin meet in Shenzhen before Trump summit",
         "The leaders met a day before a first-ever three-way summit with Donald Trump.",
         (124, 58, 237), icon_flags),
        ("U.S. POLITICS", "Peltola wins Alaska; Democrats take Senate 56–44",
         "Democrat Mary Peltola unseated Sen. Dan Sullivan in the last Senate race.",
         (14, 116, 144), icon_dome),
        ("HEALTH", "Ebola in DR Congo passes 11,000 cases",
         "The outbreak has more than doubled in three months; 5,400 deaths, the UN said.",
         (153, 27, 27), icon_virus),
        ("HEALTH", "U.S. loses measles-free status after 26 years",
         "More than 5,400 cases and 10 deaths ended a status held since 2000.",
         (194, 65, 12), icon_shield),
        ("TECH", "Nvidia posts record $115.8B quarter",
         "Revenue doubled in a year; the board blocked ex-CEO Huang's return.",
         (21, 128, 61), icon_chip),
    ]
    gx0 = MARGIN
    gy0 = y + lead_h + 12
    cw = (W - 2 * MARGIN - 14) // 2
    ch = 148
    f_kick2 = font(SANS_B, 17)
    f_head2 = font(SANS_B, 25)
    f_body2 = font(SANS, 20)
    for i, (kick, head, summ, accent, icon_fn) in enumerate(stories):
        col, row = i % 2, i // 2
        cx0 = gx0 + col * (cw + 14)
        cy0 = gy0 + row * (ch + 12)
        d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=8, fill=CARD,
                            outline=BORDER, width=2)
        # icon tile
        t = 12
        d.rounded_rectangle([cx0 + t, cy0 + t, cx0 + t + 74, cy0 + ch - t], radius=6,
                            fill=(239, 243, 247))
        icon_fn(d, (cx0 + t + 8, cy0 + t + 8, cx0 + t + 66, cy0 + ch - t - 8), accent)
        tx2 = cx0 + t + 86
        d.text((tx2, cy0 + 12), kick, font=f_kick2, fill=accent)
        lines = wrap(d, head, f_head2, cw - t - 86 - 12)
        ly2 = draw_lines(d, lines, tx2, cy0 + 36, f_head2, INK, 30)
        lines = wrap(d, summ, f_body2, cw - t - 86 - 12)
        draw_lines(d, lines, tx2, ly2 + 3, f_body2, MUTED, 25)

    # ---------- "also" strip + sources ----------
    y = gy0 + 3 * ch + 2 * 12 + 12
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + 64], radius=8, fill=(239, 243, 247))
    f_also = font(SANS_B, 19)
    f_also2 = font(SANS, 19)
    d.text((MARGIN + 16, y + 9), "Also: ", font=f_also, fill=INK)
    aw = d.textlength("Also: ", font=f_also)
    also = ("Israel's Knesset elects Matan Kahana as speaker  ·  Russian military plane "
            "crash kills 19 in Siberia  ·  Category 5 Cyclone Xavier hits the Cook Islands")
    lines = wrap(d, also, f_also2, W - 2 * MARGIN - 32 - aw)
    draw_lines(d, lines, MARGIN + 16 + aw, y + 9, f_also2, INK, 25)

    y = y + 64 + 10
    f_src = font(SANS, 18)
    src = "Sources: Reuters · Associated Press · BBC · The Wall Street Journal — 18 November 2026"
    sw = d.textlength(src, font=f_src)
    d.text(((W - sw) / 2, y), src, font=f_src, fill=MUTED)

    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    im = build()
    im.save(out, "PNG", optimize=True)
    print("saved", out, im.size)
