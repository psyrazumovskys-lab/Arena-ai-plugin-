#!/usr/bin/env python3
"""Большая правка второй тетради: контекст, роли и безопасность.

Что меняется:
  1. Новая страница «Если это не ссора» сразу после введения: признаки,
     что делать вместо упражнений, телефон 112, кризисные центры, алкоголь.
  2. Новая страница «Если ваш круг другой» после главы про круг: три круга
     (нажим–отступление, две погони, два отступления) и как читать дальше.
  3. Роль больше не назначается: на схеме «ОДИН / ДРУГОЙ» вместо «ВЫ / ПАРТНЁР»,
     плюс пояснение, что роль зависит от темы.
  4. Российский контекст: примеры (ипотека, родители, сад), цифры Росстата
     о браках и разводах, оговорка про международный опрос.
  5. Трезвость в протоколе, «третьи лица» через себя, честная врезка про то,
     что форма просьбы решает не всё.
  6. Перенумерация всех страниц, колонцифры и оглавление.

Повторный запуск ничего не меняет.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"

CSS = """
    /* ── СТОП-БЛОК: ГЛАВНАЯ ФРАЗА СТРАНИЦЫ ────────────────────────────────── */
    .stop-box {
      margin: 20px 0 8px;
      padding: 15px 18px;
      background: #FDF3E7;
      border-left: 3px solid var(--terracotta);
      border-radius: 0 8px 8px 0;
    }
    .stop-box p {
      margin: 0;
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 21px;
      line-height: 1.35;
      font-style: italic;
      color: var(--terracotta-dark);
    }
"""

PAGE_SAFETY = """  <!-- СТРАНИЦА: БЕЗОПАСНОСТЬ -->
  <div class="page-card" id="pS">
    <div class="running-head"><span>Перед началом</span><span class="rh-right">Важно</span></div>
    <h1>Если это не ссора</h1>
    <p class="chapter-lead">Тетрадь — про разговор. Есть случаи, когда разговор начинать опасно.</p>

    <p class="dropcap">Ссора — это когда двое не могут договориться и обоим от этого плохо. Бывает иначе: один боится другого. Тогда дело не в том, как вы говорите, и упражнения не помогут.</p>

    <div class="stop-box">
      <p>Не ссора — если в ней есть страх.</p>
    </div>

    <h2>Признаки</h2>
    <ul class="key-list">
      <li>Угрозы, удары, толчки, брошенные вещи.</li>
      <li>Страшно остаться с этим человеком в одной комнате.</li>
      <li>Контроль: деньги, телефон, встречи, «где ты была».</li>
      <li>После разговора становится страшнее, а не легче.</li>
    </ul>

    <p>Если вы узнали хотя бы один пункт, отложите тетрадь. Совместные упражнения здесь могут сделать хуже: они учат договариваться там, где договариваться небезопасно.</p>

    <h2>Что можно сделать вместо</h2>
    <ul class="key-list">
      <li>Если опасность сейчас — уходить туда, где есть люди. Телефон 112 работает даже без денег на счёте.</li>
      <li>Рассказать одному человеку, которому доверяете. Не «всё плохо», а конкретно: что происходит и чего вы боитесь.</li>
      <li>Обратиться в кризисный центр для женщин: в крупных городах они есть, многие консультируют по телефону и онлайн.</li>
      <li>Если кажется, что уйти некуда, — это чаще про деньги и жильё, чем про чувства. Об этом консультируют юристы центров, и уходить прямо в тот же день не обязательно.</li>
    </ul>

    <div class="margin-note">Тетрадь подождёт. Она не пропадёт и не обидится.</div>

    <h2>Про алкоголь</h2>
    <p>В России две трети тяжёлого насилия в семье происходит, когда выпивают. Поэтому разговор не начинают, если кто-то пил. Но трезвость ничего не гарантирует: примерно треть тех, кто применяет силу дома, не пьют вообще.</p>

    <p class="safety-note">Если вы читаете это и понимаете, что речь про вас, — вы не обязаны справляться сами. И не обязаны никому объяснять, почему вам страшно.</p>

    <p class="source-note">О двух третях и о трети — по данным криминологических исследований семейного насилия в России. В 2017 году побои в семье переведены в административные правонарушения; по оценкам правозащитных организаций, 60–70% пострадавших никуда не обращаются. В опросе ВЦИОМ 2025 года 10% россиян сказали, что в их семье бывают конфликты с применением силы.</p>

    <div class="folio"><span>Одна и та же ссора</span><span class="folio-page">Стр. 2 из 13</span></div>
    <div class="page-footer-nav">
      <a class="btn-nav-step back" href="#p1" onclick="goToPage('p1'); return false;">‹ Назад</a>
      <a class="btn-nav-step primary" href="#p2" onclick="goToPage('p2'); return false;">
        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>
        <span class="nav-sub">Глава 1 · Та самая ссора</span>
      </a>
    </div>
  </div>

"""

PAGE_CIRCLE = """  <!-- СТРАНИЦА: ДРУГОЙ КРУГ -->
  <div class="page-card" id="pC">
    <div class="running-head"><span>Часть I · Разобрать</span><span class="rh-right">После главы 3</span></div>
    <h1>Если ваш круг другой</h1>
    <p class="chapter-lead">Нажим и отступление — самый частый круг, но не единственный.</p>

    <p class="dropcap">В том же опросе, где набралось 74% пар с нажимом и отступлением, остальные разделились почти пополам: 13% — две погони, 13% — два отступления. Если вы не узнали себя в прошлой главе, скорее всего, вы здесь.</p>

    <h2>Три круга</h2>
    <ol class="num-list">
      <li>
        <h3>Нажим — отступление</h3>
        <p>Один требует ответа, второй замолкает. В какой-то момент роли могут поменяться местами.</p>
      </li>
      <li>
        <h3>Две погони</h3>
        <p>Оба наступают, никто не отступает. Ссора быстро переходит в крик, и оба потом помнят, кто что сказал.</p>
      </li>
      <li>
        <h3>Два отступления</h3>
        <p>Никто не начинает. Ссор мало, но и разговоров нет: вы давно не говорили о важном.</p>
      </li>
    </ol>

    <div class="line-block">
      <div class="line-label">Ваш круг</div>
      <p class="line-prompt">Отметьте, что больше похоже на вас. Можно несколько.</p>
      <div class="tick-list">
        <label class="tick-item"><input type="checkbox" data-tick="pC_which" value="1"><span class="tick-box"></span><span>Один нажимает, другой замолкает</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="pC_which" value="2"><span class="tick-box"></span><span>Оба наступаем, никто не отступает</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="pC_which" value="3"><span class="tick-box"></span><span>Оба молчим, разговора нет</span></label>
        <label class="tick-item"><input type="checkbox" data-tick="pC_which" value="4"><span class="tick-box"></span><span>По-разному: зависит от темы</span></label>
      </div>
    </div>

    <h2>Если это про две погони</h2>
    <p>Тетрадь работает, но начинать надо не с разговора, а с паузы. Двоим, которые говорят одновременно, тридцать минут не помогут: сначала стоп-слово и десять минут в разных комнатах, и только потом разговор.</p>

    <h2>Если это про два отступления</h2>
    <p>Здесь нет ссоры, которую надо разобрать, — есть тишина. Начните с главы о том, что каждый защищает, и с просьбы. Первый шаг делает тот, кто читает: второй может вообще не считать, что что-то не так.</p>

    <div class="margin-note">Дальше главы читаются как обычно: они про то, что вы защищаете, и про разговор, а не про то, кто первый начал.</div>

    <p class="source-note">74%, 13% и 13% — международный онлайн-опрос сервиса Empathi, 2022–2026: 6 159 пар, где анкету заполнили оба партнёра. Это не российская выборка, поэтому цифры говорят о том, как бывает, а не о том, как бывает у нас.</p>

    <div class="folio"><span>Одна и та же ссора</span><span class="folio-page">Стр. 6 из 13</span></div>
    <div class="page-footer-nav">
      <a class="btn-nav-step back" href="#p4" onclick="goToPage('p4'); return false;">‹ Назад</a>
      <a class="btn-nav-step primary" href="#p5" onclick="goToPage('p5'); return false;">
        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>
        <span class="nav-sub">Глава 4 · Что каждый защищает</span>
      </a>
    </div>
  </div>

"""


def set_back_link(html: str, card_id: str, target: str) -> str:
    """Меняет ссылку «Назад» в карточке: назад должна вести на новую соседнюю страницу."""
    m = re.search(r'<div class="page-card[^"]*" id="%s">' % card_id, html)
    if not m:
        raise SystemExit(f"Не найдена карточка {card_id}")
    end = html.find('<div class="page-card', m.end())
    if end == -1:
        end = html.find('<div class="save-indicator"')
    card = html[m.end():end]
    pattern = re.compile(
        r'<a class="btn-nav-step back" href="#p\w+" onclick="goToPage\(\'p\w+\'\); return false;">'
    )
    old = pattern.search(card)
    if not old:
        raise SystemExit(f"В карточке {card_id} нет ссылки «Назад»")
    new = (
        f'<a class="btn-nav-step back" href="#{target}" '
        f"onclick=\"goToPage('{target}'); return false;\">"
    )
    card = card[:old.start()] + new + card[old.end():]
    return html[:m.end()] + card + html[end:]


def insert_after_card(html: str, old_id: str, block: str) -> str:
    """Вставляет карточку сразу после карточки с указанным id."""
    m = re.search(r'<div class="page-card[^"]*" id="%s">' % old_id, html)
    if not m:
        raise SystemExit(f"Не найдена карточка {old_id}")
    start = m.start()
    end = html.find('<div class="page-card', m.end())
    if end == -1:
        end = html.find('<div class="save-indicator"')
    return html[:end] + block + html[end:]


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    if 'id="pS"' in html:
        print("Правка уже применена — ничего не делаю.")
        return 0

    # ── 1. Новые страницы ───────────────────────────────────────────────────
    html = insert_after_card(html, "p1", PAGE_SAFETY)
    html = set_back_link(html, "p2", "pS")
    html = insert_after_card(html, "p4", PAGE_CIRCLE)
    html = set_back_link(html, "p5", "pC")

    # Ссылка введения теперь ведёт на страницу безопасности
    html = html.replace(
        '<a class="btn-nav-step primary" href="#p2" onclick="goToPage(\'p2\'); return false;">\n'
        '        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>\n'
        '        <span class="nav-sub">Глава 1 · Та самая ссора</span>',
        '<a class="btn-nav-step primary" href="#pS" onclick="goToPage(\'pS\'); return false;">\n'
        '        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>\n'
        '        <span class="nav-sub">Важно · Если это не ссора</span>', 1)

    # Ссылка главы про круг теперь ведёт на «Если ваш круг другой»
    html = html.replace(
        '<a class="btn-nav-step primary" href="#p5" onclick="goToPage(\'p5\'); return false;">\n'
        '        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>\n'
        '        <span class="nav-sub">Глава 4 · Что каждый защищает</span>',
        '<a class="btn-nav-step primary" href="#pC" onclick="goToPage(\'pC\'); return false;">\n'
        '        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>\n'
        '        <span class="nav-sub">Если ваш круг другой</span>', 1)

    # ── 2. Роль больше не назначается ──────────────────────────────────────
    html = html.replace(
        '<text x="64" y="150" text-anchor="middle" font-family="Plus Jakarta Sans, sans-serif" '
        'font-size="10.5" letter-spacing="1.6" fill="#5A7365">ВЫ</text>',
        '<text x="64" y="150" text-anchor="middle" font-family="Plus Jakarta Sans, sans-serif" '
        'font-size="10.5" letter-spacing="1.6" fill="#5A7365">ОДИН</text>', 1)
    html = html.replace(
        '<text x="296" y="150" text-anchor="middle" font-family="Plus Jakarta Sans, sans-serif" '
        'font-size="10.5" letter-spacing="1.6" fill="#A95F4C">ПАРТНЁР</text>',
        '<text x="296" y="150" text-anchor="middle" font-family="Plus Jakarta Sans, sans-serif" '
        'font-size="10.5" letter-spacing="1.6" fill="#A95F4C">ДРУГОЙ</text>', 1)

    # Пояснение под схемой + честность про роли
    old_fig_tail = """      <figcaption>Один идёт навстречу, второй отступает — и каждый считает отступающим другого.</figcaption>"""
    new_fig_tail = """      <figcaption>Один идёт навстречу, второй отступает — и каждый считает отступающим другого.</figcaption>"""
    if old_fig_tail not in html:
        # ищем любую подпись под схемой круга
        m = re.search(r'<figure class="circle-diagram">[\s\S]*?</figure>', html)
        if not m:
            print("Не найдена схема круга", file=sys.stderr)
            return 1
        html = html[:m.end()] + """
    <p>Кто нажимает, а кто отступает, зависит не от характера, а от темы и от того, кому что важнее. В другой ссоре вы можете оказаться на другом конце. У пар, которые справляются, роли меняются; у пар, которые застряли, застывают.</p>

    <div class="margin-note">Тот, кто сейчас молчит, часто не холодный. Он раньше просил — и перестал. Молчание со смыслом, обида, «сам догадайся» — это тоже отступление, и оно бьёт сильнее слов.</div>""" + html[m.end():]
    else:
        html = html.replace(old_fig_tail, new_fig_tail + """
    <p>Кто нажимает, а кто отступает, зависит не от характера, а от темы и от того, кому что важнее. В другой ссоре вы можете оказаться на другом конце. У пар, которые справляются, роли меняются; у пар, которые застряли, застывают.</p>

    <div class="margin-note">Тот, кто сейчас молчит, часто не холодный. Он раньше просил — и перестал. Молчание со смыслом, обида, «сам догадайся» — это тоже отступление, и оно бьёт сильнее слов.</div>""", 1)

    # Оговорка в блоке с 74%
    html = html.replace(
        '<div class="fact-label">Насколько это часто</div>\n'
        '      <p>В большом опросе, где анкету заполнили оба партнёра, — 6 159 пар — 74%',
        '<div class="fact-label">Насколько это часто</div>\n'
        '      <p>В международном онлайн-опросе, где анкету заполнили оба партнёра, — 6 159 пар — 74%', 1)

    # ── 3. Российский контекст ──────────────────────────────────────────────
    # Примеры из нашего быта — после абзаца о приметах
    m = re.search(r'<p>У такой ссоры есть приметы\.[\s\S]*?</p>', html)
    if not m:
        print("Не найден абзац о приметах", file=sys.stderr)
        return 1
    html = html[:m.end()] + """

    <p>Тема при этом часто одна из трёх: деньги и жильё, родители, дети и быт. Ипотека, которая съедает отпуск. Мама, которая приезжает без звонка. Кто забирает из сада и кто садится на больничный.</p>""" + html[m.end():]

    # Российские цифры — перед блоком «решается / не решается»
    html = html.replace(
        '    <div class="compare">\n      <div class="compare-col">\n        <h4>Решается</h4>',
        """    <div class="fact-box">
      <div class="fact-label">Ближе к дому</div>
      <p>В России за 2024 год — 880 тысяч браков и 644 тысячи разводов. На десять свадеб восемь разводов. Цифра ничего не говорит о причинах, но говорит, что таких разговоров много.</p>
    </div>
    <p class="source-note">Росстат, 2024; соотношение браков и разводов — оценка ВЦИОМ.</p>

    <div class="compare">
      <div class="compare-col">
        <h4>Решается</h4>""", 1)

    # ── 4. Протокол: трезвость ──────────────────────────────────────────────
    html = html.replace(
        '<li><span class="checkbox"></span><span>Можно остановиться и вернуться.</span></li>\n    </ul>',
        '<li><span class="checkbox"></span><span>Можно остановиться и вернуться.</span></li>\n'
        '      <li><span class="checkbox"></span><span>Оба трезвые. Хотя бы сегодня.</span></li>\n    </ul>\n\n'
        '    <div class="margin-note">Если кто-то выпил, разговор не начинают — даже немного. Не потому, что человек плохой, а потому что так не удержать ни времени, ни правил.</div>', 1)

    # ── 5. Третьи лица ─────────────────────────────────────────────────────
    html = html.replace(
        '<li>Не обсуждать третьих лиц.</li>',
        '<li>Про третьих — только через себя: не «твоя мать вмешивается», а «мне важно, чтобы мы решали сами».</li>', 1)

    # ── 6. Честно про предел просьбы ───────────────────────────────────────
    html = html.replace(
        '    <div class="margin-note">Просьба — не слабость. Это единственная форма, в которой вас могут услышать.</div>',
        """    <div class="fact-box">
      <div class="fact-label">Если просьба не работает</div>
      <p>Форма просьбы меняет многое, но не всё. Если вы просите одно и то же годами и ничего не меняется, дело уже не в словах, а в том, хотят ли слышать. И если быт держится на одном человеке, никакая формула «когда ты..., я...» этого не исправит.</p>
    </div>

    <div class="margin-note">Просьба — не слабость. Это единственная форма, в которой вас могут услышать.</div>""", 1)

    # ── 7. CSS ─────────────────────────────────────────────────────────────
    css_anchor = "    /* ── КОРОТКАЯ ЗАПИСЬ: СТРОКА В КНИГЕ ──────────────────────────────────── */"
    if html.count(css_anchor) != 1:
        print("Не найден блок CSS", file=sys.stderr)
        return 1
    html = html.replace(css_anchor, CSS.strip("\n") + "\n\n" + css_anchor, 1)

    # ── 8. Перенумерация страниц ───────────────────────────────────────────
    starts = [m.start() for m in re.finditer(r'<div class="page-card[^"]*" id="(p\w+)">', html)]
    ids = [m.group(1) for m in re.finditer(r'<div class="page-card[^"]*" id="(p\w+)">', html)]
    if len(starts) != 16:
        print(f"Ожидалось 16 карточек, получено {len(starts)}", file=sys.stderr)
        return 1

    total = len(ids) - 1  # без обложки
    mapping = {old: f"p{i}" for i, old in enumerate(ids)}

    # токены вида p0, pS, pC — одним проходом, чтобы не переименовать дважды
    def repl(m: re.Match) -> str:
        return mapping.get(m.group(0), m.group(0))

    html = re.sub(r"\bp(?:[SC]|\d{1,2})\b", repl, html)

    # Колонцифры по порядку
    folio_iter = iter(range(1, total + 1))
    html = re.sub(r'<span class="folio-page">Стр\. \d+ из \d+</span>',
                  lambda m: f'<span class="folio-page">Стр. {next(folio_iter)} из {total}</span>', html)

    # Оглавление
    labels = ["Обложка", "Перед началом", "Если это не ссора", "Та самая ссора",
              "Почему она возвращается", "Круг", "Если круг другой",
              "Что каждый защищает", "Упрёк и просьба", "Тридцать минут",
              "Два овала", "Первый разговор", "Как прошло", "Между встречами",
              "Второй разговор", "Что дальше"]
    options = ['          <option value="p0">Обложка</option>']
    for i, name in enumerate(labels[1:], start=1):
        options.append(f'          <option value="p{i}">Стр. {i} · {name}</option>')
    html = re.sub(r'          <option value="p0">Обложка</option>[\s\S]*?</select>',
                  "\n".join(options) + "\n        </select>", html, count=1)

    SRC.write_text(html, encoding="utf-8")
    print(f"Готово: {SRC.name} — {len(html):,} символов, страниц {total}".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
