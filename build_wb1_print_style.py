#!/usr/bin/env python3
"""Собирает копию первой тетради в оформлении печатной книжечки.

Оригинал therapy-workbooks/couple_workbook_1_stop_escalation.html не меняется:
скрипт читает его и пишет отдельный файл ..._print_style.html. Содержание,
идентификаторы блоков записи и скрипт сохранения остаются прежними — меняются
только стили и шрифты. Поэтому проверки из test_workbook_entry_blocks.js
проходят и на копии.

Запуск: python3 build_wb1_print_style.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_1_stop_escalation.html"
OUT = ROOT / "therapy-workbooks" / "couple_workbook_1_print_style.html"

TITLE = "Как вовремя остановить ссору — печатное издание | PsyLab"

FONT_LINK = (
    '<link href="https://fonts.googleapis.com/css2?'
    'family=PT+Serif:ital,wght@0,400;0,700;1,400;1,700&'
    'family=PT+Sans:wght@400;700&display=swap" rel="stylesheet">'
)

CSS = r"""
    /* ==========================================================================
       ПЕЧАТНОЕ ИЗДАНИЕ В БРАУЗЕРЕ
       Перенесено из книжечки A5: кремовая бумага, PT Serif, тонкие линейки,
       трекинговые подписи, пунктирные строки для записи, номера страниц.
       Никаких теней, скруглений и цветных плашек — только бумага и волосяные линии.
       ========================================================================== */
    :root {
      --paper: #F7F5F0;
      --paper-deep: #F1EDE4;
      --ink: #2C3539;
      --body-text: #3B474C;
      --muted: #7A8288;
      --sage: #5A7365;
      --sage-wash: #EBF1ED;
      --terra: #C87D65;
      --terra-deep: #B1634B;
      --terra-wash: #FDF3E7;
      --rule: #DDD6CB;
      --rule-soft: #E8E2D8;
      /* старые имена — на случай, если где-то осталась ссылка */
      --bg-body: #F7F5F0;
      --bg-card: #FFFFFF;
      --text-main: #2C3539;
      --text-muted: #7A8288;
      --sage-primary: #5A7365;
      --sage-light: #EBF1ED;
      --terracotta: #C87D65;
      --terracotta-light: #FDF3E7;
      --border-color: #DDD6CB;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    html { -webkit-text-size-adjust: 100%; }

    body {
      font-family: "PT Serif", Georgia, "Times New Roman", serif;
      font-size: 17px;
      line-height: 1.62;
      color: var(--body-text);
      background-color: var(--paper);
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.022'/%3E%3C/svg%3E");
      padding: 0 22px 96px;
      -webkit-font-smoothing: antialiased;
    }

    .container { max-width: 620px; margin: 0 auto; }

    /* ---------------------------------------------------------------- шапка */
    .wb-navigation-bar {
      position: sticky;
      top: 0;
      z-index: 20;
      background: var(--paper);
      border-bottom: 1px solid var(--rule);
      padding: 12px 0 10px;
      margin-bottom: 30px;
    }

    .wb-nav-stepper { display: flex; align-items: center; gap: 10px; }

    .wb-step-btn {
      border: 0;
      background: transparent;
      color: var(--sage);
      font-family: "PT Serif", Georgia, serif;
      font-size: 19px;
      line-height: 1;
      width: 26px;
      height: 26px;
      cursor: pointer;
      transition: opacity .15s ease;
    }
    .wb-step-btn:disabled { opacity: .25; cursor: default; }

    .wb-page-selector-wrapper { flex: 1; position: relative; }

    .wb-page-select {
      width: 100%;
      appearance: none;
      -webkit-appearance: none;
      border: 0;
      background: transparent;
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 10.5px;
      letter-spacing: .13em;
      text-transform: uppercase;
      color: var(--muted);
      padding: 4px 0;
      cursor: pointer;
      text-align: center;
    }
    .wb-page-select:focus { outline: none; color: var(--ink); }
    .wb-select-caret { display: none; }

    /* ---------------------------------------------------------------- страницы */
    .page-card { display: none; padding-bottom: 8px; }
    .page-card.active { display: block; animation: page-in .28s ease both; }

    /* запасной ход без JavaScript — по якорю #pN */
    .page-card:target { display: block; }
    body:has(.page-card:target) .page-card.active:not(:target) { display: none; }

    @keyframes page-in {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: none; }
    }

    /* ---------------------------------------------------------------- обложка */
    .cover-card { padding-top: 0; }

    .cover-art { margin: 0 -22px 30px; }

    .cover-image {
      display: block;
      width: 100%;
      height: auto;
      border: 0;
      border-radius: 0;
      box-shadow: none;
    }

    .cover-body { padding: 0; }

    .cover-title {
      font-family: "PT Serif", Georgia, serif;
      font-size: 40px;
      line-height: 1.1;
      font-weight: 700;
      letter-spacing: -0.012em;
      color: var(--ink);
      margin: 16px 0 14px;
    }

    .cover-lead {
      font-family: "PT Serif", Georgia, serif;
      font-style: italic;
      font-size: 18.5px;
      line-height: 1.55;
      color: var(--body-text);
      max-width: 44ch;
      margin-bottom: 26px;
    }

    .cover-list {
      border-top: 1px solid var(--rule);
      padding-top: 18px;
      margin-bottom: 30px;
    }

    .cover-item {
      display: flex;
      gap: 12px;
      align-items: baseline;
      padding: 7px 0;
      font-size: 16px;
      color: var(--body-text);
    }

    .cover-dot {
      flex: 0 0 auto;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--terra);
      transform: translateY(-3px);
    }

    .btn-cover-start {
      display: inline-block;
      border: 1px solid var(--terra);
      background: transparent;
      color: var(--terra);
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 10.5px;
      letter-spacing: .18em;
      text-transform: uppercase;
      text-decoration: none;
      padding: 14px 30px;
      border-radius: 0;
      transition: background .15s ease, color .15s ease;
    }
    .btn-cover-start:hover { background: var(--terra); color: #fff; }

    .cover-meta {
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1px solid var(--rule);
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 10px;
      letter-spacing: .16em;
      text-transform: uppercase;
      color: var(--muted);
    }

    /* ---------------------------------------------------------------- набор */
    h1 {
      font-family: "PT Serif", Georgia, serif;
      font-size: 33px;
      line-height: 1.14;
      font-weight: 700;
      letter-spacing: -0.012em;
      color: var(--ink);
      margin: 6px 0 14px;
    }

    h2 {
      font-family: "PT Serif", Georgia, serif;
      font-size: 23px;
      line-height: 1.25;
      font-weight: 700;
      color: var(--ink);
      margin: 0 0 10px;
    }

    h3 {
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 10px;
      line-height: 1.4;
      font-weight: 700;
      letter-spacing: .19em;
      text-transform: uppercase;
      color: var(--terra);
      margin: 0;
    }

    p { margin-bottom: 14px; }
    p:last-child { margin-bottom: 0; }

    em { font-style: italic; }
    strong { font-weight: 700; color: var(--ink); }

    /* подпись-этикетка: «ВВЕДЕНИЕ», «ШАГ 1 ИЗ 6 · ...» */
    .badge-label,
    .badge-label.terracotta {
      display: block;
      background: none;
      border: 0;
      border-radius: 0;
      padding: 0;
      margin: 0 0 14px;
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: .2em;
      text-transform: uppercase;
      color: var(--terra);
    }

    /* маркеры вместо иконок */
    .marker {
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 12px;
      color: var(--terra);
      margin-right: 8px;
    }
    .marker.paper { color: var(--terra); }
    .marker.shield { color: var(--sage); }

    /* ---------------------------------------------------------------- картинки */
    .hero-image-wrapper { margin: 4px 0 26px; text-align: center; }

    .hero-image {
      display: inline-block;
      width: 100%;
      max-width: 430px;
      height: auto;
      border: 0;
      border-radius: 0;
      box-shadow: none;
    }

    /* ---------------------------------------------------------------- цитата */
    .quote-box {
      border: 0;
      border-left: 2px solid var(--terra);
      border-radius: 0;
      background: none;
      padding: 2px 0 2px 18px;
      margin: 22px 0;
      font-family: "PT Serif", Georgia, serif;
      font-style: italic;
      font-size: 18.5px;
      line-height: 1.5;
      color: var(--ink);
    }

    /* ---------------------------------------------------------------- плашки */
    .fact-box {
      background: var(--terra-wash);
      border-left: 3px solid var(--terra);
      border-radius: 0;
      padding: 18px 20px;
      margin: 24px 0;
    }

    .fact-label,
    .return-label {
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: .19em;
      text-transform: uppercase;
      color: var(--terra-deep);
      margin-bottom: 10px;
    }

    .fact-box p { font-size: 16px; }

    .return-box {
      background: var(--sage-wash);
      border-left: 3px solid var(--sage);
      border-radius: 0;
      padding: 18px 20px;
      margin: 24px 0;
    }

    .return-label { color: var(--sage); }

    .return-box p { font-size: 16px; }

    .return-phrases { list-style: none; margin: 12px 0; }

    .return-phrases li {
      position: relative;
      padding-left: 18px;
      margin-bottom: 8px;
      font-style: italic;
      font-size: 16.5px;
      color: var(--ink);
    }

    .return-phrases li::before {
      content: "";
      position: absolute;
      left: 0;
      top: .62em;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--terra);
    }

    .fallback-note {
      margin-top: 22px;
      padding-top: 14px;
      border-top: 1px solid var(--rule);
      font-size: 14.5px;
      font-style: italic;
      color: var(--muted);
    }

    .safety-note {
      margin-top: 20px;
      padding-top: 14px;
      border-top: 1px solid var(--rule);
      font-size: 14.5px;
      font-style: italic;
      color: var(--muted);
    }

    .bridge-card {
      border: 0;
      border-top: 1px solid var(--rule);
      background: none;
      border-radius: 0;
      padding: 22px 0 0;
      margin: 26px 0 0;
    }

    .bridge-card h2 {
      font-family: "PT Serif", Georgia, serif;
      font-size: 23px;
      color: var(--sage);
      margin: 0 0 10px;
    }

    .tx-card, .tx-list, .tx-note, .tx-small, .tx-label { font-family: inherit; }
    .tx-label {
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9px;
      letter-spacing: .19em;
      text-transform: uppercase;
      color: var(--muted);
    }
    .tx-list { list-style: none; margin: 12px 0; }
    .tx-list li {
      position: relative;
      padding-left: 18px;
      margin-bottom: 8px;
      font-size: 16px;
    }
    .tx-list li::before {
      content: "";
      position: absolute;
      left: 0;
      top: .62em;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--terra);
    }
    .tx-note { font-size: 13.5px; color: var(--muted); font-style: italic; }
    .tx-small { font-size: 13.5px; color: var(--muted); }

    /* ---------------------------------------------------------------- блоки записи */
    .interactive-card {
      border: 1px solid var(--rule);
      border-radius: 0;
      background: transparent;
      box-shadow: none;
      padding: 18px;
      margin: 22px 0;
    }

    .interactive-card.card-title-only,
    .interactive-card.card-title-only:first-child {
      border: 0;
      padding: 0;
      margin: 26px 0 10px;
      background: transparent;
    }

    .entry-block {
      border: 0;
      border-top: 1px solid var(--rule);
      border-radius: 0;
      background: transparent;
      padding: 16px 0 4px;
      margin: 0 0 26px;
    }

    .entry-kind {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: .18em;
      text-transform: uppercase;
      color: var(--sage);
    }

    .kind-icon { width: 15px; height: 15px; stroke: var(--sage); }

    .entry-header { margin-bottom: 12px; }

    .entry-lamp { display: none; }

    .entry-hint {
      display: block;
      font-family: "PT Serif", Georgia, serif;
      font-size: 16.5px;
      font-weight: 700;
      line-height: 1.45;
      color: var(--ink);
    }

    .journal-entry {
      display: block;
      width: 100%;
      min-height: 112px;
      border: 0;
      border-radius: 0;
      background-color: transparent;
      background-image: repeating-linear-gradient(
        to bottom,
        transparent 0,
        transparent 27px,
        var(--rule) 27px,
        var(--rule) 28px
      );
      background-position: 0 7px;
      padding: 0;
      font-family: "PT Serif", Georgia, serif;
      font-size: 16px;
      line-height: 28px;
      color: var(--ink);
      resize: vertical;
      outline: none;
    }

    .journal-entry::placeholder {
      font-style: italic;
      color: #A9A296;
    }

    .btn-save-entry {
      margin-top: 16px;
      border: 1px solid var(--terra);
      border-radius: 0;
      background: transparent;
      color: var(--terra);
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: .16em;
      text-transform: uppercase;
      padding: 11px 18px;
      cursor: pointer;
      transition: background .15s ease, color .15s ease;
    }
    .btn-save-entry:hover { background: var(--terra); color: #fff; }
    .btn-save-entry:active { transform: none; }

    .entry-list { margin-top: 18px; }

    .entry-empty {
      font-size: 14px;
      font-style: italic;
      color: var(--muted);
    }

    .entry-item {
      position: relative;
      padding: 10px 0 10px 18px;
      border-top: 1px solid var(--rule-soft);
      font-size: 15.5px;
      line-height: 1.5;
      color: var(--ink);
    }
    .entry-item::before {
      content: "";
      position: absolute;
      left: 0;
      top: 1.05em;
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--terra);
    }
    .entry-item.is-new { animation: entry-in .3s ease both; }

    @keyframes entry-in {
      from { opacity: 0; transform: translateY(-3px); }
      to { opacity: 1; transform: none; }
    }

    /* ---------------------------------------------------------------- термометр */
    .scale-gauge-container { margin: 20px 0 8px; }

    .scale-meter { display: flex; gap: 4px; }

    .scale-segment {
      flex: 1;
      height: 20px;
      border-radius: 0;
      background: #E4DED3;
      transition: background .2s ease;
    }
    .scale-segment.active-green { background: #8FB8A8; }
    .scale-segment.active-yellow { background: #E2C99F; }
    .scale-segment.active-red { background: var(--terra); }

    .scale-slider-range {
      width: 100%;
      margin: 14px 0 6px;
      accent-color: var(--sage);
      background: transparent;
    }

    .scale-status-banner {
      border: 0;
      border-top: 1px solid var(--rule);
      border-radius: 0;
      background: none;
      padding: 14px 0 0;
      margin-top: 10px;
      font-size: 15.5px;
      line-height: 1.55;
    }

    .zone-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      margin-right: 6px;
      transform: translateY(-1px);
    }
    .zone-dot.green { background: #8FB8A8; }
    .zone-dot.yellow { background: #E2C99F; }
    .zone-dot.red { background: var(--terra); }

    /* ---------------------------------------------------------------- дыхание */
    .breath-tool-card {
      border: 1px solid var(--rule);
      border-radius: 0;
      background: transparent;
      padding: 20px;
      text-align: center;
      margin: 22px 0;
    }

    .breath-circle-outer {
      width: 132px;
      height: 132px;
      margin: 18px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--sage);
      border-radius: 50%;
      background: transparent;
      transition: transform 4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .breath-circle-outer.expand { transform: scale(1.26); }
    .breath-circle-outer.shrink { transform: scale(0.9); }

    .breath-circle-inner {
      width: 92px;
      height: 92px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      background: var(--sage);
      color: var(--paper);
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 10px;
      letter-spacing: .12em;
      text-transform: uppercase;
      line-height: 1.5;
    }

    .btn-breath-start {
      border: 1px solid var(--sage);
      border-radius: 0;
      background: transparent;
      color: var(--sage);
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: .16em;
      text-transform: uppercase;
      padding: 11px 18px;
      cursor: pointer;
    }
    .btn-breath-start:hover { background: var(--sage); color: #fff; }

    /* ---------------------------------------------------------------- конструктор фразы */
    .builder-section { margin-bottom: 18px; }

    .builder-step-label {
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: .17em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 10px;
    }

    .chip-group { display: flex; flex-wrap: wrap; gap: 8px; }

    .choice-chip {
      border: 1px solid var(--rule);
      border-radius: 0;
      background: transparent;
      color: var(--body-text);
      font-family: "PT Serif", Georgia, serif;
      font-size: 14.5px;
      line-height: 1.35;
      padding: 9px 13px;
      cursor: pointer;
      text-align: left;
      transition: border-color .15s ease, background .15s ease;
    }
    .choice-chip:hover { border-color: var(--terra); }
    .choice-chip.selected {
      border-color: var(--terra);
      background: var(--terra-wash);
      color: var(--ink);
    }

    .built-phrase-card {
      border: 0;
      border-top: 1px solid var(--rule);
      border-radius: 0;
      background: transparent;
      padding-top: 16px;
      margin-top: 20px;
    }

    .built-phrase-text {
      font-family: "PT Serif", Georgia, serif;
      font-style: italic;
      font-size: 17px;
      line-height: 1.55;
      color: var(--ink);
      margin: 10px 0 14px;
    }

    .btn-copy-chip {
      border: 1px solid var(--sage);
      border-radius: 0;
      background: transparent;
      color: var(--sage);
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: .16em;
      text-transform: uppercase;
      padding: 10px 16px;
      cursor: pointer;
    }
    .btn-copy-chip:hover { background: var(--sage); color: #fff; }

    /* ---------------------------------------------------------------- шпаргалка */
    .sos-lockscreen-widget {
      border: 1px solid var(--rule);
      border-radius: 0;
      background: transparent;
      padding: 24px 22px;
      margin: 22px 0;
      text-align: center;
      box-shadow: none;
    }

    .sos-clock {
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 10px;
      letter-spacing: .2em;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .sos-pill-badge {
      display: inline-block;
      border: 0;
      background: none;
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: .19em;
      text-transform: uppercase;
      color: var(--terra);
      margin-bottom: 14px;
    }

    .sos-quote {
      font-family: "PT Serif", Georgia, serif;
      font-style: italic;
      font-size: 17.5px;
      line-height: 1.55;
      color: var(--ink);
      margin-bottom: 14px;
    }

    /* ---------------------------------------------------------------- низ страницы */
    .page-footer-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      border-top: 1px solid var(--rule);
      margin-top: 30px;
      padding: 16px 0 4px;
    }

    .btn-nav-step,
    .btn-nav-step.primary {
      border: 0;
      background: none;
      border-radius: 0;
      box-shadow: none;
      padding: 0;
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: .14em;
      text-transform: uppercase;
      text-decoration: none;
      color: var(--sage);
      max-width: 40%;
      line-height: 1.45;
    }
    .btn-nav-step.primary { color: var(--terra); text-align: right; max-width: 56%; }
    .btn-nav-step:hover { text-decoration: underline; text-underline-offset: 4px; }

    .page-number {
      font-family: "PT Serif", Georgia, serif;
      font-size: 12.5px;
      color: var(--muted);
      letter-spacing: .04em;
    }

    /* ---------------------------------------------------------------- плашка «сохранено» */
    .save-indicator {
      position: fixed;
      left: 50%;
      bottom: 22px;
      transform: translateX(-50%) translateY(8px);
      background: var(--paper);
      border: 1px solid var(--rule);
      border-radius: 0;
      color: var(--sage);
      font-family: "PT Sans", Arial, sans-serif;
      font-size: 9.5px;
      letter-spacing: .16em;
      text-transform: uppercase;
      padding: 10px 18px;
      opacity: 0;
      pointer-events: none;
      transition: opacity .2s ease, transform .2s ease;
      z-index: 40;
      box-shadow: none;
    }

    .save-indicator.show { opacity: 1; transform: translateX(-50%) translateY(0); }

    /* ---------------------------------------------------------------- телефон */
    @media (max-width: 640px) {
      body { font-size: 16.5px; padding: 0 16px 84px; }
      .cover-art { margin-left: -16px; margin-right: -16px; }
      .cover-title { font-size: 32px; }
      h1 { font-size: 27px; }
      h2 { font-size: 21px; }
      .cover-lead { font-size: 17px; }
      .hero-image { max-width: 100%; }
      .quote-box { font-size: 17.5px; }
      .btn-nav-step, .btn-nav-step.primary { font-size: 9px; letter-spacing: .1em; }
      .page-footer-nav { gap: 8px; }
    }
"""


def main():
    html = SRC.read_text(encoding="utf-8")

    # 1. шрифты книжечки вместо веб-шрифтов
    html = re.sub(
        r'<link href="https://fonts\.googleapis\.com/css2\?family=Cormorant[^"]*"[^>]*>',
        FONT_LINK, html, count=1)

    # 2. стили целиком заменяются на печатные
    start = html.find("<style>")
    end = html.find("</style>")
    assert start != -1 and end != -1
    html = html[:start] + "<style>" + CSS + "</style>" + html[end + len("</style>"):]

    # 3. заголовок вкладки
    html = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", html, count=1)
    html = html.replace(
        '<meta name="viewport"',
        '<meta name="color-scheme" content="light">\n  <meta name="viewport"', 1)

    # 4. убираем белые подложки из разметки — на бумаге их нет
    for old, new in [
        (' style="background:#fff;"', ''),
        (' style="background: #FFFFFF;"', ''),
        ('style="background:#5A7365; margin-top:16px;"', 'style="margin-top:16px;"'),
    ]:
        html = html.replace(old, new)

    # 5. номера страниц в подвале — как в книжечке
    counter = {"n": 1}

    def footer(match):
        counter["n"] += 1
        block = match.group(0)
        number = counter["n"]
        block = block.replace(
            '<a class="btn-nav-step primary"',
            f'<span class="page-number">{number}</span>\n      <a class="btn-nav-step primary"', 1)
        return block

    html = re.sub(r'<div class="page-footer-nav">.*?</div>', footer, html, flags=re.S)

    OUT.write_text(html, encoding="utf-8")
    print(f"собрано: {OUT.name} — {OUT.stat().st_size:,} байт")


if __name__ == "__main__":
    main()
