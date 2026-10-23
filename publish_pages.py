#!/usr/bin/env python3
"""Копирует тетрадь в папку docs/ — то, что публикуется на GitHub Pages.

Зачем: страницы сайта сейчас собираются только из папки docs/.
Там лежит один файл — рабочая тетрадь, которую отдаёт бот. Всё
остальное (другие тетради, PDF, уровни 2 и 3) на сайте не видно.

Запуск после любой правки тетради:
    python3 publish_pages.py

Проверка, что копия не отстала:
    python3 publish_pages.py --check
"""

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "therapy-workbooks" / "couple_workbook_1_stop_escalation.html"
TARGET = ROOT / "docs" / "couple_workbook_1_stop_escalation.html"


def main() -> int:
    if not SOURCE.exists():
        print(f"Нет исходника: {SOURCE}")
        return 1

    if "--check" in sys.argv:
        if not TARGET.exists():
            print("В docs/ нет копии тетради.")
            return 1
        if filecmp.cmp(SOURCE, TARGET, shallow=False):
            print("Копия в docs/ совпадает с исходником.")
            return 0
        print("Копия в docs/ отстала. Запустите: python3 publish_pages.py")
        return 1

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    size = TARGET.stat().st_size
    print(f"Опубликовано: docs/{TARGET.name} ({size:,} байт)".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
