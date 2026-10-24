#!/usr/bin/env python3
"""Переводит вторую тетрадь в печатный набор: книжная антиква, лист бумаги,
тихие линейки вместо карточек, линейки-ответы как в бланке.

Запуск: python3 pass_print_style_wb2.py
Скрипт ничего не пишет, если хотя бы один якорь не найден.
"""
from __future__ import annotations

import pathlib
import sys

SRC = pathlib.Path("therapy-workbooks/couple_workbook_2_one_quarrel.src.html")

EDITS: list[tuple[str, str, str]] = []


def edit(label: str, old: str, new: str) -> None:
    EDITS.append((label, old, new))


# ── 1. ШРИФТЫ ───────────────────────────────────────────────────────────────
edit(
    "убрать внешние шрифты",
    """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <title>""",
    """  <title>""",
)

edit(
    "встроить шрифты в файл",
    "  <style>\n",
    "  <style>\n{{FONTS}}\n",
)

# ── 2. ПАЛИТРА ──────────────────────────────────────────────────────────────
edit(
    "палитра: бумага и чернила",
    """      --bg-body: #F7F5F0;
      --bg-card: #FFFFFF;
      --text-main: #2C3539;
      --text-muted: #64748B;""",
    """      --bg-body: #E8E2D6;
      --bg-card: #FFFDF8;
      --text-main: #23282A;
      --text-muted: #6E726B;""",
)

edit(
    "палитра: линейки и подложка",
    """      --border-color: #E2DDD5;
      --paper: #F7F4EC;""",
    """      --border-color: #D9D1C1;
      --paper: #F4EFE3;""",
)

# ── 3. ОСНОВА ───────────────────────────────────────────────────────────────
edit(
    "набор страницы",
    """      color: var(--text-main);
      line-height: 1.65;
      padding: 16px 12px 96px;""",
    """      color: var(--text-main);
      font-size: 17px;
      line-height: 1.6;
      padding: 10px 10px 92px;""",
)

edit("ширина листа", ".container { max-width: 680px; margin: 0 auto; }",
     ".container { max-width: 660px; margin: 0 auto; }")

# ── 4. ВЕРХНЯЯ НАВИГАЦИЯ ────────────────────────────────────────────────────
edit(
    "шапка без плашки",
    """      position: sticky;
      top: 8px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 8px 10px;
      margin-bottom: 16px;
      box-shadow: var(--shadow-sm);""",
    """      position: sticky;
      top: 0;
      z-index: 1000;
      background: var(--bg-body);
      border: none;
      border-bottom: 1px solid var(--border-color);
      border-radius: 0;
      padding: 6px 2px 7px;
      margin-bottom: 10px;""",
)

edit(
    "стрелки шапки",
    """      min-width: 38px;
      height: 38px;
      background: var(--sage-light);
      color: var(--sage-primary);
      border: 1px solid rgba(90, 115, 101, 0.2);
      border-radius: 8px;
      font-size: 16px;
      font-weight: 700;""",
    """      min-width: 44px;
      height: 44px;
      background: transparent;
      color: var(--sage-deep);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      font-size: 15px;
      font-weight: 400;""",
)

edit(
    "название страницы в шапке",
    """      height: 38px;
      appearance: none;
      -webkit-appearance: none;
      background: #FFFFFF;
      color: var(--text-main);
      border: 1.5px solid var(--sage-primary);
      border-radius: 8px;
      padding: 0 28px 0 12px;
      font-size: 13px;
      font-weight: 600;""",
    """      height: 44px;
      appearance: none;
      -webkit-appearance: none;
      background: transparent;
      color: var(--text-main);
      border: none;
      border-bottom: 1px solid var(--border-color);
      border-radius: 0;
      padding: 0 24px 0 2px;
      font-size: 14.5px;
      font-weight: 400;
      font-style: italic;""",
)

# ── 5. ЛИСТ ─────────────────────────────────────────────────────────────────
edit(
    "лист вместо карточки",
    """    .page-card {
      display: none;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 26px 22px 20px;
      box-shadow: var(--shadow-sm);
      animation: fadeIn 0.25s ease;
    }""",
    """    .page-card {
      display: none;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 30px 24px 22px;
      box-shadow: 0 1px 0 #E3DCCD, 0 8px 20px rgba(74, 60, 38, 0.05);
      animation: fadeIn 0.2s ease;
    }""",
)

# ── 6. ЗАГОЛОВКИ И ТЕКСТ ────────────────────────────────────────────────────
edit(
    "первый заголовок",
    """    h1 {
      font-size: 31px;
      line-height: 1.14;
      font-weight: 700;
      letter-spacing: -0.2px;""",
    """    h1 {
      font-size: 32px;
      line-height: 1.08;
      font-weight: 600;
      letter-spacing: 0;""",
)

edit(
    "заголовок раздела",
    """    h2 {
      font-size: 23px;
      line-height: 1.25;
      font-weight: 700;""",
    """    h2 {
      font-size: 22px;
      line-height: 1.2;
      font-weight: 600;""",
)

edit(
    "линейка над разделом",
    """      width: 26px;
      height: 2px;
      background: var(--terracotta);""",
    """      width: 18px;
      height: 1px;
      background: var(--terracotta);""",
)

edit(
    "подзаголовок",
    "    h3 { font-size: 16px; font-weight: 700; line-height: 1.35; margin-bottom: 6px; }",
    """    h3 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 19px;
      font-weight: 600;
      line-height: 1.3;
      margin-bottom: 5px;
    }""",
)

edit(
    "пометки-ярлычки",
    """      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.09em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 20px;""",
    """      font-size: 9.5px;
      font-weight: 400;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 2px;""",
)

edit(
    "основной текст",
    """    p {
      font-size: 16px;
      line-height: 1.68;
      color: #3B474C;
      margin-bottom: 15px;""",
    """    p {
      font-size: 17px;
      line-height: 1.6;
      color: #2C3335;
      margin-bottom: 11px;""",
)

edit(
    "подзаголовок главы",
    """      font-size: 19.5px;
      line-height: 1.42;
      font-style: italic;
      color: #4A5459;
      margin-bottom: 20px;""",
    """      font-size: 18px;
      line-height: 1.45;
      font-style: italic;
      color: #4E5557;
      margin-bottom: 18px;""",
)

edit(
    "буквица",
    """      font-size: 3.35em;
      line-height: 0.78;
      font-weight: 600;
      color: var(--sage-primary);
      padding: 6px 9px 0 0;""",
    """      font-size: 3.1em;
      line-height: 0.8;
      font-weight: 600;
      color: var(--sage-deep);
      padding: 5px 8px 0 0;""",
)

edit(
    "колонтитул",
    """      margin-bottom: 22px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-color);
      font-size: 9.5px;
      font-weight: 600;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #8A918F;""",
    """      margin-bottom: 20px;
      padding-bottom: 6px;
      border-bottom: 1px solid #E7E0D2;
      font-size: 9px;
      font-weight: 400;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #8B8478;""",
)

edit("правый колонтитул", ".running-head .rh-right { color: var(--sage-primary); white-space: nowrap; }",
     ".running-head .rh-right { color: var(--sage-deep); white-space: nowrap; }")

edit(
    "номер главы",
    """      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.26em;
      color: var(--terracotta);""",
    """      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.16em;
      color: var(--terracotta-deep);""",
)

edit(
    "надзаголовок главы",
    """      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--text-muted);""",
    """      font-size: 9.5px;
      font-weight: 400;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #8B8478;""",
)

# ── 7. ВРЕЗКИ ───────────────────────────────────────────────────────────────
edit(
    "врезка с фактом",
    """    .fact-box {
      background: var(--paper);
      border-left: 3px solid var(--terracotta);
      border-radius: 0 8px 8px 0;
      padding: 16px 18px;
      margin: 20px 0;
    }""",
    """    .fact-box {
      background: transparent;
      border-left: 2px solid #D5CCBA;
      border-radius: 0;
      padding: 2px 0 2px 16px;
      margin: 20px 0;
    }""",
)

edit(
    "ярлык врезки",
    """      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.09em;
      text-transform: uppercase;
      color: var(--terracotta-deep);
      margin-bottom: 8px;""",
    """      font-size: 9.5px;
      font-weight: 400;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--terracotta-deep);
      margin-bottom: 7px;""",
)

edit("текст врезки", ".fact-box p { font-size: 15.5px; line-height: 1.58; margin-bottom: 0; }",
     ".fact-box p { font-size: 16px; line-height: 1.55; margin-bottom: 0; }")

edit(
    "цитата",
    """      border-left: 2px solid var(--terracotta);
      border-radius: 0;
      padding: 4px 0 4px 18px;
      font-style: italic;
      font-size: 18px;
      line-height: 1.5;""",
    """      border-left: 1px solid #C6BBA6;
      border-radius: 0;
      padding: 3px 0 3px 16px;
      font-style: italic;
      font-size: 17.5px;
      line-height: 1.55;""",
)

edit(
    "выноска",
    """    .pull-quote {
      margin: 32px 0;
      text-align: center;
      font-size: 24px;
      line-height: 1.3;""",
    """    .pull-quote {
      margin: 26px 0;
      padding-bottom: 16px;
      border-bottom: 1px solid #E7E0D2;
      text-align: center;
      font-size: 23px;
      line-height: 1.32;""",
)

edit(
    "линейка над выноской",
    """      width: 38px;
      height: 1px;
      background: var(--terracotta);
      margin: 0 auto 18px;""",
    """      width: 26px;
      height: 1px;
      background: var(--terracotta);
      margin: 0 auto 14px;""",
)

edit(
    "пометка на полях",
    """      padding-left: 16px;
      border-left: 1px solid var(--terracotta);
      font-size: 14.5px;
      line-height: 1.55;""",
    """      padding-left: 14px;
      border-left: 1px solid #D5CCBA;
      font-size: 15.5px;
      line-height: 1.55;""",
)

# ── 8. ИЛЛЮСТРАЦИИ ──────────────────────────────────────────────────────────
edit("выход картинки за поля", "      margin: 26px -22px;", "      margin: 24px -24px;")

edit("подпись под картинкой на всю ширину", "      padding: 10px 22px 12px;\n      font-size: 14.5px;",
     "      padding: 9px 24px 11px;\n      font-size: 15px;")

edit(
    "картинка-плашка",
    """      background: #FBF8F1;
      border: 1px solid var(--border-color);
      box-shadow: 0 3px 10px rgba(44, 53, 57, 0.05);""",
    """      background: var(--bg-card);
      border: 1px solid var(--border-color);
      box-shadow: none;""",
)

edit("подпись под плашкой", "      font-size: 14px;\n      line-height: 1.35;\n      font-style: italic;\n      color: #6B7378;",
     "      font-size: 14.5px;\n      line-height: 1.4;\n      font-style: italic;\n      color: #6E7169;")

# ── 9. СПИСКИ ───────────────────────────────────────────────────────────────
edit(
    "список с ромбами",
    """      padding-left: 20px;
      margin-bottom: 11px;
      font-size: 15.5px;
      line-height: 1.55;
      color: #3B474C;""",
    """      padding-left: 18px;
      margin-bottom: 10px;
      font-size: 16.5px;
      line-height: 1.55;
      color: #2C3335;""",
)

edit(
    "ромб",
    """      left: 2px;
      top: 9px;
      width: 5px;
      height: 5px;
      background: var(--terracotta);
      transform: rotate(45deg);""",
    """      left: 2px;
      top: 11px;
      width: 4px;
      height: 4px;
      background: var(--terracotta);""",
)

edit(
    "список с галочками",
    """      gap: 10px;
      margin-bottom: 10px;
      font-size: 15.5px;
      line-height: 1.5;
      color: #3B474C;""",
    """      gap: 9px;
      margin-bottom: 9px;
      font-size: 16.5px;
      line-height: 1.52;
      color: #2C3335;""",
)

edit(
    "квадрат галочки",
    """      width: 15px;
      height: 15px;
      margin-top: 3px;
      border: 1.3px solid var(--sage-primary);
      border-radius: 2px;
      background: #FFFFFF;""",
    """      width: 14px;
      height: 14px;
      margin-top: 4px;
      border: 1px solid #B3A893;
      border-radius: 0;
      background: transparent;""",
)

edit(
    "две колонки",
    """      background: var(--sage-light);
      border: 1px solid #D6E2DA;
      border-radius: 10px;
      padding: 14px 15px;""",
    """      background: transparent;
      border: 1px solid #D5CCBA;
      border-radius: 2px;
      padding: 13px 14px;""",
)

edit("вторая колонка", "    .compare-col.alt { background: var(--terracotta-light); border-color: #EFCDB9; }",
     "    .compare-col.alt { background: transparent; border-color: #D5CCBA; }")

edit("заголовок колонки", "      font-size: 18px;\n      font-weight: 700;\n      margin-bottom: 6px;",
     "      font-size: 18px;\n      font-weight: 600;\n      margin-bottom: 5px;")

edit("текст колонки", ".compare-col p { font-size: 14.5px; line-height: 1.5; margin-bottom: 0; }",
     ".compare-col p { font-size: 15.5px; line-height: 1.52; margin-bottom: 0; }")

edit(
    "нумерация списка",
    """      left: 0;
      top: -3px;
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 30px;""",
    """      left: 0;
      top: -2px;
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 28px;""",
)

edit("заголовок пункта", ".num-list h3 { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 19px; font-weight: 700; margin-bottom: 3px; }",
     ".num-list h3 { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 19px; font-weight: 600; margin-bottom: 3px; }")

edit("текст пункта", ".num-list p { font-size: 15.5px; line-height: 1.55; margin-bottom: 0; }",
     ".num-list p { font-size: 16.5px; line-height: 1.55; margin-bottom: 0; }")

edit("время в протоколе", "      font-size: 21px;\n      line-height: 1.05;", "      font-size: 20px;\n      line-height: 1.05;")

edit(
    "подпись времени",
    """      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 9px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: #8A918F;""",
    """      font-size: 8.5px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #8B8478;""",
)

edit("текст шага протокола", ".protocol-body p { font-size: 15px; line-height: 1.55; margin-bottom: 0; }",
     ".protocol-body p { font-size: 16px; line-height: 1.55; margin-bottom: 0; }")

edit("надпись части", "      font-size: 10.5px;\n      font-weight: 700;\n      letter-spacing: 0.22em;",
     "      font-size: 9.5px;\n      font-weight: 400;\n      letter-spacing: 0.14em;")

edit("подзаголовок части", "      font-size: 17px;\n      line-height: 1.4;", "      font-size: 17.5px;\n      line-height: 1.4;")

edit("дни недели", "      font-size: 9.5px;\n      font-weight: 600;\n      letter-spacing: 0.12em;",
     "      font-size: 9px;\n      font-weight: 400;\n      letter-spacing: 0.1em;")

edit("точка дня", "      width: 11px;\n      height: 11px;", "      width: 10px;\n      height: 10px;")

# ── 10. БЛОКИ ЗАПИСЕЙ ───────────────────────────────────────────────────────
edit(
    "рамка вопроса",
    """      background: #FAF8F5;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px;""",
    """      background: transparent;
      border: 1px solid var(--border-color);
      border-radius: 2px;
      padding: 15px 16px;""",
)

edit("номер записи", "      font-size: 10.5px;\n      font-weight: 700;\n      letter-spacing: 0.18em;",
     "      font-size: 9.5px;\n      font-weight: 400;\n      letter-spacing: 0.12em;")

edit(
    "рамка записи",
    """      border: 1px solid var(--border-color);
      border-radius: 12px;
      background: #FFFDFA;
      box-shadow: 0 1px 3px rgba(44, 53, 57, 0.04);""",
    """      border: 1px solid var(--border-color);
      border-radius: 2px;
      background: transparent;
      box-shadow: none;""",
)

edit(
    "пометка роли",
    """      padding: 4px 11px 4px 8px;
      border-radius: 100px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.05em;""",
    """      padding: 0;
      border-radius: 0;
      font-size: 9.5px;
      font-weight: 400;
      letter-spacing: 0.1em;""",
)

edit("роль: один", "    .entry-kind.kind-solo { background: var(--sage-light); color: var(--sage-primary); }",
     "    .entry-kind.kind-solo { background: transparent; color: var(--sage-deep); }")

edit("роль: вместе", "    .entry-kind.kind-pair { background: var(--terracotta-light); color: var(--terracotta-deep); }",
     "    .entry-kind.kind-pair { background: transparent; color: var(--terracotta-deep); }")

edit("пояснение к записи", ".entry-hint { font-size: 14px; line-height: 1.45; color: #6B7378; flex: 1; }",
     ".entry-hint { font-size: 15px; line-height: 1.5; color: #5E6660; flex: 1; }")

edit(
    "поле записи",
    """      border: 1px solid var(--border-color);
      border-radius: 9px;
      font-size: 16px;
      line-height: 1.55;""",
    """      border: 1px solid #D5CCBA;
      border-radius: 2px;
      font-size: 16.5px;
      line-height: 1.75;""",
)

edit(
    "кнопка сохранения",
    """      background: var(--terracotta);
      color: #FFFFFF;
      border: none;
      border-radius: 9px;
      font-size: 13.5px;
      font-weight: 600;""",
    """      background: transparent;
      color: var(--sage-deep);
      border: 1px solid var(--sage-primary);
      border-radius: 2px;
      font-size: 14.5px;
      font-weight: 400;""",
)

edit("кнопка сохранения: наведение", "    .btn-save-entry:hover { background: var(--terracotta-deep); }",
     "    .btn-save-entry:hover { background: var(--sage-primary); color: #FFFFFF; }")

edit("сохранённая запись", "      font-size: 15px;\n      line-height: 1.5;\n      color: #3B474C;\n      padding: 8px 0;\n      border-bottom: 1px solid #F0EDE7;",
     "      font-size: 16px;\n      line-height: 1.55;\n      color: #2C3335;\n      padding: 8px 0;\n      border-bottom: 1px solid #EBE4D6;")

edit(
    "врезка «если партнёр»",
    """      padding: 14px 16px;
      background: var(--sage-light);
      border-radius: 8px;
      font-size: 14.5px;
      line-height: 1.55;""",
    """      padding: 12px 14px;
      background: #F4EFE3;
      border-left: 2px solid #CFC4AF;
      border-radius: 0;
      font-size: 15.5px;
      line-height: 1.55;""",
)

edit("строка про безопасность", "      font-size: 13px;\n      line-height: 1.5;\n      color: #7A8288;",
     "      font-size: 13.5px;\n      line-height: 1.5;\n      color: #75786F;")

edit("примечание об источниках", "      font-size: 12px;\n      line-height: 1.5;\n      color: #8A918F;",
     "      font-size: 12.5px;\n      line-height: 1.5;\n      color: #8B8478;")

edit(
    "переход к первой тетради",
    """      background: var(--paper);
      border: 1px solid var(--border-color);
      border-radius: 10px;""",
    """      background: #F4EFE3;
      border: 1px solid var(--border-color);
      border-radius: 2px;""",
)

edit("ярлык перехода", """    .bridge-note .bridge-label {
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: 0.16em;""",
     """    .bridge-note .bridge-label {
      font-size: 9.5px;
      font-weight: 400;
      letter-spacing: 0.12em;""")

edit("колофон", "      font-size: 14.5px;\n      line-height: 1.5;\n      font-style: italic;\n      color: #7A8288;",
     "      font-size: 14.5px;\n      line-height: 1.5;\n      font-style: italic;\n      color: #75786F;")

edit(
    "строка внизу листа",
    """      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 13px;
      letter-spacing: 0.03em;
      color: #8A918F;""",
    """      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 13.5px;
      letter-spacing: 0.02em;
      color: #8B8478;""",
)

edit(
    "номер страницы",
    """      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 10.5px;
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #7A8288;""",
    """      font-size: 9.5px;
      font-weight: 400;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #8B8478;""",
)

edit("кнопка внизу страницы", "      border: 1px solid var(--border-color);\n      border-radius: 9px;\n      background: #FFFFFF;\n      color: var(--text-main);\n      font-size: 13.5px;\n      font-weight: 600;",
     "      border: 1px solid #D5CCBA;\n      border-radius: 2px;\n      background: var(--bg-card);\n      color: var(--text-main);\n      font-size: 14.5px;\n      font-weight: 400;")

edit("главная кнопка внизу", "      color: #FFFFFF;\n      box-shadow: 0 4px 12px rgba(90, 115, 101, 0.22);",
     "      color: #FFFFFF;\n      box-shadow: none;")

edit("подпись на кнопке", "      font-size: 12px;\n      font-weight: 500;\n      letter-spacing: 0;", "      font-size: 13px;\n      font-weight: 400;\n      letter-spacing: 0;")

# ── 11. ОБЛОЖКА ─────────────────────────────────────────────────────────────
edit(
    "обложка",
    """      padding: 0;
      overflow: hidden;
      border: none;
      box-shadow: 0 2px 18px rgba(44, 53, 57, 0.08);""",
    """      padding: 0;
      overflow: hidden;
      border: 1px solid var(--border-color);
      box-shadow: 0 8px 20px rgba(74, 60, 38, 0.06);""",
)

edit("название на обложке", "      font-size: 40px;\n      line-height: 1.05;\n      font-weight: 700;\n      letter-spacing: -0.6px;",
     "      font-size: 40px;\n      line-height: 1.06;\n      font-weight: 600;\n      letter-spacing: 0;")

edit("подзаголовок обложки", "      font-size: 15.5px;\n      line-height: 1.55;\n      color: #4A5459;", "      font-size: 16px;\n      line-height: 1.55;\n      color: #4E5557;")

edit("пункты обложки", ".cover-item { display: flex; align-items: flex-start; gap: 11px; font-size: 14.5px; line-height: 1.45; }",
     ".cover-item { display: flex; align-items: flex-start; gap: 10px; font-size: 15.5px; line-height: 1.45; }")

edit(
    "кнопка на обложке",
    """      font-size: 17px;
      font-weight: 650;
      border-radius: 12px;
      text-decoration: none;
      box-shadow: 0 6px 16px rgba(90, 115, 101, 0.28);""",
    """      font-size: 17px;
      font-weight: 400;
      border-radius: 2px;
      text-decoration: none;
      box-shadow: none;""",
)

edit("подпись под кнопкой", "    .cover-meta {\n      text-align: center;\n      margin-top: 14px;\n      font-size: 12.5px;\n      letter-spacing: 0.02em;\n      color: #7A8288;\n    }",
     "    .cover-meta {\n      text-align: center;\n      margin-top: 13px;\n      font-size: 12px;\n      letter-spacing: 0.04em;\n      color: #8B8478;\n    }")

edit("вторая кнопка обложки", "      border: 1.5px solid var(--sage-primary);\n      min-height: 48px;\n      font-size: 15px;\n      font-weight: 550;",
     "      border: 1px solid var(--sage-primary);\n      min-height: 48px;\n      font-size: 15.5px;\n      font-weight: 400;")

edit("кнопка «продолжить»", "      border: 1.5px solid var(--sage-primary);\n      border-radius: 12px;\n      background: transparent;",
     "      border: 1px solid var(--sage-primary);\n      border-radius: 2px;\n      background: transparent;")

edit("подпись «продолжить»", "      margin-bottom: 10px;\n      background: var(--sage-primary);\n      border-color: var(--sage-primary);\n      color: #FFFFFF;\n      font-size: 17px;\n      font-weight: 650;",
     "      margin-bottom: 10px;\n      background: var(--sage-primary);\n      border-color: var(--sage-primary);\n      color: #FFFFFF;\n      font-size: 17px;\n      font-weight: 400;")

edit("счётчик записей", "    .progress-line {\n      margin: 14px 0 2px;\n      font-size: 12.5px;\n      letter-spacing: 0.04em;",
     "    .progress-line {\n      margin: 13px 0 2px;\n      font-size: 12px;\n      letter-spacing: 0.08em;")

edit("заметка на обложке", "      font-size: 12.5px;\n      line-height: 1.5;\n      font-style: italic;\n      color: #7C8783;",
     "      font-size: 13px;\n      line-height: 1.5;\n      font-style: italic;\n      color: #8B8478;")

edit("записи об приватности", "      background: #FFFFFF;\n      border: 1px solid var(--border-color);\n      border-radius: 9px;\n      font-size: 13.5px;",
     "      background: #F4EFE3;\n      border: 1px solid var(--border-color);\n      border-radius: 2px;\n      font-size: 14px;")

edit("кнопки записей", "      border: 1.5px solid var(--border-color);\n      border-radius: 11px;\n      background: #FFFFFF;\n      font-family: inherit;\n      font-size: 14.5px;",
     "      border: 1px solid var(--border-color);\n      border-radius: 2px;\n      background: transparent;\n      font-family: inherit;\n      font-size: 15px;")

# ── 12. ПЕРВАЯ СТРАНИЦА ─────────────────────────────────────────────────────
edit("номер шага", "      font-family: 'Cormorant Garamond', Georgia, serif;\n      font-size: 30px;\n      line-height: 1;\n      color: var(--terracotta);",
     "      font-family: 'Cormorant Garamond', Georgia, serif;\n      font-size: 28px;\n      line-height: 1;\n      color: var(--terracotta-deep);")

edit("заголовок шага", "      font-size: 19px;\n      font-weight: 700;\n      margin-bottom: 3px;", "      font-size: 19px;\n      font-weight: 600;\n      margin-bottom: 3px;")

edit("текст шага", ".start-steps p { font-size: 15.5px; line-height: 1.55; margin: 0; }",
     ".start-steps p { font-size: 16.5px; line-height: 1.55; margin: 0; }")

edit("куда идти дальше", "    .start-steps .start-where {\n      margin-top: 4px;\n      font-size: 12.5px;\n      letter-spacing: 0.05em;\n      text-transform: uppercase;\n      color: var(--sage-primary);\n    }",
     "    .start-steps .start-where {\n      margin-top: 5px;\n      font-size: 9.5px;\n      letter-spacing: 0.1em;\n      text-transform: uppercase;\n      color: var(--sage-deep);\n    }")

edit("памятка", "      border: 1px solid var(--border-color);\n      border-radius: 12px;\n      background: #FFFFFF;\n    }\n    .memo h3 {",
     "      border: 1px solid var(--border-color);\n      border-radius: 2px;\n      background: transparent;\n    }\n    .memo h3 {")

edit("пункты памятки", "    .memo li { font-size: 15px; line-height: 1.55; margin-bottom: 5px; }",
     "    .memo li { font-size: 15.5px; line-height: 1.55; margin-bottom: 5px; }")

# ── 13. СТРОКИ-ОТВЕТЫ ───────────────────────────────────────────────────────
edit("ярлык короткой записи", """    .line-label {
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--sage-primary);""",
     """    .line-label {
      font-size: 9.5px;
      font-weight: 400;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--sage-deep);""")

edit("вопрос над строкой", "      font-size: 18px;\n      line-height: 1.38;\n      font-style: italic;\n      color: #4A5459;",
     "      font-size: 17.5px;\n      line-height: 1.4;\n      font-style: italic;\n      color: #4E5557;")

edit(
    "строка для письма",
    """      min-height: 44px;
      padding: 8px 2px 6px;
      border: none;
      border-bottom: 1px solid var(--border-color);
      border-radius: 0;
      background: transparent;
      font-family: inherit;
      font-size: 16px;
      line-height: 1.5;""",
    """      min-height: 34px;
      padding: 3px 2px 5px;
      border: none;
      border-bottom: 1px solid #C9BFA9;
      border-radius: 0;
      background: transparent;
      font-family: inherit;
      font-size: 16.5px;
      line-height: 1.55;""",
)

edit("подсказка в строке", "      color: #A6ACAC;\n      font-style: italic;", "      color: #A79E8B;\n      font-style: italic;\n      font-size: 15.5px;")

edit("строка с ответом", "    .line-field.is-written { border-bottom-color: rgba(90, 115, 101, 0.55); }",
     "    .line-field.is-written { border-bottom-color: var(--sage-primary); }")

edit("строка в списке вопросов", "    .ask-list .line-field { min-height: 38px; padding: 4px 2px 4px; }",
     "    .ask-list .line-field { min-height: 30px; padding: 2px 2px 4px; }")

# ── 14. ГАЛОЧКИ И СОДЕРЖАНИЕ ────────────────────────────────────────────────
edit("пункт с галочкой", "      gap: 11px;\n      padding: 9px 0;\n      font-size: 15.5px;\n      line-height: 1.45;\n      color: #3B474C;",
     "      gap: 10px;\n      padding: 8px 0;\n      font-size: 16.5px;\n      line-height: 1.45;\n      color: #2C3335;")

edit("разделитель галочек", "    .tick-item + .tick-item { border-top: 1px dashed rgba(226, 221, 213, 0.85); }",
     "    .tick-item + .tick-item { border-top: 1px solid #EBE4D6; }")

edit("квадрат отметки", "      border: 1.3px solid var(--sage-primary);\n      border-radius: 3px;\n      background: #FFFFFF;",
     "      border: 1px solid #B3A893;\n      border-radius: 0;\n      background: transparent;")

edit("строка содержания", "      border-bottom: 0.4pt dotted #C9C3B8;", "      border-bottom: 0.5pt dotted #C6BDA9;")

edit("номер в содержании", "      font-variant-numeric: tabular-nums;\n      color: #5A7365;", "      font-variant-numeric: tabular-nums;\n      color: var(--sage-deep);")

edit("часть в содержании", "      font-size: 11px;\n      letter-spacing: 0.14em;\n      text-transform: uppercase;\n      color: #A95F4C;",
     "      font-size: 10px;\n      letter-spacing: 0.12em;\n      text-transform: uppercase;\n      color: var(--terracotta-deep);")

edit("главная фраза страницы", "      background: #FDF3E7;\n      border-left: 3px solid var(--terracotta);\n      border-radius: 0 8px 8px 0;",
     "      background: transparent;\n      border-left: 2px solid var(--terracotta);\n      border-radius: 0;")

# ── 15. ТЕЛЕФОННЫЕ ПОПРАВКИ ─────────────────────────────────────────────────
edit(
    "размеры на телефоне",
    """      body { padding: 12px 10px 90px; }
      .page-card { padding: 22px 16px 18px; border-radius: 14px; }
      h1 { font-size: 28px; }
      h2 { font-size: 22px; margin-top: 28px; }
      h3 { font-size: 17px; }
      p { font-size: 16.5px; line-height: 1.62; }
      .chapter-lead { font-size: 18.5px; line-height: 1.44; }""",
    """      body { padding: 8px 8px 88px; }
      .page-card { padding: 24px 18px 18px; border-radius: 2px; }
      h1 { font-size: 29px; }
      h2 { font-size: 21px; margin-top: 26px; }
      h3 { font-size: 18px; }
      p { font-size: 17px; line-height: 1.58; }
      .chapter-lead { font-size: 17.5px; line-height: 1.45; }""",
)

edit("картинка на телефоне", "      .figure-bleed { margin-left: -16px; margin-right: -16px; }\n      .figure-bleed figcaption { padding: 9px 16px 11px; font-size: 14.5px; }",
     "      .figure-bleed { margin-left: -18px; margin-right: -18px; }\n      .figure-bleed figcaption { padding: 8px 18px 10px; font-size: 14.5px; }")

edit("строка на телефоне", "      .line-field { font-size: 16.5px; min-height: 48px; }\n      .line-prompt { font-size: 18.5px; }",
     "      .line-field { font-size: 16.5px; min-height: 34px; }\n      .line-prompt { font-size: 17.5px; }")

edit("кнопка сохранения на телефоне", "      .btn-save-entry { width: 100%; min-height: 48px; font-size: 15.5px; border-radius: 12px; }",
     "      .btn-save-entry { width: 100%; min-height: 48px; font-size: 15px; border-radius: 2px; }")

edit("кнопки внизу на телефоне", "      .btn-nav-step { font-size: 14.5px; min-height: 50px; }", "      .btn-nav-step { font-size: 15px; min-height: 50px; }")

edit("узкий экран", "      .page-card { padding: 20px 13px 16px; }", "      .page-card { padding: 20px 15px 16px; }")

# ── 16. КНИЖНЫЙ НАБОР ───────────────────────────────────────────────────────
edit(
    "выключка и переносы",
    """    /* На широком экране текст выключен по формату книги */
    @media (min-width: 700px) {
      p, .chapter-lead, .key-list li, .checklist li, .compare-col p { text-align: justify; hyphens: auto; -webkit-hyphens: auto; }
    }""",
    """    /* Книжный набор: абзацы с отступом, текст выключен по формату полосы */
    .page-card > p + p { text-indent: 1.35em; }

    @media (min-width: 360px) {
      p, .chapter-lead, .key-list li, .checklist li, .num-list p,
      .protocol-body p, .compare-col p, .fact-box p, .bridge-note p,
      .memo li, .entry-item, .start-steps p, .fallback-note, .quote-box p {
        text-align: justify;
        hyphens: auto;
        -webkit-hyphens: auto;
      }
    }""",
)

# ── ПРИМЕНЕНИЕ ──────────────────────────────────────────────────────────────


def main() -> int:
    html = SRC.read_text(encoding="utf-8")

    missing: list[str] = []
    for label, old, new in EDITS:
        count = html.count(old)
        if count != 1:
            missing.append(f"{label} — найдено {count}")
            continue
        html = html.replace(old, new, 1)

    if missing:
        print("Не применено:", file=sys.stderr)
        for item in missing:
            print("  · " + item, file=sys.stderr)
        return 1

    old_family = "font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif;"
    new_family = "font-family: 'PT Serif', Georgia, 'Times New Roman', serif;"
    if html.count(old_family) != 1:
        print("Не найден основной шрифт", file=sys.stderr)
        return 1
    html = html.replace(old_family, new_family)

    short = "font-family: 'Plus Jakarta Sans', sans-serif;"
    if html.count(short) != 2:
        print(f"Вспомогательный шрифт: {html.count(short)} вместо 2", file=sys.stderr)
        return 1
    html = html.replace(short, new_family)

    svg_old = 'font-family="Plus Jakarta Sans, sans-serif"'
    if html.count(svg_old) != 4:
        print(f"Шрифт на схеме: {html.count(svg_old)} вместо 4", file=sys.stderr)
        return 1
    html = html.replace(svg_old, 'font-family="PT Serif, Georgia, serif"')

    SRC.write_text(html, encoding="utf-8")
    print(f"Применено правок: {len(EDITS) + 3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
