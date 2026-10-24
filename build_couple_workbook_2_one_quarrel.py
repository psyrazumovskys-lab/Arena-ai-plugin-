#!/usr/bin/env python3
"""Собирает вторую тетрадь в один файл: подставляет иллюстрации в src.html.

Источник: therapy-workbooks/couple_workbook_2_one_quarrel.src.html
Результат: therapy-workbooks/couple_workbook_2_one_quarrel.html

Картинки лежат отдельно в therapy-workbooks/assets/, в готовый файл попадают
как base64 — тетрадь должна открываться одним файлом, без папок рядом.
"""
from __future__ import annotations

import base64
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"
OUT = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.html"
ASSETS = ROOT / "therapy-workbooks" / "assets"
FONTS = ROOT / "therapy-workbooks" / "assets" / "fonts"

IMAGES = {
    "IMG_COVER": "wb2_cover.jpg",
    "IMG_KITCHEN": "wb2_kitchen.jpg",
    "IMG_HANDS": "wb2_hands.jpg",
    "IMG_THIRTY": "wb2_thirty.jpg",
    "IMG_OVALS": "wb2_ovals.jpg",
    "IMG_SECOND": "wb2_second.jpg",
}


LATIN = (
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,"
    "U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,"
    "U+FEFF,U+FFFD"
)
CYRILLIC = "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116"

FONT_FACES = [
    ("PT Serif", "normal", 400, "pt-serif-cyrillic-400-normal.woff2", CYRILLIC),
    ("PT Serif", "normal", 400, "pt-serif-latin-400-normal.woff2", LATIN),
    ("PT Serif", "normal", 700, "pt-serif-cyrillic-700-normal.woff2", CYRILLIC),
    ("PT Serif", "normal", 700, "pt-serif-latin-700-normal.woff2", LATIN),
    ("PT Serif", "italic", 400, "pt-serif-cyrillic-400-italic.woff2", CYRILLIC),
    ("PT Serif", "italic", 400, "pt-serif-latin-400-italic.woff2", LATIN),
    ("Cormorant Garamond", "normal", 600, "cormorant-garamond-cyrillic-600-normal.woff2", CYRILLIC),
    ("Cormorant Garamond", "normal", 600, "cormorant-garamond-latin-600-normal.woff2", LATIN),
    ("Cormorant Garamond", "italic", 600, "cormorant-garamond-cyrillic-600-italic.woff2", CYRILLIC),
    ("Cormorant Garamond", "italic", 600, "cormorant-garamond-latin-600-italic.woff2", LATIN),
]


def data_uri(path: pathlib.Path) -> str:
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{payload}"


def font_css() -> str:
    """Шрифты внутрь файла: тетрадь должна открываться без интернета."""
    chunks = []
    for family, style, weight, name, ranges in FONT_FACES:
        asset = FONTS / name
        if not asset.exists():
            raise SystemExit(f"Нет файла шрифта: {asset}")
        payload = base64.b64encode(asset.read_bytes()).decode("ascii")
        chunks.append(
            "    @font-face {\n"
            f"      font-family: '{family}';\n"
            f"      font-style: {style};\n"
            f"      font-weight: {weight};\n"
            "      font-display: block;\n"
            f"      src: url(data:font/woff2;base64,{payload}) format('woff2');\n"
            f"      unicode-range: {ranges};\n"
            "    }"
        )
    return "\n".join(chunks)


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    missing = [key for key in IMAGES if "{{" + key + "}}" not in html]
    if missing:
        print("В исходнике нет меток: " + ", ".join(missing), file=sys.stderr)
        return 1

    for key, name in IMAGES.items():
        asset = ASSETS / name
        if not asset.exists():
            print(f"Нет файла иллюстрации: {asset}", file=sys.stderr)
            return 1
        html = html.replace("{{" + key + "}}", data_uri(asset))

    if "{{FONTS}}" not in html:
        print("В исходнике нет метки шрифтов {{FONTS}}", file=sys.stderr)
        return 1
    html = html.replace("{{FONTS}}", font_css())

    leftovers = [key for key in IMAGES if "{{" + key + "}}" in html]
    if leftovers or "{{" in html:
        print("Остались незаполненные метки", file=sys.stderr)
        return 1

    OUT.write_text(html, encoding="utf-8")
    size = OUT.stat().st_size
    print(f"Собрано: {OUT.relative_to(ROOT)} — {size:,} байт".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
