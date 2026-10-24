#!/usr/bin/env python3
"""Одноразовая правка: вопросы, которые тетрадь задаёт читателю, получают место для ответа.

Что делает:
  1. «Пять вопросов» на стр. 8 — под каждым вопросом своя строка.
  2. «Проверка» на стр. 6 — три критерия становятся списком с отметками и
     переезжают ПОСЛЕ записи: сначала человек пишет просьбу, потом проверяет её.

Повторный запуск ничего не меняет (проверяет наличие id).
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"

CSS = """
    /* ── ВОПРОС И СТРОКА ОТВЕТА ПОД НИМ ───────────────────────────────────── */
    .ask-list > li { margin-bottom: 12px; }
    .ask-list .ask-q {
      font-size: 16.5px;
      line-height: 1.5;
      color: #3B474C;
      margin-bottom: 1px;
    }
    .ask-list .line-field { min-height: 38px; padding: 4px 2px 4px; }
"""

OLD_P8_LIST = """    <h2>Пять вопросов</h2>
    <ol class="num-list">
      <li><p>Что мне на самом деле нужно в этой ссоре? Не «чего я требую», а «что мне нужно».</p></li>
      <li><p>Чего я боюсь, если этого не будет?</p></li>
      <li><p>Откуда это взялось в моей жизни?</p></li>
      <li><p>Что я могу дать, не потеряв себя?</p></li>
      <li><p>Какой маленький шаг я готов сделать?</p></li>
    </ol>"""

NEW_P8_LIST = """    <h2>Пять вопросов</h2>
    <p>Ответьте по строке на каждый: из этих ответов и складываются оба овала.</p>
    <ol class="num-list ask-list">
      <li>
        <div class="ask-q">Что мне на самом деле нужно в этой ссоре? Не «чего я требую», а «что мне нужно».</div>
        <textarea class="line-field" id="l8_need" rows="1" placeholder="Мне нужно ..."></textarea>
      </li>
      <li>
        <div class="ask-q">Чего я боюсь, если этого не будет?</div>
        <textarea class="line-field" id="l8_fear" rows="1" placeholder="Боюсь, что ..."></textarea>
      </li>
      <li>
        <div class="ask-q">Откуда это взялось в моей жизни?</div>
        <textarea class="line-field" id="l8_origin" rows="1" placeholder="Это началось с ..."></textarea>
      </li>
      <li>
        <div class="ask-q">Что я могу дать, не потеряв себя?</div>
        <textarea class="line-field" id="l8_can_give" rows="1" placeholder="Могу дать ..."></textarea>
      </li>
      <li>
        <div class="ask-q">Какой маленький шаг я готов сделать?</div>
        <textarea class="line-field" id="l8_small_step" rows="1" placeholder="Один шаг: ..."></textarea>
      </li>
    </ol>"""

OLD_P6_CHECK = """    <h2>Проверка</h2>
    <ul class="key-list">
      <li>Просьба выполнима сегодня? Не «стань другим».</li>
      <li>В ней одно действие, а не список?</li>
      <li>Её можно выполнить, не отказавшись от себя?</li>
    </ul>

"""

NEW_P6_CHECK = """    <h2>Проверка</h2>
    <p>Теперь посмотрите на свою просьбу и отметьте то, что про неё верно.</p>
    <div class="tick-list">
      <label class="tick-item"><input type="checkbox" data-tick="p6_check" value="1"><span class="tick-box"></span><span>Её можно выполнить сегодня — не «стань другим»</span></label>
      <label class="tick-item"><input type="checkbox" data-tick="p6_check" value="2"><span class="tick-box"></span><span>В ней одно действие, а не список</span></label>
      <label class="tick-item"><input type="checkbox" data-tick="p6_check" value="3"><span class="tick-box"></span><span>Её можно выполнить, не отказавшись от себя</span></label>
    </div>
    <div class="line-note">Если что-то осталось пустым — вернитесь к записи и поправьте.</div>
"""

P6_AFTER_ENTRY = """    <div class="margin-note">Просьба — не слабость."""


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    if 'id="l8_need"' in html:
        print("Строки под вопросами уже есть — ничего не делаю.")
        return 0

    if html.count(OLD_P8_LIST) != 1:
        print("Не найден точный блок «Пять вопросов»", file=sys.stderr)
        return 1
    html = html.replace(OLD_P8_LIST, NEW_P8_LIST, 1)

    if html.count(OLD_P6_CHECK) != 1 or html.count(P6_AFTER_ENTRY) != 1:
        print("Не найден блок «Проверка» или место после записи", file=sys.stderr)
        return 1
    html = html.replace(OLD_P6_CHECK, "", 1)
    html = html.replace(P6_AFTER_ENTRY, NEW_P6_CHECK + "\n" + P6_AFTER_ENTRY, 1)

    css_anchor = "    /* ── КОРОТКАЯ ЗАПИСЬ: СТРОКА В КНИГЕ ──────────────────────────────────── */"
    if html.count(css_anchor) != 1:
        print("Не найден блок CSS для вставки", file=sys.stderr)
        return 1
    html = html.replace(css_anchor, CSS.strip("\n") + "\n\n" + css_anchor, 1)

    SRC.write_text(html, encoding="utf-8")
    print(f"Готово: {SRC.name}, {len(html):,} символов".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
