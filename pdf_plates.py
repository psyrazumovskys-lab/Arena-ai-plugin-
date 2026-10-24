#!/usr/bin/env python3
"""Иллюстрации для печатных книжечек: бумага страницы и мягкий край.

Картинки из тетради нарисованы на своей бумаге, чуть отличающейся от бумаги
страницы. Здесь два шага, общих для обеих книжечек:

- `on_cream` перекрашивает подложку кадра в цвет бумаги (out = cream + (v - paper));
- `feather_mask` растворяет края в прозрачность, чтобы на печати не было
  видно прямоугольника кадра.

Сама иллюстрация при этом не обрезается и не растягивается.
"""
from __future__ import annotations

import pathlib

from PIL import Image

CREAM = (247, 245, 240)


def on_cream(path: pathlib.Path, out_dir: pathlib.Path) -> pathlib.Path:
    out = out_dir / f"cream_{path.stem}.jpg"
    if out.exists():
        return out
    out_dir.mkdir(parents=True, exist_ok=True)
    im = Image.open(path).convert("RGB")
    w, h = im.size
    k = max(2, int(min(w, h) * 0.02))
    px = im.load()
    samples = [px[x, k] for x in range(0, w, max(1, w // 40))]
    samples += [px[x, h - 1 - k] for x in range(0, w, max(1, w // 40))]
    samples += [px[k, y] for y in range(0, h, max(1, h // 40))]
    samples += [px[w - 1 - k, y] for y in range(0, h, max(1, h // 40))]
    paper = [max(1, sum(s[i] for s in samples) // len(samples)) for i in range(3)]
    lut = []
    for i in range(3):
        shift = CREAM[i] - paper[i]
        lut += [max(0, min(255, v + shift)) for v in range(256)]
    im.point(lut).save(out, quality=92, optimize=True)
    return out


def feather_mask(path: pathlib.Path, out_dir: pathlib.Path, size=(0, 0)) -> Image.Image:
    """Мягкая рамка: края картинки растворяются в бумаге страницы."""
    cache_dir = out_dir / "feather"
    cache_dir.mkdir(parents=True, exist_ok=True)
    iw, ih = size if size[0] else Image.open(path).size
    cached = cache_dir / f"{path.stem}_{iw}x{ih}.png"
    if cached.exists():
        return Image.open(cached)
    sw, sh = 220, max(1, int(220 * ih / iw))
    band = 0.055
    alpha = Image.new("L", (sw, sh), 255)
    px = alpha.load()
    for yy in range(sh):
        ay = min(1.0, (min(yy, sh - 1 - yy) / sh) / band)
        for xx in range(sw):
            a = min(ay, min(1.0, (min(xx, sw - 1 - xx) / sw) / band))
            if a < 1.0:
                px[xx, yy] = int(255 * (a ** 1.35)) if a > 0 else 0
    alpha = alpha.resize((iw, ih), Image.LANCZOS)
    alpha.save(cached)
    return alpha
