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

IMAGES = {
    "IMG_COVER": "wb2_cover.jpg",
    "IMG_KITCHEN": "wb2_kitchen.jpg",
    "IMG_HANDS": "wb2_hands.jpg",
    "IMG_THIRTY": "wb2_thirty.jpg",
    "IMG_OVALS": "wb2_ovals.jpg",
    "IMG_SECOND": "wb2_second.jpg",
}


def data_uri(path: pathlib.Path) -> str:
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{payload}"


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
