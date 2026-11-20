"""Draw a one-day world news summary as a cute pastel 1024x1024 poster."""

import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
MARGIN = 32
HEADER_HEIGHT = 150
GAP = 20
FOOTER_HEIGHT = 44

CREAM = "#FFF7ED"
PINK = "#FFD9E8"
PLUM = "#4A2C3A"
SLATE = "#2B2B3A"
MUTED = "#665A67"
CARD_TINTS = ["#FFE9F2", "#E3F0FF", "#E2F7E8", "#EFE7FF", "#FFEEDD", "#FFF6CC"]

HEADLINE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BODY_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

STORIES = [
    (
        "Three-way summit in Shenzhen",
        "Trump, Xi and Putin meet for the first time; talks on nuclear risks to continue.",
    ),
    (
        "World court: Myanmar committed genocide",
        "The ICJ rules against Myanmar over the Rohingya in The Hague.",
    ),
    (
        "Crimean Bridge hit a third time",
        "Ukraine strikes the rail section; train traffic halted.",
    ),
    (
        "Israeli tanks cross Gaza ceasefire line",
        "Forces push past the Yellow Line near Nuseirat.",
    ),
    (
        "Anthropic's record IPO",
        "Shares priced at $83; about $81 billion raised.",
    ),
    (
        "GTA VI is out",
        "Rockstar's game launches worldwide after 13 years.",
    ),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_to_lines(draw, text, family, start_size, max_width, max_lines, min_size):
    """Wrap text and shrink only when the requested number of lines will not fit."""
    for size in range(start_size, min_size - 1, -1):
        face = font(family, size)
        lines = textwrap.wrap(text, width=max(8, int(max_width / (size * 0.52))))
        if len(lines) <= max_lines and all(
            draw.textlength(line, font=face) <= max_width for line in lines
        ):
            return lines, face, size
    face = font(family, min_size)
    lines = textwrap.wrap(text, width=max(8, int(max_width / (min_size * 0.52))))
    return lines[:max_lines], face, min_size


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_globe(draw, cx, cy):
    """A tiny original chibi globe made only of circles, ellipses and lines."""
    radius = 51
    draw.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius),
        fill="#BFE5FF",
        outline="#8FC9EC",
        width=3,
    )
    draw.ellipse((cx - 37, cy - 28, cx - 12, cy - 3), fill="#9BD8A8")
    draw.ellipse((cx + 8, cy + 7, cx + 34, cy + 30), fill="#9BD8A8")
    draw.ellipse((cx - 4, cy - 38, cx + 13, cy - 22), fill="#9BD8A8")
    draw.ellipse((cx - 30, cy - 6, cx - 19, cy + 2), fill=PLUM)
    draw.ellipse((cx + 17, cy - 6, cx + 28, cy + 2), fill=PLUM)
    draw.ellipse((cx - 40, cy + 5, cx - 29, cy + 14), fill="#FF9FBC")
    draw.ellipse((cx + 28, cy + 5, cx + 39, cy + 14), fill="#FF9FBC")

    draw.line((cx - 49, cy + 12, cx - 68, cy + 26), fill="#8FC9EC", width=5)
    draw.line((cx + 49, cy + 12, cx + 68, cy + 26), fill="#8FC9EC", width=5)
    draw.arc((cx - 17, cy + 5, cx + 17, cy + 28), 15, 165, fill=PLUM, width=3)

    draw.polygon(
        [(cx - 19, cy - 52), (cx, cy - 62), (cx - 6, cy - 43)],
        fill="#FF9FBC",
    )
    draw.polygon(
        [(cx + 19, cy - 52), (cx, cy - 62), (cx + 6, cy - 43)],
        fill="#FF9FBC",
    )
    draw.ellipse((cx - 8, cy - 62, cx + 8, cy - 46), fill="#FFC2D6")


def draw_icon(draw, origin_x, origin_y, index):
    """Draw one simple story icon inside a 64x64 box."""
    left, top = origin_x, origin_y
    if index == 0:
        for x, colour in (
            (left + 9, "#F49DB8"),
            (left + 27, "#8FB8EE"),
            (left + 45, "#96D9AA"),
        ):
            draw.line((x, top + 8, x, top + 54), fill=colour, width=4)
            draw.rectangle((x, top + 8, x + 13, top + 26), fill=colour)
    elif index == 1:
        gold = "#D6A64A"
        draw.line((left + 32, top + 10, left + 32, top + 52), fill=gold, width=4)
        draw.line((left + 11, top + 48, left + 53, top + 48), fill=gold, width=4)
        draw.line((left + 10, top + 20, left + 54, top + 20), fill=gold, width=4)
        draw.line((left + 10, top + 20, left + 19, top + 44), fill=gold, width=2)
        draw.line((left + 54, top + 20, left + 45, top + 44), fill=gold, width=2)
        draw.line((left + 3, top + 44, left + 22, top + 44), fill=gold, width=3)
        draw.line((left + 42, top + 44, left + 61, top + 44), fill=gold, width=3)
    elif index == 2:
        blue = "#78A9D6"
        draw.arc((left + 8, top + 14, left + 56, top + 54), 185, 355, fill=blue, width=5)
        draw.line((left + 6, top + 48, left + 58, top + 48), fill=blue, width=4)
        for x in (left + 17, left + 32, left + 47):
            draw.line((x, top + 28, x, top + 47), fill=blue, width=3)
    elif index == 3:
        for x in range(left + 6, left + 42, 12):
            draw.line((x, top + 48, x + 8, top + 48), fill="#E8B83C", width=4)
        shield = [
            (left + 40, top + 18),
            (left + 58, top + 18),
            (left + 58, top + 34),
            (left + 49, top + 51),
            (left + 40, top + 34),
        ]
        draw.polygon(shield, outline=SLATE, width=3)
        draw.line((left + 42, top + 40, left + 56, top + 24), fill=SLATE, width=3)
    elif index == 4:
        green = "#63B48A"
        draw.line((left + 9, top + 50, left + 24, top + 36), fill=green, width=4)
        draw.line((left + 24, top + 36, left + 35, top + 42), fill=green, width=4)
        draw.line((left + 35, top + 42, left + 56, top + 14), fill=green, width=4)
        draw.line((left + 56, top + 14, left + 44, top + 13), fill=green, width=4)
        draw.line((left + 56, top + 14, left + 55, top + 26), fill=green, width=4)
    else:
        purple = "#9575D2"
        rounded(draw, (left + 5, top + 21, left + 59, top + 52), 13, purple)
        draw.line((left + 16, top + 28, left + 16, top + 45), fill="#FFF7ED", width=4)
        draw.line((left + 8, top + 36, left + 24, top + 36), fill="#FFF7ED", width=4)
        draw.ellipse((left + 37, top + 29, left + 46, top + 38), fill="#FFB2C9")
        draw.ellipse((left + 47, top + 36, left + 56, top + 45), fill="#FFE08A")


def main():
    output = Path(__file__).resolve().parent / "entry.png"
    image = Image.new("RGB", (SIZE, SIZE), CREAM)
    draw = ImageDraw.Draw(image)

    header_box = (MARGIN, MARGIN, SIZE - MARGIN, MARGIN + HEADER_HEIGHT)
    rounded(draw, header_box, 24, PINK)

    title_face = font(HEADLINE_FONT, 64)
    date_face = font(HEADLINE_FONT, 34)
    draw.text((MARGIN + 32, MARGIN + 15), "WORLD NEWS", font=title_face, fill=PLUM)
    draw.text(
        (MARGIN + 34, MARGIN + 96),
        "THURSDAY 19 NOVEMBER 2026",
        font=date_face,
        fill=PLUM,
    )
    draw_globe(draw, SIZE - MARGIN - 96, MARGIN + 75)

    grid_top = MARGIN + HEADER_HEIGHT + GAP
    grid_bottom = SIZE - MARGIN - FOOTER_HEIGHT
    card_w = (SIZE - 2 * MARGIN - GAP) // 2
    card_h = (grid_bottom - grid_top - 2 * GAP) // 3
    text_left_pad = 20
    text_right_pad = 18
    text_width = card_w - text_left_pad - text_right_pad

    for index, (headline, subline) in enumerate(STORIES):
        col, row = index % 2, index // 2
        x0 = MARGIN + col * (card_w + GAP)
        y0 = grid_top + row * (card_h + GAP)
        x1, y1 = x0 + card_w, y0 + card_h
        rounded(draw, (x0, y0, x1, y1), 24, CARD_TINTS[index])

        icon_x = x0 + 16
        icon_y = y0 + 14
        draw_icon(draw, icon_x, icon_y, index)

        text_x = x0 + text_left_pad
        text_y = y0 + 88
        head_lines, head_face, head_size = wrap_to_lines(
            draw, headline, HEADLINE_FONT, 32, text_width, 2, 22
        )
        for line in head_lines:
            draw.text((text_x, text_y), line, font=head_face, fill=SLATE)
            text_y += head_size + 6

        text_y += 10
        sub_lines, sub_face, sub_size = wrap_to_lines(
            draw, subline, BODY_FONT, 22, text_width, 2, 20
        )
        for line in sub_lines:
            draw.text((text_x, text_y), line, font=sub_face, fill=MUTED)
            text_y += sub_size + 3

        assert text_y <= y1 - 8, "card text overflows its card"

    footer = "All six stories happened or were first reported on 19 November 2026."
    footer_face = font(BODY_FONT, 19)
    draw.text(
        ((SIZE - draw.textlength(footer, font=footer_face)) / 2, SIZE - MARGIN - 31),
        footer,
        font=footer_face,
        fill=MUTED,
    )

    image.save(output, format="PNG", optimize=True)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
