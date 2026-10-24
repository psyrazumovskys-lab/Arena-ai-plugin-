#!/usr/bin/env python3
"""Вторая тетрадь: три прохода правок по итогам исследования и взгляда покупателя.

Проход 1 — чтобы возвращались и не боялись: продолжить с места, счётчик, «если бросили»,
           страница «с чего начать за 15 минут», приватность, стереть и скачать.
Проход 2 — чтобы не страшно начинать: содержание со временем, партнёр не обязателен,
           готовые начала фраз, готовые формулировки, сжатие плотных мест.
Проход 3 — чтобы жило после: страница «через месяц», памятка, печать, реакция на кнопку.

В конце — перенумерация страниц и пересборка переходов. Повторный запуск ничего не делает.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.src.html"

CSS = """
    /* ── ВОЗВРАТ, ПРОГРЕСС, ПРИВАТНОСТЬ ───────────────────────────────────── */
    .resume-btn {
      display: none;
      width: 100%;
      margin-top: 10px;
      padding: 13px 18px;
      border: 1.5px solid var(--sage-primary);
      border-radius: 12px;
      background: transparent;
      color: var(--sage-deep);
      font-family: inherit;
      font-size: 15.5px;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
    }
    .resume-btn.show { display: block; }
    .resume-btn small {
      display: block;
      margin-top: 2px;
      font-size: 12.5px;
      font-weight: 400;
      font-style: italic;
      color: #7C8783;
    }

    .progress-line {
      margin: 14px 0 2px;
      font-size: 12.5px;
      letter-spacing: 0.04em;
      color: #7C8783;
      text-align: center;
    }
    .progress-dots {
      display: flex;
      justify-content: center;
      gap: 6px;
      margin: 7px 0 0;
    }
    .progress-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      border: 1px solid rgba(90, 115, 101, 0.45);
      background: transparent;
    }
    .progress-dot.done { background: var(--sage-primary); border-color: var(--sage-primary); }

    .cover-note {
      margin: 14px 0 0;
      font-size: 12.5px;
      line-height: 1.5;
      font-style: italic;
      color: #7C8783;
      text-align: center;
    }

    .privacy-note {
      margin: 18px 0 6px;
      padding: 13px 15px;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: 9px;
      font-size: 13.5px;
      line-height: 1.5;
      color: #55605F;
    }
    .privacy-note strong { color: var(--sage-deep); }

    .tools-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 16px 0 6px;
    }
    .tool-btn {
      flex: 1 1 44%;
      min-height: 46px;
      padding: 11px 14px;
      border: 1.5px solid var(--border-color);
      border-radius: 11px;
      background: #FFFFFF;
      font-family: inherit;
      font-size: 14.5px;
      color: var(--text-main);
      cursor: pointer;
    }
    .tool-btn:hover { border-color: var(--sage-primary); }
    .tool-btn.danger { color: #9B4B3C; border-color: #E4C9C1; }

    /* ── СТРАНИЦА «С ЧЕГО НАЧАТЬ» ─────────────────────────────────────────── */
    .start-steps {
      list-style: none;
      counter-reset: ss;
      margin: 18px 0 10px;
      padding: 0;
    }
    .start-steps > li {
      counter-increment: ss;
      position: relative;
      padding-left: 42px;
      margin-bottom: 18px;
    }
    .start-steps > li::before {
      content: counter(ss);
      position: absolute;
      left: 0;
      top: -4px;
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 30px;
      line-height: 1;
      color: var(--terracotta);
    }
    .start-steps h3 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 19px;
      font-weight: 700;
      margin-bottom: 3px;
    }
    .start-steps p { font-size: 15.5px; line-height: 1.55; margin: 0; }
    .start-steps .start-where {
      margin-top: 4px;
      font-size: 12.5px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--sage-primary);
    }

    /* ── ПАМЯТКА ──────────────────────────────────────────────────────────── */
    .memo {
      margin: 18px 0;
      padding: 18px 20px;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      background: #FFFFFF;
    }
    .memo h3 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 8px;
    }
    .memo ol { margin: 0; padding-left: 20px; }
    .memo li { font-size: 15px; line-height: 1.55; margin-bottom: 5px; }

    /* ── ПЕЧАТЬ ───────────────────────────────────────────────────────────── */
    @media print {
      @page { size: A5 portrait; margin: 14mm 12mm; }

      html, body {
        background: #FFFFFF !important;
        color: #000000 !important;
      }
      .wb-header, .page-footer-nav, .save-indicator,
      .btn-save-entry, .resume-btn, .tools-row, .entry-empty,
      .progress-line, .progress-dots, .wb-page-selector-wrapper { display: none !important; }

      .container { max-width: none !important; margin: 0 !important; padding: 0 !important; }

      .page-card {
        display: block !important;
        padding: 0 !important;
        margin: 0 0 0 0 !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        background: #FFFFFF !important;
        break-after: page;
        page-break-after: always;
        break-inside: avoid;
      }
      .page-card:last-of-type { break-after: auto; page-break-after: auto; }

      .cover-card { border: none !important; }
      .cover-art img { max-height: 95mm; width: auto; }
      figure img { max-height: 70mm; }

      h1 { font-size: 22pt; }
      p, li { font-size: 10.5pt; line-height: 1.45; }

      .running-head { font-size: 8pt; border-bottom: 0.5pt solid #999; padding-bottom: 2mm; }
      .folio { font-size: 8pt; border-top: 0.5pt solid #999; padding-top: 2mm; margin-top: 4mm; }

      /* Поля для письма: строки через 7 мм */
      textarea, input[type="text"] {
        display: block !important;
        width: 100% !important;
        border: none !important;
        border-bottom: 0.5pt solid #BBB !important;
        background: transparent !important;
        min-height: 26.5pt !important;
        font-size: 10.5pt !important;
        color: #000 !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
      textarea.journal-entry { min-height: 106pt !important; }

      .line-field { min-height: 26.5pt !important; }
      .tick-box { border: 0.7pt solid #666 !important; background: #FFF !important; }

      a { color: #000 !important; text-decoration: none !important; }
    }
"""

PAGE_START = """  <!-- СТРАНИЦА: С ЧЕГО НАЧАТЬ -->
  <div class="page-card" id="pQ">
    <div class="running-head"><span>Перед началом</span><span class="rh-right">Короткий путь</span></div>
    <h1>Если у вас 15 минут</h1>
    <p class="chapter-lead">Тетрадь можно читать подряд, а можно — с этого места.</p>

    <p class="dropcap">Дальше пятнадцать страниц. Их не обязательно проходить по порядку: большинство людей читают такие тетради не подряд, а кусками. Если сейчас у вас есть четверть часа, сделайте три вещи — они и есть вся суть.</p>

    <ol class="start-steps">
      <li>
        <h3>Назовите ссору</h3>
        <p>Не «мы плохо общаемся», а конкретный разговор, который у вас повторяется. Одна фраза — этого достаточно.</p>
        <div class="line-block">
          <textarea class="line-field" id="l_start_name" rows="1" placeholder="Мы ссоримся из-за..."></textarea>
        </div>
        <div class="start-where">Подробнее — глава 1</div>
      </li>
      <li>
        <h3>Найдите свой шаг</h3>
        <p>В такой ссоре обычно один нажимает, а второй отступает. Подумайте, где вы в этом круге и что защищаете.</p>
        <div class="line-block">
          <textarea class="line-field" id="l_start_step" rows="1" placeholder="Когда всё начинается, я..."></textarea>
        </div>
        <div class="start-where">Подробнее — главы 3 и 4</div>
      </li>
      <li>
        <h3>Перепишите одну фразу</h3>
        <p>Возьмите то, что говорите в этой ссоре чаще всего, и скажите это как просьбу: что происходит, что вы чувствуете, о чём просите.</p>
        <div class="line-block">
          <textarea class="line-field" id="l_start_request" rows="1" placeholder="Когда..., я..., можешь...?"></textarea>
        </div>
        <div class="start-where">Подробнее — глава 5</div>
      </li>
    </ol>

    <div class="privacy-note">
      <strong>Где ваши записи.</strong> Всё, что вы пишете, остаётся в этом браузере на этом устройстве. Никуда не отправляется, и мы их не видим. Если открыть тетрадь на другом телефоне или компьютере — там будет пусто. В конце есть кнопки «скачать» и «стереть всё».
    </div>

    <p class="cover-note">Если вы откроете тетрадь через неделю, она предложит продолжить с того места, где вы остановились.</p>

    <div class="folio"><span>Одна и та же ссора</span><span class="folio-page">Стр. 1 из 15</span></div>
    <div class="page-footer-nav">
      <a class="btn-nav-step back" href="#p0" onclick="goToPage('p0'); return false;">‹ Обложка</a>
      <a class="btn-nav-step primary" href="#p1" onclick="goToPage('p1'); return false;">
        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>
        <span class="nav-sub">Введение · Про что эта тетрадь</span>
      </a>
    </div>
  </div>

"""

PAGE_MONTH = """  <!-- СТРАНИЦА: ЧЕРЕЗ МЕСЯЦ -->
  <div class="page-card" id="pM">
    <div class="running-head"><span>Послесловие</span><span class="rh-right">Через месяц</span></div>
    <h1>Вернитесь через месяц</h1>
    <p class="chapter-lead">Не для отчёта. Чтобы увидеть, что изменилось, а что нет.</p>

    <p class="dropcap">Один разговор не делает отношения другими — он показывает, что они могут быть другими. Понять, стало ли что-то меняться, можно не по ощущению «вроде лучше», а по трём вопросам. Задайте их себе примерно через месяц.</p>

    <div class="line-block">
      <div class="line-label">Три вопроса через месяц</div>
      <textarea class="line-field" id="l_month_alive" rows="1" placeholder="Из нашего договора живёт: ..."></textarea>
      <textarea class="line-field" id="l_month_dead" rows="1" placeholder="Не живёт: ..."></textarea>
      <textarea class="line-field" id="l_month_new" rows="1" placeholder="Оказалось важнее, чем я думал(а): ..."></textarea>
    </div>

    <div class="memo">
      <h3>Одна страница на память</h3>
      <ol>
        <li>У вашей ссоры есть имя. Она не про чашку.</li>
        <li>Она возвращается не потому, что вы плохие, а потому что разница настоящая.</li>
        <li>В ней у каждого есть свой шаг. Роль зависит от темы, а не от характера.</li>
        <li>За упрёком стоит просьба. Просьбу можно выполнить сегодня.</li>
        <li>Тридцать минут с правилами лучше трёх часов без них.</li>
        <li>Если становится страшно — это уже не ссора, и тетрадь здесь не поможет.</li>
      </ol>
    </div>

    <h2>Ваши записи</h2>
    <p>Их можно забрать с собой или стереть. Ни то, ни другое не обязательно.</p>
    <div class="tools-row">
      <button type="button" class="tool-btn" onclick="downloadEntries()">Скачать мои записи</button>
      <button type="button" class="tool-btn danger" onclick="clearAllData()">Стереть всё</button>
    </div>
    <p class="source-note">Записи хранятся только в этом браузере. Если вы открываете тетрадь на другом устройстве или в другом браузере, там будет пусто. Общий доступ к устройству тетрадь не закрывает: если это важно, проходите её со своего телефона.</p>

    <div class="folio"><span>Одна и та же ссора</span><span class="folio-page">Стр. 13 из 15</span></div>
    <div class="page-footer-nav">
      <a class="btn-nav-step back" href="#p15" onclick="goToPage('p15'); return false;">‹ Назад</a>
      <a class="btn-nav-step primary" href="#p0" onclick="goToPage('p0'); return false;">
        <span class="nav-main">В начало тетради</span>
        <span class="nav-sub">Обложка</span>
      </a>
    </div>
  </div>

"""

JS_ADD = """
  // ── Возврат на последнюю страницу ─────────────────────────────────────────
  var LAST_PAGE_KEY = 'wb_couples_l2_one_quarrel_last_page';

  function rememberPage(pId) {
    if (pId === 'p0') return;
    try { localStorage.setItem(LAST_PAGE_KEY, pId); } catch (e) {}
  }

  function currentTitle(pId) {
    var sel = document.getElementById('pageSelect');
    if (sel) {
      for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].value === pId) {
          return sel.options[i].textContent.replace('Стр. ', '').replace(' · ', ' — ');
        }
      }
    }
    return pId;
  }

  function showResume() {
    var btn = document.getElementById('resumeBtn');
    if (!btn) return;
    var saved = null;
    try { saved = localStorage.getItem(LAST_PAGE_KEY); } catch (e) {}
    if (!saved || saved === 'p0' || pages.indexOf(saved) === -1) {
      btn.classList.remove('show');
      return;
    }
    var t = currentTitle(saved);
    btn.innerHTML = 'Продолжить' + (t ? '<small>' + t + '</small>' : '');
    btn.setAttribute('data-page', saved);
    btn.classList.add('show');
  }

  // ── Счётчик сделанного ────────────────────────────────────────────────────
  function updateProgress() {
    var done = 0;
    for (var i = 0; i < inputIds.length; i++) {
      if (readEntries(inputIds[i]).length) done++;
    }
    var line = document.getElementById('progressLine');
    if (line) {
      line.textContent = done === 0
        ? 'Записей пока нет'
        : 'Сделано записей: ' + done + ' из ' + inputIds.length;
    }
    var dots = document.getElementById('progressDots');
    if (dots) {
      Array.prototype.forEach.call(dots.children, function (dot, idx) {
        dot.classList.toggle('done', idx < done);
      });
    }
  }

  // ── Скачать и стереть ─────────────────────────────────────────────────────
  function downloadEntries() {
    var lines = ['Одна и та же ссора — мои записи', ''];
    var data = false;

    for (var i = 0; i < inputIds.length; i++) {
      var arr = readEntries(inputIds[i]);
      if (!arr.length) continue;
      data = true;
      lines.push('— — —');
      lines.push('');
      arr.forEach(function (t) { lines.push(t); lines.push(''); });
    }

    var lineFields = document.querySelectorAll('.line-field, .journal-entry');
    var extra = [];
    Array.prototype.forEach.call(lineFields, function (el) {
      var v = '';
      try { v = localStorage.getItem('wb_couples_l2_one_quarrel_line_' + el.id) || ''; } catch (e) {}
      if (!v && el.value) v = el.value;
      if (v.trim()) extra.push(v.trim());
    });
    Array.prototype.forEach.call(document.querySelectorAll('.tick-item input'), function (input) {
      try {
        if (localStorage.getItem('wb_couples_l2_one_quarrel_tick_' + input.getAttribute('data-tick') + '_' + input.value) === '1') {
          var label = input.parentElement.textContent.trim();
          extra.push('✓ ' + label);
        }
      } catch (e) {}
    });
    if (extra.length) {
      data = true;
      lines.push('— — —');
      lines.push('');
      lines.push('Короткие заметки:');
      lines.push('');
      extra.forEach(function (t) { lines.push(t); });
    }

    if (!data) {
      alert('Пока нечего сохранять: вы ещё ничего не написали.');
      return;
    }

    var blob = new Blob([lines.join('\\n')], { type: 'text/plain;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'одна-и-та-же-ссора-мои-записи.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  }

  function clearAllData() {
    var ok = confirm('Стереть все записи? Это навсегда — вернуть их будет нельзя.\\n\\nЕсли хотите сохранить, сначала нажмите «Скачать мои записи».');
    if (!ok) return;
    var keys = [];
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (k && k.indexOf('wb_couples_l2_one_quarrel') === 0) keys.push(k);
    }
    keys.forEach(function (k) { try { localStorage.removeItem(k); } catch (e) {} });
    location.reload();
  }
"""


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    if 'id="pQ"' in html:
        print("Правки уже применены — ничего не делаю.")
        return 0

    def sub(old: str, new: str, count: int = 1) -> None:
        nonlocal html
        if old not in html:
            raise SystemExit("Не найдено: " + old[:70])
        html = html.replace(old, new, count)

    # ── CSS ────────────────────────────────────────────────────────────────
    css_anchor = "    /* ── СТОП-БЛОК: ГЛАВНАЯ ФРАЗА СТРАНИЦЫ ────────────────────────────────── */"
    sub(css_anchor, CSS.strip("\n") + "\n\n" + css_anchor)

    # ── ПРОХОД 1: обложка ──────────────────────────────────────────────────
    sub(
        '''      <a class="btn-cover-start" href="#p1" onclick="goToPage('p1'); return false;">Начать</a>
      <div class="cover-meta">8 записей · две встречи по 40 минут · можно возвращаться</div>''',
        '''      <a class="btn-cover-start" href="#p1" onclick="goToPage('p1'); return false;">Начать</a>
      <button type="button" class="resume-btn" id="resumeBtn" onclick="goToPage(this.getAttribute('data-page'))">Продолжить</button>
      <div class="progress-line" id="progressLine">Записей пока нет</div>
      <div class="progress-dots" id="progressDots">
        <span class="progress-dot"></span><span class="progress-dot"></span><span class="progress-dot"></span><span class="progress-dot"></span>
        <span class="progress-dot"></span><span class="progress-dot"></span><span class="progress-dot"></span><span class="progress-dot"></span>
      </div>
      <div class="cover-meta">8 записей · две встречи по 40 минут · можно возвращаться</div>
      <p class="cover-note">Если вы бросили на неделю — ничего не потерялось. Откройте и продолжите с того места, где остановились. Тетрадь не обидится.</p>''',
    )

    # ── ПРОХОД 1: страница «с чего начать» ─────────────────────────────────
    m = re.search(r'<div class="page-card[^"]*" id="p0">', html)
    if not m:
        raise SystemExit("Нет обложки")
    end = html.find('<div class="page-card', m.end())
    html = html[:end] + PAGE_START + html[end:]

    # ссылка введения теперь ведёт со второй страницы
    sub(
        '''      <a class="btn-nav-step back" href="#p0" onclick="goToPage('p0'); return false;">‹ Обложка</a>
      <a class="btn-nav-step primary" href="#p2" onclick="goToPage('p2'); return false;">
        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>
        <span class="nav-sub">Важно · Если это не ссора</span>''',
        '''      <a class="btn-nav-step back" href="#pQ" onclick="goToPage('pQ'); return false;">‹ Назад</a>
      <a class="btn-nav-step primary" href="#p2" onclick="goToPage('p2'); return false;">
        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>
        <span class="nav-sub">Важно · Если это не ссора</span>''',
    )

    # ── ПРОХОД 2: сжатие введения и слияние двух врезок ───────────────────
    sub(
        '''    <p class="dropcap">У большинства пар есть разговоры, которые возвращаются. Меняются слова, время суток, повод — а разговор тот же. Через десять минут вы оба уже на знакомых местах, и каждый знает, чем это закончится.</p>

    <p>Когда такой спор называют вслух, с ним впервые можно что-то сделать. Поэтому первая часть — про то, чтобы его узнать. Вторая — про разговор, в котором можно услышать друг друга и не потерять себя.</p>''',
        '''    <p class="dropcap">У большинства пар есть разговоры, которые возвращаются. Меняются слова, время суток, повод — а разговор тот же. Через десять минут вы оба уже на знакомых местах, и каждый знает, чем это закончится.</p>

    <p>Когда такой спор называют вслух, с ним впервые можно что-то сделать. Первая часть — про то, чтобы его узнать, вторая — про разговор, в котором можно услышать друг друга и не потерять себя.</p>''',
    )

    sub(
        '''    <div class="margin-note">Тетрадь не требует, чтобы партнёр читал её вместе с вами. Но требует, чтобы вы читали её в спокойный час, а не посреди ссоры.</div>''',
        '''    <div class="margin-note">Тетрадь не требует, чтобы партнёр читал её вместе с вами, — и не требует, чтобы он вообще участвовал. Но требует спокойного часа, а не ссоры.</div>''',
    )

    # слить две врезки: «из первой тетради» + «если проходите сами»
    m = re.search(r'    <div class="bridge-note">[\s\S]*?</div>\n\n    <div class="fallback-note">[\s\S]*?</div>\n', html)
    if not m:
        raise SystemExit("Не найдены врезки на введении")
    merged = '''    <div class="bridge-note">
      <div class="bridge-label">Если вы пришли из первой тетради</div>
      <p>Первая учила останавливать ссору: пауза, стоп-слово, возвращение. Эта начинает там, где та заканчивается. Если первой тетради не было — ничего страшного, но если ссоры пока нечем остановить, начните с неё: без паузы разговор быстро становится её продолжением.</p>
      <p><strong>Если вы проходите это одна.</strong> Всё, что помечено «вместе с партнёром», можно сделать одной: записать свою часть, примерить свою фразу. Партнёр нужен только для одного — для самого разговора, и то не обязательно.</p>
    </div>
'''
    html = html[:m.start()] + merged + html[m.end():]

    # ── ПРОХОД 2: партнёр не условие (титул части II) ─────────────────────
    sub(
        '''        <p class="part-lead">Через неделю. С записями — и с разговором, который вы проведёте иначе.</p>''',
        '''        <p class="part-lead">Через неделю. С записями — и с разговором, который вы проведёте иначе.</p>
        <p class="part-lead">Вторую часть можно пройти и одной. Разговор вдвоём — возможность, а не экзамен, который надо сдать.</p>''',
    )

    # ── ПРОХОД 2: готовые формулировки ────────────────────────────────────
    m = re.search(r'    <div class="quote-box">\s*<span class="quote-label">Можно сказать так</span>[\s\S]*?</div>\n', html)
    if not m:
        raise SystemExit("Не найден блок «Можно сказать так»")
    phrases = m.group(0) + '''
    <h2>Что можно сказать, не сочиняя</h2>
    <p>Возьмите любую и доскажите своими словами. Ночью, когда не придумывается, это важнее красоты.</p>
    <ul class="key-list">
      <li>«Я хочу разобраться, а не победить. Давай тридцать минут, и всё».</li>
      <li>«Когда ты смотришь в телефон, пока я рассказываю, я чувствую, что говорю в пустоту».</li>
      <li>«Мне не нужно, чтобы ты согласился. Мне нужно, чтобы ты понял, почему мне это важно».</li>
      <li>«Мне важно, чтобы мы решали это сами — вдвоём, без подсказок снаружи».</li>
      <li>«Я сейчас не могу продолжать. Вернусь через полчаса, и мы продолжим».</li>
      <li>«Я услышал. Дай мне минуту, я хочу ответить, а не защититься».</li>
    </ul>
'''
    html = html[:m.start()] + phrases + html[m.end():]

    # ── ПРОХОД 2: готовые начала фраз в больших записях ───────────────────
    starts = {
        'q2_the_quarrel': 'Начинается с того, что...&#10;Дальше я...&#10;Заканчивается тем, что...',
        'q2_my_circle': 'Когда всё начинается, я...&#10;Партнёр в ответ...&#10;Через полчаса мы...',
        'q2_what_i_protect': 'Если это останется так навсегда, я буду...&#10;Если уступлю, я боюсь потерять...&#10;Самое важное здесь...',
        'q2_my_request': 'Вместо «ты всегда...» — «когда..., я..., можешь...?»',
        'q2_two_ovals': 'Не отдам: ...&#10;Могу двигаться: ...',
        'q2_first_words': 'Я хочу поговорить о...&#10;Потому что для меня...&#10;Мне страшно, что...',
        'q2_how_it_went': 'Что получилось...&#10;Где сорвались, и из-за чего...&#10;В следующий раз я...',
        'q2_our_agreement': 'Когда ссора начнётся, я...&#10;А ты...&#10;Через месяц мы...',
    }
    for fid, ph in starts.items():
        pat = re.compile(r'(<textarea class="journal-entry" id="%s" placeholder=")([^"]*)(")' % fid)
        if not pat.search(html):
            raise SystemExit("Не найдено поле " + fid)
        html = pat.sub(lambda mm: mm.group(1) + ph + mm.group(3), html, count=1)

    # ── ПРОХОД 2: снятие «синдрома отличницы» ─────────────────────────────
    sub(
        '''      <li><span class="checkbox"></span><span>Если станет слишком больно — остановитесь. Тетрадь подождёт.</span></li>''',
        '''      <li><span class="checkbox"></span><span>Если станет слишком больно — остановитесь. Тетрадь подождёт.</span></li>
      <li><span class="checkbox"></span><span>Тетрадь не делает вас семейным психологом. Если после неё кажется, что теперь вы должны вести все разговоры правильно, — это не цель.</span></li>''',
    )

    # ── ПРОХОД 3: страница «через месяц» — последняя в тетради ────────────
    anchor = html.find('<div class="save-indicator"')
    if anchor == -1:
        raise SystemExit("Не найден конец книги")
    html = html[:anchor] + PAGE_MONTH + html[anchor:]

    # последняя страница «Что дальше» теперь ведёт на «через месяц»
    sub(
        '''      <a class="btn-nav-step primary" href="#p0" onclick="goToPage('p0'); return false;">
        <span class="nav-main">В начало тетради</span>
        <span class="nav-sub">Обложка</span>''',
        '''      <a class="btn-nav-step primary" href="#pM" onclick="goToPage('pM'); return false;">
        <span class="nav-main">Дальше <span class="nav-arrow">›</span></span>
        <span class="nav-sub">Через месяц · Вернуться</span>''',
    )
    # и кнопка «назад» у «через месяц» — на «Что дальше»
    html = html.replace(
        '''      <a class="btn-nav-step back" href="#p15" onclick="goToPage('p15'); return false;">‹ Назад</a>
      <a class="btn-nav-step primary" href="#p0" onclick="goToPage('p0'); return false;">
        <span class="nav-main">В начало тетради</span>''',
        '''      <a class="btn-nav-step back" href="#p15" onclick="goToPage('p15'); return false;">‹ Назад</a>
      <a class="btn-nav-step primary" href="#p0" onclick="goToPage('p0'); return false;">
        <span class="nav-main">В начало тетради</span>''',
        1,
    )

    # обещание «вернитесь к записи 8» убираем из послесловия — теперь есть страница
    sub(
        '''    <p>Через месяц вернитесь к записи 8 и посмотрите, что из договора живёт, а что нет. Это и будет проверка — не для отчёта, а для себя.</p>''',
        '''    <p>Через месяц вернитесь сюда: на следующей странице три вопроса, по которым видно, сдвинулось ли что-то.</p>''',
    )

    # ── ПРОХОД 3: скрипт — динамический список страниц и новые функции ────
    sub(
        "  var pages = ['p0', 'p1', 'p3', 'p4', 'p5', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15'];",
        "  // Список страниц берём из разметки: так он не разъедется при добавлении страниц.\n"
        "  var pages = Array.prototype.map.call(\n"
        "    document.querySelectorAll('.page-card'),\n"
        "    function (el) { return el.id; }\n"
        "  );",
    )

    sub(
        '''  function goToPage(pId) {
    var idx = pages.indexOf(pId);
    if (idx !== -1) {
      currentPageIndex = idx;
      updateView();
    }
  }''',
        '''  function goToPage(pId) {
    var idx = pages.indexOf(pId);
    if (idx !== -1) {
      currentPageIndex = idx;
      updateView();
      if (pId !== 'p0') {
        rememberPage(pId);
        showResume();
      }
      updateProgress();
    }
  }''',
    )

    # реакция кнопки сохранения
    sub(
        '''    textarea.value = '';
    saveData(fieldId, '');
    triggerSaveIndicator();''',
        '''    textarea.value = '';
    saveData(fieldId, '');
    triggerSaveIndicator();
    updateProgress();''',
    )

    sub(
        '''  function triggerSaveIndicator() {
    var ind = document.getElementById('saveIndicator');
    if (!ind) return;
    ind.classList.add('show');
    setTimeout(function () { ind.classList.remove('show'); }, 1500);
  }''',
        '''  function triggerSaveIndicator() {
    var ind = document.getElementById('saveIndicator');
    if (!ind) return;
    ind.textContent = 'Записано на устройстве';
    ind.classList.add('show');
    setTimeout(function () { ind.classList.remove('show'); }, 1800);
  }''',
    )

    # ── вставка новых функций перед DOMContentLoaded ──────────────────────
    sub("  window.addEventListener('DOMContentLoaded', function () {", JS_ADD + "\n  window.addEventListener('DOMContentLoaded', function () {")

    # ── инициализация при загрузке ────────────────────────────────────────
    init_pat = re.compile(
        r"    // Прямая ссылка на страницу \(#p\d+\)[^\n]*\n"
        r"    var hashId = window\.location\.hash\.replace\('#', ''\);\n"
        r"    if \(pages\.indexOf\(hashId\) !== -1\) \{\n"
        r"      goToPage\(hashId\);\n"
        r"    \} else \{\n"
        r"      updateView\(\);\n"
        r"    \}"
    )
    init_new = """    updateProgress();
    showResume();

    // Прямая ссылка на страницу (#p7) открывает именно её, а не обложку
    var hashId = window.location.hash.replace('#', '');
    if (pages.indexOf(hashId) !== -1) {
      goToPage(hashId);
    } else {
      updateView();
    }"""
    if not init_pat.search(html):
        raise SystemExit("Не найден блок инициализации")
    html = init_pat.sub(lambda m: init_new, html, count=1)

    SRC.write_text(html, encoding="utf-8")
    print(f"Готово: {SRC.name} — {len(html):,} символов".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
