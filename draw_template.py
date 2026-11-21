#!/usr/bin/env python3
"""make.fun news-image TEMPLATE (1024x1024), drawn with PIL.

Flat newspaper front page, central world map (the layout that ran for
19 Nov 2026). All content comes from a data module (default: sample_news)
-- PAGE for the masthead/numbers/date-check/footer and STORIES for the
20 drawn panels + ALSO line. To use it for a new day, copy sample_news.py,
replace the verified stories, and run:  python3 draw_template.py [output]
Deterministic: fixed fonts, fixed geometry, no randomness, no network.
main.py (stdlib-only) just copies entry.png to the output dir.

Style: newspaper front page, like the top-ranked entries -- cream paper,
large serif date, red italic standfirst, region bar, red numbers strip,
3 hero panels, small-panel matrix (16 drawn), numbered world map, two-column
briefs, DATE CHECK box, source footer. Flat vector editorial
illustration: one recognisable icon scene per panel, flat colour
blocks + thin dark outlines, muted paper palette (cream, navy, brick
red, forest green, ochre). Neon is used in the GTA panel only.
No pixel figures, no real faces: summit figures are simple cartoon
half-bodies (hair / suit / tie, no facial detail) or table + flags.
Content: only verified 19 Nov 2026 stories from
NEWS_BRIEF_2026-11-19.md. Deterministic: fixed fonts, fixed geometry,
no randomness, no network.
Run:  python3 draw.py [output_path]   (default: entry.png next to this file)
main.py (stdlib-only) just copies entry.png to the output dir.
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

from sample_news import PAGE, STORIES

W, H = 1024, 1024
DJ = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = DJ + "DejaVuSerif-Bold.ttf"
SERIF = DJ + "DejaVuSerif.ttf"
SANS_B = DJ + "DejaVuSans-Bold.ttf"
SANS = DJ + "DejaVuSans.ttf"

PAPER = "#F7F1E3"
CARD = "#FFFDF6"
INK = "#1A1A1A"
INK2 = "#3A3A3A"
RED = "#B03A2E"
RED2 = "#C8102E"
NAVY = "#1F3A5F"
GREEN = "#2E6B4A"
OCHRE = "#C08A3E"
SKY = "#B9CDE0"
SAND = "#E8D5A8"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, font, fill, leading=None):
    x, y = xy
    leading = leading or int(font.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def badge(draw, x, y, n, r=13):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED2,
                 outline="#FFFFFF", width=2)
    f = F(SANS_B, 14 if r >= 13 else 11)
    t = str(n)
    tw = draw.textlength(t, font=f)
    draw.text((x + r - tw / 2, y + r - 9), t, font=f, fill="#FFFFFF")


def flag(d, x, y, w, h, kind):
    """Small flat flag: cn / us / ru / dk."""
    if kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill="#DE2910", outline=INK, width=1)
        d.ellipse([x + 3, y + 3, x + 10, y + 10], fill="#FFDE00")
    elif kind == "us":
        for i in range(7):
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill="#FFFFFF" if i % 2 else "#B22234")
        d.rectangle([x, y, x + w * 0.4, y + h * 0.45], fill="#3C3B6E")
    elif kind == "ru":
        for i, c in enumerate(["#FFFFFF", "#0039A6", "#D52B1E"]):
            d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                        fill=c)
    elif kind == "ve":
        for i, c in enumerate(["#FFCC00", "#003893", "#CF142B"]):
            d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                        fill=c)
        for sx in (4, 10, 16):
            d.ellipse([x + sx, y + h // 2 - 2, x + sx + 3, y + h // 2 + 1],
                      fill="#FFFFFF")
    elif kind == "dk":
        d.rectangle([x, y, x + w, y + h], fill="#C60C30", outline=INK, width=1)
        d.rectangle([x + w * 0.28, y, x + w * 0.42, y + h], fill="#FFFFFF")
        d.rectangle([x, y + h * 0.38, x + w, y + h * 0.58], fill="#FFFFFF")


def half_body(d, cx, base_y, skin, hair, suit):
    """Simple cartoon half-body: head, hair, suit, tie. No face detail."""
    d.ellipse([cx - 13, base_y - 52, cx + 13, base_y - 26],
              fill=skin, outline=INK, width=2)
    d.pieslice([cx - 13, base_y - 52, cx + 13, base_y - 30], 180, 360,
               fill=hair)
    d.polygon([(cx - 20, base_y - 26), (cx + 20, base_y - 26),
               (cx + 26, base_y), (cx - 26, base_y)], fill=suit,
              outline=INK, width=2)
    d.polygon([(cx - 4, base_y - 26), (cx + 4, base_y - 26),
               (cx, base_y - 8)], fill=RED2)


def smoke_plume(d, x, y, w, h):
    """Layered smoke column: three offset ellipses, dark base to pale top."""
    d.ellipse([x, y + h - 18, x + w, y + h], fill="#8A8A8A",
              outline="#6A6A6A", width=1)
    d.ellipse([x + 3, y + h // 2, x + w - 3, y + h - 8], fill="#A9A9A9",
              outline="#8A8A8A", width=1)
    d.ellipse([x + 6, y, x + w - 6, y + h // 2 + 4], fill="#C9C9C9",
              outline="#A9A9A9", width=1)


# ---------------------------------------------------------------- figures
def draw_summit(d, x, y, w, h):
    """Shenzhen trilateral: navy room, oval table, 3 flags, 3 half-bodies."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x, y + h - 26, x + w, y + h], fill="#8A6D3B")
    # window skyline
    for bx, bw, bh in [(10, 26, 34), (42, 20, 48), (68, 30, 28),
                       (104, 22, 42), (240, 26, 36), (272, 20, 46)]:
        d.rectangle([x + bx, y + 8 + (48 - bh), x + bx + bw, y + 56],
                    fill="#3A5A80", outline="#1A2A40", width=1)
    # three figures behind the table
    for cx, skin, hair, suit in [(x + 70, "#E8C9A0", "#1A1A1A", "#2B2B2B"),
                                 (x + w // 2, "#F0D0B0", "#8A6D3B", "#3A3A5F"),
                                 (x + w - 70, "#E8C9A0", "#C0C0C0", "#4A2B2B")]:
        half_body(d, cx, y + h - 26, skin, hair, suit)
    # oval table + flags
    d.ellipse([x + 30, y + h - 34, x + w - 30, y + h - 6], fill="#D9C9A8",
              outline=INK, width=2)
    flag(d, x + 52, y + h - 30, 26, 16, "cn")
    flag(d, x + w // 2 - 13, y + h - 30, 26, 16, "us")
    flag(d, x + w - 78, y + h - 30, 26, 16, "ru")


def draw_gta(d, x, y, w, h):
    """GTA VI: the only neon panel -- purple-pink sunset, palm, car."""
    for i in range(h):
        t = i / max(1, h)
        r = int(180 + (255 - 180) * t)
        g = int(80 + (120 - 80) * t)
        b = int(180 + (80 - 180) * t)
        d.line([x, y + i, x + w, y + i], fill=(r, g, b))
    d.ellipse([x + w - 78, y + 10, x + w - 28, y + 60], fill="#FFD23F",
              outline="#E8A800", width=2)
    # palm silhouette
    d.polygon([(x + 18, y + h), (x + 24, y + h), (x + 26, y + 26),
               (x + 20, y + 26)], fill="#1A1A1A")
    for a in (-50, -20, 10, 40):
        rad = math.radians(a - 90)
        d.line([x + 23, y + 26, x + 23 + 34 * math.cos(rad),
                y + 26 + 18 * math.sin(rad)], fill="#1A1A1A", width=4)
    # skyline + car
    d.rectangle([x, y + h - 34, x + w, y + h - 22], fill="#2A1A4A")
    for bx in range(6):
        d.rectangle([x + 50 + bx * 36, y + h - 58, x + 78 + bx * 36,
                     y + h - 22], fill="#3A2A5A", outline="#FF6EC7", width=1)
    d.rectangle([x, y + h - 22, x + w, y + h], fill="#14142A")
    d.polygon([(x + w // 2 - 52, y + h - 20), (x + w // 2 - 34, y + h - 34),
               (x + w // 2 + 30, y + h - 34), (x + w // 2 + 54, y + h - 20)],
              fill="#E83E8C", outline="#FFFFFF", width=2)
    d.rectangle([x + w // 2 - 56, y + h - 20, x + w // 2 + 58, y + h - 10],
                fill="#C8102E", outline="#FFFFFF", width=2)
    for wx in (x + w // 2 - 34, x + w // 2 + 30):
        d.ellipse([wx - 8, y + h - 12, wx + 8, y + h + 4], fill="#1A1A1A",
                  outline="#FFFFFF", width=2)
    d.text((x + 10, y + 8), "VI", font=F(SANS_B, 34), fill="#FFFFFF")


def draw_anthropic(d, x, y, w, h):
    """Anthropic IPO: dark market screen, green bars, $83."""
    d.rectangle([x, y, x + w, y + h], fill="#0F2A1A")
    d.rectangle([x, y, x + w, y + 22], fill="#14264E")
    d.text((x + 8, y + 4), "ANT  ·  NASDAQ", font=F(SANS_B, 12),
           fill="#FFFFFF")
    bars = [18, 30, 26, 42, 38, 56, 52, 68]
    for i, bh in enumerate(bars):
        bx = x + 14 + i * 36
        d.rectangle([bx, y + h - 14 - bh, bx + 22, y + h - 14],
                    fill="#2ECC71", outline="#1F7A3A", width=1)
    d.line([(x + 10, y + h - 32), (x + w - 10, y + h - 66)], fill="#FFD23F",
           width=3)
    d.rectangle([x + w - 96, y + 30, x + w - 10, y + 62], fill="#FFFFFF",
                outline=INK, width=2)
    d.text((x + w - 88, y + 34), "$83", font=F(SANS_B, 22), fill=GREEN)


def draw_icj(d, x, y, w, h):
    """ICJ: courthouse, scales, gavel (compact, h-relative)."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x + 14, y + 14, x + w - 14, y + h - 4], fill="#E8DCC8",
                outline=INK, width=2)
    d.polygon([(x + 8, y + 14), (x + w // 2, y + 2), (x + w - 8, y + 14)],
              fill="#8A6D3B", outline=INK, width=2)
    for cx in (x + 34, x + w // 2, x + w - 34):
        d.rectangle([cx - 6, y + 18, cx + 6, y + h - 6], fill="#FFFFFF",
                    outline=INK, width=1)
    cx, cy = x + w // 2, y + h - 12
    d.line([cx, cy - 14, cx, cy + 2], fill=INK, width=2)
    d.line([cx - 16, cy - 14, cx + 16, cy - 14], fill=INK, width=2)
    for sx in (cx - 16, cx + 16):
        d.line([sx, cy - 14, sx, cy - 6], fill=INK, width=2)
        d.polygon([(sx - 6, cy - 6), (sx + 6, cy - 6), (sx, cy - 1)],
                  fill="#FFD23F", outline=INK, width=1)
    d.rectangle([x + w - 34, y + 4, x + w - 12, y + 12], fill="#8A6D3B",
                outline=INK, width=2)


def draw_cop31(d, x, y, w, h):
    """COP31: earth, thermometer, leaf -- no cross, no pin."""
    d.rectangle([x, y, x + w, y + h], fill="#DCE7E0")
    cx, cy = x + 48, y + h // 2 + 2
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill="#3B82D6",
              outline=NAVY, width=2)
    d.polygon([(cx - 20, cy - 6), (cx - 4, cy - 16), (cx + 8, cy - 2),
               (cx - 2, cy + 12)], fill=GREEN, outline="#1F5A3A", width=1)
    d.polygon([(cx + 4, cy + 6), (cx + 18, cy + 2), (cx + 16, cy + 16)],
              fill=GREEN, outline="#1F5A3A", width=1)
    # thermometer, right: white tube, red mercury, no cross over it
    tx = x + w - 34
    d.rectangle([tx, y + 8, tx + 12, y + h - 20], fill="#FFFFFF",
                outline=INK, width=2)
    d.ellipse([tx - 3, y + h - 26, tx + 15, y + h - 8], fill=RED2,
              outline=INK, width=2)
    d.rectangle([tx + 4, y + h - 34, tx + 8, y + h - 14], fill=RED2)
    for ty in (y + 16, y + 28, y + 40):
        d.line([tx + 12, ty, tx + 18, ty], fill=INK, width=2)
    # leaf, bottom left
    d.ellipse([x + 10, y + h - 24, x + 36, y + h - 8], fill=GREEN,
              outline="#1F5A3A", width=2)


def draw_cyclone(d, x, y, w, h):
    """Cyclone Akvan: spiral over the coast."""
    d.rectangle([x, y, x + w, y + h], fill="#9FB8CC")
    cx, cy = x + w // 2, y + h // 2 - 4
    R = max(8, h // 2 - 4)
    for r, a0 in ((R, 20), (R * 3 // 4, 110), (R // 2, 200), (R // 4, 290)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 240,
              fill="#FFFFFF", width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED2)
    d.polygon([(x, y + h - 14), (x + w, y + h - 14), (x + w, y + h),
               (x, y + h)], fill=GREEN)
    for lx in (x + 16, x + 52, x + 88):
        d.line([lx, y + h - 24, lx - 6, y + h - 10], fill="#3B6E9E", width=2)


def draw_kerch(d, x, y, w, h):
    """Kerch Bridge: broken span over water (compact, h-relative)."""
    d.rectangle([x, y, x + w, y + h], fill="#FDE8C8")
    d.rectangle([x, y + h - 12, x + w, y + h], fill="#7FB8D9")
    for i in range(4):
        wx = x + 14 + i * 52
        d.arc([wx, y + h - 10, wx + 34, y + h - 2], 180, 360,
              fill="#FFFFFF", width=2)
    d.rectangle([x + 20, y + 10, x + 34, y + h - 12], fill="#8A6D3B",
                outline="#5C4630", width=2)
    d.rectangle([x + w - 34, y + 10, x + w - 20, y + h - 12], fill="#8A6D3B",
                outline="#5C4630", width=2)
    d.line([x + 8, y + 18, x + 84, y + 18], fill="#5C4630", width=4)
    d.line([x + w - 84, y + 18, x + w - 8, y + 18], fill="#5C4630", width=4)
    d.line([x + 84, y + 18, x + 100, y + 30], fill=RED2, width=3)
    d.line([x + w - 84, y + 18, x + w - 100, y + 30], fill=RED2, width=3)


def draw_riyadh(d, x, y, w, h):
    """Riyadh PIF Tower: tall glass tower, cracked windows, smoke."""
    d.rectangle([x, y, x + w, y + h], fill="#1F2A44")
    d.rectangle([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + h - 6],
                fill="#7FB8D9", outline="#FFFFFF", width=2)
    for wy in range(y + 14, y + h - 12, 12):
        d.rectangle([x + w // 2 - 28, wy, x + w // 2 - 6, wy + 6],
                    fill="#DCE9F7")
        d.rectangle([x + w // 2 + 6, wy, x + w // 2 + 28, wy + 6],
                    fill="#3B6E9E")
    # cracked floors
    d.line([x + w // 2 - 30, y + 34, x + w // 2 + 10, y + 46], fill=RED2,
           width=3)
    d.line([x + w // 2 + 10, y + 46, x + w // 2 - 10, y + 58], fill=RED2,
           width=3)
    smoke_plume(d, x + w // 2 - 52, y + 2, 18, 30)
    for bx, bw in ((x + 8, 26), (x + w - 34, 26)):
        d.rectangle([bx, y + h - 34, bx + bw, y + h - 6], fill="#3A5A80",
                    outline="#1A2A40", width=1)


def draw_gaza(d, x, y, w, h):
    """Gaza: tank as the single icon, rubble below (compact, h-relative)."""
    d.rectangle([x, y, x + w, y + h], fill="#EFE0C0")
    d.rectangle([x + 22, y + 8, x + w - 22, y + 24], fill="#5C4630",
                outline=INK, width=2)
    d.rectangle([x + 46, y + 24, x + w - 46, y + 32], fill="#3A3A3A",
                outline=INK, width=2)
    d.line([x + w - 46, y + 16, x + w - 8, y + 12], fill=INK, width=3)
    for wx in (x + 40, x + 70, x + 100, x + 130):
        d.ellipse([wx - 7, y + 30, wx + 7, y + 42], fill="#1A1A1A",
                  outline="#000000", width=1)
    d.polygon([(x + 8, y + h - 6), (x + 44, y + h - 6), (x + 44, y + h - 12),
               (x + 56, y + h - 16), (x + 68, y + h - 6)], fill=INK2)
    d.polygon([(x + 120, y + h - 6), (x + w - 8, y + h - 6),
               (x + w - 8, y + h - 12), (x + w - 30, y + h - 12),
               (x + w - 30, y + h - 16), (x + w - 52, y + h - 6)],
              fill=INK)


def draw_greenland(d, x, y, w, h):
    """Denmark-Greenland: iceberg, island, Danish flag."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 22, x + w, y + h], fill="#3B82D6")
    d.polygon([(x + 18, y + h - 22), (x + 52, y + h - 52),
               (x + 86, y + h - 22)], fill="#FFFFFF", outline=INK, width=2)
    d.polygon([(x + 96, y + h - 22), (x + 124, y + h - 42),
               (x + 152, y + h - 22)], fill="#DCE9F7", outline=INK, width=2)
    d.polygon([(x + w - 62, y + 12), (x + w - 30, y + 8), (x + w - 14, y + 30),
               (x + w - 44, y + 44), (x + w - 66, y + 28)], fill="#9DB894",
              outline=GREEN, width=2)
    flag(d, x + 12, y + 10, 30, 18, "dk")


def draw_nkorea(d, x, y, w, h):
    """North Korea: cooling tower + warning triangle."""
    d.rectangle([x, y, x + w, y + h], fill="#E8E4D8")
    d.polygon([(x + 34, y + h - 10), (x + 44, y + 16), (x + 74, y + 16),
               (x + 84, y + h - 10)], fill="#C9C9C9", outline=INK, width=2)
    d.ellipse([x + 40, y + 12, x + 78, y + 24], fill="#8A8A8A",
              outline=INK, width=2)
    for sx, sy in ((x + 96, y + 18), (x + 108, y + 10), (x + 120, y + 20)):
        d.ellipse([sx - 7, sy, sx + 7, sy + 10], fill="#B9B9B9",
                  outline="#8A8A8A", width=1)
    d.polygon([(x + w - 42, y + h - 12), (x + w - 22, y + h - 48),
               (x + w - 2, y + h - 12)], fill="#FFD23F", outline=INK,
              width=2)
    d.text((x + w - 27, y + h - 38), "!", font=F(SANS_B, 20), fill=INK)
    d.line([x + 10, y + h - 10, x + w - 10, y + h - 10], fill=INK, width=2)


def draw_bangladesh(d, x, y, w, h):
    """Bangladesh: placards + flame, no people drawn."""
    d.rectangle([x, y, x + w, y + h], fill="#FDE8C8")
    d.rectangle([x + 10, y + 12, x + 94, y + 34], fill=RED2, outline=INK,
                width=2)
    d.text((x + 14, y + 17), "SHUTDOWN", font=F(SANS_B, 11), fill="#FFFFFF")
    for px, py in ((x + 96, y + 14), (x + 130, y + 22), (x + 160, y + 12)):
        d.rectangle([px, py, px + 26, py + 18], fill="#FFFFFF", outline=INK,
                    width=2)
        d.line([px + 13, py + 18, px + 13, py + 34], fill=INK, width=2)
    d.polygon([(x + w // 2 - 12, y + h - 8), (x + w // 2 - 20, y + h - 30),
               (x + w // 2 - 6, y + h - 22), (x + w // 2, y + h - 42),
               (x + w // 2 + 8, y + h - 22), (x + w // 2 + 20, y + h - 30),
               (x + w // 2 + 12, y + h - 8)], fill="#E86A1A",
              outline="#B03A2E", width=2)
    d.rectangle([x, y + h - 8, x + w, y + h], fill="#8A6D3B")



def draw_venezuela(d, x, y, w, h):
    """Venezuela deal: US + VE flags, signed document, red seal."""
    d.rectangle([x, y, x + w, y + h], fill="#DCE9F7")
    flag(d, x + 12, y + 10, 44, 26, "us")
    flag(d, x + w - 56, y + 10, 44, 26, "ve")
    d.rectangle([x + 30, y + h - 34, x + w - 30, y + h - 8], fill="#FFFFFF",
                outline=INK, width=2)
    for ly in (y + h - 28, y + h - 22, y + h - 16):
        d.line([x + 38, ly, x + w - 52, ly], fill="#8A8A8A", width=2)
    d.ellipse([x + w - 48, y + h - 28, x + w - 32, y + h - 12], fill=RED2,
              outline="#8E2B20", width=2)
    d.line([x + 56, y + 44, x + 76, y + 52], fill=INK, width=3)
    d.line([x + w - 76, y + 44, x + w - 56, y + 52], fill=INK, width=3)


def draw_hormuz(d, x, y, w, h):
    """Hormuz: tanker on the strait, flames, layered smoke (reported)."""
    d.rectangle([x, y, x + w, y + h], fill="#FDE8C8")
    d.rectangle([x, y + h - 22, x + w, y + h], fill="#3B82D6")
    for wx in (x + 14, x + 60, x + 106):
        d.arc([wx, y + h - 18, wx + 28, y + h - 6], 180, 360,
              fill="#FFFFFF", width=2)
    # tanker hull + containers + bridge
    d.polygon([(x + 14, y + h - 30), (x + w - 14, y + h - 30),
               (x + w - 26, y + h - 12), (x + 26, y + h - 12)],
              fill="#5C4630", outline=INK, width=2)
    for i, c in enumerate(["#C8102E", "#2E6B4A", "#C08A3E", "#1F3A5F"]):
        d.rectangle([x + 26 + i * 32, y + h - 52, x + 52 + i * 32, y + h - 30],
                    fill=c, outline=INK, width=1)
    d.rectangle([x + w - 44, y + h - 56, x + w - 20, y + h - 30],
                fill="#FFFFFF", outline=INK, width=2)
    # flames on deck, smoke column above
    for fx, fh in ((x + 40, 14), (x + 58, 20), (x + 78, 12)):
        d.polygon([(fx - 8, y + h - 30), (fx, y + h - 30 - fh),
                   (fx + 8, y + h - 30)], fill="#E86A1A", outline="#B03A2E",
                  width=1)
    smoke_plume(d, x + w // 2 - 9, y + 4, 18, 26)


def draw_senegal(d, x, y, w, h):
    """Senegal: tilted boat, life ring, waves, gull."""
    d.rectangle([x, y, x + w, y + h], fill="#B9CDE0")
    d.rectangle([x, y + h - 26, x + w, y + h], fill="#3B82D6")
    for wx in (x + 10, x + 56, x + 102, x + 148):
        d.arc([wx, y + h - 20, wx + 26, y + h - 8], 180, 360,
              fill="#FFFFFF", width=2)
    # tilted boat
    d.polygon([(x + 34, y + h - 44), (x + 150, y + h - 56),
               (x + 138, y + h - 30), (x + 48, y + h - 22)],
              fill="#8A6D3B", outline="#5C4630", width=2)
    d.line([x + 92, y + h - 50, x + 92, y + h - 68], fill=INK, width=3)
    d.polygon([(x + 92, y + h - 68), (x + 118, y + h - 52),
               (x + 92, y + h - 52)], fill="#FFFFFF", outline=INK, width=1)
    # life ring floating beside it
    d.ellipse([x + w - 42, y + h - 34, x + w - 16, y + h - 8], fill="#FFFFFF",
              outline=RED2, width=4)
    d.ellipse([x + w - 34, y + h - 26, x + w - 24, y + h - 16], fill="#3B82D6",
              outline=RED2, width=2)
    d.arc([x + 16, y + 10, x + 34, y + 22], 200, 340, fill=INK, width=2)


def draw_redcrab(d, x, y, w, h):
    """Christmas Island red crabs: three crabs on sand, palm, sea."""
    d.rectangle([x, y, x + w, y + h], fill="#B9E0C9")
    d.rectangle([x, y + h - 30, x + w, y + h], fill="#3B82D6")
    d.rectangle([x, y + h - 34, x + w, y + h - 30], fill="#E8D5A8")
    # palm, left
    d.polygon([(x + 12, y + 8), (x + 16, y + 8), (x + 18, y + 34),
               (x + 14, y + 34)], fill="#8A6D3B")
    for a in (-50, -10, 30):
        rad = math.radians(a - 90)
        d.line([x + 15, y + 10, x + 15 + 22 * math.cos(rad),
                y + 10 + 12 * math.sin(rad)], fill=GREEN, width=3)
    # three crabs
    for cx, cy, sc in ((x + 62, y + h - 44, 1.0), (x + 108, y + h - 38, 0.85),
                       (x + 148, y + h - 46, 0.9)):
        r = int(13 * sc)
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=RED2,
                  outline="#8E2B20", width=2)
        for lx in (-1, 0, 1):
            d.line([cx + lx * 6, cy + r // 2, cx + lx * 10, cy + r],
                   fill="#8E2B20", width=2)
        for sx in (-1, 1):
            d.line([cx + sx * r, cy, cx + sx * (r + 8), cy - 4],
                   fill="#8E2B20", width=2)
            ex0 = min(cx + sx * (r + 6), cx + sx * (r + 12))
            ex1 = max(cx + sx * (r + 6), cx + sx * (r + 12))
            d.ellipse([ex0, cy - 8, ex1, cy - 2],
                      fill=RED2, outline="#8E2B20", width=1)
        d.line([cx - 5, cy - r // 2, cx - 5, cy - r // 2 - 6], fill=INK, width=2)
        d.line([cx + 5, cy - r // 2, cx + 5, cy - r // 2 - 6], fill=INK, width=2)



def draw_gashusky(d, x, y, w, h):
    """Gas Husky: LPG tanker, GAS tank, life ring. Rescue confirmed Thu."""
    d.rectangle([x, y, x + w, y + h], fill="#B9CDE0")
    d.rectangle([x, y + h - 10, x + w, y + h], fill="#3B82D6")
    d.polygon([(x + 20, y + h - 22), (x + w - 20, y + h - 26),
               (x + w - 30, y + h - 12), (x + 30, y + h - 12)],
              fill="#5C4630", outline=INK, width=2)
    d.ellipse([x + w // 2 - 14, y + 2, x + w // 2 + 14, y + 18],
              fill="#FFFFFF", outline=INK, width=2)
    d.text((x + w // 2 - 10, y + 5), "GAS", font=F(SANS_B, 9), fill=RED2)
    d.ellipse([x + w - 34, y + 2, x + w - 14, y + 22], fill="#FFFFFF",
              outline=RED2, width=3)
    d.ellipse([x + w - 29, y + 7, x + w - 19, y + 17], fill="#3B82D6",
              outline=RED2, width=2)


def draw_trumpiran(d, x, y, w, h):
    """Trump on Iran: podium, mic, quote bubble."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x + 14, y + 4, x + 130, y + 22], fill="#FFFFFF",
                outline=INK, width=2)
    d.text((x + 18, y + 7), "SEE WHAT HAPPENS", font=F(SANS_B, 9),
           fill=RED2)
    d.line([x + w // 2, y + h - 16, x + w // 2 - 14, y + 24], fill="#C0C0C0",
           width=3)
    d.ellipse([x + w // 2 - 18, y + 20, x + w // 2 - 10, y + 28],
              fill="#1A1A1A")
    d.rectangle([x + w // 2 - 40, y + h - 16, x + w // 2 + 40, y + h],
                fill="#8A6D3B", outline=INK, width=2)


def draw_japantobacco(d, x, y, w, h):
    """Japan Tobacco: cigarette pack + $8.9bn charge stamp."""
    d.rectangle([x, y, x + w, y + h], fill="#EFE0C0")
    d.rectangle([x + 24, y + 6, x + 104, y + h - 8], fill="#FFFFFF",
                outline=INK, width=2)
    d.rectangle([x + 24, y + 6, x + 104, y + 18], fill=RED2)
    d.text((x + 30, y + 8), "JT", font=F(SANS_B, 9), fill="#FFFFFF")
    for ly in (y + 24, y + 30):
        d.line([x + 32, ly, x + 96, ly], fill="#8A8A8A", width=2)
    d.rectangle([x + w - 120, y + 8, x + w - 16, y + 30], fill="#FFFFFF",
                outline=RED2, width=2)
    d.text((x + w - 114, y + 11), "$8.9bn", font=F(SANS_B, 13), fill=RED2)
    smoke_plume(d, x + w - 60, y + h - 22, 16, 20)


def draw_sudan(d, x, y, w, h):
    """Sudan: flag stripes, desert sun, defection arrow."""
    d.rectangle([x, y, x + w, y + h], fill="#FDE8C8")
    d.ellipse([x + w - 56, y + 4, x + w - 20, y + 40], fill="#FFD23F",
              outline="#E8A800", width=2)
    for i, c in enumerate(["#D52B1E", "#FFFFFF", "#1A1A1A", "#007A3D"]):
        d.rectangle([x + 16, y + 8 + i * 6, x + 96, y + 14 + i * 6],
                    fill=c, outline=INK, width=1)
    d.line([x + 110, y + 10, x + 150, y + 30], fill=RED2, width=4)
    d.polygon([(x + 150, y + 30), (x + 138, y + 22), (x + 138, y + 38)],
              fill=RED2)
    d.polygon([(x, y + h - 12), (x + w, y + h - 12), (x + w, y + h),
               (x, y + h)], fill="#C08A3E")


MAP_DOTS = {1: (320, 32), 2: (72, 48), 3: (88, 34), 4: (218, 28),
            5: (232, 48), 6: (312, 52), 7: (262, 22), 8: (272, 58),
            9: (244, 64), 10: (150, 12), 11: (336, 24), 12: (304, 44),
            13: (96, 88), 14: (284, 70), 15: (202, 74), 16: (318, 108),
            17: (248, 40), 18: (58, 38), 19: (348, 44), 20: (238, 82)}


def draw_map(d, x, y, w, h):
    """Simplified world map with numbered dots 1-20."""
    s = min(w / 380.0, h / 150.0)
    ox = x + (w - 380 * s) / 2
    oy = y + (h - 150 * s) / 2

    def P(pts):
        return [(ox + px * s, oy + py * s) for px, py in pts]

    d.rectangle([x, y, x + w, y + h], fill="#DCE7E0", outline=INK, width=2)
    land = "#8FAE7E"
    d.polygon(P([(18, 22), (92, 14), (108, 40), (78, 62), (40, 58),
                 (14, 42)]), fill=land, outline="#4E7A3E", width=2)
    d.polygon(P([(84, 78), (118, 74), (112, 112), (92, 128), (78, 96)]),
              fill=land, outline="#4E7A3E", width=2)
    d.polygon(P([(196, 18), (232, 12), (240, 34), (214, 46), (192, 36)]),
              fill=land, outline="#4E7A3E", width=2)
    d.polygon(P([(198, 56), (244, 52), (252, 92), (228, 118), (206, 96)]),
              fill=land, outline="#4E7A3E", width=2)
    d.polygon(P([(248, 14), (356, 10), (372, 44), (330, 66), (276, 60),
                 (250, 38)]), fill=land, outline="#4E7A3E", width=2)
    d.ellipse([ox + 330 * s, oy + 104 * s, ox + 372 * s, oy + 128 * s],
              fill=land, outline="#4E7A3E", width=2)
    dots = MAP_DOTS
    f = F(SANS_B, 10)
    r = max(6, int(8 * s))
    for n, (dx, dy) in dots.items():
        cx, cy = ox + dx * s, oy + dy * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED2,
                  outline="#FFFFFF", width=2)
        t = str(n)
        d.text((cx - d.textlength(t, font=f) / 2, cy - 7), t, font=f,
               fill="#FFFFFF")


# ---------------------------------------------------------------- page
def panel(d, x, y, w, h, img_h, n, tag, head, sub, fn, head_size=16):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    fn(d, x + 3, y + 3, w - 6, img_h)
    badge(d, x + w - 36, y + 6, n)
    f = F(SANS_B, 10)
    d.text((x + 10, y + img_h + 6), tag, font=f, fill=RED)
    f = F(SANS_B, head_size)
    lines = wrap(d, head, f, w - 20)[:2]
    yy = text_block(d, (x + 10, y + img_h + 20), lines, f, INK,
                    leading=int(head_size * 1.12))
    f = F(SANS, 11 if head_size >= 13 else 10)
    lines = wrap(d, sub, f, w - 20)[:2]
    text_block(d, (x + 10, yy + 1), lines, f, INK2, leading=int(f.size * 1.12))



# ---------------------------------------------------------------- template
FIGURE = {
    "summit": draw_summit, "gta": draw_gta, "anthropic": draw_anthropic,
    "icj": draw_icj, "cop31": draw_cop31, "kerch": draw_kerch,
    "greenland": draw_greenland, "nkorea": draw_nkorea,
    "venezuela": draw_venezuela, "senegal": draw_senegal,
    "riyadh": draw_riyadh, "hormuz": draw_hormuz, "gaza": draw_gaza,
    "sudan": draw_sudan, "cyclone": draw_cyclone,
    "bangladesh": draw_bangladesh, "redcrab": draw_redcrab,
    "gashusky": draw_gashusky, "trumpiran": draw_trumpiran,
    "japantobacco": draw_japantobacco,
}

# Fixed geometry per row: (y, w, h, img_h, x_step, head_size).
# Mid-row panels have fixed x positions (two flank the central map).
ROW_GEOM = {
    "hero": (178, 330, 180, 92, 338, 17),
    "row1": (364, 195, 118, 46, 203, 12),
    "row3": (670, 195, 118, 46, 203, 12),
    "row4": (794, 330, 118, 46, 339, 13),
}
MID_X = [8, 186, 668, 846]
MID_GEOM = (488, 170, 176, 88, 13)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f = F(SANS_B, 12)
    d.text((8, 8), PAGE["masthead_left"], font=f, fill=RED)
    d.text((W - 8 - d.textlength(PAGE["masthead_right"], font=f), 8),
           PAGE["masthead_right"], font=f, fill=INK2)
    f = F(SERIF_B, 44)
    d.text((8, 26), PAGE["date_title"], font=f, fill=INK)
    f = F(SERIF, 15)
    d.text((8, 78), PAGE["standfirst"], font=f, fill=RED)
    d.line([8, 102, 1016, 102], fill=INK, width=2)

    # ---- region bar ----
    regions = [(name, n, col) for (name, n), col in zip(
        PAGE["regions"],
        ["#C9D8B8", "#B9CDE0", "#E8D5A8", "#E3C9C2",
         "#D8C9A8", "#CFCFCF", "#D8D8E8"])]
    x = 8
    seg_w = (W - 16) // len(regions)
    f = F(SANS_B, 13)
    for name, n, col in regions:
        d.rectangle([x, 108, x + seg_w - 4, 130], fill=col, outline=INK,
                    width=1)
        t = f"{name} {n}"
        d.text((x + (seg_w - 4 - d.textlength(t, font=f)) / 2, 114), t,
               font=f, fill=INK)
        x += seg_w

    # ---- numbers strip ----
    f = F(SANS_B, 11)
    d.text((8, 136), PAGE["numbers_title"], font=f, fill=RED)
    nx = 8
    bw = (W - 16) // 6
    for v, lbl in PAGE["numbers"]:
        d.rectangle([nx, 152, nx + bw - 6, 166], fill="#FFFFFF",
                    outline=INK, width=1)
        d.text((nx + 6, 154), v, font=F(SANS_B, 12), fill=RED2)
        d.text((nx + 6 + d.textlength(v, font=F(SANS_B, 12)) + 5, 155),
               lbl, font=F(SANS, 10), fill=INK)
        nx += bw
    d.line([8, 172, 1016, 172], fill=INK, width=1)

    # ---- story rows (geometry fixed, content from STORIES) ----
    by_row = {}
    for s in STORIES:
        by_row.setdefault(s["row"], []).append(s)

    def draw_row(row, geom):
        y, w, h, img_h, step, hs = geom
        placed = []
        xx = 8
        for s in by_row.get(row, []):
            panel(d, xx, y, w, h, img_h, s["n"], s["tag"],
                  s["headline"], s["sub"], FIGURE[s["figure"]],
                  head_size=hs)
            placed.append((s["n"], xx, y, w, h))
            xx += step
        return placed

    draw_row("hero", ROW_GEOM["hero"])
    row1_xy = draw_row("row1", ROW_GEOM["row1"])

    # ---- middle band: central map + 4 tall flank panels ----
    my, mw, mh, mimg, mhs = MID_GEOM
    mid_xy = []
    for i, s in enumerate(by_row.get("mid", [])):
        mx = MID_X[i]
        panel(d, mx, my, mw, mh, mimg, s["n"], s["tag"], s["headline"],
              s["sub"], FIGURE[s["figure"]], head_size=mhs)
        mid_xy.append((s["n"], mx, my, mw, mh))

    draw_map(d, 360, 488, 304, 176)
    f = F(SANS_B, 11)
    d.text((368, 644), "WHERE IT HAPPENED", font=f, fill=INK)

    row3_xy = draw_row("row3", ROW_GEOM["row3"])
    draw_row("row4", ROW_GEOM["row4"])

    # ---- leader lines: map dot -> nearest edge of its panel ----
    ms = min(304 / 380.0, 176 / 150.0)
    mox, moy = 360, 488 + (176 - 150 * ms) / 2
    dots_px = {n: (mox + dx * ms, moy + dy * ms)
               for n, (dx, dy) in MAP_DOTS.items()}
    edges = {}
    for n, px, py, pw, ph in row1_xy:
        edges[n] = (px + pw // 2, py + ph)
    for n, px, py, pw, ph in mid_xy:
        edges[n] = (px + pw, py + ph // 2) if px < 360 else (px, py + ph // 2)
    for n, px, py, pw, ph in row3_xy:
        edges[n] = (px + pw // 2, py)
    for n, (dx, dy) in dots_px.items():
        if n in edges:
            ex, ey = edges[n]
            ux, uy = ex - dx, ey - dy
            ln = math.hypot(ux, uy) or 1.0
            sx, sy = dx + 10 * ux / ln, dy + 10 * uy / ln
            d.line([sx, sy, ex, ey], fill="#8A8A8A", width=1)
        else:
            d.line([dx, dy, dx, 664], fill="#8A8A8A", width=1)

    # ---- also (text-only stories) ----
    f = F(SANS, 11)
    d.text((8, 918), PAGE["also"], font=f, fill="#222222")

    # ---- date check ----
    d.rectangle([8, 934, 1016, 972], outline=RED2, width=3, fill="#FDECEC")
    f = F(SANS_B, 12)
    d.text((20, 939), "DATE CHECK — NOT %s NEWS:" % PAGE["date_short"],
           font=f, fill=RED2)
    f = F(SANS, 12)
    d.text((20, 954), PAGE["date_check"], font=f, fill=INK2)

    # ---- footer ----
    f = F(SANS, 11)
    d.text((8, 980), PAGE["sources"], font=f, fill="#555555")
    d.text((W - 8 - d.textlength(PAGE["credit"], font=f), 980),
           PAGE["credit"], font=f, fill="#555555")

    img.save(out, "PNG", optimize=True)
    print("saved", out, img.size)


if __name__ == "__main__":
    main()
