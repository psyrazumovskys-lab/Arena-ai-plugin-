#!/usr/bin/env python3
"""Финальная сборка второй тетради: номера страниц, переходы, оглавление, колонцифры.

Выполняется один раз после всех содержательных правок. Порядок страниц берётся
из разметки — единственный источник правды. Повторы безопасны: если страницы уже
перенумерованы и переходы верны, скрипт ничего не меняет.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"

# Время на каждую страницу и пометка «можно одной» — для оглавления.
PAGES_META = {
    "Содержание": ("2 мин", True),
    "Перед началом": ("2 мин", True),
    "Если у вас 15 минут": ("15 мин", True),
    "Если это не ссора": ("3 мин", True),
    "Та самая ссора": ("5 мин", True),
    "Почему она возвращается": ("5 мин", True),
    "Круг, в который вы попадаете": ("6 мин", True),
    "Если ваш круг другой": ("4 мин", True),
    "Что каждый защищает": ("5 мин", True),
    "Упрёк и просьба": ("6 мин", True),
    "Тридцать минут": ("7 мин", True),
    "Два овала": ("5 мин", True),
    "Первый разговор": ("6 мин", False),
    "Как прошло": ("5 мин", True),
    "Между встречами": ("4 мин", True),
    "Второй разговор": ("6 мин", False),
    "Что дальше": ("4 мин", True),
    "Вернитесь через месяц": ("3 мин", True),
}


def card_spans(html: str) -> list[tuple[str, int, int]]:
    """Возвращает (id, начало, конец) каждой карточки в порядке документа."""
    marks = [(m.group(1), m.start()) for m in re.finditer(r'<div class="page-card[^"]*" id="([^"]+)">', html)]
    spans = []
    for i, (pid, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else html.find('<div class="save-indicator"')
        spans.append((pid, start, end))
    return spans


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    spans = card_spans(html)
    if not spans:
        print("Карточки не найдены", file=sys.stderr)
        return 1

    total = len(spans) - 1  # без обложки

    # ── 1. Перенумерация id через временные метки ───────────────────────────
    old_ids = [pid for pid, _, _ in spans]
    mapping = {old: f"@@PG{i}@@" for i, old in enumerate(old_ids)}

    pattern = re.compile(r"\b(?:p\d{1,2}|pQ|pM|pS|pC)\b")

    def to_temp(m: re.Match) -> str:
        return mapping.get(m.group(0), m.group(0))

    html = pattern.sub(to_temp, html)
    for old, temp in mapping.items():
        html = html.replace(temp, f"p{old_ids.index(old)}")

    spans = card_spans(html)
    ids = [pid for pid, _, _ in spans]

    # ── 2. Переходы: вперёд по порядку, назад по порядку, последняя — в начало ──
    for i, (pid, start, end) in enumerate(spans):
        if i == 0:
            continue  # у обложки нет нижней навигации
        card = html[start:end]
        prev_id = ids[i - 1]
        next_id = ids[i + 1] if i + 1 < len(ids) else "p0"

        back_pat = re.compile(
            r'<a class="btn-nav-step back" href="#\w+" onclick="goToPage\(\'\w+\'\); return false;">'
        )
        card, n_back = back_pat.subn(
            f'<a class="btn-nav-step back" href="#{prev_id}" '
            f"onclick=\"goToPage('{prev_id}'); return false;\">",
            card, count=1,
        )
        if n_back != 1:
            print(f"В карточке {pid} нет ссылки «Назад»", file=sys.stderr)
            return 1

        fwd_pat = re.compile(
            r'<a class="btn-nav-step primary" href="#\w+" onclick="goToPage\(\'\w+\'\); return false;">'
        )
        card, n_fwd = fwd_pat.subn(
            f'<a class="btn-nav-step primary" href="#{next_id}" '
            f"onclick=\"goToPage('{next_id}'); return false;\">",
            card, count=1,
        )
        if n_fwd != 1:
            print(f"В карточке {pid} нет кнопки «Дальше»", file=sys.stderr)
            return 1

        html = html[:start] + card + html[end:]
        spans = card_spans(html)

    # ── 3. Колонцифры ──────────────────────────────────────────────────────
    counter = {"n": 0}

    def folio(m: re.Match) -> str:
        counter["n"] += 1
        return f'<span class="folio-page">Стр. {counter["n"]} из {total}</span>'

    html = re.sub(r'<span class="folio-page">Стр\. \d+ из \d+</span>', folio, html)

    # ── 4. Оглавление ──────────────────────────────────────────────────────
    options = ['          <option value="p0">Обложка</option>']
    labels = []
    for i, (pid, start, end) in enumerate(card_spans(html)):
        if i == 0:
            continue
        card = html[start:end]
        m = re.search(r"<h1[^>]*>(.*?)</h1>", card, re.S)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else f"Страница {i}"
        title = title.replace("&nbsp;", " ").replace("  ", " ")
        minutes, alone = PAGES_META.get(title, ("", True))
        label = title
        if minutes:
            label += f" · {minutes}"
        if not alone:
            label += " · вдвоём"
        labels.append((pid, title, label))
        options.append(f'          <option value="{pid}">Стр. {i} · {label}</option>')

    html = re.sub(
        r'          <option value="p0">Обложка</option>[\s\S]*?</select>',
        "\n".join(options) + "\n        </select>",
        html, count=1,
    )

    # ── 5. Номера страниц в печатном содержании ───────────────────────────
    folio_of = {pid: i for i, (pid, _, _) in enumerate(spans) if i > 0}

    def toc_page(m: re.Match) -> str:
        target = m.group(1)
        num = folio_of.get(target)
        return (f'<li data-target="{target}">'
                + m.group(2)
                + f'<span class="toc-page">{num if num else "—"}</span>'
                + m.group(3) + "</li>")

    html = re.sub(
        r'<li data-target="(p\d+)">([\s\S]*?)<span class="toc-page">[^<]*</span>([\s\S]*?)</li>',
        toc_page, html,
    )
    spans = card_spans(html)

    SRC.write_text(html, encoding="utf-8")
    print(f"Готово: {len(card_spans(html))} карточек, {total} страниц")
    for pid, title, label in labels:
        print(f"  {pid:4} {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
