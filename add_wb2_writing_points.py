#!/usr/bin/env python3
"""Одноразовая правка: добавляет короткие строки и списки с отметками во вторую тетрадь.

Скрипт идемпотентен по смыслу: если строки уже вставлены, повторный запуск ничего
не сделает (проверяет наличие id). После правки .src.html нужно пересобрать
build_couple_workbook_2_one_quarrel.py.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"

CSS = """
    /* ── КОРОТКАЯ ЗАПИСЬ: СТРОКА В КНИГЕ ──────────────────────────────────── */
    .line-block {
      margin: 22px 0 26px;
    }
    .line-label {
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--sage-primary);
      margin-bottom: 5px;
    }
    .line-prompt {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 18px;
      line-height: 1.38;
      font-style: italic;
      color: #4A5459;
      margin-bottom: 4px;
    }
    .line-field {
      display: block;
      width: 100%;
      min-height: 44px;
      padding: 8px 2px 6px;
      border: none;
      border-bottom: 1px solid var(--border-color);
      border-radius: 0;
      background: transparent;
      font-family: inherit;
      font-size: 16px;
      line-height: 1.5;
      color: var(--text-main);
      resize: none;
      overflow: hidden;
    }
    .line-field + .line-field { margin-top: 10px; }
    .line-field:focus {
      outline: none;
      border-bottom-color: var(--sage-primary);
    }
    .line-field::placeholder {
      color: #A6ACAC;
      font-style: italic;
    }
    .line-block.is-written .line-field { border-bottom-color: rgba(90, 115, 101, 0.55); }
    .line-note {
      margin-top: 8px;
      font-size: 12.5px;
      line-height: 1.45;
      font-style: italic;
      color: #8A918F;
    }

    /* ── ОТМЕТКИ В СПИСКЕ ─────────────────────────────────────────────────── */
    .tick-list { margin: 6px 0 2px; }
    .tick-item {
      display: flex;
      align-items: flex-start;
      gap: 11px;
      padding: 9px 0;
      font-size: 15.5px;
      line-height: 1.45;
      color: #3B474C;
      cursor: pointer;
      position: relative;
    }
    .tick-item + .tick-item { border-top: 1px dashed rgba(226, 221, 213, 0.85); }
    .tick-item input {
      position: absolute;
      width: 1px;
      height: 1px;
      opacity: 0;
    }
    .tick-box {
      flex-shrink: 0;
      width: 17px;
      height: 17px;
      margin-top: 2px;
      border: 1.3px solid var(--sage-primary);
      border-radius: 3px;
      background: #FFFFFF;
      position: relative;
    }
    .tick-item input:checked + .tick-box {
      background: var(--sage-primary);
      border-color: var(--sage-primary);
    }
    .tick-item input:checked + .tick-box::after {
      content: '';
      position: absolute;
      left: 5px;
      top: 1px;
      width: 5px;
      height: 9px;
      border: solid #FFFFFF;
      border-width: 0 1.8px 1.8px 0;
      transform: rotate(42deg);
    }
    .tick-item input:focus-visible + .tick-box {
      outline: 2px solid var(--terracotta);
      outline-offset: 2px;
    }
"""

# ── вставки: (якорь, что вставить после якоря, id для проверки повторного запуска) ──
AFTER = []
BEFORE = []

# p1 — спокойный час для тетради
AFTER.append((
    '<li><span class="checkbox"></span><span>Если станет слишком больно — остановитесь. Тетрадь подождёт.</span></li>\n    </ul>',
    """

    <div class="line-block">
      <div class="line-label">Спокойный час</div>
      <p class="line-prompt">Когда у меня бывает час без спешки, чтобы сесть за это?</p>
      <textarea class="line-field" id="l1_quiet_hour" rows="1" placeholder="Например: суббота утром, пока все спят"></textarea>
      <div class="line-note">Эти строки сохраняются сами, кнопки нет.</div>
    </div>""",
    'l1_quiet_hour',
))

# p2 — приметы ссоры, отметки
AFTER.append((
    '<li>Проходит день-два, всё возвращается на места — до следующего раза.</li>\n    </ul>',
    """

    <div class="line-block">
      <div class="line-label">Приметы</div>
      <p class="line-prompt">Отметьте, что узнаёте про вашу ссору.</p>
      <div class="tick-list">
        <label class="tick-item"><input type="checkbox" data-tick="p2_signs" value="1"><span class="tick-box"></span><span>Могу пересказать её заранее, почти слово в слово</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p2_signs" value="2"><span class="tick-box"></span><span>Начинается с мелочи, а заканчивается темой постарше</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p2_signs" value="3"><span class="tick-box"></span><span>Знаю, чем кончится, и всё равно иду</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p2_signs" value="4"><span class="tick-box"></span><span>После неё никто не выиграл</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p2_signs" value="5"><span class="tick-box"></span><span>Через день-два всё как прежде — до следующего раза</span></label>
      </div>
    </div>""",
    'p2_signs',
))

# p3 — перенос теории на свою ссору
BEFORE.append((
    '<div class="pull-quote">Постоянные разногласия не исчезают.',
    """<div class="line-block">
      <div class="line-label">Ваша ссора</div>
      <p class="line-prompt">Перенесите на неё: что здесь решается, а что нет?</p>
      <textarea class="line-field" id="l3_solvable" rows="1" placeholder="Решается: ..."></textarea>
      <textarea class="line-field" id="l3_perpetual" rows="1" placeholder="Не решается: ..."></textarea>
    </div>

    """,
    'l3_solvable',
))

# p4 — взгляд с другой стороны
BEFORE.append((
    '<div class="folio"><span>Одна и та же ссора</span><span class="folio-page">Стр. 4 из 13</span></div>',
    """<div class="line-block">
      <p class="line-prompt">Если бы партнёр описал мой шаг в этом круге — что бы он сказал?</p>
      <textarea class="line-field" id="l4_partner_view" rows="1" placeholder="Со стороны это выглядит так: ..."></textarea>
    </div>

    """,
    'l4_partner_view',
))

# p5 — места для двух напечатанных вопросов
BEFORE.append((
    '<div class="interactive-card card-title-only ask">\n      <div class="ask-num">Запись 3</div>',
    """<div class="line-block">
      <p class="line-prompt">Две строки под эти вопросы — коротко, как есть.</p>
      <textarea class="line-field" id="l5_if_forever" rows="1" placeholder="Если это останется так навсегда, я буду..."></textarea>
      <textarea class="line-field" id="l5_what_fear" rows="1" placeholder="Если уступлю, я боюсь потерять..."></textarea>
    </div>

    """,
    'l5_if_forever',
))

# p7 — когда и где
AFTER.append((
    '<li><span class="checkbox"></span><span>Можно остановиться и вернуться.</span></li>\n    </ul>',
    """

    <div class="line-block">
      <div class="line-label">Наш разговор</div>
      <p class="line-prompt">Когда и где вы попробуете эти тридцать минут?</p>
      <textarea class="line-field" id="l7_when_day" rows="1" placeholder="День: ..."></textarea>
      <textarea class="line-field" id="l7_where" rows="1" placeholder="Где: ..."></textarea>
    </div>""",
    'l7_when_day',
))

# p7 — что будет труднее всего, отметки
BEFORE.append((
    '<figure class="figure-bleed">\n      <img src="{{IMG_THIRTY}}"',
    """<div class="line-block">
      <div class="line-label">Перед первым разговором</div>
      <p class="line-prompt">Что будет труднее всего? Отметьте — потом проверите себя.</p>
      <div class="tick-list">
        <label class="tick-item"><input type="checkbox" data-tick="p7_hardest" value="1"><span class="tick-box"></span><span>Не перебивать, пока говорит другой</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p7_hardest" value="2"><span class="tick-box"></span><span>Держаться тридцати минут и не съехать в старое</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p7_hardest" value="3"><span class="tick-box"></span><span>Говорить «я», а не «ты»</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p7_hardest" value="4"><span class="tick-box"></span><span>Не вспоминать прошлые ссоры</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p7_hardest" value="5"><span class="tick-box"></span><span>Остановиться, когда становится горячо</span></label>
      </div>
    </div>

    """,
    'p7_hardest',
))

# p9 — что хочу, чтобы поняли
BEFORE.append((
    '<div class="interactive-card card-title-only ask">\n      <div class="ask-num">Запись 6</div>',
    """<div class="line-block">
      <p class="line-prompt">Что вы хотите, чтобы партнёр понял в этом разговоре?</p>
      <textarea class="line-field" id="l9_what_understood" rows="1" placeholder="Самое главное, что должно дойти: ..."></textarea>
    </div>

    """,
    'l9_what_understood',
))

# p10 — что было в этот раз, отметки
BEFORE.append((
    '<p>И то, и другое — не приговор.',
    """<div class="line-block">
      <div class="line-label">Что было в этот раз</div>
      <p class="line-prompt">Отметьте, что заметили. Можно и то, и другое.</p>
      <div class="tick-list">
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="1"><span class="tick-box"></span><span>Прозвучало что-то новое</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="2"><span class="tick-box"></span><span>Голос повысился — и кто-то сам остановился</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="3"><span class="tick-box"></span><span>Не дошли до знакомого финала</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="4"><span class="tick-box"></span><span>Появилось конкретное действие, а не «я постараюсь»</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="5"><span class="tick-box"></span><span>Разошлись не по разным комнатам</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="6"><span class="tick-box"></span><span>Те же фразы, почти дословно</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="7"><span class="tick-box"></span><span>Один замолчал, второй говорил громче</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="8"><span class="tick-box"></span><span>Появился старый счёт: «а помнишь, ты...»</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="p10_what_happened" value="9"><span class="tick-box"></span><span>Разговор закончился усталостью, а не решением</span></label>
      </div>
    </div>

    """,
    'p10_what_happened',
))

# p11 — неделя наблюдений
AFTER.append((
    '<div class="week-caption">Достаточно одного наблюдения в день.</div>',
    """

    <div class="line-block">
      <div class="line-label">Неделя наблюдений</div>
      <p class="line-prompt">Три строки за неделю — этого достаточно.</p>
      <textarea class="line-field" id="l11_noticed" rows="1" placeholder="Один раз круг был заметен так: ..."></textarea>
      <textarea class="line-field" id="l11_helped" rows="1" placeholder="Остановиться помогло: ..."></textarea>
      <textarea class="line-field" id="l11_try" rows="1" placeholder="Во второй раз хочу попробовать: ..."></textarea>
    </div>""",
    'l11_noticed',
))

# p12 — одно изменение
BEFORE.append((
    '<p class="source-note">Если вы проходите тетрадь один',
    """<div class="line-block">
      <p class="line-prompt">Одно изменение, с которого начну — самое маленькое.</p>
      <textarea class="line-field" id="l12_one_change" rows="1" placeholder="В следующий раз я..."></textarea>
    </div>

    """,
    'l12_one_change',
))

# p13 — две строки на прощание
BEFORE.append((
    '<h2>Когда нужен специалист</h2>',
    """<div class="line-block">
      <div class="line-label">После тетради</div>
      <p class="line-prompt">Две строки на прощание.</p>
      <textarea class="line-field" id="l13_take_away" rows="1" placeholder="Забираю с собой: ..."></textarea>
      <textarea class="line-field" id="l13_not_yet" rows="1" placeholder="Пока не получается: ..."></textarea>
    </div>

    """,
    'l13_take_away',
))

JS_ANCHOR = "  window.addEventListener('DOMContentLoaded', function () {"
JS_NEW = """  // Короткие строки и отметки: сохраняются сами, без кнопки
  var LINE_PREFIX = 'wb_couples_l2_one_quarrel_line_';
  var TICK_PREFIX = 'wb_couples_l2_one_quarrel_tick_';

  function fitLine(el) {
    el.style.height = 'auto';
    el.style.height = Math.max(44, el.scrollHeight) + 'px';
  }

  function initLineField(el) {
    var block = el.closest('.line-block');
    var saved = null;
    try { saved = localStorage.getItem(LINE_PREFIX + el.id); } catch (e) {}
    if (saved) el.value = saved;
    fitLine(el);
    if (block) block.classList.toggle('is-written', !!el.value.trim());
    el.addEventListener('input', function () {
      fitLine(el);
      try { localStorage.setItem(LINE_PREFIX + el.id, el.value); } catch (e) {}
      if (block) block.classList.toggle('is-written', !!el.value.trim());
    });
  }

  function initTick(input) {
    var key = TICK_PREFIX + input.getAttribute('data-tick') + '_' + input.value;
    try { if (localStorage.getItem(key) === '1') input.checked = true; } catch (e) {}
    input.addEventListener('change', function () {
      try { localStorage.setItem(key, input.checked ? '1' : ''); } catch (e) {}
    });
  }

""" + JS_ANCHOR

INIT_ANCHOR = """      renderEntries(id);
    });
"""
INIT_NEW = """      renderEntries(id);
    });

    Array.prototype.forEach.call(document.querySelectorAll('.line-field'), initLineField);
    Array.prototype.forEach.call(document.querySelectorAll('.tick-item input'), initTick);
"""

MOBILE_ANCHOR = """      .entry-hint { font-size: 14.5px; }"""
MOBILE_NEW = """      .entry-hint { font-size: 14.5px; }
      .line-field { font-size: 16.5px; min-height: 48px; }
      .line-prompt { font-size: 18.5px; }
      .tick-item { font-size: 16px; padding: 11px 0; }
      .tick-box { width: 19px; height: 19px; }"""


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    if 'id="l1_quiet_hour"' in html:
        print("Строки уже добавлены — ничего не делаю.")
        return 0

    for anchor, insert, marker in AFTER:
        if html.count(anchor) != 1:
            print(f"Якорь встречается {html.count(anchor)} раз: {anchor[:60]}", file=sys.stderr)
            return 1
        html = html.replace(anchor, anchor + insert, 1)

    for anchor, insert, marker in BEFORE:
        if html.count(anchor) != 1:
            print(f"Якорь встречается {html.count(anchor)} раз: {anchor[:60]}", file=sys.stderr)
            return 1
        html = html.replace(anchor, insert + anchor, 1)

    css_anchor = "    /* ── ПЛАВКАЯ ПЛАШКА ────────────────────────────────────────────────────── */"
    if css_anchor not in html:
        print("Не найден блок CSS для вставки", file=sys.stderr)
        return 1
    html = html.replace(css_anchor, CSS.strip("\n") + "\n\n" + css_anchor, 1)

    if html.count(JS_ANCHOR) != 1 or html.count(INIT_ANCHOR) != 1 or html.count(MOBILE_ANCHOR) != 1:
        print("Не найдено место для скрипта или мобильных стилей", file=sys.stderr)
        return 1
    html = html.replace(JS_ANCHOR, JS_NEW, 1)
    html = html.replace(INIT_ANCHOR, INIT_NEW, 1)
    html = html.replace(MOBILE_ANCHOR, MOBILE_NEW, 1)

    SRC.write_text(html, encoding="utf-8")
    print(f"Готово: {SRC.name}, {len(html):,} символов".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
