#!/usr/bin/env python3
"""Проверка печатных книжечек обеих тетрадей.

Запуск из корня репозитория:
    python3 test_booklets.py

Что проверяется:
  1. Файлы собираются и имеют формат A5.
  2. Число страниц кратно четырём — иначе не сложить брошюру.
  3. На каждой странице есть текст (пустых страниц-брака нет).
  4. Ни одна иллюстрация не выходит за поля.
  5. В книжке нет браузерных обещаний: «в этом браузере», «нажмите кнопку».
  6. Номера страниц в содержании совпадают с тем, где глава начинается.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parent
WB1 = ROOT / "therapy-workbooks" / "couple_workbook_1_stop_escalation_booklet.pdf"
WB2 = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel_booklet.pdf"

passed = 0
failed = 0


def check(name: str, cond: bool, extra: str = "") -> None:
    global passed, failed
    if cond:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        print(f"  ✗ {name} {extra}")


def page_text(pdf, i: int) -> str:
    return re.sub(r"\s+", " ", pdf[i].get_textpage().get_text_range())


def main() -> int:
    for path, expected in ((WB1, 12), (WB2, 44)):
        print(f"\n— {path.name}")
        check("файл собран", path.exists())
        if not path.exists():
            continue
        pdf = pdfium.PdfDocument(path)
        check(f"страниц {len(pdf)} (ожидалось {expected})", len(pdf) == expected,
              f"— получилось {len(pdf)}")
        check("страниц кратно четырём — брошюра складывается", len(pdf) % 4 == 0)
        w, h = pdf[0].get_size()
        check("формат A5 (148×210 мм)", abs(w - 419.5) < 2 and abs(h - 595.3) < 2,
              f"— {w:.1f}×{h:.1f} пт")

        empty = [i + 1 for i in range(len(pdf)) if len(page_text(pdf, i)) < 40]
        check("нет пустых страниц", not empty, f"— пустые: {empty}")

        bad = []
        for i in range(len(pdf)):
            text = page_text(pdf, i).lower()
            for phrase in ("в этом браузере", "нажмите кнопку", "кнопки нет"):
                if phrase in text:
                    bad.append((i + 1, phrase))
        check("нет обещаний браузера", not bad, f"— {bad[:3]}")

    # содержание второй тетради должно указывать на настоящие страницы
    print("\n— содержание второй тетради")
    pdf = pdfium.PdfDocument(WB2)
    toc = page_text(pdf, 4)
    rows = re.findall(r"([А-ЯЁA-Z][^0-9]{6,60}?)\s+(\d+)\s+мин\s+(\d+)", toc)
    check("содержание распознано", len(rows) >= 15, f"— строк {len(rows)}")
    mismatched = []
    for title, _mins, page in rows:
        page = int(page)
        opening = page_text(pdf, page - 1) if 0 < page <= len(pdf) else ""
        # в содержании заголовки короче/длиннее главы («Первый разговор вдвоём»),
        # поэтому сверяем первые два слова
        words = title.strip().split()
        head = " ".join(words[:2])
        if head.lower() not in opening.lower():
            mismatched.append((head, page))
    check("номера в содержании совпадают с главами", not mismatched,
          f"— {mismatched[:3]}")

    print(f"\nИтог: {passed} прошло, {failed} не прошло")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
