#!/usr/bin/env python3
"""Render review-only Edoworks compositions. These are not browser screenshots."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
SCALE = 2
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"


class Canvas:
    def __init__(self, width: int, height: int, background: str):
        self.width, self.height = width, height
        self.image = Image.new("RGB", (width * SCALE, height * SCALE), background)
        self.draw = ImageDraw.Draw(self.image)

    def font(self, size: int, bold: bool = False, serif: bool = False):
        return ImageFont.truetype(SERIF if serif else SANS_BOLD if bold else SANS, size * SCALE)

    def rect(self, x: int, y: int, w: int, h: int, fill: str, radius: int = 0, outline: str | None = None, stroke: int = 1):
        box = (x * SCALE, y * SCALE, (x + w) * SCALE, (y + h) * SCALE)
        self.draw.rounded_rectangle(box, radius * SCALE, fill=fill, outline=outline, width=stroke * SCALE)

    def line(self, x1: int, y1: int, x2: int, y2: int, color: str, width: int = 1):
        self.draw.line((x1 * SCALE, y1 * SCALE, x2 * SCALE, y2 * SCALE), fill=color, width=width * SCALE)

    def text(self, x: int, y: int, value: str, size: int, color: str, bold: bool = False, serif: bool = False):
        self.draw.text((x * SCALE, y * SCALE), value, font=self.font(size, bold, serif), fill=color, stroke_width=0)

    def lines(self, x: int, y: int, values: list[str], size: int, color: str, leading: int, bold: bool = False, serif: bool = False) -> int:
        for value in values:
            self.text(x, y, value, size, color, bold, serif)
            y += leading
        return y

    def paragraph(self, x: int, y: int, value: str, size: int, color: str, max_width: int, leading: int) -> int:
        words = value.split()
        lines: list[str] = []
        current = ""
        font = self.font(size)
        for word in words:
            trial = f"{current} {word}" if current else word
            if self.draw.textlength(trial, font=font) <= max_width * SCALE:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return self.lines(x, y, lines, size, color, leading)

    def pill(self, x: int, y: int, value: str, bg: str, fg: str, border: str | None = None, size: int = 13):
        font = self.font(size, True)
        w = int(self.draw.textlength(value, font=font) / SCALE) + 26
        self.rect(x, y, w, 32, bg, 16, border)
        self.text(x + 13, y + 7, value, size, fg, True)
        return w

    def button(self, x: int, y: int, value: str, bg: str, fg: str, border: str | None = None):
        font = self.font(15, True)
        w = int(self.draw.textlength(value, font=font) / SCALE) + 40
        self.rect(x, y, w, 48, bg, 10, border)
        self.text(x + 20, y + 15, value, 15, fg, True)
        return w

    def paste_image(self, path: Path, x: int, y: int, w: int, h: int):
        source = Image.open(path).convert("RGBA")
        source.thumbnail((w * SCALE, h * SCALE), Image.Resampling.LANCZOS)
        px = x * SCALE + (w * SCALE - source.width) // 2
        py = y * SCALE + (h * SCALE - source.height) // 2
        self.image.paste(source, (px, py), source)

    def save(self, name: str):
        image = self.image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        image.save(HERE / name, optimize=True)


def header(c: Canvas, dark: bool):
    fg = "#F7F8FF" if dark else "#171923"
    muted = "#AEB9D3" if dark else "#4C5361"
    border = "#34415D" if dark else "#D8D8DF"
    c.line(0, 72, c.width, 72, border)
    x = 64 if c.width > 600 else 24
    c.text(x, 21, "Edoworks", 25, fg, True)
    if c.width > 600:
        c.text(x + 156, 29, "software factory", 13, muted)
        c.text(c.width - 230, 29, "Work", 14, fg, True)
        c.text(c.width - 140, 29, "Notes", 14, fg)
    else:
        c.text(c.width - 116, 27, "Work  ·  Notes", 13, fg)


def footer(c: Canvas, y: int, dark: bool):
    line = "#34415D" if dark else "#D8D8DF"
    muted = "#AEB9D3" if dark else "#4C5361"
    x = 64 if c.width > 600 else 24
    c.line(x, y, c.width - x, y, line)
    c.text(x, y + 22, "© 2026 Edoworks · Foculoom LLC", 12, muted)
    if c.width > 600:
        c.text(c.width - 260, y + 22, "Portfolio   ·   Blog   ·   Privacy", 12, muted)


def home_editorial(width: int):
    mobile = width < 600
    c = Canvas(width, 1790 if mobile else 1120, "#F7F6F2")
    header(c, False)
    x = 24 if mobile else 64
    c.text(x, 110 if mobile else 142, "EDOWORKS  /  RESEARCH · BUILD · VERIFY", 12, "#5830B2", True)
    if mobile:
        c.lines(x, 151, ["Focused software,", "built with", "evidence."], 42, "#171923", 49, serif=True)
        c.paragraph(x, 320, "Edoworks researches, builds, verifies, and documents focused software. Each case study shows what exists today and what remains in qualification.", 16, "#4C5361", 340, 24)
        c.button(x, 421, "Explore the work  →", "#5830B2", "#FFFFFF")
        fx, fy, fw, fh = 24, 504, width - 48, 485
    else:
        c.lines(x, 185, ["Focused software,", "built with evidence."], 66, "#171923", 75, serif=True)
        c.paragraph(x, 365, "Edoworks researches, builds, verifies, and documents focused software. Each case study shows what exists today and what remains in qualification.", 20, "#4C5361", 600, 30)
        c.button(x, 481, "Explore the work  →", "#5830B2", "#FFFFFF")
        fx, fy, fw, fh = 730, 130, 486, 520
    c.rect(fx, fy, fw, fh, "#FFF8EA", 22, "#D7BD87")
    c.pill(fx + 24, fy + 23, "IN QUALIFICATION · NO PUBLIC DOWNLOAD", "#FFFDF7", "#71371F", "#D7BD87", 11 if mobile else 12)
    c.paste_image(HERE / "sophie-reference.png", fx + 25, fy + 63, fw - 50, 255 if mobile else 305)
    c.text(fx + 24, fy + (324 if mobile else 376), "NowNest", 31 if mobile else 34, "#28231D", True, serif=True)
    c.paragraph(fx + 24, fy + (368 if mobile else 423), "Save it for later. Return to now.", 16, "#625A50", fw - 48, 22)
    c.text(fx + 24, fy + (414 if mobile else 466), "View qualification record  →", 14, "#71371F", True)
    c.text(fx + 24, fy + fh - 34, "Original Sophie illustration · not an app screenshot", 11, "#625A50")
    sy = 1045 if mobile else 733
    c.text(x, sy, "Selected work", 29 if mobile else 34, "#171923", serif=True)
    c.text(x, sy + 51, "Every project carries its current status beside the story.", 14 if mobile else 16, "#4C5361")
    if mobile:
        cards = [(24, sy + 105, width - 48, 220), (24, sy + 343, width - 48, 245)]
    else:
        cards = [(64, sy + 113, 558, 204), (642, sy + 113, 574, 204)]
    (a, b) = cards
    c.rect(*a, "#FFFFFF", 16, "#D8D8DF")
    c.pill(a[0] + 20, a[1] + 20, "CONCEPT PREVIEW · BETA NOT OPEN", "#FFF0E8", "#873B23", "#D9AC9B", 11)
    c.text(a[0] + 20, a[1] + 67, "Mews & Woofs", 25, "#171923", True, serif=True)
    c.paragraph(a[0] + 20, a[1] + 110, "A playful pet-sound idea being tested as a concept preview.", 15, "#4C5361", a[2] - 40, 21)
    c.text(a[0] + 20, a[1] + a[3] - 35, "Open concept record  →", 14, "#5830B2", True)
    c.rect(*b, "#EDEEF3", 16, "#CFD2DC")
    c.pill(b[0] + 20, b[1] + 20, "RETIRED · NO ACTIVE OFFER", "#FFFFFF", "#4C5361", "#ADB3C0", 11)
    c.text(b[0] + 20, b[1] + 67, "Rung", 25, "#171923", True, serif=True)
    c.paragraph(b[0] + 20, b[1] + 110, "Rung was a repository-evidence audit engine built by Edoworks. It is retired and is not an active product or paid offer.", 15, "#4C5361", b[2] - 40, 21)
    c.text(b[0] + 20, b[1] + b[3] - 35, "Read archive record  →", 14, "#5830B2", True)
    footer(c, 1736 if mobile else 1080, False)
    c.save(f"editorial-home-{width}.png")


def portfolio_editorial(width: int):
    mobile = width < 600
    c = Canvas(width, 1710 if mobile else 1285, "#F7F6F2")
    header(c, False)
    x = 24 if mobile else 64
    c.text(x, 112 if mobile else 136, "PORTFOLIO  /  CURRENT STATUS", 12, "#5830B2", True)
    c.lines(x, 152 if mobile else 172, ["Work, with its", "current status."], 40 if mobile else 57, "#171923", 48 if mobile else 67, serif=True)
    c.paragraph(x, 268 if mobile else 326, "Explore current qualification work, concept experiments, and retired projects. Each record states its current availability.", 16 if mobile else 19, "#4C5361", 340 if mobile else 900, 24 if mobile else 29)
    fy = 375 if mobile else 445
    fw = width - 48 if mobile else 1152
    fh = 535 if mobile else 420
    c.rect(x, fy, fw, fh, "#FFF8EA", 20, "#D7BD87")
    if mobile:
        c.pill(x + 18, fy + 19, "IN QUALIFICATION · NO PUBLIC DOWNLOAD", "#FFFDF7", "#71371F", "#D7BD87", 11)
        c.paste_image(HERE / "sophie-reference.png", x + 18, fy + 60, fw - 36, 250)
        c.text(x + 18, fy + 310, "NowNest", 32, "#28231D", True, serif=True)
        c.paragraph(x + 18, fy + 358, "An offline iPhone and iPad app for saving an interruption without losing your place.", 15, "#625A50", fw - 36, 22)
        c.text(x + 18, fy + 449, "View qualification record  →", 14, "#71371F", True)
        c.text(x + 18, fy + 499, "Original illustration · not current app UI", 11, "#625A50")
    else:
        c.rect(x, fy, 470, fh, "#FFFDF7", 20)
        c.paste_image(HERE / "sophie-reference.png", x + 22, fy + 35, 426, 315)
        c.text(x + 28, fy + 378, "Original illustration · not current app UI", 12, "#625A50")
        bx = x + 505
        c.pill(bx, fy + 47, "01  /  IN QUALIFICATION · NO PUBLIC DOWNLOAD", "#FFFDF7", "#71371F", "#D7BD87", 12)
        c.text(bx, fy + 117, "NowNest", 44, "#28231D", True, serif=True)
        c.paragraph(bx, fy + 187, "An offline iPhone and iPad app for saving an interruption without losing your place. It keeps the current next action visible and brings saved ideas back with context.", 18, "#625A50", 575, 27)
        c.button(bx, fy + 333, "View qualification record  →", "#D99324", "#28231D")
    sy = 968 if mobile else 918
    c.text(x, sy, "Other records", 28 if mobile else 32, "#171923", serif=True)
    if mobile:
        cards = [(24, sy + 55, width - 48, 240), (24, sy + 315, width - 48, 270)]
    else:
        cards = [(64, sy + 71, 558, 211), (642, sy + 71, 574, 211)]
    a, b = cards
    c.rect(*a, "#FFFFFF", 15, "#D8D8DF")
    c.pill(a[0] + 20, a[1] + 20, "02  /  CONCEPT PREVIEW · BETA NOT OPEN", "#FFF0E8", "#873B23", "#D9AC9B", 11)
    c.text(a[0] + 20, a[1] + 70, "Mews & Woofs", 25, "#171923", True, serif=True)
    c.paragraph(a[0] + 20, a[1] + 113, "A playful pet-sound and context concept. The preview is not a shipped iOS product.", 15, "#4C5361", a[2] - 40, 21)
    c.text(a[0] + 20, a[1] + a[3] - 35, "Open concept record  →", 14, "#5830B2", True)
    c.rect(*b, "#EDEEF3", 15, "#CFD2DC")
    c.pill(b[0] + 20, b[1] + 20, "03  /  RETIRED · NO ACTIVE OFFER", "#FFFFFF", "#4C5361", "#ADB3C0", 11)
    c.text(b[0] + 20, b[1] + 70, "Rung", 25, "#171923", True, serif=True)
    c.paragraph(b[0] + 20, b[1] + 113, "Rung was a repository-evidence audit engine built by Edoworks. It is retired and is not an active product or paid offer.", 15, "#4C5361", b[2] - 40, 21)
    c.text(b[0] + 20, b[1] + b[3] - 35, "Read archive record  →", 14, "#5830B2", True)
    footer(c, 1662 if mobile else 1235, False)
    c.save(f"editorial-portfolio-{width}.png")


def home_night(width: int):
    mobile = width < 600
    c = Canvas(width, 2050 if mobile else 1485, "#0B1020")
    header(c, True)
    x = 24 if mobile else 64
    y = 104 if mobile else 126
    w = width - 48 if mobile else 1152
    h = 452 if mobile else 400
    c.rect(x, y, w, h, "#15203A", 18, "#3A4D70")
    for gx in range(x + 28, x + w, 44):
        c.line(gx, y + 14, gx, y + h - 14, "#20304C")
    c.line(x + 25, y + 31, x + w - 25, y + 31, "#45577A")
    c.text(x + 25, y + 51, "EDOWORKS     /     RESEARCH   ·   BUILD   ·   VERIFY", 11 if mobile else 13, "#AEC6FF", True)
    if mobile:
        c.lines(x + 25, y + 105, ["Focused", "software,", "built with", "evidence."], 42, "#F7F8FF", 50, bold=True)
        c.paragraph(x + 25, y + 321, "Edoworks researches, builds, verifies, and documents focused software. Case studies show what exists today.", 15, "#BCC8DD", w - 50, 22)
    else:
        c.lines(x + 34, y + 110, ["Focused software,", "built with evidence."], 65, "#F7F8FF", 79, bold=True)
        c.paragraph(x + 34, y + 291, "Edoworks researches, builds, verifies, and documents focused software. Each case study shows what exists today.", 18, "#BCC8DD", 760, 27)
        c.text(x + w - 252, y + 315, "01  RESEARCH", 14, "#AEC6FF", True)
        c.text(x + w - 252, y + 342, "02  BUILD", 14, "#AEC6FF", True)
        c.text(x + w - 252, y + 369, "03  VERIFY", 14, "#AEC6FF", True)
    fy = 598 if mobile else 571
    fh = 600 if mobile else 460
    c.rect(x, fy, w, fh, "#FFF8EA", 16, "#D7BD87")
    if mobile:
        c.text(x + 22, fy + 26, "01  /  CURRENT WORK", 12, "#71371F", True)
        c.pill(x + 22, fy + 61, "IN QUALIFICATION · NO PUBLIC DOWNLOAD", "#FFFDF7", "#71371F", "#D7BD87", 11)
        c.paste_image(HERE / "sophie-reference.png", x + 16, fy + 104, w - 32, 220)
        c.text(x + 22, fy + 330, "NowNest", 33, "#28231D", True)
        c.paragraph(x + 22, fy + 378, "Save it for later. Return to now. An offline iPhone and iPad app for saving an interruption without losing your place.", 15, "#625A50", w - 44, 22)
        c.button(x + 22, fy + 491, "View qualification record  →", "#D99324", "#28231D")
        c.text(x + 22, fy + 564, "Original Sophie illustration · not app UI", 11, "#625A50")
    else:
        c.text(x + 34, fy + 33, "01  /  CURRENT WORK", 13, "#71371F", True)
        c.pill(x + 34, fy + 78, "IN QUALIFICATION · NO PUBLIC DOWNLOAD", "#FFFDF7", "#71371F", "#D7BD87", 12)
        c.text(x + 34, fy + 139, "NowNest", 52, "#28231D", True)
        c.paragraph(x + 34, fy + 226, "Save it for later. Return to now. An offline iPhone and iPad app for saving an interruption without losing your place.", 19, "#625A50", 540, 28)
        c.button(x + 34, fy + 356, "View qualification record  →", "#D99324", "#28231D")
        c.paste_image(HERE / "sophie-reference.png", x + 680, fy + 46, 430, 330)
        c.text(x + 740, fy + 417, "Original illustration · not current app UI", 12, "#625A50")
    sy = 1254 if mobile else 1082
    c.text(x, sy, "More from the factory", 30 if mobile else 36, "#F7F8FF", True)
    if mobile:
        cards = [(24, sy + 65, width - 48, 240), (24, sy + 325, width - 48, 275)]
    else:
        cards = [(64, sy + 85, 558, 205), (642, sy + 85, 574, 205)]
    a, b = cards
    c.rect(*a, "#2B1B29", 15, "#754C59")
    c.text(a[0] + 20, a[1] + 25, "02   CONCEPT PREVIEW · BETA NOT OPEN", 11, "#FFD0BE", True)
    c.text(a[0] + 20, a[1] + 69, "Mews & Woofs", 27, "#F7F8FF", True)
    c.paragraph(a[0] + 20, a[1] + 120, "A playful pet-sound idea being tested as a concept preview.", 15, "#E5C6CC", a[2] - 40, 22)
    c.text(a[0] + 20, a[1] + a[3] - 35, "Open concept record  →", 14, "#FFD0BE", True)
    c.rect(*b, "#17243B", 15, "#506180")
    c.text(b[0] + 20, b[1] + 25, "03   RETIRED · NO ACTIVE OFFER", 11, "#AEC6FF", True)
    c.text(b[0] + 20, b[1] + 69, "Rung", 27, "#F7F8FF", True)
    c.paragraph(b[0] + 20, b[1] + 120, "Rung was a repository-evidence audit engine built by Edoworks. It is retired and is not an active product or paid offer.", 15, "#BCC8DD", b[2] - 40, 22)
    c.text(b[0] + 20, b[1] + b[3] - 35, "Read archive record  →", 14, "#AEC6FF", True)
    footer(c, 2005 if mobile else 1440, True)
    c.save(f"night-home-{width}.png")


def portfolio_night(width: int):
    mobile = width < 600
    c = Canvas(width, 1840 if mobile else 1420, "#0B1020")
    header(c, True)
    x = 24 if mobile else 64
    c.text(x, 111 if mobile else 135, "PORTFOLIO  /  CURRENT STATUS", 12, "#AEC6FF", True)
    c.lines(x, 151 if mobile else 171, ["Work, with its", "current status."], 42 if mobile else 62, "#F7F8FF", 50 if mobile else 73, bold=True)
    c.paragraph(x, 268 if mobile else 333, "Current qualification work, concept experiments, and retired projects. Every record states its current availability.", 16 if mobile else 19, "#BCC8DD", 340 if mobile else 910, 24 if mobile else 29)
    fy = 373 if mobile else 446
    fw = width - 48 if mobile else 1152
    fh = 600 if mobile else 430
    c.rect(x, fy, fw, fh, "#FFF8EA", 16, "#D7BD87")
    if mobile:
        c.text(x + 19, fy + 19, "01 / NOW IN QUALIFICATION", 12, "#71371F", True)
        c.pill(x + 19, fy + 54, "NO PUBLIC DOWNLOAD", "#FFFDF7", "#71371F", "#D7BD87", 11)
        c.paste_image(HERE / "sophie-reference.png", x + 15, fy + 95, fw - 30, 245)
        c.text(x + 19, fy + 343, "NowNest", 34, "#28231D", True)
        c.paragraph(x + 19, fy + 393, "An offline iPhone and iPad app for saving an interruption without losing your place.", 15, "#625A50", fw - 38, 22)
        c.button(x + 19, fy + 490, "View qualification record  →", "#D99324", "#28231D")
        c.text(x + 19, fy + 562, "Original illustration · not app UI", 11, "#625A50")
    else:
        c.text(x + 34, fy + 31, "01 / NOW IN QUALIFICATION", 13, "#71371F", True)
        c.pill(x + 34, fy + 76, "NO PUBLIC DOWNLOAD", "#FFFDF7", "#71371F", "#D7BD87", 12)
        c.text(x + 34, fy + 139, "NowNest", 51, "#28231D", True)
        c.paragraph(x + 34, fy + 229, "An offline iPhone and iPad app for saving an interruption without losing your place. The next action stays visible.", 19, "#625A50", 535, 28)
        c.button(x + 34, fy + 350, "View qualification record  →", "#D99324", "#28231D")
        c.paste_image(HERE / "sophie-reference.png", x + 670, fy + 42, 436, 322)
        c.text(x + 720, fy + 392, "Original illustration · not current app UI", 12, "#625A50")
    sy = 1030 if mobile else 939
    c.text(x, sy, "Archive & experiments", 29 if mobile else 34, "#F7F8FF", True)
    if mobile:
        cards = [(24, sy + 65, width - 48, 250), (24, sy + 335, width - 48, 280)]
    else:
        cards = [(64, sy + 87, 558, 235), (642, sy + 87, 574, 235)]
    a, b = cards
    c.rect(*a, "#2B1B29", 15, "#754C59")
    c.text(a[0] + 22, a[1] + 28, "02 / CONCEPT PREVIEW · BETA NOT OPEN", 11, "#FFD0BE", True)
    c.text(a[0] + 22, a[1] + 75, "Mews & Woofs", 28, "#F7F8FF", True)
    c.paragraph(a[0] + 22, a[1] + 129, "A playful pet-sound and context concept. The preview is not a shipped iOS product.", 15, "#E5C6CC", a[2] - 44, 22)
    c.text(a[0] + 22, a[1] + a[3] - 36, "Open concept record  →", 14, "#FFD0BE", True)
    c.rect(*b, "#17243B", 15, "#506180")
    c.text(b[0] + 22, b[1] + 28, "03 / RETIRED · NO ACTIVE OFFER", 11, "#AEC6FF", True)
    c.text(b[0] + 22, b[1] + 75, "Rung", 28, "#F7F8FF", True)
    c.paragraph(b[0] + 22, b[1] + 129, "Rung was a repository-evidence audit engine built by Edoworks. It is retired and is not an active product or paid offer.", 15, "#BCC8DD", b[2] - 44, 22)
    c.text(b[0] + 22, b[1] + b[3] - 36, "Read archive record  →", 14, "#AEC6FF", True)
    footer(c, 1795 if mobile else 1370, True)
    c.save(f"night-portfolio-{width}.png")


if __name__ == "__main__":
    for width in (390, 1280):
        home_editorial(width)
        portfolio_editorial(width)
        home_night(width)
        portfolio_night(width)
