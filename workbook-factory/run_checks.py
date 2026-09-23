#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единая проверка фабрики тетрадей (по образцу plugin-navigator/source/build_and_test.py).

Шаги:
  1. Сборка всех спек из specs/ + встроенная валидация HTML.
  2. Синтаксис встроенного JavaScript (node --check), если node доступен.
  3. Функциональные тесты готовых тетрадей в jsdom (node test_workbook_runtime.js).
  4. Сверка центра скачиваний: base64 в index.html совпадает с файлами на диске.

Запуск:  python3 run_checks.py            (всё)
         python3 run_checks.py --quick    (только сборка и валидация)
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import build_workbook

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
INDEX = REPO_ROOT / "index.html"
NODE_MODULES = HERE / "test-runtime" / "node_modules"

ok = 0
bad = []


def report(cond: bool, label: str, extra: str = ""):
    global ok
    if cond:
        ok += 1
        print("  ✓ %s" % label)
    else:
        bad.append(label + ((" — " + extra) if extra else ""))
        print("  ✗ %s%s" % (label, (" — " + extra) if extra else ""))


def step_build() -> list[Path]:
    print("\n[1/4] Сборка спек")
    specs = sorted((HERE / "specs").glob("*.json"))
    report(bool(specs), "найдены спеки: %d" % len(specs))
    outs = []
    for spec in specs:
        res = build_workbook.build(spec)
        errs = build_workbook.validate(res)
        report(not errs, "%s → %s (%d КБ, полей %d, механик %d)"
               % (spec.name, Path(res["out"]).name, res["bytes"] // 1024, res["fields"], res["widgets"]),
               "; ".join(errs[:3]))
        outs.append(Path(res["out"]))
    return outs


def step_js_syntax(outs: list[Path]):
    print("\n[2/4] Синтаксис встроенного JS")
    node = shutil.which("node")
    if not node:
        print("  · node не найден — пропускаем")
        return
    with tempfile.TemporaryDirectory() as tmp:
        for out in outs:
            doc = out.read_text(encoding="utf-8")
            scripts = re.findall(r"<script>(.*?)</script>", doc, re.S)
            for i, sc in enumerate(scripts):
                f = Path(tmp) / ("%s_%d.js" % (out.stem, i))
                f.write_text(sc, encoding="utf-8")
                r = subprocess.run([node, "--check", str(f)], capture_output=True, text=True)
                report(r.returncode == 0, "%s · script #%d (%d строк)"
                       % (out.name, i, sc.count("\n")), r.stderr.strip()[:200])


def step_jsdom(outs: list[Path]):
    print("\n[3/4] Функциональные тесты в jsdom")
    node = shutil.which("node")
    if not node:
        print("  · node не найден — пропускаем")
        return
    if not NODE_MODULES.exists():
        print("  · нет test-runtime/node_modules — выполните: cd test-runtime && npm install jsdom@26")
        return
    r = subprocess.run([node, str(HERE / "test_workbook_runtime.js")] + [str(o) for o in outs],
                       capture_output=True, text=True, cwd=str(HERE))
    tail = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()][-6:]
    for ln in tail:
        print("    " + ln)
    report(r.returncode == 0, "jsdom-тесты прошли", "; ".join(tail[-2:]))


def step_download_center():
    print("\n[4/4] Центр скачиваний (index.html)")
    if not INDEX.exists():
        print("  · index.html не найден — пропускаем")
        return
    doc = INDEX.read_text(encoding="utf-8")
    checked = 0
    for out in sorted((REPO_ROOT / "therapy-workbooks").glob("*.html")):
        m = re.search(r"downloadB64\('([A-Za-z0-9+/=]+)', '%s', 'text/html'\)" % re.escape(out.name), doc)
        if not m:
            continue
        payload = base64.b64decode(m.group(1))
        report(payload == out.read_bytes(),
               "%s: base64 в index.html совпадает с файлом (%d байт)" % (out.name, len(payload)))
        checked += 1
    report(checked >= 2, "в центре скачиваний найдены карточки тетрадей: %d" % checked)
    report(doc.count("<div") == doc.count("</div>"), "баланс <div>/</div> в index.html",
           "%d против %d" % (doc.count("<div"), doc.count("</div>")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="только сборка и валидация")
    args = ap.parse_args()

    print("=" * 70)
    print("Проверка workbook-factory")
    print("=" * 70)
    outs = step_build()
    step_js_syntax(outs)
    if not args.quick:
        step_jsdom(outs)
        step_download_center()

    print("\n" + "-" * 70)
    print("Пройдено проверок: %d" % ok)
    if bad:
        print("Провалено: %d" % len(bad))
        for b in bad:
            print("  ✗ %s" % b)
        return 1
    print("Все проверки пройдены ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
