#!/usr/bin/env python3
"""THE WORLD TODAY - front page for Thursday 26 November 2026.
Deterministic: fixed seed, no timestamps, no network. PIL only.
Writes entry.png (1024x1024) next to this script's parent dir.
Structure (playbook): 3 leads + 10 secondary + 22 briefs = 35 stories,
timeline, markets strip, numbered world map, DATE CHECK box.
All 35 stories first reported on 26 Nov 2026; see NEWS.md for sources
and the excluded 24-25 Nov stories.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "entry.png"

W, H = 1024, 1024
MARGIN = 32
CW = W - 2 * MARGIN  # 960

PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (158, 27, 27)
GREY = (85, 85, 85)
LIGHT_GREY = (120, 115, 105)
NAVY = (28, 42, 68)
SKY = (222, 232, 238)
LAND = (168, 178, 150)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

RNG = random.Random(20261126)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip() if cur else w
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(path, text, max_size, max_w, min_size=10):
    size = max_size
    while size > min_size:
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def draw_centered(d, y, text, fnt, fill=INK):
    d.text((W / 2, y), text, font=fnt, fill=fill, anchor="ma")


def draw_wrapped(d, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, y, x0, x1, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=1)
d.rectangle([15, 15, W - 16, H - 16], outline=INK, width=1)

y = 18

# ---------------------------------------------------------------- masthead
mast_f = fit_font(SERIF_B, "THE WORLD TODAY", 52, CW)
draw_centered(d, y, "THE WORLD TODAY", mast_f)
y += int(mast_f.size * 1.02)

date_f = font(SANS_B, 18)
draw_centered(d, y, "THURSDAY,  26  NOVEMBER  2026", date_f)
y += 24

tag_f = font(SANS, 11)
draw_centered(d, y, "THE DAY'S WORLD NEWS  —  IN ONE PAGE  •  35 STORIES, ALL FIRST REPORTED TODAY",
              tag_f, fill=GREY)
y += 16

rule(d, y, MARGIN, W - MARGIN, width=3, fill=RED)
y += 4
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 6

# ---------------------------------------------------------------- timeline strip (single line)
tl_f = font(SANS, 11)
tl_lab = font(SANS_B, 11)
d.text((MARGIN, y), "THE DAY IN TIME (WIB) — ", font=tl_lab, fill=RED)
x0 = MARGIN + tl_lab.getlength("THE DAY IN TIME (WIB) — ")
tl = ("07:00 MoD letters to 100,000 veterans  •  07:30 Taipei confirms 15% tariff  •  "
      "08:15 Storm lashes East Coast  •  21:00 Chess Game 3 in Geneva")
d.text((x0, y), tl, font=tl_f, fill=INK)
y += 17
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 6

# ---------------------------------------------------------------- LEAD 1: Taiwan tariffs
d.text((MARGIN, y), "TRADE  •  LEAD STORY", font=font(SANS_B, 12), fill=RED)
y += 15
lead_f = font(SERIF_B, 28)
d.text((MARGIN, y), "TAIPEI: 15% IS THE FLOOR", font=lead_f, fill=INK)
y += 31
deck_f = font(SERIF, 15)
deck = ("Taiwan confirms the US tariff rate for the island is 15% — the lowest tier, "
        "with Japan, South Korea, the EU and Switzerland. It rises to 25% if talks fail.")
y = draw_wrapped(d, MARGIN, y, deck, deck_f, CW, leading=18)
y += 3

# --- illustration: proposed tariff bars (USTR, 14 economies)
bar_x0, bar_y0 = MARGIN, y
bar_x1, bar_y1 = W - MARGIN, y + 46
d.rectangle([bar_x0, bar_y0, bar_x1, bar_y1], fill=(232, 226, 210), outline=INK, width=1)
bars = [("TAIWAN  15%", 15), ("JAPAN  15%", 15), ("S. KOREA  15%", 15),
        ("EU  15%", 15), ("CHINA  up to 20%", 20), ("IF TALKS FAIL  25%", 25)]
bw = (bar_x1 - bar_x0 - 24) // 6
for i, (lab, pct) in enumerate(bars):
    bx = bar_x0 + 12 + i * bw
    bh = int(26 * pct / 25)
    d.text((bx + (bw - 10) // 2, bar_y0 + 3), lab.split("  ")[0], font=font(SANS, 8),
           fill=GREY, anchor="ma")
    d.rectangle([bx, bar_y1 - 5 - bh, bx + bw - 10, bar_y1 - 5], fill=RED)
    d.text((bx + (bw - 10) // 2, bar_y1 - 5 - bh + 2), f"{pct}%", font=font(SANS_B, 9),
           fill=(255, 255, 255), anchor="ma")
y = bar_y1 + 3
d.text((MARGIN, y), "USTR Section 301 proposals: 15% for five economies; China capped at 20%. Taipei confirms its rate at 08:30 today.",
       font=font(SANS, 10), fill=GREY)
y += 13
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 6

# ---------------------------------------------------------------- LEADS 2 & 3 (two columns)
col_w = (CW - 24) // 2
col2_x = MARGIN + col_w + 24
lead23_y0 = y

def mini_storm(d, x0, y0, w, h):
    """Storm sky, slanted rain, a grounded parade balloon."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(38, 52, 74), outline=INK, width=1)
    d.ellipse([x0 + 12, y0 + 5, x0 + 90, y0 + 26], fill=(90, 100, 120))
    d.ellipse([x0 + 60, y0 + 2, x0 + 140, y0 + 22], fill=(110, 120, 140))
    for i in range(14):
        rx = x0 + 10 + i * 30 + RNG.randint(-4, 4)
        ry = y0 + 24 + RNG.randint(0, 2)
        d.line([(rx, ry), (rx - 6, ry + 7)], fill=(170, 190, 220), width=2)
    bx, by = x0 + w - 78, y0 + h - 24
    d.ellipse([bx - 34, by - 12, bx + 34, by + 6], fill=(200, 60, 60), outline=(255, 255, 255), width=1)
    d.line([(bx - 20, by + 4), (bx - 30, y0 + h - 12)], fill=(220, 220, 220), width=1)
    d.line([(bx + 20, by + 4), (bx + 30, y0 + h - 12)], fill=(220, 220, 220), width=1)
    d.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(255, 230, 150))
    d.text((x0 + 8, y0 + h - 11), "PARADE MOVED TO SATURDAY", font=font(SANS_B, 9),
           fill=(38, 52, 74))


def mini_letter(d, x0, y0, w, h):
    """MoD letter: envelope, red seal, '100,000'."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 210), outline=INK, width=1)
    ex0, ey0 = x0 + 14, y0 + 14
    ex1, ey1 = x0 + w - 14, y0 + h - 4
    d.rectangle([ex0, ey0, ex1, ey1], fill=(250, 246, 236), outline=INK, width=1)
    d.line([(ex0, ey0), ((ex0 + ex1) // 2, (ey0 + ey1) // 2)], fill=GREY, width=1)
    d.line([(ex1, ey0), ((ex0 + ex1) // 2, (ey0 + ey1) // 2)], fill=GREY, width=1)
    cx, cy = (ex0 + ex1) // 2, (ey0 + ey1) // 2
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=RED, outline=(120, 20, 20), width=1)
    d.text((cx, cy - 6), "M", font=font(SERIF_B, 11), fill=(255, 255, 255), anchor="ma")
    for i, c in enumerate([(158, 27, 27), (255, 255, 255), (28, 42, 68)]):
        d.rectangle([x0 + w - 34 + i * 8, y0 + 4, x0 + w - 28 + i * 8, y0 + 12], fill=c)
    d.text((x0 + 8, y0 + 3), "100,000 LETTERS", font=font(SANS_B, 10), fill=RED)


# --- Lead 2: Thanksgiving storm
d.text((MARGIN, lead23_y0), "WEATHER  •  USA", font=font(SANS_B, 12), fill=RED)
hf = font(SERIF_B, 21)
d.text((MARGIN, lead23_y0 + 15), "THANKSGIVING STORM", font=hf, fill=INK)
d.text((MARGIN, lead23_y0 + 38), "BATTERS EAST COAST", font=hf, fill=INK)
y2 = draw_wrapped(d, MARGIN, lead23_y0 + 62,
                  "Gusts of 50–60 mph in New York; 70 million under wind "
                  "alerts; rain and floods from Wilmington to Boston.",
                  font(SANS, 12), col_w, leading=14)
mini_storm(d, MARGIN, y2 + 3, col_w, 44)
lead2_bot = y2 + 3 + 44

# --- Lead 3: UK MoD letters
d.text((col2_x, lead23_y0), "DEFENCE  •  BRITAIN", font=font(SANS_B, 12), fill=RED)
d.text((col2_x, lead23_y0 + 15), "BRITAIN CALLS UP", font=hf, fill=INK)
d.text((col2_x, lead23_y0 + 38), "ITS VETERANS", font=hf, fill=INK)
y3 = draw_wrapped(d, col2_x, lead23_y0 + 62,
                  "MoD writes to about 100,000 reservists as Russia "
                  "tensions rise. Kushner: Europe has no Ukraine plan.",
                  font(SANS, 12), col_w, leading=14)
mini_letter(d, col2_x, y3 + 3, col_w, 44)
lead3_bot = y3 + 3 + 44

y = max(lead2_bot, lead3_bot) + 5
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 5

# ---------------------------------------------------------------- markets strip
d.text((MARGIN, y), "THE MARKETS — WEDNESDAY'S CLOSE, IN THURSDAY'S WRAPS",
       font=font(SANS_B, 13), fill=INK)
y += 16
mk = [("DOW", "50,182.95  +0.33%"), ("S&P 500", "7,182.78  −0.25%"),
      ("NASDAQ", "23,585.80  −0.62%"), ("BRENT", "$94.61  +3.5%"),
      ("WTI", "$83.68  +2.0%"), ("GOLD", "$3,484  −2%"),
      ("NVIDIA", "−3.9%  $149.30"), ("VIX", "28.29")]
seg_w = CW // 4
for i, (k, v) in enumerate(mk):
    cx = MARGIN + (i % 4) * seg_w
    cy = y + (i // 4) * 16
    kf = font(SANS_B, 12)
    d.text((cx, cy), f"{k} ", font=kf, fill=RED)
    d.text((cx + kf.getlength(f"{k} "), cy), v, font=font(SANS, 12), fill=INK)
y += 34
d.text((MARGIN, y),
       "Dow erased a 1,100-point fall; Nasdaq was −4.6% at its worst. Q3 GDP +4.3%; core PCE +0.3%. US markets shut today.",
       font=font(SANS, 11), fill=GREY)
y += 13
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 5

# ---------------------------------------------------------------- secondary 10 (numbered 4–13)
d.text((MARGIN, y), "THE REST OF THE DAY — IN BRIEF", font=font(SANS_B, 14), fill=INK)
y += 18
sec = [
    ("4", "Kushner: Europe has no convincing plan for peace in Ukraine."),
    ("5", "Gordon Ramsay named new Top Gear host."),
    ("6", "Nurses demand protection from trans law; RCN campaign."),
    ("7", "Chess Game 3 today in Geneva; scores level 1–1."),
    ("8", "SWS: 9.8m Filipino families rate themselves poor in Q3."),
    ("9", "Duterte ICC trial: prosecutors plan 100 witnesses."),
    ("10", "Senate cuts P19.8B aid to boost PhilHealth."),
    ("11", "Anthropic shares fall below IPO price."),
    ("12", "VP Sara Duterte challenges court ruling on arrest."),
    ("13", "King Felipe VI eyes Philippines visit; coast guard +3 ships."),
]
sec_row_h = 19
for i, (num, text) in enumerate(sec):
    sx = MARGIN + (i % 2) * (col_w + 24)
    sy = y + (i // 2) * sec_row_h
    nf = font(SANS_B, 13)
    d.text((sx, sy), num, font=nf, fill=RED)
    nw = nf.getlength(num + "  ")
    draw_wrapped(d, sx + nw, sy, text, font(SANS, 12), col_w - nw, leading=14)
y += 5 * sec_row_h + 1
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 5

# ---------------------------------------------------------------- world map (numbered pins)
d.text((MARGIN, y), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=INK)
y += 17
map_x0, map_y0 = MARGIN, y
map_x1, map_y1 = W - MARGIN, y + 62
d.rectangle([map_x0, map_y0, map_x1, map_y1], fill=SKY, outline=INK, width=1)
mw, mh = map_x1 - map_x0, map_y1 - map_y0
OX, OY = map_x0, map_y0
YS = mh / 76.0  # continents drawn in a 960x76 reference box
def P(pts):
    return [(OX + x, OY + y * YS) for x, y in pts]
d.polygon(P([(60, 12), (130, 6), (200, 12), (240, 20), (285, 24), (278, 36),
           (240, 40), (165, 40), (130, 46), (82, 36), (52, 24)]), fill=LAND)  # N America
d.polygon(P([(270, 44), (310, 40), (350, 48), (360, 60), (330, 70), (290, 66), (262, 54)]), fill=LAND)  # S America
d.polygon(P([(448, 10), (500, 6), (534, 14), (526, 26), (482, 28), (448, 20)]), fill=LAND)  # Europe
d.polygon(P([(464, 32), (516, 28), (542, 40), (530, 58), (494, 60), (470, 46)]), fill=LAND)  # Africa
d.polygon(P([(550, 8), (654, 4), (756, 10), (824, 18), (842, 28), (792, 34),
           (722, 38), (654, 34), (584, 30), (546, 20)]), fill=LAND)  # Asia
d.polygon(P([(756, 56), (816, 52), (834, 62), (800, 68), (760, 64)]), fill=LAND)  # Australia
for gx in range(map_x0 + 80, map_x1, 80):
    d.line([(gx, map_y0), (gx, map_y1)], fill=(200, 212, 220), width=1)
for gy in range(map_y0 + 21, map_y1, 21):
    d.line([(map_x0, gy), (map_x1, gy)], fill=(200, 212, 220), width=1)
pins = [
    ("1", "TAIPEI", 776, 26), ("2", "NEW YORK", 288, 16),
    ("3", "LONDON", 462, 14), ("4", "GENEVA", 496, 28),
    ("5", "MANILA", 800, 40), ("6", "NEW DELHI", 648, 30),
    ("7", "WASHINGTON", 262, 36),
]
for num, lab, px, py in pins:
    py = py * YS
    d.ellipse([map_x0 + px - 9, map_y0 + py - 9, map_x0 + px + 9, map_y0 + py + 9],
              fill=RED, outline=(255, 255, 255), width=2)
    tf = font(SANS_B, 10)
    tw = tf.getlength(num)
    d.text((map_x0 + px - tw / 2, map_y0 + py - 6), num, font=tf, fill=(255, 255, 255))
y = map_y1 + 3
key = ("1 TAIPEI   2 NEW YORK   3 LONDON   4 GENEVA   5 MANILA   6 NEW DELHI   7 WASHINGTON")
d.text((MARGIN, y), key, font=font(SANS, 11), fill=GREY)
y += 12
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 5

# ---------------------------------------------------------------- briefs 22: ALSO ON 26 NOVEMBER
d.text((MARGIN, y), "ALSO ON 26 NOVEMBER", font=font(SANS_B, 14), fill=INK)
y += 16
briefs = [
    "UN warns HIV infections could rise after funding cuts",
    "M5.1 quake hits Antique, Philippines",
    "India marks Constitution Day and National Milk Day",
    "House moves on rooftop solar; P10-B budget clears Senate",
    "Romualdez seeks reconsideration of his suspension",
    "NBI subpoenas comedian JP Aguilera over remarks",
    "SWS: 69% of Filipinos aware of flood-control probe",
    "MANIBELA calls off protest; Maysan Road reopens",
    "Meralco–LRTA partner on LRT-1 Cavite extension",
    "DOE tells gas stations to justify rollback delays",
    "NPC: 11 agencies yet to explain data breaches",
    "MGEN Renewables posts earnings; red-tape cuts urged",
    "Bulgarian beach container spills Santa decorations",
    "US markets shut for Thanksgiving; early close Friday",
    "NBC airs 2025 Macy's rerun; 100th parade now Saturday",
    "Poundland in administration",
    "May criticises TikToks at No 10",
    "Sterling avoids jail over nitrous oxide crash",
    "BSP concerned over falling foreign reserves",
    "PNP praised for ASEAN Summit security",
    "Cebu City sets Christmas caroling hours",
    "Taiwan: DPP's He Xinchun campaigns with Tsai and Lai",
]
bf = font(SANS, 11)
row_h = 12
for i, text in enumerate(briefs):
    bx = MARGIN + (i % 2) * (col_w + 24)
    by = y + (i // 2) * row_h
    d.text((bx, by), "▪", font=bf, fill=RED)
    d.text((bx + 12, by), text, font=bf, fill=INK)
y += 11 * row_h + 1
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 5

# ---------------------------------------------------------------- DATE CHECK box (8 items, 4 rows)
box_y0 = y
box_h = 78
d.rectangle([MARGIN, box_y0, W - MARGIN, box_y0 + box_h], fill=(238, 230, 214),
            outline=RED, width=2)
d.text((MARGIN + 10, box_y0 + 5), "DATE CHECK — BIG STORIES THAT ARE NOT 26 NOVEMBER",
       font=font(SANS_B, 12), fill=RED)
dc = [
    "USTR unveils 14-economy tariffs — 25 Nov",
    "Houthi claim on Ras Tanura; Brent $94.61 — 25 Nov",
    "Sudan: RSF drones kill 19 in Blue Nile — 24–25 Nov",
    "Cairo tanker fire, 30–31 killed — 25 Nov",
    "Bangladesh garment wage +36% — 25 Nov",
    "Malaysia sues Google, $146M — 25 Nov",
    "Ramaphosa wins Phala Phala case — 25 Nov",
    "Shenzhou-24; first Pakistani in orbit — 25 Nov",
]
dcf = font(SANS, 11)
for i, text in enumerate(dc):
    bx = MARGIN + 10 + (i % 2) * ((CW - 20) // 2)
    by = box_y0 + 22 + (i // 2) * 12
    d.text((bx, by), "✕  " + text, font=dcf, fill=INK)
y = box_y0 + box_h + 3
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 4

# ---------------------------------------------------------------- footer
foot_f = font(SANS_B, 11)
draw_centered(d, y, "THE WORLD TODAY  •  THURSDAY 26 NOVEMBER 2026  •  SOURCES: REUTERS, AP, BBC, TELEGRAPH, CHESS.COM",
              foot_f, fill=GREY)
y += 13
print("final y:", y, "canvas H:", H)
assert y <= H - 14, f"overflow: y={y} > {H}"

img.save(OUT, format="PNG", optimize=True)
print("saved", OUT, img.size)
