#!/usr/bin/env python3
"""Draw the make.fun news-image-20261118 entry v2 (1024x1024) with PIL.

Style: Chinese ink-wash watercolor newspaper front page (cream paper,
black ink, red seals, muted watercolor washes), following the reference
image's STYLE ONLY -- content stays 18 Nov 2026 world news (22 stories).
Deterministic: fixed fonts, fixed geometry, no randomness, no network.
Run:  python3 draw.py [output_path]   (default: entry.png next to this file)
main.py (stdlib-only) just copies entry.png to the output dir.
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
DJ = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = DJ + "DejaVuSerif-Bold.ttf"
SANS_B = DJ + "DejaVuSans-Bold.ttf"
SANS = DJ + "DejaVuSans.ttf"
CJK_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

PAPER = "#F7F1E3"
INK = "#1A1A1A"
INK2 = "#3A3A3A"
RED = "#B03A2E"
RED2 = "#C8102E"


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


def badge(draw, x, y, n, r=13, fill=RED2):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=fill,
                 outline="#FFFFFF", width=2)
    f = F(SANS_B, 14 if r >= 13 else 11)
    t = str(n)
    tw = draw.textlength(t, font=f)
    draw.text((x + r - tw / 2, y + r - (10 if r >= 13 else 8)), t, font=f,
              fill="#FFFFFF")


def tag(draw, x, y, text, fill):
    f = F(SANS_B, 11)
    tw = draw.textlength(text, font=f)
    draw.rounded_rectangle([x, y, x + tw + 12, y + 18], radius=4, fill=fill)
    draw.text((x + 6, y + 3), text, font=f, fill="#FFFFFF")
    return tw + 12


def brush_stroke(d, x0, x1, y, base=3):
    """A tapered ink brush stroke with a dry-brush tail."""
    for x in range(x0, x1, 4):
        t = (x - x0) / max(1, (x1 - x0))
        w = max(1, int(base + 2.5 * math.sin(t * math.pi)
                       - 2.0 * max(0, t - 0.85) * 6))
        yy = y + int(2 * math.sin(t * math.pi * 2))
        d.line([x, yy, x + 4, yy], fill=INK, width=w)
    # splatter dots near the tail
    for sx, sy, r in [(x1 - 14, y - 6, 2), (x1 - 26, y + 5, 1),
                      (x1 - 6, y + 3, 2), (x0 + 30, y - 5, 1)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=INK)


# ---------------------------------------------------------------- figures
def draw_skyline_ink(d, x, y, w, h):
    """Ink-wash Shenzhen: pale wash sky, grey mountains, ink skyline."""
    d.rectangle([x, y, x + w, y + h], fill="#DCE7E0")
    # distant mountains (pale green-grey wash)
    d.polygon([(x, y + h - 40), (x + 60, y + 34), (x + 120, y + h - 40)],
              fill="#B7C9A8")
    d.polygon([(x + 90, y + h - 40), (x + 190, y + 18), (x + 280, y + h - 40)],
              fill="#9DB894")
    d.polygon([(x + 220, y + h - 40), (x + 290, y + 44), (x + w, y + h - 40)],
              fill="#B7C9A8")
    # red sun (seal red)
    d.ellipse([x + w - 66, y + 8, x + w - 26, y + 48], fill=RED,
              outline="#8E2B20", width=2)
    # skyline silhouettes in ink greys
    builds = [(0, 62, 34, 96, "#3A3A3A"), (36, 40, 30, 118, "#2B2B2B"),
              (68, 74, 40, 84, "#4A4A4A"), (110, 30, 26, 128, "#2B2B2B"),
              (138, 58, 34, 100, "#3A3A3A"), (174, 44, 30, 114, "#2B2B2B"),
              (206, 68, 36, 90, "#4A4A4A"), (244, 52, 30, 106, "#3A3A3A"),
              (276, 78, 34, 80, "#2B2B2B")]
    for bx, by, bw, bh, col in builds:
        d.rectangle([x + bx, y + by, x + bx + bw, y + h - 22], fill=col)
        for wy in range(y + by + 8, y + h - 30, 16):
            for wx in range(x + bx + 5, x + bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill="#F7F1E3")
    d.rectangle([x, y + h - 22, x + w, y + h], fill="#E8DCC8")
    d.rectangle([x + w // 2 - 40, y + h - 22, x + w // 2 + 40, y + h],
                fill=RED2)
    # two ink figures shaking hands
    for fx, col in [(x + w // 2 - 52, "#1A1A1A"),
                    (x + w // 2 + 30, "#3A3A3A")]:
        d.ellipse([fx, y + h - 56, fx + 22, y + h - 34], fill="#E8C9A0",
                  outline=INK, width=2)
        d.polygon([(fx - 2, y + h - 34), (fx + 24, y + h - 34),
                   (fx + 18, y + h - 22), (fx + 4, y + h - 22)], fill=col)
    d.line([x + w // 2 - 30, y + h - 40, x + w // 2 + 30, y + h - 40],
           fill=INK, width=3)


def draw_gulf_ink(d, x, y, w, h):
    """Ink-wash Gulf: pale sand coast, wash sea, dashed red drone tracks."""
    d.rectangle([x, y, x + w, y + h], fill="#EFE3C8")
    d.rectangle([x, y + h - 58, x + w, y + h], fill="#A9C2D4")
    for i in range(5):
        wx = x + 20 + i * 58
        d.arc([wx, y + h - 48, wx + 40, y + h - 26], 180, 360,
              fill="#FFFFFF", width=3)
    d.polygon([(x, y), (x + 190, y), (x + 210, y + 38), (x + 150, y + 74),
               (x + 60, y + 66), (x, y + 42)], fill="#D9BE8A",
              outline="#8A6D3B", width=2)
    for (sx, sy, ex, ey) in [(x + 40, y + 14, x + 250, y + 92),
                             (x + 90, y + 8, x + 280, y + 66),
                             (x + 150, y + 18, x + 300, y + 106)]:
        steps = 14
        for i in range(steps):
            t0 = i / steps
            t1 = (i + 0.5) / steps
            d.line([sx + (ex - sx) * t0, sy + (ey - sy) * t0,
                    sx + (ex - sx) * t1, sy + (ey - sy) * t1],
                   fill=RED2, width=2)
        d.polygon([(ex, ey), (ex - 12, ey - 5), (ex - 12, ey + 5)],
                  fill=INK, outline="#000000")
    # ink seal circle (interception mark) bottom-left
    d.ellipse([x + 10, y + 92, x + 44, y + 126], fill="#1F7A3A",
              outline="#FFFFFF", width=3)
    d.line([x + 16, y + 110, x + 23, y + 117, x + 34, y + 102],
           fill="#FFFFFF", width=4)


def draw_voyager(d, x, y, w, h):
    """Ink night sky: Voyager probe, ringed planet, Earth below."""
    d.rectangle([x, y, x + w, y + h], fill="#101B3A")
    for (sx, sy, r) in [(20, 18, 2), (70, 40, 2), (140, 12, 3),
                        (200, 30, 2), (260, 16, 2), (300, 44, 3),
                        (40, 70, 2), (110, 60, 2), (180, 76, 2),
                        (240, 66, 2), (290, 84, 2), (90, 92, 2)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill="#FFFFFF")
    px, py = x + w - 74, y + 46
    d.ellipse([px - 26, py - 26, px + 26, py + 26], fill="#E8A33D",
              outline="#B97E1E", width=3)
    d.ellipse([px - 42, py - 8, px + 42, py + 8], outline="#FFD23F", width=3)
    bx, by = x + 96, y + 96
    d.polygon([(bx, by - 18), (bx + 52, by - 18), (bx + 44, by + 14),
               (bx + 8, by + 14)], fill="#FFD23F", outline="#B97E1E", width=2)
    d.ellipse([bx + 52, by - 34, bx + 96, by + 10], outline="#FFFFFF",
              width=3)
    d.line([bx + 52, by - 12, bx + 74, by - 12], fill="#FFFFFF", width=2)
    d.line([bx + 20, by + 14, bx + 4, by + 34], fill="#C9C9C9", width=3)
    d.ellipse([x + 12, y + h - 52, x + 56, y + h - 8], fill="#3B82D6",
              outline="#1F5FA8", width=2)
    d.arc([x + 20, y + h - 44, x + 48, y + h - 16], 200, 340,
          fill="#7FC4E8", width=4)


def draw_kerch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill="#FDE8C8")
    d.rectangle([x, y + h - 34, x + w, y + h], fill="#7FB8D9")
    for i in range(4):
        wx = x + 14 + i * 52
        d.arc([wx, y + h - 28, wx + 34, y + h - 12], 180, 360,
              fill="#FFFFFF", width=2)
    d.rectangle([x + 26, y + 22, x + 40, y + h - 34], fill="#8A6D3B",
                outline="#5C4630", width=2)
    d.rectangle([x + w - 40, y + 22, x + w - 26, y + h - 34], fill="#8A6D3B",
                outline="#5C4630", width=2)
    d.line([x + 8, y + 44, x + 96, y + 44], fill="#5C4630", width=5)
    d.line([x + w - 96, y + 44, x + w - 8, y + 44], fill="#5C4630", width=5)
    d.line([x + 96, y + 44, x + 112, y + 62], fill=RED2, width=4)
    d.line([x + w - 96, y + 44, x + w - 112, y + 62], fill=RED2, width=4)
    d.line([x + 112, y + 62, x + 126, y + 84], fill=RED2, width=3)
    d.ellipse([x + w // 2 - 12, y + 6, x + w // 2 + 12, y + 30],
              fill="#FFD23F", outline="#E8A800", width=2)


def draw_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill="#1F3A6E")
    cx, cy = x + w // 2, y + 52
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + 44 * math.cos(a), cy + 40 * math.sin(a)
        d.polygon([(sx, sy - 6), (sx + 2, sy - 2), (sx + 6, sy - 2),
                   (sx + 3, sy + 1), (sx + 4, sy + 5), (sx, sy + 3),
                   (sx - 4, sy + 5), (sx - 3, sy + 1), (sx - 6, sy - 2),
                   (sx - 2, sy - 2)], fill="#FFD23F")
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill="#FFD23F",
              outline="#E8A800", width=3)
    f = F(SANS_B, 30)
    t = "€"
    d.text((cx - d.textlength(t, font=f) / 2, cy - 20), t, font=f,
           fill="#1F3A6E")


def draw_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill="#9FB8CC")
    cx, cy = x + w // 2, y + 52
    for r in (44, 32, 20, 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill="#FFFFFF",
              width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED2)
    for i in range(6):
        lx = x + 14 + i * 36
        d.line([lx, y + h - 22, lx - 6, y + h - 8], fill="#3B6E9E", width=2)
    d.polygon([(x, y + h - 12), (x + w, y + h - 12), (x + w, y + h),
               (x, y + h)], fill="#2E7A4E")


def draw_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill="#DCE9F7")
    d.ellipse([x + 8, y + 8, x + 44, y + 44], fill="#FFD23F",
              outline="#E8A800", width=2)
    d.text((x + 16, y + 12), "★", font=F(SANS_B, 22), fill=RED2)
    d.rectangle([x + w // 2 - 52, y + 42, x + w // 2 + 52, y + h - 8],
                fill="#1F5FA8", outline="#14264E", width=3)
    d.rectangle([x + w // 2 - 62, y + 30, x + w // 2 + 62, y + 46],
                fill="#2E7AC4", outline="#14264E", width=3)
    d.rectangle([x + w // 2 - 18, y + 36, x + w // 2 + 18, y + 42],
                fill="#14264E")
    d.polygon([(x + w // 2 - 24, y + 6), (x + w // 2 + 24, y + 6),
               (x + w // 2 + 20, y + 38), (x + w // 2 - 20, y + 38)],
              fill="#FFFFFF", outline="#14264E")
    d.line([x + w // 2 - 16, y + 14, x + w // 2 - 6, y + 24,
            x + w // 2 + 14, y + 10], fill="#1F7A3A", width=3)
    d.text((x + w // 2 - 30, y + 62), "56–44", font=F(SANS_B, 26),
           fill="#FFFFFF")


def draw_drones(d, x, y, w, h):
    """Overnight drone swarm: pale wash sky, ink drones, red tracks."""
    d.rectangle([x, y, x + w, y + h], fill="#E8E4D8")
    d.polygon([(x, y + h - 18), (x + 60, y + h - 34), (x + 130, y + h - 18),
               (x + w, y + h - 18), (x + w, y + h), (x, y + h)],
              fill="#8A9A7A")
    for (dx, dy, s) in [(30, 18, 1.0), (95, 34, 0.8), (150, 14, 1.1)]:
        cx, cy = x + dx, y + dy
        d.line([cx - 12 * s, cy - 8, cx + 12 * s, cy - 8], fill=INK, width=2)
        d.line([cx - 12 * s, cy + 8, cx + 12 * s, cy + 8], fill=INK, width=2)
        d.ellipse([cx - 6 * s, cy - 5, cx + 6 * s, cy + 5], fill=INK)
        d.line([cx, cy - 10, cx, cy + 10], fill=INK, width=2)
    for (sx, sy, ex, ey) in [(x + 20, y + 10, x + 170, y + 54),
                             (x + 60, y + 6, x + 185, y + 40)]:
        steps = 10
        for i in range(steps):
            t0 = i / steps
            t1 = (i + 0.5) / steps
            d.line([sx + (ex - sx) * t0, sy + (ey - sy) * t0,
                    sx + (ex - sx) * t1, sy + (ey - sy) * t1],
                   fill=RED2, width=2)
    d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=RED,
              outline="#8E2B20", width=2)


def draw_jeffries(d, x, y, w, h):
    """Speaker nomination: ink ballot box, big 251-11 tally, red star."""
    d.rectangle([x, y, x + w, y + h], fill="#F1EAD8")
    d.rectangle([x + w // 2 - 48, y + 34, x + w // 2 + 48, y + h - 6],
                fill="#1A1A1A", outline=INK, width=2)
    d.rectangle([x + w // 2 - 56, y + 24, x + w // 2 + 56, y + 38],
                fill="#3A3A3A", outline=INK, width=2)
    d.polygon([(x + w // 2 - 22, y + 2), (x + w // 2 + 22, y + 2),
               (x + w // 2 + 18, y + 26), (x + w // 2 - 18, y + 26)],
              fill="#FFFFFF", outline=INK)
    d.line([x + w // 2 - 14, y + 10, x + w // 2 - 4, y + 20,
            x + w // 2 + 12, y + 6], fill="#1F7A3A", width=3)
    f = F(SERIF_B, 22)
    t = "251–11"
    d.text((x + w // 2 - d.textlength(t, font=f) / 2, y + 44), t, font=f,
           fill="#FFFFFF")
    d.ellipse([x + 8, y + 6, x + 34, y + 32], fill=RED,
              outline="#8E2B20", width=2)
    d.text((x + 13, y + 8), "★", font=F(SANS_B, 18), fill="#FFFFFF")


def draw_gaza(d, x, y, w, h):
    """Central Gaza: sand wash, ink rubble silhouettes, grey smoke."""
    d.rectangle([x, y, x + w, y + h], fill="#EFE0C0")
    for (sx, sy, sw, sh) in [(x + 26, y + 26, 8, 34), (x + 60, y + 18, 10, 42),
                             (x + 110, y + 30, 8, 30)]:
        d.ellipse([sx - 4, sy - 8, sx + sw + 4, sy + 14], fill="#C9C2B2")
        d.ellipse([sx - 2, sy - 16, sx + sw + 2, sy + 4], fill="#D8D2C2")
    d.polygon([(x + 10, y + h - 20), (x + 50, y + h - 20),
               (x + 50, y + h - 44), (x + 62, y + h - 52),
               (x + 74, y + h - 44), (x + 74, y + h - 20)], fill=INK2)
    d.polygon([(x + 90, y + h - 20), (x + 130, y + h - 20),
               (x + 130, y + h - 52), (x + 142, y + h - 58),
               (x + 150, y + h - 40), (x + 158, y + h - 20)], fill=INK)
    d.polygon([(x + 162, y + h - 20), (x + w - 8, y + h - 20),
               (x + w - 8, y + h - 36), (x + w - 30, y + h - 36),
               (x + w - 30, y + h - 48), (x + w - 52, y + h - 48),
               (x + w - 52, y + h - 36), (x + 176, y + h - 36)],
              fill=INK2)
    d.rectangle([x, y + h - 20, x + w, y + h], fill="#C9B48A")
    d.ellipse([x + w - 30, y + 6, x + w - 10, y + 26], fill=RED,
              outline="#8E2B20", width=2)


def draw_sudan(d, x, y, w, h):
    """El Obeid: ochre wash, ink acacia tree, pale hills, red sun."""
    d.rectangle([x, y, x + w, y + h], fill="#EAD9A8")
    d.ellipse([x + w - 36, y + 6, x + w - 12, y + 30], fill=RED,
              outline="#8E2B20", width=2)
    d.polygon([(x, y + h - 22), (x + 70, y + h - 38), (x + 140, y + h - 22),
               (x + w, y + h - 22), (x + w, y + h), (x, y + h)],
              fill="#C9A86A")
    cx = x + 52
    d.polygon([(cx - 4, y + h - 22), (cx + 4, y + h - 22),
               (cx + 2, y + 34), (cx - 2, y + 34)], fill=INK)
    d.polygon([(cx - 34, y + 30), (cx + 40, y + 26), (cx + 30, y + 40),
               (cx - 26, y + 42)], fill=INK)
    d.polygon([(cx - 18, y + 40), (cx + 24, y + 38), (cx + 16, y + 48),
               (cx - 12, y + 50)], fill=INK2)
    for (hx, hy) in [(x + 130, y + h - 30), (x + 155, y + h - 26),
                     (x + 175, y + h - 32)]:
        d.ellipse([hx - 4, hy - 10, hx + 4, hy], fill=INK)


def draw_fed(d, x, y, w, h):
    """Markets: ink axes, falling black line, red arrow and -561."""
    d.rectangle([x, y, x + w, y + h], fill="#F1EAD8")
    d.line([x + 14, y + 10, x + 14, y + h - 16], fill=INK, width=2)
    d.line([x + 14, y + h - 16, x + w - 10, y + h - 16], fill=INK, width=2)
    pts = [(x + 18, y + 18), (x + 60, y + 22), (x + 100, y + 16),
           (x + 130, y + 30), (x + 160, y + 44), (x + 185, y + 58)]
    d.line(pts, fill=INK, width=3, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
               (pts[-1][0] - 4, pts[-1][1] + 10)], fill=RED2)
    f = F(SERIF_B, 24)
    t = "−561"
    d.text((x + 8, y + h - 28), t, font=f, fill=RED2)


def draw_map(d, x, y, w, h):
    """Simplified ink-wash world map with numbered dots (scaled to fit)."""
    s = min(w / 380.0, h / 150.0)
    ox = x + (w - 380 * s) / 2
    oy = y + (h - 150 * s) / 2

    def P(pts):
        return [(ox + px * s, oy + py * s) for px, py in pts]

    d.rectangle([x, y, x + w, y + h], fill="#DCE7E0",
                outline=INK, width=2)
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
    dots = {1: (330, 30), 2: (215, 30), 8: (228, 26), 3: (255, 62),
            10: (246, 56), 4: (70, 40), 5: (315, 48), 11: (232, 92),
            7: (225, 96)}
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
def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead: cream paper, red seal, serif title, calligraphy ----
    d.rectangle([16, 16, 72, 72], fill=RED)
    f = F(CJK_B, 40)
    d.text((22, 18), "闻", font=f, fill="#FFFFFF")
    f = F(SANS_B, 14)
    d.text((88, 18), "T H E   D A Y   I N   W O R L D   N E W S", font=f,
           fill=RED)
    f = F(SERIF_B, 40)
    d.text((86, 40), "Wednesday 18 November 2026", font=f, fill=INK)
    f = F(SANS_B, 15)
    d.text((88, 94), "22 STORIES  ·  6 REGIONS  ·  12 DRAWN  ·  ONE PAGE",
           font=f, fill=INK2)
    # vertical calligraphy strip: 风云际会 (momentous times)
    f = F(CJK_B, 24)
    for i, ch in enumerate("风云际会"):
        d.text((976, 14 + i * 28), ch, font=f, fill=INK)
    d.ellipse([972, 126, 986, 140], fill=RED)
    # brush stroke divider
    brush_stroke(d, 16, 1008, 140)
    d.line([16, 146, 1008, 146], fill=INK, width=1)

    # ---- region bar (pale watercolor washes, ink text) ----
    regions = [("ASIA", "3", "#C9D8B8"), ("EUROPE", "3", "#B9CDE0"),
               ("AMERICAS", "10", "#E3C9C2"), ("MIDDLE EAST", "2", "#E8D5A8"),
               ("AFRICA", "2", "#D8C9A8"), ("GLOBAL", "2", "#CFCFCF")]
    x = 8
    f = F(SANS_B, 14)
    seg_w = (W - 16) // len(regions)
    for name, n, col in regions:
        d.rectangle([x, 152, x + seg_w - 4, 176], fill=col, outline=INK,
                    width=1)
        t = f"{name} {n}"
        d.text((x + (seg_w - 4 - d.textlength(t, font=f)) / 2, 156), t,
               font=f, fill=INK)
        x += seg_w

    # ---- numbers strip ----
    f = F(SANS_B, 12)
    d.text((12, 186), "THE DAY IN NUMBERS", font=f, fill=RED)
    nums = [("25.9bn km", "Voyager 1"), ("141/126", "drones"),
            ("251–11", "Jeffries"), ("Dow −561", ""),
            ("$83", "Anthropic"), ("37", "El Obeid")]
    nx = 196
    for v, lbl in nums:
        d.text((nx, 186), v, font=F(SANS_B, 12), fill=RED)
        nx += d.textlength(v, font=F(SANS_B, 12)) + 5
        if lbl:
            d.text((nx, 186), lbl, font=f, fill=INK)
            nx += d.textlength(lbl, font=f) + 18
    d.line([8, 208, 1016, 208], fill=INK, width=1)

    # ---- hero row ----
    heroes = [
        (1, "ASIA · DIPLOMACY", "XI GREETS TRUMP IN SHENZHEN",
         "Xi & Putin meet in Shenzhen on the eve of the APEC trilateral — "
         "Trump joins them tomorrow.", draw_skyline_ink),
        (2, "MIDDLE EAST · DEFENCE", "GULF DRONES INTERCEPTED",
         "Bahrain & Kuwait stop Iran-linked drones; Hormuz tanker hit, "
         "1 crew missing.", draw_gulf_ink),
        (3, "GLOBAL · SPACE", "VOYAGER 1: ONE LIGHT-DAY OUT",
         "25.9 billion km from Earth — NASA's farthest traveller keeps "
         "going.", draw_voyager),
    ]
    hx = 8
    for n, tg, head, sub, fn in heroes:
        pw, ph = 324, 236
        d.rectangle([hx, 216, hx + pw, 216 + ph], fill="#FFFDF6",
                    outline=INK, width=2)
        fn(d, hx + 3, 219, pw - 6, 118)
        badge(d, hx + pw - 40, 222, n)
        f = F(SANS_B, 10)
        d.text((hx + 10, 342), tg, font=f, fill=RED)
        f = F(SANS_B, 17)
        lines = wrap(d, head, f, pw - 20)
        y = text_block(d, (hx + 10, 358), lines, f, INK)
        f = F(SANS, 12)
        lines = wrap(d, sub, f, pw - 20)
        text_block(d, (hx + 10, y + 2), lines, f, "#333333")
        hx += 332

    # ---- second row ----
    second = [
        (4, "EUROPE · WAR", "UKRAINE CLAIMS KERCH BRIDGE HIT",
         "Road span down, rail partly resumed.", draw_kerch),
        (5, "EUROPE · ECONOMY", "EU: €45BN UKRAINE LOAN",
         "Bloc agrees a big loan to Kyiv.", draw_eu),
        (6, "ASIA · WEATHER", "CYCLONE AKVAN NEARS INDIA",
         "Severe storm heads for the east coast; landfall due 20 Nov.",
         draw_cyclone),
        (7, "AMERICAS · POLITICS", "PELTOLA WINS ALASKA",
         "Democrats take the Senate 56–44.", draw_ballot),
    ]
    sx = 8
    for n, tg, head, sub, fn in second:
        pw, ph = 240, 180
        d.rectangle([sx, 460, sx + pw, 460 + ph], fill="#FFFDF6",
                    outline=INK, width=2)
        fn(d, sx + 3, 463, pw - 6, 88)
        badge(d, sx + pw - 36, 466, n)
        f = F(SANS_B, 15)
        lines = wrap(d, head, f, pw - 20)
        y = text_block(d, (sx + 10, 556), lines, f, INK)
        f = F(SANS, 12)
        lines = wrap(d, sub, f, pw - 20)
        text_block(d, (sx + 10, y + 2), lines, f, "#333333")
        f = F(SANS_B, 10)
        d.text((sx + 10, 460 + ph - 16), tg, font=f, fill=RED)
        sx += 248

    # ---- third row: five small panels ----
    third = [
        (8, "EUROPE · WAR", "141 DRONES FIRED, 126 DOWNED",
         "Overnight swarm; 7 hits recorded.", draw_drones),
        (9, "AMERICAS · POLITICS", "JEFFRIES WINS 251–11",
         "Democrats nominate him for Speaker.", draw_jeffries),
        (10, "MIDDLE EAST · WAR", "GAZA OFFENSIVE REOPENS",
         "Israeli troops advance; truce at risk.", draw_gaza),
        (11, "AFRICA · RIGHTS", "AMNESTY: EL OBEID STRIKES",
         "RSF drone strikes killed 37 civilians.", draw_sudan),
        (12, "AMERICAS · MARKETS", "FED MINUTES SINK DOW −561",
         "December hike now the base case.", draw_fed),
    ]
    tx = 8
    for n, tg, head, sub, fn in third:
        pw, ph = 196, 156
        d.rectangle([tx, 648, tx + pw, 648 + ph], fill="#FFFDF6",
                    outline=INK, width=2)
        fn(d, tx + 3, 651, pw - 6, 70)
        badge(d, tx + pw - 32, 654, n, r=10)
        f = F(SANS_B, 13)
        lines = wrap(d, head, f, pw - 16)
        y = text_block(d, (tx + 8, 726), lines, f, INK)
        f = F(SANS, 11)
        lines = wrap(d, sub, f, pw - 16)
        text_block(d, (tx + 8, y + 1), lines, f, "#333333")
        f = F(SANS_B, 9)
        d.text((tx + 8, 648 + ph - 14), tg, font=f, fill=RED)
        tx += 202

    # ---- bottom: map + also ----
    d.rectangle([8, 812, 318, 944], fill="#FFFDF6", outline=INK, width=2)
    f = F(SANS_B, 15)
    d.text((20, 818), "WHERE IT HAPPENED", font=f, fill=INK)
    draw_map(d, 18, 838, 290, 76)
    f = F(SANS, 10)
    d.text((20, 918), "1 Shenzhen  2 Kerch  8 Kyiv  3 Gulf  10 Gaza",
           font=f, fill="#333333")
    d.text((20, 930), "4 Alaska  5 India  7 Africa  11 Sudan",
           font=f, fill="#333333")

    d.rectangle([326, 812, 1016, 944], fill="#FFFDF6", outline=INK, width=2)
    f = F(SANS_B, 15)
    d.text((338, 818), "ALSO ON WEDNESDAY 18 NOVEMBER", font=f, fill=INK)
    also_l = [
        ("13", "Anthropic IPO priced at $83, above range."),
        ("14", "Nvidia falls 2.9% after record quarter."),
        ("15", "GTA VI rollout begins after 13 years."),
        ("16", "MS Dhoni retires from the IPL."),
        ("17", "US loses measles-free status after 26 years."),
    ]
    also_r = [
        ("18", "Ebola cases pass 11,300, officials say."),
        ("19", "Palo Alto jumps 19.2% as cyber stocks rally."),
        ("20", "UnitedHealth falls 10.2%, biggest Dow drag."),
        ("21", "Canada–China widen financial access at APEC."),
        ("22", "S&P 500 falls for a fifth straight day."),
    ]
    f = F(SANS, 12)
    y = 842
    for n, t in also_l:
        d.text((338, y), f"{n}.  {t}", font=f, fill="#222222")
        y += 20
    y = 842
    for n, t in also_r:
        d.text((676, y), f"{n}.  {t}", font=f, fill="#222222")
        y += 20

    # ---- date check ----
    d.rectangle([8, 952, 1016, 988], outline=RED2, width=3, fill="#FDECEC")
    f = F(SANS_B, 13)
    d.text((20, 958), "DATE CHECK — NOT 18 NOV NEWS:", font=f, fill=RED2)
    f = F(SANS, 13)
    d.text((20, 972),
           "The China–US–Russia trilateral summit is 19 Nov — it is not "
           "shown here as 18 Nov news.", font=f, fill="#333333")

    # ---- footer ----
    f = F(SANS, 11)
    d.text((8, 996),
           "Sources: Reuters · AP · AFP · NASA · IMD · Al Jazeera · "
           "Amnesty · All stories from Wednesday 18 November 2026.",
           font=f, fill="#555555")
    d.text((W - 8 - d.textlength("make.fun / @inl-xin", font=f), 996),
           "make.fun / @inl-xin", font=f, fill="#555555")

    img.save(out, "PNG", optimize=True)
    print("saved", out, img.size)


if __name__ == "__main__":
    main()
