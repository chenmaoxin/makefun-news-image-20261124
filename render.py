#!/usr/bin/env python3
"""Render the 24 November 2026 'world in one image' newspaper poster (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 44
CW = W - 2 * MARGIN

PAPER = (248, 244, 236)
INK = (22, 19, 13)
RED = (176, 30, 36)
GRAY = (96, 89, 76)
BODY = (43, 39, 31)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def F(path, size):
    return ImageFont.truetype(path, size)


def text_w(s, font):
    return d.textlength(s, font=font)


def draw_tracked_center(s, y, font, color, tracking=6):
    w = sum(d.textlength(ch, font=font) for ch in s) + tracking * (len(s) - 1)
    x = (W - w) / 2
    for ch in s:
        d.text((x, y), ch, font=font, fill=color)
        x += d.textlength(ch, font=font) + tracking


def wrap(s, font, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_lines(lines, x, y, font, color, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += leading
    return y


def rule(y, thick=3):
    d.rectangle([MARGIN, y, W - MARGIN, y + thick - 1], fill=INK)
    return y + thick


def story(x, y, w, kicker, headline, summary):
    d.text((x, y), kicker, font=F(SANS_B, 17), fill=RED)
    y += 22
    hf = F(SERIF_B, 25)
    y = draw_lines(wrap(headline, hf, w), x, y, hf, INK, 28)
    y += 3
    sf = F(SANS, 18)
    y = draw_lines(wrap(summary, sf, w), x, y, sf, BODY, 22)
    return y


# ---------- masthead ----------
y = 22
y = rule(y, 6) + 8
y = rule(y, 2) + 11
draw_tracked_center("THE WORLD IN ONE IMAGE", y, F(SANS_B, 22), INK, tracking=9)
y += 30
draw_tracked_center("TUESDAY, 24 NOVEMBER 2026", y, F(SERIF_B, 46), INK, tracking=1)
y += 56
y = rule(y, 2) + 6
y = rule(y, 4) + 13

# ---------- lead ----------
d.text((MARGIN, y), "BUSINESS  ·  UNITED STATES", font=F(SANS_B, 18), fill=RED)
y += 25
lf = F(SERIF_B, 44)
y = draw_lines(wrap("HUANG IS BACK: NVIDIA REINSTATES ITS FOUNDER AS CEO", lf, CW),
               MARGIN, y, lf, INK, 48)
y += 5
sf = F(SANS, 21)
y = draw_lines(wrap("Ousted 11 days ago amid scandal, Jensen Huang was reinstated as "
                    "Nvidia's CEO after Trump personally pressed the board to act.", sf, CW),
               MARGIN, y, sf, BODY, 26)
y += 10
band_h = 38
d.rectangle([MARGIN, y, W - MARGIN, y + band_h], fill=INK)
stat = "SHARES +31.5% IN A DAY  ·  NEARLY $1 TRILLION ADDED — LARGEST ONE-DAY GAIN EVER"
size = 20
stf = F(SANS_B, size)
while text_w(stat, stf) > CW - 24 and size > 10:
    size -= 1
    stf = F(SANS_B, size)
d.text(((W - text_w(stat, stf)) / 2, y + 9), stat, font=stf, fill=PAPER)
y += band_h + 12
y = rule(y, 3) + 11

# ---------- grid ----------
col_w = (CW - 34) // 2
x2 = MARGIN + col_w + 34
row1 = max(
    story(MARGIN, y, col_w, "MIDDLE EAST  ·  ENERGY",
          "TANKERS HIT MINES IN STRAIT OF HORMUZ",
          "Iran's Guards say three oil tankers struck naval mines and caught fire "
          "despite a US escort, as Gulf shipping attacks hit a war high."),
    story(x2, y, col_w, "WAR  ·  LIBYA",
          "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
          "Kyiv's sea drones sank the corvette Merkury in Benghazi harbour, 2,400 km "
          "from the front; the UN calls for an investigation."),
)
y = row1 + 9
d.line([MARGIN, y, W - MARGIN, y], fill=GRAY, width=1)
y += 9
row2 = max(
    story(MARGIN, y, col_w, "CLIMATE  ·  TÜRKIYE",
          "CLIMATE SUMMIT COLLAPSES OVER FOSSIL FUELS",
          "COP31 in Antalya ended with no deal — the first failed climate summit "
          "since 2009 — after 90 nations rejected a text silent on fossil fuels."),
    story(x2, y, col_w, "ASIA  ·  WORLD COURT",
          "14 NATIONS BACK GENOCIDE RULING ON MYANMAR",
          "Britain sanctions Myanmar's president and army chiefs after the World "
          "Court ruled its military committed genocide against the Rohingya."),
)
y = row2 + 9
d.line([MARGIN, y, W - MARGIN, y], fill=GRAY, width=1)
y += 9
row3 = max(
    story(MARGIN, y, col_w, "TECHNOLOGY  ·  US COURTS",
          "STATES SUE SPACEX OVER GROK IMAGES",
          "Virginia and Oregon are first to sue, alleging Grok's 'spicy mode' made "
          "child abuse images and non-consensual pictures."),
    story(x2, y, col_w, "SPORT  ·  FOOTBALL",
          "US TO CO-HOST 2031 WOMEN'S WORLD CUP",
          "FIFA gives the first 48-team Women's World Cup to the US, Mexico, Costa "
          "Rica and Jamaica; the UK hosts in 2035."),
)
y = row3 + 11
y = rule(y, 3) + 9

# ---------- in brief ----------
bf = F(SANS, 18)
bhf = F(SANS_B, 18)
head = "IN BRIEF   "
bw = text_w(head, bhf)
d.text((MARGIN, y), head, font=bhf, fill=RED)
brief = ("Indonesia confirms 24 dead in a candy-factory fire, about 30 still missing  ·  "
         "NATO responds to reports of a possible Russian nuclear-armed satellite  ·  "
         "Houthis say Saudi air strikes in Yemen killed or wounded more than 25 people")
y = draw_lines(wrap(brief, bf, CW - bw), MARGIN + bw, y, bf, BODY, 23)
y += 8
y = rule(y, 4) + 7
draw_tracked_center("ONE DAY  ·  ONE IMAGE  ·  24 NOVEMBER 2026", y, F(SANS_B, 16), GRAY, tracking=4)

print("bottom edge used:", y + 24, "of", H)
img.save("/home/hatch/workspace/makefun-trial/entry/entry.png", optimize=True)
print("saved")
