#!/usr/bin/env python3
"""Печатная книжечка второй тетради «Одна и та же ссора» — A5.

Текст берётся из собранного HTML (`couple_workbook_2_one_quarrel.html`), чтобы
книжка и тетрадь не расходились: правим текст в одном месте, печать собирается
из него же. Стиль — тот же, что у книжечки первой тетради: кремовая бумага,
PT Serif в тексте, PT Sans в подписях, волосяные линии, поля 16 мм, строки
для письма 7 мм под ручку.

Каждый экран тетради начинается с новой страницы; длинные экраны
переносятся, а поле записи всегда занимает остаток страницы — как в обычной
бумажной тетради.

Запуск из корня репозитория:
    python3 generate_pdf_couple_l2_booklet.py
"""

from __future__ import annotations

import base64
import io
import math
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

import pdf_plates as plates

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel.html"
FONT_DIR = ROOT / "therapy-workbooks" / "assets" / "fonts"
OUT = ROOT / "therapy-workbooks" / "couple_workbook_2_one_quarrel_booklet.pdf"
IMG_DIR = Path("/tmp/wb2_booklet_img")

W, H = A5
M = 16 * mm
CW = W - 2 * M
TOP = H - 15 * mm
BOTTOM = 17 * mm

CREAM = HexColor("#F7F5F0")
INK = HexColor("#2C3539")
BODY = HexColor("#3B474C")
MUTED = HexColor("#6A7378")
SAGE = HexColor("#5A7365")
SAGE_LIGHT = HexColor("#EBF1ED")
TERRA = HexColor("#C87D65")
TERRA_DEEP = HexColor("#B1634B")
TERRA_LIGHT = HexColor("#FDF3E7")
RULE = HexColor("#DDD6CB")
RULE_SOFT = HexColor("#E8E2D8")
PAPER_DEEP = HexColor("#F1EDE4")
DOTS = HexColor("#C9C3B8")
FAINT = HexColor("#8E877D")

BOOK_TITLE = "Одна и та же ссора"

# ── шрифты ──────────────────────────────────────────────────────────────────
def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("PTSerif", str(FONT_DIR / "PTSerif-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("PTSerif-Bold", str(FONT_DIR / "PTSerif-700-normal.ttf")))
    pdfmetrics.registerFont(TTFont("PTSerif-Italic", str(FONT_DIR / "PTSerif-400-italic.ttf")))
    pdfmetrics.registerFont(TTFont("PTSans", str(FONT_DIR / "PTSans-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("PTSans-Bold", str(FONT_DIR / "PTSans-700-normal.ttf")))
    pdfmetrics.registerFontFamily(
        "PTSerif", normal="PTSerif", bold="PTSerif-Bold",
        italic="PTSerif-Italic", boldItalic="PTSerif-Bold",
    )
    pdfmetrics.registerFontFamily(
        "PTSans", normal="PTSans", bold="PTSans-Bold",
        italic="PTSans", boldItalic="PTSans-Bold",
    )


STYLES: dict[str, ParagraphStyle] = {}


def build_styles() -> None:
    base = dict(fontName="PTSerif", fontSize=10.2, leading=14.4, textColor=BODY,
                allowWidows=0, allowOrphans=0)
    STYLES["body"] = ParagraphStyle("body", **base)
    STYLES["body_tight"] = ParagraphStyle("body_tight", parent=STYLES["body"], spaceBefore=0)
    STYLES["small"] = ParagraphStyle("small", parent=STYLES["body"], fontSize=9.3, leading=13.2)
    STYLES["lead"] = ParagraphStyle(
        "lead", fontName="PTSerif-Italic", fontSize=10.7, leading=15.2,
        textColor=HexColor("#40505A"),
    )
    STYLES["h1"] = ParagraphStyle("h1", fontName="PTSerif-Bold", fontSize=21, leading=25)
    STYLES["h1"].textColor = INK
    STYLES["h1_cover"] = ParagraphStyle(
        "h1_cover", fontName="PTSerif-Bold", fontSize=29, leading=32.5, textColor=INK,
    )
    STYLES["h2"] = ParagraphStyle(
        "h2", fontName="PTSerif-Bold", fontSize=13.2, leading=17, textColor=INK,
    )
    STYLES["h3"] = ParagraphStyle(
        "h3", fontName="PTSerif-Bold", fontSize=10.6, leading=14, textColor=INK,
    )
    STYLES["quote"] = ParagraphStyle(
        "quote", fontName="PTSerif-Italic", fontSize=10.6, leading=15,
        textColor=HexColor("#40544A"),
    )
    STYLES["note"] = ParagraphStyle(
        "note", fontName="PTSerif-Italic", fontSize=9.2, leading=13, textColor=MUTED,
    )
    STYLES["source"] = ParagraphStyle(
        "source", fontName="PTSans", fontSize=7.0, leading=9.8, textColor=FAINT,
    )
    STYLES["sans"] = ParagraphStyle(
        "sans", fontName="PTSans", fontSize=8.6, leading=12.2, textColor=BODY,
    )
    STYLES["tick"] = ParagraphStyle(
        "tick", fontName="PTSerif", fontSize=9.9, leading=13.6, textColor=BODY,
    )


# ── маленькие помощники ─────────────────────────────────────────────────────
# Соответствие «страница тетради» → «страница книжки». Заполняется в main()
PAGE_MAP: dict[int, int] = {}
REF_RE = re.compile(r"(страниц[уыеа]?\s+)(\d{1,2})(?!\d)", re.IGNORECASE)


def fix_refs(text: str) -> str:
    """Ссылки внутри текста («вернитесь на страницу 4») — в печатных номерах.

    В тетради на экране страницы 1–18, в книжке они другие: иначе ссылка
    на бумаге отправляет читателя не туда.
    """
    if not PAGE_MAP:
        return text

    def sub(m):
        n = int(m.group(2))
        return f"{m.group(1)}{PAGE_MAP.get(n, n)}"

    return REF_RE.sub(sub, text)


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("&", "&amp;")
    return text


def clean_inline(text: str) -> str:
    """Как clean, но с сохранением пробела на стыке с соседним тегом.

    Без этого «<strong>Пометка.</strong> Это значит…» склеивается в
    «Пометка.Это значит».
    """
    text = re.sub(r"\s+", " ", str(text)).replace("&", "&amp;")
    if text != text.strip():
        head = " " if text[:1] == " " else ""
        tail = " " if text[-1:] == " " else ""
        text = head + text.strip() + tail
    return text


def inline(el: Tag) -> str:
    """Разметка абзаца для reportlab: strong/em/br сохраняются."""
    out = []
    for node in el.children:
        if isinstance(node, NavigableString):
            out.append(clean(str(node)))
        elif isinstance(node, Tag):
            inner = inline(node)
            if node.name in ("strong", "b"):
                out.append(f"<b>{inner}</b>")
            elif node.name in ("em", "i"):
                out.append(f"<i>{inner}</i>")
            elif node.name == "br":
                out.append("<br/>")
            else:
                out.append(inner)
    return "".join(out).replace("&amp;", "&", 0)


def markup(el: Tag) -> str:
    """Текст элемента как разметка reportlab (с экранированием)."""
    def walk(node) -> str:
        if isinstance(node, NavigableString):
            return clean_inline(node)
        if not isinstance(node, Tag):
            return ""
        if node.name == "br":
            return "<br/>"
        inner = "".join(walk(n) for n in node.children)
        if node.name in ("strong", "b"):
            return f"<b>{inner}</b>"
        if node.name in ("em", "i"):
            return f"<i>{inner}</i>"
        return inner
    text = "".join(walk(n) for n in el.children)
    return fix_refs(re.sub(r"\s+", " ", text).strip())


def text_of(el: Tag) -> str:
    return fix_refs(re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip())


def measure(html: str, style: str, width: float, extra: dict | None = None) -> float:
    st = STYLES[style]
    if extra:
        st = ParagraphStyle("tmp", parent=st, **extra)
    return Paragraph(html, st).wrap(width, 10000)[1]


def draw_para(c, html, x, y, width, style="body", extra=None) -> float:
    st = STYLES[style]
    if extra:
        st = ParagraphStyle("tmp", parent=st, **extra)
    p = Paragraph(html, st)
    _, h = p.wrapOn(c, width, 10000)
    p.drawOn(c, x, y - h)
    return y - h


def kicker(c, text, x, y, color=SAGE, size=6.9, space=1.35):
    c.saveState()
    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont("PTSans-Bold", size)
    t.setFillColor(color)
    t.setCharSpace(space)
    t.textOut(text.upper())
    c.drawText(t)
    c.restoreState()


def tracked_text(c, text, x, y, font="PTSans-Bold", size=7.0, color=SAGE, space=1.2):
    """Текст с разрядкой через текстовый объект (Tc живёт в графическом состоянии)."""
    c.saveState()
    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(space)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()


def rule(c, x, y, width, color=RULE, lw=0.55):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x, y, x + width, y)
    c.restoreState()


def card(c, x, y, width, height, fill=SAGE_LIGHT, bar=None, bar_color=TERRA):
    c.saveState()
    c.setFillColor(fill)
    c.rect(x, y - height, width, height, stroke=0, fill=1)
    if bar:
        c.setFillColor(bar_color)
        c.rect(x, y - height, bar, height, stroke=0, fill=1)
    c.restoreState()


# ── картинки ────────────────────────────────────────────────────────────────
def extract_images(html: str) -> list[Path]:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    pat = re.compile(r'src="data:image/(jpeg|png);base64,([^"]+)"')
    paths = []
    for i, m in enumerate(pat.finditer(html)):
        p = IMG_DIR / f"img_{i:02d}.{m.group(1)}"
        if not p.exists():
            p.write_bytes(base64.b64decode(m.group(2)))
        paths.append(p)
    return paths


def on_cream(path: Path) -> Path:
    return plates.on_cream(path, IMG_DIR)


def image_size(path: Path) -> tuple[float, float]:
    im = Image.open(path)
    return im.width, im.height


def draw_image(c, path: Path, x, y_top, width) -> float:
    from reportlab.lib.utils import ImageReader

    iw, ih = image_size(path)
    height = width * ih / iw
    src = ImageReader(str(on_cream(path)))
    mask = ImageReader(plates.feather_mask(path, IMG_DIR, (iw, ih)))
    c.drawImage(src, x, y_top - height, width, height, mask=mask)
    return height


# ─────────────────────────────────────────────────────────────────────────────
class Book:
    """Поток страниц: сам переносит блок на новую страницу, если не влез."""

    def __init__(self, c):
        self.c = c
        self.page = 0
        self.y = TOP
        self.running = ("", "")
        self.starts: dict[str, int] = {}
        self.first_page = True
        self.folio_done = set()
        self.tight = False   # экран не влез — верстаем плотнее на пару пунктов

    def gap(self, value: float) -> float:
        return value * (0.82 if self.tight else 1.0)

    # ---- страницы -----------------------------------------------------
    def new_page(self, running=None):
        c = self.c
        if not self.first_page:
            self.folio()
            c.showPage()
        self.first_page = False
        self.page += 1
        c.setFillColor(CREAM)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        if running is not None:
            self.running = running
        left, right = self.running
        if left or right:
            c.saveState()
            if left:
                tracked_text(c, left.upper(), M, TOP + 5.2 * mm, "PTSans", 6.8, MUTED, 1.15)
            if right:
                wtext = right.upper()
                width = pdfmetrics.stringWidth(wtext, "PTSans", 6.8) + 1.15 * len(wtext)
                tracked_text(c, wtext, M + CW - width, TOP + 5.2 * mm, "PTSans", 6.8, MUTED, 1.15)
            c.restoreState()
            rule(c, M, TOP + 3.4 * mm, CW, RULE_SOFT, 0.5)
        self.y = TOP

    def folio(self, skip=False):
        if skip or self.page <= 1 or self.page in self.folio_done:
            return
        self.folio_done.add(self.page)
        c = self.c
        c.saveState()
        c.setFont("PTSans", 7.4)
        c.setFillColor(FAINT)
        c.drawCentredString(W / 2, 10 * mm, str(self.page))
        c.restoreState()

    def fits(self, h: float) -> bool:
        return self.y - h >= BOTTOM

    def need(self, h: float, running_extra=None):
        if not self.fits(h):
            self.new_page()
            return True
        return False

    def space(self, pts: float):
        self.y -= self.gap(pts)

    # ---- блоки --------------------------------------------------------
    def para(self, html, style="body", before=0.0, after=2.8 * mm, width=None,
             x=None, indent=0.0, keep_with_next=False):
        """Абзац с переносом через страницу — как в книге.

        Если абзац не помещается целиком, он разрывается по строкам, а не
        уезжает на новую страницу целиком: иначе в конце главы остаются
        страницы с одной фразой.
        """
        width = width or (CW - indent)
        x = M + indent if x is None else x
        before = self.gap(before)
        after = self.gap(after)
        if before:
            self.y -= before
        st = STYLES[style]
        c = self.c
        rest = Paragraph(html, st)
        total = 0.0
        first = True
        while True:
            avail = self.y - BOTTOM
            if avail < st.leading * 2:
                self.new_page()
                if keep_with_next and first:
                    self.y = TOP
                avail = self.y - BOTTOM
            w, h = rest.wrap(width, avail)
            if h <= avail:
                rest.drawOn(c, x, self.y - h)
                self.y -= h
                total += h
                break
            frags = rest.split(width, avail)
            if len(frags) < 2 or frags[0].height < st.leading * 2:
                self.new_page()
                if keep_with_next and first:
                    self.y = TOP
                continue
            frag, rest = frags[0], frags[1]
            frag.wrap(width, avail)
            frag.drawOn(c, x, self.y - frag.height)
            total += frag.height
            self.new_page()
            first = False
        self.y -= after
        return total

    def heading(self, html, style="h2", before=5.4 * mm, after=2.4 * mm, keep=16 * mm):
        h = measure(html, style, CW)
        before, after = self.gap(before), self.gap(after)
        if before:
            self.y -= before
        if self.y - h - keep < BOTTOM and self.page > 1:
            self.new_page()
            self.y = TOP - 2 * mm
        draw_para(self.c, html, M, self.y, CW, style)
        self.y -= h + after

    def kicker(self, text, color=SAGE, before=0.0, after=2.2 * mm):
        self.y -= before
        if self.y - 4 * mm < BOTTOM:
            self.new_page()
        kicker(self.c, text, M, self.y - 2.2 * mm, color)
        self.y -= 2.2 * mm + after

    def hairline(self, before=3 * mm, after=3 * mm, color=RULE):
        self.y -= before
        if self.y - 2 < BOTTOM:
            self.new_page()
        rule(self.c, M, self.y, CW, color)
        self.y -= after

    # ---- записи -------------------------------------------------------
    def writing_lines(self, rows: float = 1.0, indent: float = 0.0,
                      after=3.2 * mm, gap=7 * mm, fill_to_bottom=False,
                      reserve: float = 0.0):
        """Строки под ручку с шагом 7 мм.

        fill_to_bottom — поле занимает всю оставшуюся часть страницы:
        так в бумажной тетради и бывает.
        """
        c = self.c
        x = M + indent
        width = CW - indent
        floor = BOTTOM + reserve
        if fill_to_bottom:
            rows = int((self.y - floor - 2 * mm) // gap)
            if rows < 3:
                # совсем не осталось места — начинаем страницу заново
                self.new_page()
                rows = int((self.y - floor - 2 * mm) // gap)
            rows = max(rows, 3)
        else:
            rows = max(1, int(rows))
            if self.y - rows * gap < BOTTOM:
                self.new_page()
        c.saveState()
        c.setStrokeColor(DOTS)
        c.setLineWidth(0.5)
        c.setDash(1.1, 2.3)
        first = self.y - 1.4 * mm
        for i in range(rows):
            c.line(x, first - i * gap, x + width, first - i * gap)
        c.restoreState()
        self.y = first - (rows - 1) * gap - after

    def tick_rows(self, items, after=3.2 * mm):
        c = self.c
        for item in items:
            html = markup(item)
            h = max(measure(html, "tick", CW - 7 * mm), 5.6 * mm)
            if self.y - h < BOTTOM:
                self.new_page()
            box = 3.0 * mm
            c.saveState()
            c.setStrokeColor(HexColor("#B9B1A4"))
            c.setLineWidth(0.55)
            c.rect(M + 0.4 * mm, self.y - 4.4 * mm, box, box, stroke=1, fill=0)
            c.restoreState()
            draw_para(c, html, M + 7 * mm, self.y - 1.2 * mm, CW - 7 * mm, "tick")
            self.y -= h + 1.4 * mm
        self.y -= after


# ── тексты, которые в печати звучат иначе ───────────────────────────────────
PRINT_REPLACE = {
    # браузерных кнопок на бумаге нет — обещание должно остаться честным
    "Их можно забрать с собой или стереть. Ни то, ни другое не обязательно.":
        "Их можно переписать начисто, сфотографировать или оставить как есть. "
        "Ни то, ни другое не обязательно.",
    # про закладку в браузере и заметки в телефоне на бумаге говорить нечего
    "Если вы откроете тетрадь через неделю, она предложит продолжить с того места, "
    "где вы остановились.": "",
    "Если неудобно печатать — наговорите ответ голосом в заметки телефона и "
    "перенесите сюда.": "",
    "Эти строки сохраняются сами, кнопки нет.": "",
    # в бумаге запись и так остаётся на странице — повторять нечего
    "Всё, что вы напишете, остаётся в этом браузере: никуда не отправляется, "
    "и мы этого не видим.": "",
}

PRINT_COVER_NOTE = (
    "Если вы бросили на неделю — ничего не потерялось. Вернитесь с того места, "
    "где остановились. Тетрадь не обидится."
)

PRINT_PRIVACY = (
    "<b>Где ваши записи.</b> Всё, что вы пишете, остаётся на этих страницах. "
    "Никуда не отправляется, и мы их не видим. Если захотите сохранить — "
    "сфотографируйте заполненные страницы; если захотите начать заново — "
    "возьмите новую тетрадь. Старую можно просто убрать."
)

PRINT_SOURCE_END = (
    "Это печатная версия тетради: записи остаются на бумаге и видны тому, "
    "кто возьмёт её в руки. Если это важно, храните тетрадь там, где её не "
    "увидит никто лишний."
)

# ─────────────────────────────────────────────────────────────────────────────
# Оценка высоты: чтобы поле записи не съедало место у следующего блока
# ─────────────────────────────────────────────────────────────────────────────
def estimate_block(el: Tag, ctx: dict) -> float:
    """Сколько места займёт блок — чтобы поле записи оставило ему место.

    Это именно оценка: точные размеры зависят от переноса строк. Но если
    оценка занижена, после поля записи блок уезжает на пустую страницу —
    а пустая страница в тетради выглядит как брак.
    """
    cls = classes(el)
    name = el.name

    if cls & SKIP or "running-head" in cls or "folio" in cls:
        return 0.0
    # выходные данные уезжают на последнюю страницу — место на экране не занимают
    if "colophon" in cls:
        return 0.0
    if name == "h1":
        return measure(markup(el), "h1", CW) + 7 * mm
    if name == "h2":
        return measure(markup(el), "h2", CW) + 7.6 * mm
    if name == "h3":
        return measure(markup(el), "h3", CW) + 5 * mm
    if "line-block" in cls:
        h = 0.0
        label = el.select_one(".line-label")
        prompt = el.select_one(".line-prompt")
        note = el.select_one(".line-note")
        if label is not None:
            h += 5.2 * mm
        if prompt is not None:
            h += measure(markup(prompt), "note", CW) + 2.2 * mm
        h += (len(el.select(".line-field")) + len(el.select(".tick-item"))) * 9.6 * mm
        if note is not None:
            h += measure(markup(note), "note", CW) + 2.4 * mm
        return h + 3.2 * mm
    if "margin-note" in cls:
        return measure(markup(el), "note", CW - 14 * mm) + 5 * mm
    if "source-note" in cls:
        txt = text_of(el)
        if "браузере" in txt:
            txt = PRINT_SOURCE_END
        return measure(clean(txt), "source", CW) + 5.4 * mm
    if "fact-box" in cls:
        body = el.find("p")
        inner = CW - 12 * mm
        h = measure(markup(body) if body is not None else markup(el), "small", inner)
        return h + (9 * mm if el.select_one(".fact-label") is not None else 6 * mm) + 4 * mm
    if "bridge-note" in cls:
        inner = CW - 12 * mm
        h = sum(measure(markup(p), "small", inner) for p in el.find_all("p"))
        return h + 4 * mm * len(el.find_all("p")) + 6 * mm + 5 * mm
    if "fallback-note" in cls:
        return measure(markup(el), "small", CW - 13 * mm) + 13 * mm
    if "stop-box" in cls:
        return measure(markup(el.find("p") or el), "h3", CW - 12 * mm) + 12 * mm
    if "quote-box" in cls:
        inner = CW - 13 * mm
        h = sum(measure(markup(p), "quote", inner) for p in el.find_all("p"))
        return h + 6 * mm * len(el.find_all("p")) + 10 * mm
    if "pull-quote" in cls:
        return measure(markup(el), "quote", CW - 20 * mm) + 9 * mm
    if "compare" in cls:
        colw = (CW - 5 * mm) / 2
        h = 0.0
        for col in el.select(".compare-col"):
            head, p = col.find("h4"), col.find("p")
            h = max(h, (measure(markup(head), "h3", colw - 8.4 * mm) if head else 0)
                    + (measure(markup(p), "small", colw - 8.4 * mm) if p else 0)
                    + 8.4 * mm + 3 * mm)
        return h + 4.4 * mm
    if "memo" in cls:
        inner = CW - 16 * mm
        return sum(measure(markup(li), "small", inner) + 2 * mm for li in el.find_all("li")) + 18 * mm
    if "tick-list" in cls:
        return len(el.select(".tick-item")) * 7 * mm + 3 * mm
    if "interactive-card" in cls:
        return 22 * mm
    if "chapter-open" in cls:
        return 8.4 * mm
    if "part-head" in cls:
        return 24 * mm
    if "week-line" in cls:
        return 12 * mm
    if "week-caption" in cls:
        return 8 * mm
    if "colophon" in cls:
        return 26 * mm
    if name == "figure":
        img = el.find("img")
        if img is None:
            return 12 * mm
        path = ctx["image_by_src"].get(img.get("src", ""))
        if path is None:
            return 12 * mm
        iw, ih = image_size(path)
        return CW * ih / iw + 10 * mm
    if name == "ul":
        return sum(measure(markup(li), "body", CW - 7 * mm) + 2 * mm for li in el.find_all("li")) + 3 * mm
    if name == "ol":
        return sum(measure(markup(li), "body", CW - 9 * mm) + 2 * mm
                   for li in el.find_all("li", recursive=False)) + 3 * mm
    if name == "p":
        style = "lead" if "chapter-lead" in cls else (
            "note" if cls & {"cover-note", "partner-note", "safety-note"} else "body")
        txt = text_of(el)
        if txt in PRINT_REPLACE:
            txt = PRINT_REPLACE[txt]
            if not txt:
                return 0.0
        return measure(clean(txt), style, CW) + 3.4 * mm
    return 10 * mm


# ─────────────────────────────────────────────────────────────────────────────
# Элементы
# ─────────────────────────────────────────────────────────────────────────────
SKIP = {
    "folio", "page-footer-nav", "tools-row", "progress-line", "progress-dots",
    "btn-cover-start", "resume-btn", "cover-note-js",
}


def classes(el: Tag) -> set[str]:
    return set(el.get("class", []))


def render(book: Book, el: Tag, ctx: dict) -> None:
    c = book.c
    cls = classes(el)
    name = el.name

    if cls & SKIP:
        return

    # Короткий хвост после блока (одна сноска, одно примечание) не должен
    # уезжать на пустую страницу: если блок и хвост вместе не влезают,
    # начинаем с новой страницы — тогда они встанут рядом.
    tail = ctx.get("tail", 0.0)
    own = estimate_block(el, ctx)
    if own and 0 < tail < 34 * mm:
        avail = book.y - BOTTOM
        if own <= avail and own + tail > avail and avail < own + tail + 40 * mm:
            book.new_page()

    # ── заголовки ───────────────────────────────────────────────────────
    if name == "h1":
        book.space(1.5 * mm)
        h = measure(markup(el), "h1", CW)
        if not book.fits(h + 12 * mm):
            book.new_page()
        draw_para(c, markup(el), M, book.y, CW, "h1")
        book.y -= h + 2.4 * mm
        rule(c, M, book.y, 22 * mm, TERRA, 1.2)
        book.y -= 3.4 * mm
        return

    if name == "h2":
        book.heading(markup(el), "h2", before=5.2 * mm, after=2.0 * mm)
        return

    if name == "h3":
        book.heading(markup(el), "h3", before=3.2 * mm, after=1.6 * mm)
        return

    if name == "h4":
        h = measure(markup(el), "h3", CW)
        if not book.fits(h + 8 * mm):
            book.new_page()
        book.kicker(text_of(el), color=TERRA_DEEP, after=1.4 * mm)
        return

    # ── открытие главы и части ──────────────────────────────────────────
    if "chapter-open" in cls:
        fig = el.select_one(".chapter-fig")
        kind = el.select_one(".chapter-kicker")
        book.space(0)
        if fig is not None:
            c.saveState()
            c.setFont("PTSerif-Bold", 15)
            c.setFillColor(TERRA_DEEP)
            c.drawString(M, book.y - 5.4 * mm, text_of(fig))
            w = pdfmetrics.stringWidth(text_of(fig), "PTSerif-Bold", 15)
            if kind is not None:
                tracked_text(c, text_of(kind).upper(), M + w + 3.6 * mm,
                             book.y - 5.0 * mm, "PTSans", 6.9, MUTED, 1.3)
            c.restoreState()
            book.y -= 8.4 * mm
        return

    if "part-head" in cls:
        num = el.select_one(".part-num")
        kick = el.select_one(".part-kicker")
        leads = el.select(".part-lead")
        need = 26 * mm + sum(measure(markup(p), "lead", CW - 20 * mm) + 2 * mm for p in leads)
        if not book.fits(need):
            book.new_page()
        top = book.y
        if num is not None:
            c.saveState()
            c.setFont("PTSerif-Bold", 40)
            c.setFillColor(TERRA)
            c.drawString(M, top - 12 * mm, text_of(num))
            c.restoreState()
        if kick is not None:
            kicker(c, text_of(kick), M + 21 * mm, top - 8.6 * mm, TERRA_DEEP, size=7.4)
        rule(c, M + 21 * mm, top - 11 * mm, 18 * mm, RULE, 0.6)
        book.y = top - 18 * mm
        for lead in leads:
            book.para(markup(lead), "lead", width=CW - 20 * mm, x=M + 21 * mm,
                      after=2.2 * mm)
        book.y -= 1.6 * mm
        book.hairline(before=1 * mm, after=4 * mm)
        return

    # ── абзацы ──────────────────────────────────────────────────────────
    if name == "p":
        if "chapter-lead" in cls:
            book.para(markup(el), "lead", after=3.4 * mm)
            return
        if "source-note" in cls:
            txt = text_of(el)
            if "браузере" in txt:
                txt = PRINT_SOURCE_END
            book.hairline(before=3 * mm, after=1.6 * mm, color=RULE_SOFT)
            book.para(clean(txt), "source", after=2.4 * mm)
            return
        if "safety-note" in cls:
            html = markup(el)
            h = measure(html, "note", CW - 6 * mm)
            if not book.fits(h + 8 * mm):
                book.new_page()
            card(c, M, book.y, CW, h + 6 * mm, PAPER_DEEP, 1.3 * mm, TERRA)
            draw_para(c, html, M + 6.5 * mm, book.y - 3 * mm, CW - 12 * mm, "note")
            book.y -= h + 6 * mm + 3.4 * mm
            return
        if "cover-note" in cls:
            txt = text_of(el)
            if txt in PRINT_REPLACE:
                if not PRINT_REPLACE[txt]:
                    return
                book.para(clean(PRINT_REPLACE[txt]), "note", after=2.0 * mm)
                return
            book.para(markup(el), "note", after=2.0 * mm)
            return
        if "partner-note" in cls:
            book.para(markup(el), "note", after=3.2 * mm)
            return
        txt = text_of(el)
        if txt in PRINT_REPLACE:
            if not PRINT_REPLACE[txt]:
                return
            txt = PRINT_REPLACE[txt]
        book.para(clean(txt), "body", after=2.9 * mm)
        return

    # ── списки ──────────────────────────────────────────────────────────
    if name == "ul" and "checklist" in cls:
        for li in el.find_all("li", recursive=False):
            html = markup(li)
            h = measure(html, "tick", CW - 7 * mm)
            if not book.fits(max(h, 5 * mm) + 4 * mm):
                book.new_page()
            c.saveState()
            c.setFillColor(SAGE)
            c.circle(M + 1.4 * mm, book.y - 3.2 * mm, 0.95 * mm, stroke=0, fill=1)
            c.restoreState()
            draw_para(c, html, M + 6.4 * mm, book.y - 1.2 * mm, CW - 6.4 * mm, "tick")
            book.y -= max(h, 5 * mm) + 1.6 * mm
        book.y -= 2.6 * mm
        return

    if name == "ul" and "key-list" in cls:
        for li in el.find_all("li", recursive=False):
            html = markup(li)
            h = measure(html, "body", CW - 6.4 * mm)
            if not book.fits(max(h, 5 * mm) + 4 * mm):
                book.new_page()
            c.saveState()
            c.setFillColor(TERRA)
            c.circle(M + 1.3 * mm, book.y - 3.3 * mm, 0.8 * mm, stroke=0, fill=1)
            c.restoreState()
            draw_para(c, html, M + 6.4 * mm, book.y - 1.2 * mm, CW - 6.4 * mm, "body")
            book.y -= max(h, 5 * mm) + 1.7 * mm
        book.y -= 2.6 * mm
        return

    if name == "ol" and "contents-list" in cls:
        render_contents(book, el, ctx)
        return

    if name == "ol" and "protocol" in cls:
        render_protocol(book, el)
        return

    if name == "ol" and "start-steps" in cls:
        render_start_steps(book, el)
        return

    if name == "ol" and "num-list" in cls:
        render_num_list(book, el)
        return

    if "tick-list" in cls:
        items = el.select("li, .tick-item")
        book.tick_rows(items)
        return

    # ── карточки и врезки ───────────────────────────────────────────────
    if "fact-box" in cls:
        label = el.select_one(".fact-label")
        body = el.find("p")
        html = markup(body) if body is not None else markup(el)
        inner_w = CW - 12 * mm
        h_text = measure(html, "small", inner_w)
        h = h_text + (9 * mm if label is not None else 6 * mm)
        if not book.fits(h + 4 * mm):
            book.new_page()
        card(c, M, book.y, CW, h, PAPER_DEEP)
        yy = book.y - 4.4 * mm
        if label is not None:
            kicker(c, text_of(label), M + 6 * mm, yy - 1.6 * mm, SAGE)
            yy -= 4.4 * mm
        draw_para(c, html, M + 6 * mm, yy, inner_w, "small")
        book.y -= h + 4 * mm
        return

    if "stop-box" in cls:
        html = markup(el.find("p") or el)
        h = measure(html, "h3", CW - 12 * mm)
        if not book.fits(h + 14 * mm):
            book.new_page()
        card(c, M, book.y, CW, h + 8 * mm, TERRA_LIGHT, 1.6 * mm, TERRA)
        draw_para(c, html, M + 7 * mm, book.y - 4 * mm, CW - 14 * mm, "h3")
        book.y -= h + 8 * mm + 4 * mm
        return

    if "margin-note" in cls:
        html = markup(el)
        w = CW - 14 * mm
        h = measure(html, "note", w)
        if not book.fits(h + 6 * mm):
            book.new_page()
        c.saveState()
        c.setStrokeColor(TERRA)
        c.setLineWidth(0.9)
        c.line(M + 5 * mm, book.y, M + 5 * mm, book.y - h - 1 * mm)
        c.restoreState()
        draw_para(c, html, M + 10 * mm, book.y, w - 3 * mm, "note")
        book.y -= h + 4.6 * mm
        return

    if "bridge-note" in cls:
        label = el.select_one(".bridge-label")
        paras = el.find_all("p")
        inner_w = CW - 12 * mm
        hs = [measure(markup(p), "small", inner_w) for p in paras]
        h = sum(hs) + 4 * mm * max(0, len(hs) - 1) + 6 * mm + (5 * mm if label else 0)
        if not book.fits(h + 4 * mm):
            book.new_page()
        card(c, M, book.y, CW, h, SAGE_LIGHT)
        yy = book.y - 4 * mm
        if label is not None:
            kicker(c, text_of(label), M + 6 * mm, yy - 1.4 * mm, SAGE)
            yy -= 5 * mm
        for p, ph in zip(paras, hs):
            draw_para(c, markup(p), M + 6 * mm, yy, inner_w, "small")
            yy -= ph + 4 * mm
        book.y -= h + 4 * mm
        return

    if "privacy-note" in cls:
        html = PRINT_PRIVACY
        inner_w = CW - 12 * mm
        h = measure(html, "small", inner_w)
        if not book.fits(h + 12 * mm):
            book.new_page()
        card(c, M, book.y, CW, h + 9 * mm, PAPER_DEEP)
        draw_para(c, html, M + 6 * mm, book.y - 4.5 * mm, inner_w, "small")
        book.y -= h + 9 * mm + 4.6 * mm
        return

    if "fallback-note" in cls:
        html = markup(el)
        inner_w = CW - 12 * mm
        h = measure(html, "small", inner_w)
        if not book.fits(h + 12 * mm):
            book.new_page()
        card(c, M, book.y, CW, h + 9 * mm, SAGE_LIGHT, 1.3 * mm, SAGE)
        draw_para(c, html, M + 6.5 * mm, book.y - 4.5 * mm, CW - 13 * mm, "small")
        book.y -= h + 9 * mm + 4.6 * mm
        return

    if "pull-quote" in cls:
        html = markup(el)
        h = measure(html, "quote", CW - 20 * mm)
        if not book.fits(h + 16 * mm):
            book.new_page()
        book.y -= 3 * mm
        c.saveState()
        c.setStrokeColor(TERRA)
        c.setLineWidth(0.8)
        c.line(M + 6 * mm, book.y + 1 * mm, M + 6 * mm, book.y - h)
        c.restoreState()
        draw_para(c, html, M + 13 * mm, book.y, CW - 20 * mm,
                  extra={"fontName": "PTSerif-Italic", "fontSize": 12.4, "leading": 17.4,
                         "textColor": HexColor("#41544A")})
        book.y -= h + 6.6 * mm
        return

    if "compare" in cls:
        cols = el.select(".compare-col")
        render_compare(book, cols)
        return

    if "quote-box" in cls:
        render_quote(book, el)
        return

    if "memo" in cls:
        render_memo(book, el)
        return

    if "week-line" in cls:
        render_week(book, el)
        return

    if "week-caption" in cls:
        book.para(clean(text_of(el)), "note", after=3.4 * mm)
        return

    if "colophon" in cls:
        # выходные данные книги ставятся на последнюю страницу — запоминаем
        ctx["colophon"] = el
        return

    # ── записи ──────────────────────────────────────────────────────────
    if "interactive-card" in cls:
        num = el.select_one(".ask-num")
        title = el.find("h3")
        book.space(4 * mm)
        # «Запись N», её заголовок и начало поля — одно целое:
        # заголовок не должен оставаться один в низу страницы
        if not book.fits(18 * mm + 26 * mm + 49 * mm):
            book.new_page()
            book.space(2 * mm)
        if num is not None:
            kicker(c, text_of(num), M, book.y - 2.2 * mm, TERRA_DEEP)
            book.y -= 5.4 * mm
        if title is not None:
            h = measure(markup(title), "h2", CW)
            draw_para(c, markup(title), M, book.y, CW, "h2")
            book.y -= h + 2.2 * mm
        rule(c, M, book.y, 16 * mm, TERRA, 1.1)
        book.y -= 4 * mm
        return

    if "entry-block" in cls:
        render_entry(book, el, ctx)
        return

    if "line-block" in cls:
        render_line_block(book, el, ctx)
        return

    if "line-note" in cls:
        txt = text_of(el)
        if txt in PRINT_REPLACE and not PRINT_REPLACE[txt]:
            return
        book.para(clean(PRINT_REPLACE.get(txt, txt)), "note", after=3.2 * mm)
        return

    if "start-where" in cls:
        book.para(clean("Подробнее — " + text_of(el).replace("Подробнее — ", "")),
                  "note", after=1.4 * mm)
        return

    # ── иллюстрации ─────────────────────────────────────────────────────
    if name == "figure" and "circle-diagram" in cls:
        render_circle(book, el)
        return

    if name == "figure":
        render_figure(book, el, ctx)
        return

    # ── прочее ──────────────────────────────────────────────────────────
    if "running-head" in cls:
        return

    if "cover-art" in cls or "cover-body" in cls:
        return  # обложка рисуется отдельно

    # неизвестный блок: не молчим, иначе текст тихо потеряется
    raise SystemExit(f"Не знаю, как напечатать <{name} class='{' '.join(sorted(cls))}'>")


# ── отдельные элементы ──────────────────────────────────────────────────────
def render_contents(book: Book, el: Tag, ctx: dict) -> None:
    c = book.c
    pages: dict[str, int] = ctx.get("toc_pages", {})
    for li in el.find_all("li", recursive=False):
        title = li.select_one(".toc-title")
        num = li.select_one(".toc-page")
        mins = li.select_one(".toc-min")
        target = li.get("data-target", "")
        label = text_of(title) if title else ""
        page = pages.get(target, num.get_text(strip=True) if num else "")
        mtext = text_of(mins) if mins else ""
        h = 5.4 * mm
        if not book.fits(h + 3 * mm):
            book.new_page()
        c.saveState()
        c.setFont("PTSerif", 9.4)
        c.setFillColor(BODY)
        c.drawString(M, book.y - 3.4 * mm, label)
        tw = pdfmetrics.stringWidth(label, "PTSerif", 9.4)
        right = M + CW - 15 * mm
        lx = M + tw + 2.4 * mm
        if lx < right - 4 * mm:
            c.setStrokeColor(HexColor("#CFC8BC"))
            c.setLineWidth(0.45)
            c.setDash(0.5, 2.2)
            c.line(lx, book.y - 2 * mm, right, book.y - 2 * mm)
            c.setDash()
        c.setFont("PTSans", 7.4)
        c.setFillColor(SAGE)
        c.drawRightString(right, book.y - 3.2 * mm, mtext)
        c.setFillColor(BODY)
        c.setFont("PTSans", 7.8)
        c.drawRightString(M + CW, book.y - 3.2 * mm, str(page))
        c.restoreState()
        book.y -= h
    book.y -= 2.6 * mm


def render_protocol(book: Book, el: Tag) -> None:
    c = book.c
    for step in el.select(".protocol-step"):
        time = step.select_one(".protocol-time")
        body = step.select_one(".protocol-body")
        title = body.find("h3") if body else None
        paras = body.find_all("p") if body else []
        ttxt = text_of(time).replace(" мин", " мин")
        col = 15 * mm
        html_title = markup(title) if title is not None else ""
        hs = [measure(markup(p), "small", CW - col) for p in paras]
        h = measure(html_title, "h3", CW - col) + 1.4 * mm + sum(hs) + 1.8 * mm * len(hs)
        if not book.fits(h + 4 * mm):
            book.new_page()
        c.saveState()
        c.setFont("PTSans-Bold", 7.6)
        c.setFillColor(TERRA_DEEP)
        c.drawString(M, book.y - 3.6 * mm, ttxt)
        c.restoreState()
        yy = draw_para(c, html_title, M + col, book.y, CW - col, "h3")
        yy -= 1.4 * mm
        for p, ph in zip(paras, hs):
            draw_para(c, markup(p), M + col, yy, CW - col, "small")
            yy -= ph + 1.8 * mm
        book.y -= h + 3.4 * mm
        rule(c, M, book.y + 1.6 * mm, CW, RULE_SOFT, 0.4)


def render_start_steps(book: Book, el: Tag) -> None:
    c = book.c
    for i, li in enumerate(el.find_all("li", recursive=False), start=1):
        title = li.find("h3")
        p = li.find("p")
        line = li.select_one(".line-field")
        where = li.select_one(".start-where")
        head_h = measure(markup(title), "h3", CW - 10 * mm) if title else 0
        p_h = measure(markup(p), "small", CW - 10 * mm) if p else 0
        total = max(head_h + 1.4 * mm + p_h + 12 * mm, 22 * mm)
        if not book.fits(total + 4 * mm):
            book.new_page()
        c.saveState()
        c.setFont("PTSerif-Bold", 13)
        c.setFillColor(TERRA)
        c.drawString(M, book.y - 4.4 * mm, str(i))
        c.restoreState()
        yy = book.y
        if title is not None:
            yy = draw_para(c, markup(title), M + 9 * mm, yy, CW - 9 * mm, "h3")
        if p is not None:
            yy -= 1.2 * mm
            yy = draw_para(c, markup(p), M + 9 * mm, yy, CW - 9 * mm, "small")
        book.y = yy - 2 * mm
        if line is not None:
            book.writing_lines(rows=1, indent=9 * mm, after=1.6 * mm)
        if where is not None:
            draw_para(c, f"<i>{clean(text_of(where))}</i>", M + 9 * mm, book.y,
                      CW - 9 * mm, "note")
            book.y -= 4.6 * mm
        book.y -= 3.6 * mm


def render_num_list(book: Book, el: Tag) -> None:
    c = book.c
    ask = "ask-list" in classes(el)
    for i, li in enumerate(el.find_all("li", recursive=False), start=1):
        if li.find_parent("ol") is not el:
            continue
        if ask:
            q = li.select_one(".ask-q")
            txt = markup(q) if q is not None else markup(li)
            h = measure(txt, "body", CW - 9 * mm)
            if not book.fits(h + 14 * mm):
                book.new_page()
            c.saveState()
            c.setFont("PTSerif-Bold", 10)
            c.setFillColor(TERRA_DEEP)
            c.drawString(M, book.y - 3.4 * mm, f"{i}")
            c.restoreState()
            yy = draw_para(c, txt, M + 7 * mm, book.y, CW - 7 * mm, "body")
            book.y = yy - 1.6 * mm
            book.writing_lines(rows=1, indent=7 * mm, after=3.0 * mm)
            continue
        title = li.find("h3")
        p = li.find("p")
        head_h = measure(markup(title), "h3", CW - 9 * mm) if title else 0
        p_h = measure(markup(p), "small", CW - 9 * mm) if p else 0
        total = head_h + (1.4 * mm + p_h if p else 0)
        if not book.fits(total + 5 * mm):
            book.new_page()
        c.saveState()
        c.setFont("PTSans-Bold", 7.4)
        c.setFillColor(SAGE)
        c.circle(M + 2.6 * mm, book.y - 2.6 * mm, 2.6 * mm, stroke=0, fill=1)
        c.setFillColor(CREAM)
        c.drawCentredString(M + 2.6 * mm, book.y - 3.6 * mm, str(i))
        c.restoreState()
        yy = book.y
        if title is not None:
            yy = draw_para(c, markup(title), M + 7.5 * mm, yy, CW - 7.5 * mm, "h3")
        if p is not None:
            yy -= 1.2 * mm
            yy = draw_para(c, markup(p), M + 7.5 * mm, yy, CW - 7.5 * mm, "small")
        book.y = yy - 3.2 * mm


def render_compare(book: Book, cols) -> None:
    c = book.c
    gap = 5 * mm
    colw = (CW - gap) / 2
    pad = 4.2 * mm
    heights = []
    for col in cols:
        head = col.find("h4")
        p = col.find("p")
        h = measure(markup(head), "h3", colw - 2 * pad) if head else 0
        h += measure(markup(p), "small", colw - 2 * pad) if p else 0
        heights.append(h + 2 * pad + 3 * mm)
    total_h = max(heights)
    if not book.fits(total_h + 4 * mm):
        book.new_page()
    for idx, col in enumerate(cols):
        x = M + idx * (colw + gap)
        head = col.find("h4")
        p = col.find("p")
        fill = TERRA_LIGHT if idx else SAGE_LIGHT
        card(c, x, book.y, colw, total_h, fill)
        yy = book.y - pad
        if head is not None:
            kicker(c, text_of(head), x + pad, yy - 2.4 * mm,
                   TERRA_DEEP if idx else SAGE, size=6.6, space=1.1)
            yy -= 6 * mm
        if p is not None:
            draw_para(c, markup(p), x + pad, yy, colw - 2 * pad, "small")
    book.y -= total_h + 4.4 * mm


def render_quote(book: Book, el: Tag) -> None:
    c = book.c
    items = []
    for child in el.children:
        if not isinstance(child, Tag):
            continue
        if "quote-label" in classes(child):
            items.append(("label", text_of(child), "after" in classes(child)))
        elif child.name == "p":
            items.append(("text", markup(child), False))
    pad = 5 * mm
    h_body = 0
    for kind, val, _ in items:
        h_body += measure(val, "quote", CW - 2 * pad - 3 * mm) if kind == "text" else 6 * mm
    h = h_body + 2 * pad
    if not book.fits(h + 4 * mm):
        book.new_page()
    card(c, M, book.y, CW, h, PAPER_DEEP, 1.5 * mm, SAGE)
    yy = book.y - pad
    for kind, val, is_after in items:
        if kind == "label":
            kicker(c, val, M + pad + 2 * mm, yy - 2.2 * mm,
                   TERRA_DEEP if is_after else SAGE, size=6.5, space=1.2)
            yy -= 6 * mm
        else:
            yy = draw_para(c, val, M + pad + 2 * mm, yy, CW - 2 * pad - 3 * mm, "quote")
            yy -= 1.6 * mm
    book.y -= h + 4.4 * mm


def render_memo(book: Book, el: Tag) -> None:
    c = book.c
    title = el.find("h3")
    items = [markup(li) for li in el.find_all("li")]
    pad = 5 * mm
    inner = CW - 2 * pad - 6 * mm
    hs = [measure(f"{i}. {t}", "small", inner) for i, t in enumerate(items, 1)]
    h = (measure(markup(title), "h3", inner) + 3 * mm if title else 0) + sum(hs) \
        + 2 * mm * len(hs) + 2 * pad
    if not book.fits(h + 4 * mm):
        book.new_page()
    card(c, M, book.y, CW, h, SAGE_LIGHT)
    yy = book.y - pad
    if title is not None:
        th = measure(markup(title), "h3", inner)
        draw_para(c, markup(title), M + pad, yy, inner, "h3")
        yy -= th + 3 * mm
    for i, (txt, hh) in enumerate(zip(items, hs), start=1):
        p = Paragraph(f"{i}. {txt}", STYLES["small"])
        p.wrapOn(c, inner, 10000)
        p.drawOn(c, M + pad, yy - hh)
        yy -= hh + 2 * mm
    book.y -= h + 4.4 * mm


def render_week(book: Book, el: Tag) -> None:
    c = book.c
    days = el.select(".week-day")
    if not book.fits(14 * mm):
        book.new_page()
    step = CW / len(days)
    for i, day in enumerate(days):
        x = M + i * step + step / 2
        c.saveState()
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.circle(x, book.y - 4.6 * mm, 3.4 * mm, stroke=1, fill=0)
        c.setFont("PTSans", 7.2)
        c.setFillColor(BODY)
        c.drawCentredString(x, book.y - 5.4 * mm, text_of(day))
        c.restoreState()
    book.y -= 12 * mm


def render_notes_page(book: Book) -> None:
    """Страница «Для заметок»: строки для письма во всю полосу."""
    c = book.c
    c.saveState()
    c.setFont("PTSerif-Bold", 15)
    c.setFillColor(INK)
    c.drawString(M, book.y - 5 * mm, "Для заметок")
    c.restoreState()
    book.y -= 9 * mm
    rule(c, M, book.y, 22 * mm, TERRA, 1.2)
    book.y -= 5 * mm
    book.writing_lines(rows=99, fill_to_bottom=True)


def render_colophon(book: Book, el: Tag) -> None:
    c = book.c
    lines = [text_of(p) for p in el.find_all("p")]
    if not book.fits(26 * mm):
        book.new_page()
    book.y -= 4 * mm
    cx = W / 2
    c.saveState()
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(cx - 24 * mm, book.y, cx - 3 * mm, book.y)
    c.line(cx + 3 * mm, book.y, cx + 24 * mm, book.y)
    c.setStrokeColor(TERRA)
    c.circle(cx, book.y, 1.6 * mm, stroke=1, fill=0)
    c.restoreState()
    book.y -= 7 * mm
    for i, line in enumerate(lines):
        c.saveState()
        c.setFont("PTSerif" if i == 0 else "PTSans", 9.4 if i == 0 else 7.4)
        c.setFillColor(INK if i == 0 else MUTED)
        c.drawCentredString(cx, book.y, line)
        c.restoreState()
        book.y -= 5.4 * mm
    # одна строка на прощание: без неё последняя страница выглядит пустой
    book.y -= 6 * mm
    c.saveState()
    c.setFont("PTSerif-Italic", 9.4)
    c.setFillColor(BODY)
    c.drawCentredString(cx, book.y, "Тетрадь закончилась, а разговор — нет.")
    c.restoreState()



def render_circle(book: Book, el: Tag) -> None:
    """Круг «нажим — отступление»: рисуем заново, уже векторно.

    SVG из тетради переносить в PDF нельзя: наконечники стрелок делаются
    маркерами, а их PDF не понимает — стрелки теряют направление.
    """
    c = book.c
    cap = el.find("figcaption")
    box_h = 58 * mm
    cap_h = measure(markup(cap), "note", CW) if cap is not None else 0
    if not book.fits(box_h + cap_h + 8 * mm):
        book.new_page()
    top = book.y - 1 * mm
    # пропорции из SVG: 360×190
    sx = CW / 360.0
    oy = top - 4 * mm

    def px(x):  # x из системы SVG
        return M + x * sx

    def py(y):  # y сверху вниз, как в SVG
        return oy - y * sx

    r = 28 * sx
    c.saveState()
    # левый круг — «один»
    c.setFillColor(SAGE_LIGHT)
    c.setStrokeColor(SAGE)
    c.setLineWidth(0.7)
    c.circle(px(64), py(96), r, stroke=1, fill=1)
    # правый круг — «другой»
    c.setFillColor(TERRA_LIGHT)
    c.setStrokeColor(TERRA)
    c.circle(px(296), py(96), r, stroke=1, fill=1)

    # верхняя дуга: от левого к правому
    p = c.beginPath()
    p.moveTo(px(100), py(74))
    p.curveTo(px(150), py(48), px(210), py(48), px(258), py(72))
    c.setStrokeColor(TERRA)
    c.setLineWidth(0.9)
    c.drawPath(p, stroke=1, fill=0)
    # нижняя дуга: от правого к левому
    p = c.beginPath()
    p.moveTo(px(260), py(122))
    p.curveTo(px(210), py(148), px(150), py(148), px(102), py(124))
    c.setStrokeColor(SAGE)
    c.drawPath(p, stroke=1, fill=0)

    def arrow_head(x, y, dx, dy, color):
        L = 3.2 * mm
        w = 1.6 * mm
        norm = math.hypot(dx, dy) or 1
        ux, uy = dx / norm, dy / norm
        bx, by = x - ux * L, y - uy * L
        c.setFillColor(color)
        p = c.beginPath()
        p.moveTo(x, y)
        p.lineTo(bx - uy * w, by + ux * w)
        p.lineTo(bx + uy * w, by - ux * w)
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    arrow_head(px(258), py(72), 1, -0.45, TERRA)
    arrow_head(px(102), py(124), -1, -0.45, SAGE)

    tracked_text(c, "ОДИН", px(64) - 8 * mm, py(152), "PTSerif", 6.6, SAGE, 1.3)
    tracked_text(c, "ДРУГОЙ", px(296) - 11 * mm, py(152), "PTSerif", 6.6, TERRA_DEEP, 1.3)
    tracked_text(c, "НАЖИМ", px(180) - 8 * mm, py(40), "PTSerif", 6.4, TERRA_DEEP, 1.4)
    tracked_text(c, "ОТСТУПЛЕНИЕ", px(180) - 19 * mm, py(180), "PTSerif", 6.4, SAGE, 1.4)
    c.restoreState()

    book.y = oy - 190 * sx - (cap_h + 3 * mm if cap is not None else 4 * mm)
    if cap is not None:
        draw_para(c, markup(cap), M, book.y + cap_h, CW, "note")
        book.y -= 2 * mm


def render_figure(book: Book, el: Tag, ctx: dict) -> None:
    """Иллюстрация: вписать в остаток страницы, не обрезая.

    Высота — главное ограничение: вертикальная картинка во всю ширину
    не влезает в A5, и её нельзя ни обрезать, ни уронить за нижнее поле.
    Поэтому считаем ширину от свободной высоты.
    """
    c = book.c
    img = el.find("img")
    cap = el.find("figcaption")
    if img is None:
        return
    path = ctx["image_by_src"].get(img.get("src", ""))
    if path is None:
        raise SystemExit("Не нашёл файл иллюстрации")
    iw, ih = image_size(path)
    aspect = ih / iw
    cap_text = markup(cap) if cap is not None else ""
    plate = "figure-plate" in classes(el)
    max_w = CW * (0.78 if plate else 1.0)

    def cap_height(width):
        if not cap_text:
            return 0.0
        return measure(cap_text, "note", width) + 3.2 * mm

    def place(width):
        x = M + (CW - width) / 2
        h = width * aspect
        draw_image(c, path, x, book.y - 1 * mm, width)
        book.y -= h + 1 * mm + 3.2 * mm
        if cap_text:
            ch = measure(cap_text, "note", width)
            draw_para(c, cap_text, x, book.y, width, "note")
            book.y -= ch + 2.2 * mm
        book.y -= 2.4 * mm

    # 1) во всю ширину, если влезает
    if max_w * aspect + cap_height(max_w) + 6 * mm <= book.y - BOTTOM:
        place(max_w)
        return
    # 2) по ширине полосы на новой странице — но только если влезает по высоте
    room = TOP - BOTTOM - cap_height(max_w) - 8 * mm
    fit_w = min(max_w, room / aspect)
    if max_w * aspect + 6 * mm > book.y - BOTTOM:
        book.new_page()
    # 3) на новой странице вписываем в свободную высоту
    room = book.y - BOTTOM - cap_height(max_w) - 6 * mm
    width = min(max_w, room / aspect)
    place(width)


def render_entry(book: Book, el: Tag, ctx: dict) -> None:
    """Поле записи: подпись, подсказка и линейки до низа страницы."""
    c = book.c
    kind = el.select_one(".entry-kind")
    hint = el.select_one(".entry-hint")
    kind_txt = text_of(kind) if kind is not None else ""
    pair = "kind-pair" in classes(kind) if kind is not None else False
    hint_html = markup(hint) if hint is not None else ""
    hint_h = measure(hint_html, "h3", CW) if hint_html else 0
    head = 8 * mm + hint_h + 2.4 * mm
    # Запись начинается с новой страницы, если под подписью не остаётся
    # места хотя бы на восемь строк: шапка не должна стоять одна.
    reserve = min(ctx.get("reserve", 0.0), 45 * mm)
    if book.y - head - 8 * 7 * mm < BOTTOM + reserve:
        book.new_page()
    if kind_txt:
        color = TERRA_DEEP if pair else SAGE
        c.saveState()
        c.setFillColor(color)
        c.circle(M + 1.3 * mm, book.y - 2.6 * mm, 1.1 * mm, stroke=0, fill=1)
        c.restoreState()
        kicker(c, kind_txt, M + 5 * mm, book.y - 3.1 * mm, color, size=6.7, space=1.25)
        book.y -= 5.6 * mm
    if hint_html:
        draw_para(c, hint_html, M, book.y, CW, "h3")
        book.y -= hint_h + 2.4 * mm
    book.writing_lines(fill_to_bottom=True, after=0, reserve=reserve)


def render_line_block(book: Book, el: Tag, ctx: dict | None = None) -> None:
    c = book.c
    label = el.select_one(".line-label")
    prompt = el.select_one(".line-prompt")
    note = el.select_one(".line-note")
    fields = el.select(".line-field")
    ticks = el.select(".tick-list")
    # Сколько места нужно, чтобы под подписью осталось место писать.
    # Последний блок страницы довольствуется тремя строками, а блок,
    # после которого ещё есть текст, требует восьми — иначе подпись
    # оказывается внизу страницы, а писать негде.
    if ctx and ctx.get("tail", 0.0) > 0:
        need_rows = 1
    elif ctx and ctx.get("is_last"):
        need_rows = 3
    else:
        need_rows = 8
    head = 0.0
    if label is not None and text_of(label):
        head += 5.2 * mm
    if prompt is not None:
        head += measure(markup(prompt), "note", CW) + 2.2 * mm
    if prompt is not None or (label is not None and text_of(label)):
        if not book.fits(head + need_rows * 7 * mm):
            book.new_page()
    if label is not None and text_of(label):
        kicker(c, text_of(label), M, book.y - 2.2 * mm, TERRA_DEEP)
        book.y -= 5.2 * mm
    if prompt is not None:
        html = markup(prompt)
        h = measure(html, "note", CW)
        draw_para(c, html, M, book.y, CW, "note")
        book.y -= h + 2.2 * mm
    if not book.fits(12 * mm):
        book.new_page()
    for idx, _ in enumerate(fields):
        last = idx == len(fields) - 1
        fill = last and not ticks and ctx["tail"] <= 0
        book.writing_lines(rows=1, after=2.6 * mm, fill_to_bottom=fill)
    for tick_list in ticks:
        book.tick_rows(tick_list.select("label, .tick-item"), after=2.6 * mm)
    if note is not None:
        txt = text_of(note)
        if PRINT_REPLACE.get(txt, txt):
            book.para(clean(PRINT_REPLACE.get(txt, txt)), "note", after=2.4 * mm)
    book.y -= 1.6 * mm


# ─────────────────────────────────────────────────────────────────────────────
# Обложка
# ─────────────────────────────────────────────────────────────────────────────
def page_cover(book: Book, card_el: Tag, ctx: dict) -> None:
    c = book.c
    book.new_page(running=("", ""))
    art = card_el.select_one(".cover-art img")
    body = card_el.select_one(".cover-body")
    path = ctx["image_by_src"].get(art.get("src")) if art is not None else None
    top = H
    if path is not None:
        iw, ih = image_size(path)
        h = W * ih / iw
        c.drawImage(str(on_cream(path)), 0, H - h, W, h, mask="auto")
        top = H - h
    badge = body.select_one(".badge-label")
    title = body.find("h1")
    lead = body.select_one(".cover-lead")
    items = [text_of(i) for i in body.select(".cover-item")]
    meta = body.select_one(".cover-meta")
    cover_rule = body.select_one(".cover-rule")

    y = top - 14 * mm
    if badge is not None:
        kicker(c, text_of(badge), M, y, TERRA_DEEP, size=7.0, space=1.4)
        y -= 10 * mm
    th = measure(markup(title), "h1_cover", CW)
    draw_para(c, markup(title), M, y, CW, "h1_cover")
    y -= th + 4 * mm
    if cover_rule is not None:
        rule(c, M, y, 26 * mm, TERRA, 1.3)
        y -= 5.4 * mm
    if lead is not None:
        lh = measure(markup(lead), "lead", CW * 0.96)
        draw_para(c, markup(lead), M, y, CW * 0.96, "lead")
        y -= lh + 7 * mm
    c.saveState()
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(M, y + 2 * mm, M + CW, y + 2 * mm)
    c.restoreState()
    for item in items:
        c.saveState()
        c.setFillColor(TERRA)
        c.circle(M + 1.1 * mm, y - 1.6 * mm, 0.75 * mm, stroke=0, fill=1)
        c.restoreState()
        draw_para(c, clean(item), M + 5.4 * mm, y, CW - 5.4 * mm, "small")
        y -= 5.6 * mm
    note = body.select_one(".cover-note")
    if note is not None:
        draw_para(c, clean(PRINT_COVER_NOTE), M, y - 4 * mm, CW * 0.96, "note")
    c.saveState()
    c.setFont("PTSans", 7.2)
    c.setFillColor(MUTED)
    meta_txt = "8 записей · два разговора по 30 минут · можно без партнёра"
    tracked_text(c, meta_txt.upper(), M, 24 * mm, "PTSans", 7.2, MUTED, 0.9)
    c.setFont("PTSans-Bold", 7.2)
    c.setFillColor(SAGE)
    c.drawRightString(M + CW, 24 * mm, "УРОВЕНЬ 2")
    c.restoreState()
    rule(c, M, 30 * mm, CW, RULE, 0.6)


# ─────────────────────────────────────────────────────────────────────────────
def build(cards, images, toc_pages=None, draw=True):
    c = canvas.Canvas(str(OUT), pagesize=A5) if draw else None
    book = Book(c) if draw else None
    return book, c


def toc_entries(soup) -> list[tuple[str, str]]:
    lst = soup.select_one(".contents-list")
    out = []
    if lst is None:
        return out
    for li in lst.find_all("li"):
        title = li.select_one(".toc-title")
        out.append((li.get("data-target", ""), text_of(title) if title else ""))
    return out


def main() -> int:
    register_fonts()
    build_styles()
    html = SRC.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    images = extract_images(html)
    image_by_src = {}
    idx = 0
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if idx < len(images):
            image_by_src[src] = images[idx]
        idx += 1
    ctx = {"images": images, "image_by_src": image_by_src, "toc_pages": {}}

    cards = soup.select(".page-card")
    ids = [c.get("id") for c in cards]
    if ids != [f"p{i}" for i in range(len(cards))]:
        raise SystemExit(f"Страницы идут не подряд: {ids}")

    tight: set[str] = set()
    notebook_page: dict[int, int] = {}

    def run(toc_pages):
        c = canvas.Canvas(str(OUT), pagesize=A5)
        book = Book(c)
        ctx["toc_pages"] = toc_pages
        ctx["tight_cards"] = tight
        starts = {}
        notebook_page.clear()
        for card_el in cards:
            cid = card_el.get("id")
            if cid == "p0":
                page_cover(book, card_el, ctx)
                book.folio(skip=True)
                continue
            rh = card_el.select_one(".running-head")
            running = ("", "")
            if rh is not None:
                spans = rh.find_all("span", recursive=False)
                left = text_of(spans[0]) if spans else ""
                right = text_of(rh.select_one(".rh-right")) if rh.select_one(".rh-right") else ""
                running = (left, right)
            book.new_page(running=running)
            starts[cid] = book.page
            folio_span = card_el.select_one(".folio-page")
            if folio_span is not None:
                m = re.search(r"Стр\.\s*(\d+)", folio_span.get_text(" ", strip=True))
                if m:
                    notebook_page[int(m.group(1))] = book.page
            book.tight = cid in ctx.get("tight_cards", set())
            children = [ch for ch in card_el.children if isinstance(ch, Tag)]
            for i, child in enumerate(children):
                rest = children[i + 1:]
                raw = sum(estimate_block(nxt, ctx) for nxt in rest)
                # Держим место только под короткий хвост экрана (сноска, примечание):
                # длинную часть главы после поля записи переносим на следующую
                # страницу — иначе строки для письма остаются в три штуки.
                ctx["reserve"] = raw + 2 * mm if 0 < raw < 45 * mm else 0.0
                ctx["tail"] = raw
                ctx["is_last"] = raw <= 0
                render(book, child, ctx)
            # короткий «хвост» экрана на отдельной странице — верстаем плотнее
            if cid != "p0" and book.page > starts[cid] and (TOP - book.y) < 42 * mm:
                tight.add(cid)
            book.folio()
        # ── конец книги ─────────────────────────────────────────────────
        # Книжка печатается брошюрой: число страниц должно делиться на четыре,
        # иначе последняя тетрадь листа останется пустой половиной.
        # Добираем недостающие страницы «Для заметок» — они всегда пригодятся.
        note_running = ("", "")
        # выходные данные займут ещё одну страницу — её и считаем
        while (book.page + 1) % 4:
            book.new_page(running=note_running)
            render_notes_page(book)
        # выходные данные — на последней странице, у нижнего поля
        if ctx.get("colophon") is not None:
            book.new_page(running=("", ""))
            book.folio()
            book.y = BOTTOM + 26 * mm
            render_colophon(book, ctx["colophon"])
            c.showPage()
        total = book.page
        return c, book, starts, total

    # первый прогон — чтобы узнать, с какой страницы начинается каждая глава
    _, book, starts, total = run({})
    PAGE_MAP.update(notebook_page)
    pages = {k: v for k, v in starts.items()}
    # второй и третий прогоны: номера в содержании и плотная вёрстка
    # там, где экран оставлял почти пустую страницу
    for _ in range(3):
        before_tight = set(tight)
        c, book, starts2, total2 = run(pages)
        if starts2 != starts:
            pages = starts2
            continue
        if tight == before_tight:
            break

    c.setTitle("Одна и та же ссора — рабочая тетрадь, уровень 2")
    c.setAuthor("PsyLab")
    c.setSubject("Тетрадь для пар · печатная версия")
    c.save()
    print(f"Готово: {OUT} — {OUT.stat().st_size:,} байт, страниц: {total2}".replace(",", " "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
