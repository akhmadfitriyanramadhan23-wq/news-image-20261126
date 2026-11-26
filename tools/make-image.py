#!/usr/bin/env python3
"""The World Today — front page for Thursday 26 November 2026.

One 1024x1024 PNG newspaper page carrying 35 stories, every one of
them first reported on 26 November 2026: three leads, ten more stories,
twenty-two briefs, plus a timeline, Wednesday's market closes, a
numbered world map and a DATE CHECK box naming the big 24–25 November
stories that other round-ups wrongly present as today's news.

PIL only. Deterministic: a fixed seed drives the few random details,
and nothing reads the clock or the network. Run it with
`python3 tools/make-image.py` — it writes ../entry.png.
See NEWS.md (kept out of the repository) for the sources.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
OUTFILE = BASE / "entry.png"

SHEET_W, SHEET_H = 1024, 1024
SIDE = 32
BODY_W = SHEET_W - 2 * SIDE
HALF_W = (BODY_W - 24) // 2

CREAM = (247, 242, 231)
BLACK = (17, 17, 17)
CRIMSON = (158, 27, 27)
SLATE = (85, 85, 85)
OCEAN = (222, 232, 238)
FIELD = (168, 178, 150)
STORMBLUE = (38, 52, 74)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_rng = random.Random(20261126)
_cache = {}


def face(kind, size):
    """Load (and cache) a TrueType face at the requested size."""
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(kind, size)
    return _cache[key]


def flow_lines(text, fnt, width):
    """Break text into lines that fit `width` under font `fnt`."""
    out, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


# ------------------------------------------------------------------ content
TIMELINE = [
    ("07:00", "MoD letters to 100,000 veterans"),
    ("07:30", "Taipei confirms 15% tariff"),
    ("08:15", "Storm lashes East Coast"),
    ("21:00", "Chess Game 3 in Geneva"),
]

TARIFFS = [
    ("Taiwan", 15), ("Japan", 15), ("South Korea", 15),
    ("EU", 15), ("China", 20), ("If talks fail", 25),
]

SECONDARY = [
    "Kushner: Europe has no convincing plan for peace in Ukraine.",
    "Gordon Ramsay named new Top Gear host.",
    "Nurses demand protection from trans law; RCN campaign.",
    "Chess Game 3 today in Geneva; scores level 1–1.",
    "SWS: 9.8m Filipino families rate themselves poor in Q3.",
    "Duterte ICC trial: prosecutors plan 100 witnesses.",
    "Senate cuts P19.8B aid to boost PhilHealth.",
    "Anthropic shares fall below IPO price.",
    "VP Sara Duterte challenges court ruling on arrest.",
    "King Felipe VI eyes Philippines visit; coast guard +3 ships.",
]

BRIEFS = [
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

DATECHECK = [
    "USTR unveils 14-economy tariffs — 25 Nov",
    "Houthi claim on Ras Tanura; Brent $94.61 — 25 Nov",
    "Sudan: RSF drones kill 19 in Blue Nile — 24–25 Nov",
    "Cairo tanker fire, 30–31 killed — 25 Nov",
    "Bangladesh garment wage +36% — 25 Nov",
    "Malaysia sues Google, $146M — 25 Nov",
    "Ramaphosa wins Phala Phala case — 25 Nov",
    "Shenzhou-24; first Pakistani in orbit — 25 Nov",
]

MARKETS = [
    ("DOW", "50,182.95 +0.33%"),
    ("S&P 500", "7,182.78 −0.25%"),
    ("NASDAQ", "23,585.80 −0.62%"),
    ("BRENT", "$94.61 +3.5%"),
    ("WTI", "$83.68 +2.0%"),
    ("GOLD", "$3,484 −2%"),
    ("NVIDIA", "−3.9% $149.30"),
    ("VIX", "28.29"),
]

PINS = [
    {"n": "1", "place": "TAIPEI", "x": 780, "y": 24},
    {"n": "2", "place": "NEW YORK", "x": 288, "y": 18},
    {"n": "3", "place": "LONDON", "x": 460, "y": 13},
    {"n": "4", "place": "GENEVA", "x": 498, "y": 27},
    {"n": "5", "place": "MANILA", "x": 802, "y": 38},
    {"n": "6", "place": "NEW DELHI", "x": 650, "y": 28},
    {"n": "7", "place": "WASHINGTON", "x": 262, "y": 32},
]


# ------------------------------------------------------------------ the sheet
class Sheet:
    def __init__(self):
        self.canvas = Image.new("RGB", (SHEET_W, SHEET_H), CREAM)
        self.pen = ImageDraw.Draw(self.canvas)
        self.y = 18
        self.pen.rectangle([10, 10, SHEET_W - 11, SHEET_H - 11],
                           outline=BLACK, width=1)
        self.pen.rectangle([15, 15, SHEET_W - 16, SHEET_H - 16],
                           outline=BLACK, width=1)

    def gap(self, px):
        self.y += px

    def hline(self, weight=1, colour=BLACK):
        self.pen.line([(SIDE, self.y), (SHEET_W - SIDE, self.y)],
                      fill=colour, width=weight)

    def centred(self, text, kind, size, colour=BLACK):
        f = face(kind, size)
        x = (SHEET_W - self.pen.textlength(text, font=f)) / 2
        self.pen.text((x, self.y), text, font=f, fill=colour)
        self.y += int(size * 1.05)

    def paragraph(self, text, kind, size, width, x=SIDE, colour=BLACK,
                  leading=None):
        f = face(kind, size)
        step = leading if leading is not None else int(size * 1.3)
        for ln in flow_lines(text, f, width):
            self.pen.text((x, self.y), ln, font=f, fill=colour)
            self.y += step

    def kicker(self, text, size=12):
        self.pen.text((SIDE, self.y), text, font=face(SANS_B, size),
                      fill=CRIMSON)
        self.y += size + 3


def draw_tariff_chart(sheet, top, height):
    """Horizontal bars for the USTR Section 301 proposals."""
    pen = sheet.pen
    x0, x1 = SIDE, SHEET_W - SIDE
    pen.rectangle([x0, top, x1, top + height], fill=(232, 226, 210),
                  outline=BLACK, width=1)
    slot = (x1 - x0 - 24) // len(TARIFFS)
    for i, (name, pct) in enumerate(TARIFFS):
        bx = x0 + 12 + i * slot
        bar_h = int(26 * pct / 25)
        label = name.upper()
        lf = face(SANS_R, 8)
        lx = bx + (slot - 10) / 2 - pen.textlength(label, font=lf) / 2
        pen.text((lx, top + 3), label, font=lf, fill=SLATE)
        pen.rectangle([bx, top + height - 5 - bar_h, bx + slot - 10,
                       top + height - 5], fill=CRIMSON)
        vf = face(SANS_B, 9)
        val = f"{pct}%"
        vx = bx + (slot - 10) / 2 - pen.textlength(val, font=vf) / 2
        pen.text((vx, top + height - 5 - bar_h + 2), val, font=vf,
                 fill=(255, 255, 255))


def draw_storm_panel(pen, x0, y0, w, h):
    """Storm sky, slanted rain and a grounded parade balloon."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=STORMBLUE,
                  outline=BLACK, width=1)
    pen.ellipse([x0 + 12, y0 + 5, x0 + 90, y0 + 26], fill=(90, 100, 120))
    pen.ellipse([x0 + 60, y0 + 2, x0 + 140, y0 + 22], fill=(110, 120, 140))
    for i in range(14):
        rx = x0 + 10 + i * 30 + _rng.randint(-4, 4)
        ry = y0 + 24 + _rng.randint(0, 2)
        pen.line([(rx, ry), (rx - 6, ry + 7)], fill=(170, 190, 220), width=2)
    bx, by = x0 + w - 78, y0 + h - 24
    pen.ellipse([bx - 34, by - 12, bx + 34, by + 6], fill=(200, 60, 60),
                outline=(255, 255, 255), width=1)
    pen.line([(bx - 20, by + 4), (bx - 30, y0 + h - 12)],
             fill=(220, 220, 220), width=1)
    pen.line([(bx + 20, by + 4), (bx + 30, y0 + h - 12)],
             fill=(220, 220, 220), width=1)
    pen.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(255, 230, 150))
    pen.text((x0 + 8, y0 + h - 11), "PARADE MOVED TO SATURDAY",
             font=face(SANS_B, 9), fill=STORMBLUE)


def draw_letter_panel(pen, x0, y0, w, h):
    """An MoD envelope with a red wax seal."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 210),
                  outline=BLACK, width=1)
    ex0, ey0 = x0 + 14, y0 + 14
    ex1, ey1 = x0 + w - 14, y0 + h - 4
    pen.rectangle([ex0, ey0, ex1, ey1], fill=(250, 246, 236),
                  outline=BLACK, width=1)
    cx, cy = (ex0 + ex1) // 2, (ey0 + ey1) // 2
    pen.polygon([(ex0, ey0), (ex1, ey0), (cx, cy)], outline=SLATE)
    pen.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=CRIMSON,
                outline=(120, 20, 20), width=1)
    mf = face(SERIF_B, 11)
    pen.text((cx - pen.textlength("M", font=mf) / 2, cy - 6), "M",
             font=mf, fill=(255, 255, 255))
    for i, c in enumerate([(158, 27, 27), (255, 255, 255), (28, 42, 68)]):
        pen.rectangle([x0 + w - 34 + i * 8, y0 + 4,
                       x0 + w - 28 + i * 8, y0 + 12], fill=c)
    pen.text((x0 + 8, y0 + 3), "100,000 LETTERS", font=face(SANS_B, 10),
             fill=CRIMSON)


def lead_column(sheet, x, kicker_text, heads, deck, panel):
    """One of the two second-lead columns; returns its bottom y."""
    pen = sheet.pen
    top = sheet.y
    pen.text((x, top), kicker_text, font=face(SANS_B, 12), fill=CRIMSON)
    hf = face(SERIF_B, 21)
    for j, hd in enumerate(heads):
        pen.text((x, top + 15 + j * 23), hd, font=hf, fill=BLACK)
    f = face(SANS_R, 12)
    yy = top + 62
    for ln in flow_lines(deck, f, HALF_W):
        pen.text((x, yy), ln, font=f, fill=BLACK)
        yy += 14
    panel(pen, x, yy + 3, HALF_W, 44)
    return yy + 3 + 44


def build():
    s = Sheet()
    pen = s.pen

    # ---------------------------------------------------------- masthead
    s.centred("THE WORLD TODAY", SERIF_B, 52)
    s.centred("THURSDAY,  26  NOVEMBER  2026", SANS_B, 18)
    s.gap(6)
    s.centred("THE DAY'S WORLD NEWS — ONE PAGE  •  35 STORIES, EACH FIRST REPORTED TODAY",
              SANS_R, 11, SLATE)
    s.gap(5)
    s.hline(3, CRIMSON)
    s.gap(4)
    s.hline(1)
    s.gap(6)

    # ---------------------------------------------------------- timeline
    lab = "THE DAY IN TIME (WIB) — "
    lf = face(SANS_B, 11)
    pen.text((SIDE, s.y), lab, font=lf, fill=CRIMSON)
    tx = SIDE + pen.textlength(lab, font=lf)
    bits = "  •  ".join(f"{t} {what}" for t, what in TIMELINE)
    pen.text((tx, s.y), bits, font=face(SANS_R, 11), fill=BLACK)
    s.gap(17)
    s.hline(1)
    s.gap(6)

    # ---------------------------------------------------------- lead 1
    s.kicker("TRADE  •  LEAD STORY")
    pen.text((SIDE, s.y), "TAIPEI: 15% IS THE FLOOR",
             font=face(SERIF_B, 28), fill=BLACK)
    s.gap(31)
    s.paragraph(
        "Taiwan confirms the US tariff rate for the island is 15% — the lowest tier, "
        "with Japan, South Korea, the EU and Switzerland. It rises to 25% if talks fail.",
        SERIF_R, 15, BODY_W, leading=18)
    s.gap(3)
    draw_tariff_chart(s, s.y, 46)
    s.gap(49)
    pen.text((SIDE, s.y),
             "USTR Section 301 proposals: 15% for five economies; China capped at 20%. Taipei confirms its rate at 08:30 today.",
             font=face(SANS_R, 10), fill=SLATE)
    s.gap(13)
    s.hline(1)
    s.gap(6)

    # ---------------------------------------------------------- leads 2 & 3
    col2 = SIDE + HALF_W + 24
    bottom = max(
        lead_column(s, SIDE, "WEATHER  •  USA",
                    ["THANKSGIVING STORM", "BATTERS EAST COAST"],
                    "Gusts of 50–60 mph in New York; 70 million under wind "
                    "alerts; rain and floods from Wilmington to Boston.",
                    draw_storm_panel),
        lead_column(s, col2, "DEFENCE  •  BRITAIN",
                    ["BRITAIN CALLS UP", "ITS VETERANS"],
                    "MoD writes to about 100,000 reservists as Russia "
                    "tensions rise. Kushner: Europe has no Ukraine plan.",
                    draw_letter_panel),
    )
    s.y = bottom + 5
    s.hline(1)
    s.gap(5)

    # ---------------------------------------------------------- markets
    pen.text((SIDE, s.y), "THE MARKETS — WEDNESDAY'S CLOSE, IN THURSDAY'S WRAPS",
             font=face(SANS_B, 13), fill=BLACK)
    s.gap(16)
    seg = BODY_W // 4
    for i, (name, val) in enumerate(MARKETS):
        cx = SIDE + (i % 4) * seg
        cy = s.y + (i // 4) * 16
        kf = face(SANS_B, 12)
        pen.text((cx, cy), f"{name} ", font=kf, fill=CRIMSON)
        pen.text((cx + pen.textlength(f"{name} ", font=kf), cy), val,
                 font=face(SANS_R, 12), fill=BLACK)
    s.gap(34)
    pen.text((SIDE, s.y),
             "Dow erased a 1,100-point fall; Nasdaq was −4.6% at its worst. Q3 GDP +4.3%; core PCE +0.3%. US markets shut today.",
             font=face(SANS_R, 11), fill=SLATE)
    s.gap(13)
    s.hline(1)
    s.gap(5)

    # ---------------------------------------------------------- ten more
    pen.text((SIDE, s.y), "MORE OF THE DAY", font=face(SANS_B, 14), fill=BLACK)
    s.gap(18)
    for i, item in enumerate(SECONDARY):
        sx = SIDE + (i % 2) * (HALF_W + 24)
        sy = s.y + (i // 2) * 19
        nf = face(SANS_B, 13)
        num = str(i + 4)
        pen.text((sx, sy), num, font=nf, fill=CRIMSON)
        nx = sx + pen.textlength(num + "  ", font=nf)
        for ln in flow_lines(item, face(SANS_R, 12), HALF_W - (nx - sx)):
            pen.text((nx, sy), ln, font=face(SANS_R, 12), fill=BLACK)
            sy += 14
    s.gap(5 * 19 + 1)
    s.hline(1)
    s.gap(5)

    # ---------------------------------------------------------- world map
    pen.text((SIDE, s.y), "ON THE MAP", font=face(SANS_B, 14), fill=BLACK)
    s.gap(17)
    mx0, my0 = SIDE, s.y
    mx1, my1 = SHEET_W - SIDE, s.y + 62
    pen.rectangle([mx0, my0, mx1, my1], fill=OCEAN, outline=BLACK, width=1)
    ys = (my1 - my0) / 76.0

    def blob(cx, cy, rx, ry):
        pen.ellipse([mx0 + cx - rx, my0 + cy * ys - ry,
                     mx0 + cx + rx, my0 + cy * ys + ry], fill=FIELD)

    blob(120, 24, 100, 18)  # North America, west
    blob(215, 28, 75, 16)   # North America, east
    blob(300, 52, 40, 18)   # South America, north
    blob(310, 66, 28, 14)   # South America, south
    blob(486, 15, 40, 10)   # Europe
    blob(498, 42, 32, 15)   # Africa, north
    blob(505, 56, 24, 10)   # Africa, south
    blob(640, 15, 105, 13)  # Asia, north
    blob(715, 30, 75, 11)   # Asia, south
    blob(795, 60, 34, 8)    # Australia
    for gx in range(mx0 + 80, mx1, 80):
        pen.line([(gx, my0), (gx, my1)], fill=(200, 212, 220), width=1)
    for gy in range(my0 + 21, my1, 21):
        pen.line([(mx0, gy), (mx1, gy)], fill=(200, 212, 220), width=1)
    for pin in PINS:
        px, py = mx0 + pin["x"], my0 + pin["y"] * ys
        pen.ellipse([px - 9, py - 9, px + 9, py + 9], fill=CRIMSON,
                    outline=(255, 255, 255), width=2)
        tf = face(SANS_B, 10)
        pen.text((px - pen.textlength(pin["n"], font=tf) / 2, py - 6),
                 pin["n"], font=tf, fill=(255, 255, 255))
    s.y = my1 + 3
    key = "  ".join(f"{p['n']} {p['place']}" for p in PINS)
    pen.text((SIDE, s.y), key, font=face(SANS_R, 11), fill=SLATE)
    s.gap(12)
    s.hline(1)
    s.gap(5)

    # ---------------------------------------------------------- briefs
    pen.text((SIDE, s.y), "ALSO ON 26 NOVEMBER", font=face(SANS_B, 14),
             fill=BLACK)
    s.gap(16)
    bf = face(SANS_R, 11)
    for i, item in enumerate(BRIEFS):
        bx = SIDE + (i % 2) * (HALF_W + 24)
        by = s.y + (i // 2) * 12
        pen.text((bx, by), "▪", font=bf, fill=CRIMSON)
        pen.text((bx + 12, by), item, font=bf, fill=BLACK)
    s.gap(11 * 12 + 1)
    s.hline(1)
    s.gap(5)

    # ---------------------------------------------------------- date check
    box_top = s.y
    box_h = 78
    pen.rectangle([SIDE, box_top, SHEET_W - SIDE, box_top + box_h],
                  fill=(238, 230, 214), outline=CRIMSON, width=2)
    pen.text((SIDE + 10, box_top + 5),
             "DATE CHECK — BIG STORIES THAT ARE NOT 26 NOVEMBER",
             font=face(SANS_B, 12), fill=CRIMSON)
    dcf = face(SANS_R, 11)
    for i, item in enumerate(DATECHECK):
        bx = SIDE + 10 + (i % 2) * ((BODY_W - 20) // 2)
        by = box_top + 22 + (i // 2) * 12
        pen.text((bx, by), "✕  " + item, font=dcf, fill=BLACK)
    s.y = box_top + box_h + 3
    s.hline(1)
    s.gap(4)

    # ---------------------------------------------------------- footer
    s.centred("THE WORLD TODAY  •  THURSDAY 26 NOVEMBER 2026  •  SOURCES: REUTERS, AP, BBC, TELEGRAPH, CHESS.COM",
              SANS_B, 11, SLATE)
    print("final y:", s.y, "canvas H:", SHEET_H)
    assert s.y <= SHEET_H - 14, f"overflow: y={s.y} > {SHEET_H}"
    s.canvas.save(OUTFILE, format="PNG", optimize=True)
    print("saved", OUTFILE, s.canvas.size)


if __name__ == "__main__":
    build()
