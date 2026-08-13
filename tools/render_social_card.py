"""Render assets/img/social-card.png -- the og:image for link previews.

1200x630 is the size Slack, Teams, LinkedIn and X all crop from. The card is
drawn rather than photographed so the group name stays legible at the ~500px
width most feeds actually display.

The mark is main_logo.svg's geometry in cream on the brand teal -- transcribed
1:1 from that file, so mirror any change to it here. Rendered at 2x and
downsampled: Pillow antialiases text but not the geometry.

Type is Segoe UI because the site's Roboto/Roboto Slab are webfonts and are not
installed locally. If you ever have Roboto Slab on hand, point TITLE_FONT at it
for an exact match with the site's headings.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

TEAL = (0x0F, 0x4A, 0x54, 255)
CREAM = (0xF7, 0xF5, 0xEF, 255)
GOLD = (0xC1, 0x80, 0x2B, 255)

S = 2                      # supersample factor
W, H = 1200 * S, 630 * S

TITLE_FONT = "C:/Windows/Fonts/segoeuib.ttf"
BODY_FONT = "C:/Windows/Fonts/segoeui.ttf"

# The mark, in main_logo.svg's 200-unit space, placed on the card.
MARK_SIZE = 340 * S
MARK_X, MARK_Y = 96 * S, 145 * S
U = MARK_SIZE / 200.0

RING_R = 88.0
ARCS = [(20.97, 137.81), (155.78, 363.00)]
NODES = [(54.0, 60.0), (100.0, 46.0), (146.0, 60.0)]
FEET = [(72.0, 138.4), (128.0, 140.7)]


def p(x, y):
    return (MARK_X + x * U, MARK_Y + y * U)


def stroke(draw, pts, colour, width_units):
    w = width_units * U
    xy = [p(x, y) for x, y in pts]
    draw.line(xy, fill=colour, width=max(1, int(round(w))))
    r = w / 2.0
    for cx, cy in xy:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)


def arc_points(a0, a1, step=0.5):
    n = max(2, int(abs(a1 - a0) / step))
    return [
        (
            100 + RING_R * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            100 + RING_R * math.sin(math.radians(a0 + (a1 - a0) * i / n)),
        )
        for i in range(n + 1)
    ]


def draw_mark(base):
    d = ImageDraw.Draw(base)
    for a0, a1 in ARCS:
        stroke(d, arc_points(a0, a1), CREAM, 7)

    rays = Image.new("RGBA", base.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    for node in NODES:
        for foot in FEET:
            stroke(rd, [node, foot], CREAM, 2.5)
    rays.putalpha(rays.getchannel("A").point(lambda v: int(v * 0.85)))
    base.alpha_composite(rays)

    stroke(d, [(8.0, 156.0), (60.0, 134.0), (104.0, 150.0), (192.0, 116.0)], GOLD, 7)
    for cx, cy in NODES:
        x, y = p(cx, cy)
        r = 9 * U
        d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM)


def main():
    card = Image.new("RGBA", (W, H), TEAL)
    draw_mark(card)
    d = ImageDraw.Draw(card)

    title = ImageFont.truetype(TITLE_FONT, 68 * S)
    # 25px keeps the longest tagline line clear of the right edge; some feeds
    # crop the card slightly, so it should not run to the bleed.
    body = ImageFont.truetype(BODY_FONT, 25 * S)

    x = 512 * S
    y = 186 * S
    for line in ("Multimodal Spatial", "Imaging Group"):
        d.text((x, y), line, font=title, fill=CREAM)
        y += 82 * S

    y += 22 * S
    d.rounded_rectangle([x, y, x + 128 * S, y + 5 * S], radius=3 * S, fill=GOLD)

    y += 34 * S
    muted = CREAM[:3] + (215,)
    for line in ("Department of Geomatics Engineering",
                 "Schulich School of Engineering \u00b7 University of Calgary"):
        d.text((x, y), line, font=body, fill=muted)
        y += 40 * S

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    card.convert("RGB").resize((1200, 630), Image.LANCZOS).save(
        os.path.join(out, "assets", "img", "social-card.png")
    )
    print("done")


if __name__ == "__main__":
    main()
