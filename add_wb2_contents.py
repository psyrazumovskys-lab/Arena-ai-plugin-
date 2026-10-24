#!/usr/bin/env python3
"""Добавляет во вторую тетрадь страницу «Содержание» с временем и пометкой «вдвоём».

Номера страниц подставляет finalize_wb2_pages.py после перенумерации.
Повторный запуск безопасен: если страница уже есть, скрипт ничего не делает.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"

CSS = """
    /* ── СОДЕРЖАНИЕ ─────────────────────────────────────────── */
    .contents-list {
      list-style: none;
      margin: 6mm 0 0;
      padding: 0;
      font-size: 15px;
    }
    .contents-list li {
      display: grid;
      grid-template-columns: 1fr auto auto;
      align-items: baseline;
      gap: 6px;
      padding: 2.2mm 0;
      border-bottom: 0.4pt dotted #C9C3B8;
    }
    .contents-list li:last-child { border-bottom: none; }
    .contents-list li.toc-part { border-bottom: none; padding-bottom: 0; display: block; }
    .toc-title { color: #2C3539; }
    .toc-note {
      display: block;
      font-size: 12px;
      letter-spacing: 0.04em;
      color: #8A8578;
      margin-top: 1mm;
    }
    .toc-min {
      font-size: 12px;
      color: #8A8578;
      min-width: 10mm;
      text-align: right;
    }
    .toc-page {
      font-variant-numeric: tabular-nums;
      color: #5A7365;
      min-width: 8mm;
      text-align: right;
    }
    .toc-part {
      list-style: none;
      margin: 5mm 0 1mm;
      padding: 0;
      font-size: 11px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #A95F4C;
    }
"""

# Заголовок → (время, можно ли одному, пометка)
META = {
    "Если у вас 15 минут": ("15 мин", True, "Три вещи, из которых состоит всё остальное"),
    "Эта тетрадь — про одну ссору": ("4 мин", True, "Зачем она и как ей пользоваться"),
    "Если это не ссора": ("3 мин", True, "Когда тетрадь не подходит"),
    "Та самая ссора": ("5 мин", True, ""),
    "Почему она возвращается": ("5 мин", True, ""),
    "Круг, в который вы попадаете": ("6 мин", True, ""),
    "Если ваш круг другой": ("4 мин", True, "Если вы не узнали себя в схеме"),
    "Что каждый защищает": ("5 мин", True, ""),
    "Упрёк и просьба": ("6 мин", True, ""),
    "Тридцать минут": ("7 мин", True, "Рамка для разговора"),
    "Два овала": ("5 мин", True, ""),
    "Первый разговор": ("6 мин", False, "Вдвоём или одному"),
    "Как прошло": ("5 мин", True, ""),
    "Между встречами": ("4 мин", True, ""),
    "Второй разговор": ("6 мин", False, "Вдвоём или одному"),
    "Что дальше": ("4 мин", True, ""),
    "Вернитесь через месяц": ("3 мин", True, ""),
}


def cards(html: str) -> list[tuple[str, str, int, int]]:
    marks = [(m.group(1), m.start()) for m in re.finditer(r'<div class="page-card[^"]*" id="(p\d+|pC|pQ|pM)">', html)]
    out = []
    for i, (pid, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else html.find('<div class="save-indicator"')
        seg = html[start:end]
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", seg, re.S)
        title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else ""
        out.append((pid, title, start, end))
    return out


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    if 'id="pC"' in html:
        print("Содержание уже есть — ничего не делаю.")
        return 0

    items = [(pid, title) for pid, title, _, _ in cards(html)
             if pid not in ("p0", "p1") and title in META]
    if not items:
        print("Не из чего собрать содержание", file=sys.stderr)
        return 1

    part_two = "Часть II · Попробовать"
    rows = []
    for pid, title in items:
        minutes, alone, note = META[title]
        if title == "Первый разговор":
            rows.append(f'      <li class="toc-part">{part_two}</li>')
        marks = [] if alone else ['<span class="toc-note">вдвоём</span>']
        note_html = f'<span class="toc-note">{note}</span>' if note else ""
        rows.append(
            f'      <li data-target="{pid}"><span class="toc-title">{title}'
            f'{note_html}{"".join(marks)}</span>'
            f'<span class="toc-page">—</span>'
            f'<span class="toc-min">{minutes}</span></li>'
        )

    page = f'''  <!-- СТРАНИЦА: СОДЕРЖАНИЕ -->
  <div class="page-card" id="pC">
    <div class="running-head"><span>Перед началом</span><span class="rh-right">Содержание</span></div>
    <h1>Содержание</h1>
    <p class="chapter-lead">Сколько времени занимает каждая глава и где партнёр не нужен.</p>

    <ol class="contents-list">
{chr(10).join(rows)}
    </ol>

    <p class="source-note">Время примерное: оно посчитано для человека, который читает и пишет без спешки. Главы можно проходить не по порядку — но первые две лучше прочитать до заданий.</p>

    <div class="folio"><span>Одна и та же ссора</span><span class="folio-page">Стр. 2 из 18</span></div>
    <div class="page-footer-nav">
      <a class="btn-nav-step back" href="#p2" onclick="goToPage('p2'); return false;">‹ Назад</a>
      <a class="btn-nav-step primary" href="#p3" onclick="goToPage('p3'); return false;">
        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>
        <span class="nav-sub">Важно · Если это не ссора</span>
      </a>
    </div>
  </div>

'''

    # вставляем сразу после карточки введения
    pos = html.index('<div class="page-card" id="p3">')
    # отступаем к началу строки/комментария перед карточкой
    line_start = html.rfind('\n', 0, pos) + 1
    html = html[:line_start] + page + html[line_start:]

    html = html.replace("    /* ── СТОП-БЛОК:", CSS + "\n    /* ── СТОП-БЛОК:", 1)
    SRC.write_text(html, encoding="utf-8")
    print(f"Добавлено содержание: {len(rows)} строк")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
