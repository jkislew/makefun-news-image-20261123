#!/usr/bin/env python3
"""The World Today — Monday 23 November 2026.

A deterministic newspaper front page that sums up Monday 23 November
2026's world news in one 1024x1024 image. Drawn entirely with PIL:
no network, no timestamps, no randomness — two runs write identical bytes.

Lead story: the COP31 climate talks in Antalya collapse with no deal and
no mention of fossil fuels in the final draft. Six more stories fill the
front page: the Iran-US war spreading across the Gulf to Bahrain and
Saudi Arabia; a Russian cargo ship ablaze off Finland; a Russian drone
strike on a residential building in the Kyiv region; a factory fire in
Indonesia with dozens missing; a Delta Air Lines system outage grounding
Thanksgiving travel; and the International Court of Justice ruling that
Myanmar committed genocide against the Rohingya.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34

PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (178, 34, 27)
TEAL = (15, 95, 92)
GOLD = (176, 124, 12)
GREY = (96, 92, 84)
WHITE = (255, 255, 255)
SKY = (214, 231, 228)
FLAME = (224, 110, 30)
SMOKE = (120, 118, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def draw_spaced(draw, y, text, fnt, fill, spacing=3):
    """Draw text with extra letter spacing, centred."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


def rule(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def masthead(draw):
    rule(draw, 30, MARGIN, W - MARGIN, 3)
    draw_centered(draw, 40, "THE WORLD TODAY",
                  font(SERIF, 62), INK)
    draw_spaced(draw, 118, "ONE DAY  ·  ONE PICTURE  ·  SEVEN STORIES",
                font(SANS_BOLD, 13), GREY, spacing=2)
    rule(draw, 144, MARGIN, W - MARGIN, 2)
    draw_centered(draw, 154, "MONDAY 23 NOVEMBER 2026",
                  font(SANS_BOLD, 30), RED)
    rule(draw, 192, MARGIN, W - MARGIN, 3, RED)


# ---------------------------------------------------------------- scenes
def scene_globe(draw, x0, y0, x1, y1):
    """Lead art: a cracked globe over smokestacks — the talks collapse."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2 - 10
    r = 105
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL,
                 outline=INK, width=3)
    # landmasses: flat gold blobs
    draw.ellipse([cx - 78, cy - 62, cx - 8, cy - 6], fill=GOLD)
    draw.ellipse([cx + 12, cy + 8, cx + 72, cy + 66], fill=GOLD)
    draw.ellipse([cx - 30, cy + 42, cx + 18, cy + 82], fill=(46, 125, 90))
    draw.ellipse([cx + 38, cy - 78, cx + 88, cy - 34], fill=(46, 125, 90))
    # the crack: jagged red line splitting the globe
    crack = [(cx - 52, cy - 96), (cx - 30, cy - 48), (cx - 58, cy - 6),
             (cx - 22, cy + 34), (cx - 44, cy + 70), (cx - 18, cy + 100)]
    draw.line(crack, fill=RED, width=7, joint="curve")
    # smokestacks and smoke at the base
    base = y1 - 34
    for sx in (x0 + 30, x0 + 78, x0 + 126):
        draw.rectangle([sx, base - 46, sx + 26, base], fill=INK)
        draw.ellipse([sx - 8, base - 78, sx + 14, base - 56], fill=SMOKE)
        draw.ellipse([sx + 6, base - 92, sx + 34, base - 66], fill=SMOKE)
    draw.rectangle([x0, base, x1, y1], fill=INK)
    draw.text((x0 + 14, y1 - 30), "ANTALYA — NO DEAL",
              font=font(SANS_BOLD, 13), fill=WHITE)


def scene_hormuz(draw, x0, y0, x1, y1):
    """Missile arcs over a Gulf sea."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 222, 190))
    sea = y0 + (y1 - y0) * 2 // 3
    draw.rectangle([x0, sea, x1, y1], fill=TEAL)
    draw.line([(x0 + 8, sea + 6), (x1 - 8, sea + 6)], fill=WHITE, width=2)
    draw.line([(x0 + 20, sea + 18), (x1 - 20, sea + 18)], fill=WHITE, width=2)
    # two missile arcs, red, with flame dots
    draw.arc([x0 + 6, y0 + 4, x0 + 150, y0 + 96], 200, 340, fill=RED, width=4)
    draw.arc([x0 + 120, y0 + 2, x0 + 260, y0 + 88], 200, 340, fill=RED, width=4)
    draw.ellipse([x0 + 132, y0 + 8, x0 + 146, y0 + 22], fill=FLAME)
    draw.ellipse([x0 + 238, y0 + 2, x0 + 252, y0 + 16], fill=FLAME)
    # base silhouette on the horizon
    draw.rectangle([x0 + 96, sea - 26, x0 + 190, sea], fill=INK)
    draw.rectangle([x0 + 138, sea - 44, x0 + 148, sea - 26], fill=INK)


def scene_ship(draw, x0, y0, x1, y1):
    """A cargo ship burning on dark water."""
    draw.rectangle([x0, y0, x1, y1], fill=(24, 38, 52))
    sea = y0 + (y1 - y0) * 3 // 4
    draw.rectangle([x0, sea, x1, y1], fill=(16, 60, 74))
    # hull and containers
    draw.polygon([(x0 + 18, sea - 8), (x0 + 268, sea - 8),
                  (x0 + 248, sea + 16), (x0 + 38, sea + 16)], fill=(150, 40, 30))
    for i, cx in enumerate((x0 + 52, x0 + 108, x0 + 164)):
        draw.rectangle([cx, sea - 44, cx + 44, sea - 10],
                       fill=(GOLD if i % 2 == 0 else (200, 200, 190)))
    # flames and smoke from the bow (kept inside the icon band)
    bx = x0 + 216
    draw.polygon([(bx, sea - 12), (bx + 18, sea - 56), (bx + 34, sea - 28),
                  (bx + 50, sea - 58), (bx + 62, sea - 12)], fill=FLAME)
    draw.ellipse([bx - 6, sea - 56, bx + 30, sea - 28], fill=SMOKE)
    draw.ellipse([bx + 18, sea - 60, bx + 58, sea - 32], fill=SMOKE)


def scene_kyiv(draw, x0, y0, x1, y1):
    """A residential block struck, a drone above, smoke rising."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 220, 208))
    # apartment block, one corner shattered
    draw.rectangle([x0 + 40, y0 + 30, x0 + 210, y1 - 8], fill=(120, 110, 96))
    for r in range(3):
        for c in range(4):
            wx, wy = x0 + 58 + c * 42, y0 + 46 + r * 34
            draw.rectangle([wx, wy, wx + 24, wy + 18], fill=(247, 243, 232))
    # shattered corner: dark jagged hole + smoke
    draw.polygon([(x0 + 162, y0 + 30), (x0 + 210, y0 + 30), (x0 + 210, y0 + 78),
                  (x0 + 188, y0 + 58), (x0 + 176, y0 + 72)], fill=INK)
    draw.ellipse([x0 + 176, y0 + 2, x0 + 206, y0 + 26], fill=SMOKE)
    # quadcopter drone, clear of the smoke
    dx, dy = x0 + 252, y0 + 30
    draw.ellipse([dx - 12, dy - 8, dx + 12, dy + 8], fill=INK)
    draw.line([(dx - 22, dy - 12), (dx + 22, dy - 12)], fill=INK, width=3)
    draw.line([(dx - 22, dy + 12), (dx + 22, dy + 12)], fill=INK, width=3)


def scene_factory(draw, x0, y0, x1, y1):
    """A sawtooth factory with flames and a ladder."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 228, 210))
    base = y1 - 10
    # sawtooth roof
    draw.polygon([(x0 + 20, base), (x0 + 20, y0 + 44), (x0 + 80, y0 + 20),
                  (x0 + 80, y0 + 44), (x0 + 140, y0 + 20), (x0 + 140, y0 + 44),
                  (x0 + 200, y0 + 20), (x0 + 200, y0 + 44), (x0 + 260, y0 + 44),
                  (x0 + 260, base)], fill=(150, 96, 60), outline=INK)
    draw.rectangle([x0 + 34, base - 34, x0 + 58, base], fill=INK)
    draw.rectangle([x0 + 220, base - 34, x0 + 244, base], fill=INK)
    # flames from the middle bay
    draw.polygon([(x0 + 110, base), (x0 + 128, y0 + 30), (x0 + 146, base - 6),
                  (x0 + 164, y0 + 22), (x0 + 182, base)], fill=FLAME)
    draw.ellipse([x0 + 118, y0 + 2, x0 + 156, y0 + 26], fill=SMOKE)
    # ladder leaning on the wall
    draw.line([(x0 + 250, base), (x0 + 228, y0 + 52)], fill=RED, width=4)
    draw.line([(x0 + 262, base), (x0 + 240, y0 + 52)], fill=RED, width=4)


def scene_delta(draw, x0, y0, x1, y1):
    """A grounded plane under a warning triangle and a stopped clock."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # runway
    draw.rectangle([x0, y1 - 16, x1, y1], fill=INK)
    # plane silhouette, parked on the tarmac
    draw.polygon([(x0 + 44, y1 - 40), (x0 + 206, y1 - 40), (x0 + 246, y1 - 30),
                  (x0 + 206, y1 - 24), (x0 + 60, y1 - 24)], fill=INK)
    draw.polygon([(x0 + 118, y1 - 40), (x0 + 146, y1 - 66),
                  (x0 + 162, y1 - 66), (x0 + 148, y1 - 40)], fill=INK)
    draw.polygon([(x0 + 52, y1 - 28), (x0 + 40, y1 - 50),
                  (x0 + 52, y1 - 50), (x0 + 62, y1 - 28)], fill=INK)
    # warning triangle
    tx, ty = x0 + 232, y0 + 12
    draw.polygon([(tx, ty), (tx + 34, ty + 52), (tx - 34, ty + 52)],
                 fill=GOLD, outline=INK)
    draw.text((tx - 5, ty + 14), "!", font=font(SANS_BOLD, 26), fill=INK)
    # stopped clock
    cx, cy = x0 + 40, y0 + 30
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=WHITE,
                 outline=INK, width=3)
    draw.line([(cx, cy), (cx, cy - 13)], fill=INK, width=3)
    draw.line([(cx, cy), (cx + 10, cy + 3)], fill=INK, width=3)


def scene_scales(draw, x0, y0, x1, y1):
    """Scales of justice over a courtroom red band."""
    draw.rectangle([x0, y0, x1, y1], fill=(240, 234, 222))
    cx = (x0 + x1) // 2
    top, bot = y0 + 10, y1 - 8
    draw.line([(cx, top), (cx, bot)], fill=INK, width=4)
    draw.line([(cx - 74, top + 16), (cx + 74, top + 16)], fill=INK, width=4)
    draw.ellipse([cx - 7, top - 4, cx + 7, top + 10], fill=GOLD)
    for s in (-1, 1):
        px = cx + s * 74
        draw.line([(px, top + 16), (px, top + 34)], fill=INK, width=3)
        draw.polygon([(px - 30, top + 34), (px + 30, top + 34),
                      (px, top + 58)], fill=GOLD, outline=INK)
    draw.rectangle([x0, bot, x1, y1], fill=RED)


# ---------------------------------------------------------------- layout
LEAD = {
    "kicker": "CLIMATE  ·  ANTALYA",
    "headline": "CLIMATE TALKS\nCOLLAPSE",
    "standfirst": ("COP31 ends with no deal — and no mention of fossil "
                   "fuels in the final text — as governments walk away "
                   "divided."),
}

STORIES = [
    ("THE GULF  ·  WAR", RED, scene_hormuz,
     "WAR SPREADS\nACROSS THE GULF",
     "Iranian missiles hit a US base in Bahrain; Saudi Arabia "
     "intercepts a Houthi missile."),
    ("FINLAND  ·  THE BALTIC", TEAL, scene_ship,
     "SHIP ABLAZE\nOFF FINLAND",
     "A Russian cargo ship burns after a drone strike; another "
     "blast hits Benghazi port."),
    ("UKRAINE  ·  KYIV REGION", RED, scene_kyiv,
     "DRONE HITS\nKYIV REGION",
     "At least 14 missing after a Russian drone strikes a "
     "residential building, Kyiv says."),
    ("INDONESIA  ·  FACTORY FIRE", FLAME, scene_factory,
     "FACTORY FIRE,\nDOZENS MISSING",
     "Rescuers search the ruins of a candy factory blaze as "
     "the death toll climbs."),
    ("USA  ·  THANKSGIVING", TEAL, scene_delta,
     "DELTA'S SYSTEM\nFAILS",
     "A weight-and-balance outage delays hundreds of flights "
     "on Thanksgiving week."),
    ("THE HAGUE  ·  JUSTICE", GOLD, scene_scales,
     "GENOCIDE RULING\nAT THE HAGUE",
     "The UN's top court rules Myanmar committed genocide "
     "against the Rohingya."),
]


def lead_panel(draw):
    x0, y0, x1, y1 = MARGIN, 206, W - MARGIN, 508
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=INK, width=2)
    scene_globe(draw, x0 + 2, y0 + 2, 592, y1 - 2)
    draw.line([(592, y0), (592, y1)], fill=INK, width=2)
    tx = 612
    draw.text((tx, y0 + 16), LEAD["kicker"], font=font(SANS_BOLD, 14), fill=RED)
    rule(draw, y0 + 44, tx, x1 - 16, 2, RED)
    draw.multiline_text((tx, y0 + 58), LEAD["headline"],
                        font=font(SERIF, 40), fill=INK, spacing=6)
    body = wrap(draw, LEAD["standfirst"], font(SANS, 17), x1 - 16 - tx)
    y = y0 + 178
    for line in body:
        draw.text((tx, y), line, font=font(SANS, 17), fill=INK)
        y += 24
    draw.text((tx, y1 - 34), "TALKS BREAK DOWN  ·  NO AGREEMENT",
              font=font(SANS_BOLD, 13), fill=GREY)


def story_cell(draw, x0, y0, kicker, color, scene, headline, summary):
    w, h = 308, 206
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=WHITE, outline=INK, width=2)
    scene(draw, x0 + 2, y0 + 2, x0 + w - 2, y0 + 88)
    draw.line([(x0, y0 + 88), (x0 + w, y0 + 88)], fill=INK, width=2)
    tx = x0 + 12
    draw.text((tx, y0 + 96), kicker, font=font(SANS_BOLD, 11), fill=color)
    draw.multiline_text((tx, y0 + 114), headline,
                        font=font(SERIF, 19), fill=INK, spacing=3)
    lines = wrap(draw, summary, font(SANS, 13), w - 24)
    y = y0 + 162
    for line in lines[:2]:
        draw.text((tx, y), line, font=font(SANS, 13), fill=GREY)
        y += 17


def footer(draw):
    draw_centered(
        draw, 964,
        "Sources: Reuters · AP · BBC · CNN — reported Monday 23 November 2026",
        font(SANS, 13), GREY)
    draw_centered(draw, 984, "make.fun  ·  news-image-20261123",
                  font(SANS_BOLD, 11), GREY)


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead_panel(draw)
    xs = [MARGIN, MARGIN + 324, MARGIN + 648]
    ys = [524, 746]
    for i, story in enumerate(STORIES):
        story_cell(draw, xs[i % 3], ys[i // 3], *story)
    footer(draw)
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print("wrote", out)

