#!/usr/bin/env python3
"""Собирает текст второй тетради для чтения и правок (тот, что лежит в Drive документом).

Источник: therapy-workbooks/couple_workbook_2_one_quarrel.src.html
Результат: therapy-workbooks/couple_workbook_2_one_quarrel_TEXT.txt

Зачем: тетрадь удобно читать с телефона, но в HTML поля ввода и картинки мешают
вычитывать текст. Здесь тот же текст построчно, со служебными пометками в квадратных
скобках: глава, где стоит иллюстрация, где начинается запись и что в ней за подсказка.
"""
from __future__ import annotations

import html as html_mod
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"
OUT = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel_TEXT.txt"


def clean(chunk: str) -> str:
    def running_head(m: re.Match) -> str:
        left = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        right = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        return f"\n[{left} · {right}]\n"

    chunk = re.sub(
        r'<div class="running-head">(.*?)<span class="rh-right">(.*?)</span>\s*</div>',
        running_head, chunk, flags=re.S,
    )
    chunk = re.sub(r"<svg[\s\S]*?</svg>", "", chunk)
    chunk = re.sub(r'<div class="entry-list"[\s\S]*?</div>\s*</div>', "", chunk)
    chunk = re.sub(r'<div class="page-footer-nav">[\s\S]*?</div>\s*</div>', "", chunk)
    chunk = re.sub(r'<a class="btn-cover-start"[^>]*>[^<]*</a>', "", chunk)

    chunk = re.sub(r'<figure class="figure-bleed">', "\n[ИЛЛЮСТРАЦИЯ во всю ширину] ", chunk)
    chunk = re.sub(r'<figure class="figure-plate">', "\n[ИЛЛЮСТРАЦИЯ, врезка] ", chunk)
    chunk = re.sub(r"<figcaption>", "\n  подпись: ", chunk)

    chunk = re.sub(r'<div class="entry-kind[^"]*">.*?</span></div>',
                   lambda m: "\nЗАПИСЬ — " + ("Вместе с партнёром" if "kind-pair" in m.group(0) else "Индивидуально"),
                   chunk, flags=re.S)
    chunk = re.sub(r'<span class="entry-hint">', "\n  подсказка: ", chunk)
    chunk = re.sub(r'<textarea class="journal-entry"[^>]*placeholder="([^"]*)"[^>]*>\s*</textarea>',
                   lambda m: "\n  поле: " + html_mod.unescape(m.group(1)).replace("&#10;", " / ") + "\n",
                   chunk)
    chunk = re.sub(r'<textarea class="line-field"[^>]*placeholder="([^"]*)"[^>]*>\s*</textarea>',
                   lambda m: "\n  строка: " + html_mod.unescape(m.group(1)) + "\n", chunk)
    chunk = re.sub(r'<button[^>]*class="btn-save-entry"[^>]*>.*?</button>', "", chunk, flags=re.S)

    chunk = re.sub(r'<div class="week-line">[\s\S]*?</div>', "", chunk)
    chunk = re.sub(r'<div class="folio">[\s\S]*?<span class="folio-page">(.*?)</span>\s*</div>',
                   lambda m: "\n[" + m.group(1) + "]\n", chunk)
    chunk = re.sub(r'<div class="line-label">', "\n", chunk)
    chunk = re.sub(r'<div class="line-prompt">', "\n", chunk)
    chunk = re.sub(r'<div class="quote-label[^"]*">', "\n  ", chunk)
    chunk = re.sub(r'<div class="ask-num">', "\n", chunk)
    chunk = re.sub(r'<div class="bridge-label">', "\n", chunk)
    chunk = re.sub(r'<div class="fact-label">', "\n", chunk)
    chunk = re.sub(r'<div class="protocol-time">', "\n", chunk)
    chunk = re.sub(r'<div class="part-num">', "\nЧАСТЬ ", chunk)
    chunk = re.sub(r'<span class="chapter-fig">', "", chunk)
    chunk = re.sub(r'<span class="chapter-kicker">', "", chunk)

    def tick(m: re.Match) -> str:
        return "\n  [ ] " + re.sub(r"<[^>]+>", "", m.group(1)).strip()

    chunk = re.sub(r'<label class="tick-item">[\s\S]*?<span class="tick-box"></span><span>(.*?)</span></label>',
                   tick, chunk)

    chunk = re.sub(r"<br\s*/?>", "\n", chunk)
    chunk = re.sub(r"</(p|h1|h2|h3|h4|li|figcaption|div|span|text)>", "\n", chunk)
    chunk = re.sub(r"<[^>]+>", "", chunk)
    chunk = html_mod.unescape(chunk).replace("\u00a0", " ")

    lines = [re.sub(r"[ \t]+", " ", line).rstrip() for line in chunk.split("\n")]
    out, blank = [], 0
    for line in lines:
        if not line.strip():
            blank += 1
            if blank > 1:
                continue
            out.append("")
        else:
            blank = 0
            out.append(line.strip())
    text = "\n".join(out).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def main() -> int:
    src = SRC.read_text(encoding="utf-8")
    body = src[src.find('<div class="container">'):]
    body = body[:body.find('<div class="save-indicator"')]

    parts = re.split(r'<div class="page-card[^"]*" id="(p\d+)">', body)
    pages = [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2)]

    out = [
        "ОДНА И ТА ЖЕ ССОРА",
        "Тетрадь для пар · Уровень 2",
        "",
        "ТЕКСТ ДЛЯ ЧТЕНИЯ И ПРАВОК",
        "Это не сама тетрадь, а её текст — чтобы читать с телефона и отмечать, что поправить.",
        "Рабочая версия с картинками, кнопками и сохранением записей — файл «05_Тетрадь_Одна_и_та_же_ссора.html».",
        "",
        "Как читать пометки: [в квадратных скобках] — служебное (глава, иллюстрация). «ЗАПИСЬ» — большое поле "
        "с кнопкой и накоплением записей. «строка» — короткая линия, которая сохраняется сама. «[ ]» — пункт, "
        "который читатель отмечает галочкой.",
        "",
        "=" * 60,
    ]

    for i, (pid, chunk) in enumerate(pages):
        out += ["", "ОБЛОЖКА" if pid == "p0" else f"СТРАНИЦА {pid[1:]}", "", clean(chunk), ""]
        if i != len(pages) - 1:
            out.append("=" * 60)

    text = "\n".join(out) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print(f"Готово: {OUT.name} — {len(text):,} символов".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
