#!/usr/bin/env python3
"""Шрифты внутрь файла: тетрадь должна открываться без интернета.

Общий модуль для обеих тетрадей. Берёт woff2 из therapy-workbooks/assets/fonts
и собирает @font-face с data:URI и unicode-range (латиница + кириллица).
"""
from __future__ import annotations

import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "therapy-workbooks" / "assets" / "fonts"

LATIN = (
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,"
    "U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,"
    "U+FEFF,U+FFFD"
)
CYRILLIC = "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116"

FACES = [
    ("PT Serif", "normal", 400, "pt-serif-cyrillic-400-normal.woff2", CYRILLIC),
    ("PT Serif", "normal", 400, "pt-serif-latin-400-normal.woff2", LATIN),
    ("PT Serif", "normal", 700, "pt-serif-cyrillic-700-normal.woff2", CYRILLIC),
    ("PT Serif", "normal", 700, "pt-serif-latin-700-normal.woff2", LATIN),
    ("PT Serif", "italic", 400, "pt-serif-cyrillic-400-italic.woff2", CYRILLIC),
    ("PT Serif", "italic", 400, "pt-serif-latin-400-italic.woff2", LATIN),
    ("PT Sans", "normal", 400, "pt-sans-cyrillic-400-normal.woff2", CYRILLIC),
    ("PT Sans", "normal", 400, "pt-sans-latin-400-normal.woff2", LATIN),
    ("PT Sans", "normal", 700, "pt-sans-cyrillic-700-normal.woff2", CYRILLIC),
    ("PT Sans", "normal", 700, "pt-sans-latin-700-normal.woff2", LATIN),
]


def font_css() -> str:
    chunks = []
    for family, style, weight, name, ranges in FACES:
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
