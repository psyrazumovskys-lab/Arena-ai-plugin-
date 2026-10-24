#!/usr/bin/env python3
"""Печатная книжечка «Как вовремя остановить ссору» — A5, 12 страниц.

Это не распечатка HTML. Верстка собрана заново под печать:

- формат A5 (148×210 мм): 12 страниц = 3 листа A4 при двусторонней печати,
  ровно под буклетную брошюровку;
- книжная типографика: PT Serif для текста, PT Sans для надзаголовков;
- вместо полей ввода — пунктирные строки под ручку с шагом 7 мм (как в обычной
  тетради в линейку), число строк считается от нижней границы страницы;
- шкала кипения — печатная линейка из 10 делений вместо ползунка;
- шпаргалка — карточка 85×54 мм под вырезание (влезает в кошелёк);
- блок возврата после паузы вынесен на отдельную страницу;
- на второй странице — содержание с номерами страниц;
- иллюстрации стоят в родной пропорции (в печати ничего не обрезается),
  их бумага подогнана под кремовый фон страницы, поэтому не видно рамки.

Запуск из корня репозитория:
    python3 generate_pdf_couple_l1_booklet.py
"""

from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
SRC_HTML = ROOT / "therapy-workbooks" / "couple_workbook_1_stop_escalation.html"
FONT_DIR = ROOT / "therapy-workbooks" / "assets" / "fonts"
OUT = ROOT / "therapy-workbooks" / "couple_workbook_1_stop_escalation_booklet.pdf"
IMG_DIR = Path("/tmp/booklet_img")

W, H = A5
M = 16 * mm
CW = W - 2 * M
TOP = H - 16 * mm

# ── палитра из HTML ─────────────────────────────────────────────────────────
CREAM = HexColor("#F7F5F0")
TEXT = HexColor("#2C3539")
MUTED = HexColor("#7A8288")
BODY = HexColor("#3B474C")
SAGE = HexColor("#5A7365")
SAGE_LIGHT = HexColor("#EBF1ED")
TERRA = HexColor("#C87D65")
TERRA_LIGHT = HexColor("#FDF3E7")
RULE = HexColor("#DDD6CB")
DOTS = HexColor("#C9C3B8")
Z_GREEN = HexColor("#8FB8A8")
Z_SAND = HexColor("#E2C99F")
Z_RED = HexColor("#C87D65")


# ── шрифты ──────────────────────────────────────────────────────────────────
def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("PTSerif", str(FONT_DIR / "PTSerif-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("PTSerif-Bold", str(FONT_DIR / "PTSerif-700-normal.ttf")))
    pdfmetrics.registerFont(TTFont("PTSerif-Italic", str(FONT_DIR / "PTSerif-400-italic.ttf")))
    pdfmetrics.registerFont(TTFont("PTSans", str(FONT_DIR / "PTSans-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("PTSans-Bold", str(FONT_DIR / "PTSans-700-normal.ttf")))
    pdfmetrics.registerFontFamily(
        "PTSerif",
        normal="PTSerif",
        bold="PTSerif-Bold",
        italic="PTSerif-Italic",
        boldItalic="PTSerif-Bold",
    )
    pdfmetrics.registerFontFamily("PTSans", normal="PTSans", bold="PTSans-Bold",
                                  italic="PTSans", boldItalic="PTSans-Bold")


STYLES = {}


def build_styles() -> None:
    STYLES["body"] = ParagraphStyle(
        "body", fontName="PTSerif", fontSize=10.2, leading=14.2,
        textColor=BODY, alignment=0,
    )
    STYLES["body_small"] = ParagraphStyle(
        "body_small", parent=STYLES["body"], fontSize=9.0, leading=13.0,
    )
    STYLES["lead"] = ParagraphStyle(
        "lead", fontName="PTSerif-Italic", fontSize=10.3, leading=14.6,
        textColor=HexColor("#4A5459"),
    )
    STYLES["h1"] = ParagraphStyle(
        "h1", fontName="PTSerif-Bold", fontSize=20, leading=23.6,
        textColor=TEXT,
    )
    STYLES["h1_cover"] = ParagraphStyle(
        "h1_cover", fontName="PTSerif-Bold", fontSize=27, leading=30.5,
        textColor=TEXT,
    )
    STYLES["h3"] = ParagraphStyle(
        "h3", fontName="PTSans-Bold", fontSize=9.4, leading=12.6,
        textColor=TEXT,
    )
    STYLES["quote"] = ParagraphStyle(
        "quote", fontName="PTSerif-Italic", fontSize=20 / 2.4, leading=13.4,
        textColor=HexColor("#41544A"),
    )
    STYLES["note"] = ParagraphStyle(
        "note", fontName="PTSans", fontSize=8.0, leading=11.2,
        textColor=MUTED,
    )
    STYLES["label"] = ParagraphStyle(
        "label", fontName="PTSans-Bold", fontSize=7.2, leading=10,
        textColor=SAGE,
    )


# ── примитивы ───────────────────────────────────────────────────────────────
def para(c, text, x, y, width, style="body", extra=None):
    """Рисует абзац от верхней границы y, возвращает новую верхнюю границу."""
    st = STYLES[style]
    if extra:
        st = ParagraphStyle("tmp", parent=st, **extra)
    p = Paragraph(text, st)
    _, h = p.wrapOn(c, width, 2000)
    p.drawOn(c, x, y - h)
    return y - h


def tracked(c, text, x, y, font="PTSans-Bold", size=7.4, color=SAGE, space=1.2):
    """Текст с разрядкой.

    Важно: Tc в PDF — часть графического состояния и не сбрасывается сам,
    поэтому всё заворачивается в q…Q. Без этого разрядка утекает во весь
    остальной текст на странице и он вылезает за поля.
    """
    c.saveState()
    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(space)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()


def kicker(c, text, x, y, color=SAGE, size=7.4, space=1.6):
    tracked(c, text.upper(), x, y, size=size, color=color, space=space)
    return y


def heading(c, text, x, y, width, style="h1"):
    return para(c, text, x, y, width, style)


def rule(c, x, y, width, color=RULE, lw=0.6):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x, y, x + width, y)
    c.restoreState()


def writing_lines(c, x, y, width, bottom=18 * mm, gap=7 * mm, count=None):
    """Пунктирные строки под ручку.

    Шаг 7 мм — как в обычной тетради в линейку: взрослому человеку так писать
    удобнее, и строк на странице помещается больше. Число строк считается само
    от нижней границы (bottom), поэтому низ страницы не пустует и ничего
    не наезжает на номер страницы.
    """
    if count is None:
        count = max(1, int((y - bottom) // gap) + 1)
    c.saveState()
    c.setStrokeColor(DOTS)
    c.setLineWidth(0.55)
    c.setDash(1.2, 2.2)
    for i in range(count):
        c.line(x, y - i * gap, x + width, y - i * gap)
    c.restoreState()
    return y - (count - 1) * gap


def bullet(c, text, x, y, width, dot_color=SAGE, style="body", gap_after=2.6 * mm):
    c.saveState()
    c.setFillColor(dot_color)
    c.circle(x + 1.1 * mm, y - 3.2 * mm, 1.05 * mm, stroke=0, fill=1)
    c.restoreState()
    y2 = para(c, text, x + 5.2 * mm, y, width - 5.2 * mm, style)
    return y2 - gap_after


def numbered(c, num, text, x, y, width, style="body"):
    c.saveState()
    c.setFillColor(SAGE_LIGHT)
    c.circle(x + 3.0 * mm, y - 3.0 * mm, 3.0 * mm, stroke=0, fill=1)
    c.setFillColor(SAGE)
    c.setFont("PTSans-Bold", 7.6)
    c.drawCentredString(x + 3.0 * mm, y - 3.9 * mm, str(num))
    c.restoreState()
    y2 = para(c, text, x + 9.5 * mm, y, width - 9.5 * mm, style)
    return min(y2, y - 6 * mm)


def card_bg(c, x, y, width, height, fill=SAGE_LIGHT, radius=2.2 * mm):
    c.saveState()
    c.setFillColor(fill)
    c.roundRect(x, y - height, width, height, radius, stroke=0, fill=1)
    c.restoreState()


def scissors(c, x, y, color=HexColor("#B3ABA0"), lw=0.5):
    """Маленькие ножницы для линии отреза.

    Символа ✂ в PT Sans нет — в печати он превращается в пустой квадрат,
    поэтому рисуем вручную: два кольца и два лезвия.
    """
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(CREAM)
    c.setLineWidth(lw)
    r = 0.62 * mm
    c.setLineWidth(0.45)
    c.circle(x + r, y + 0.7 * mm, r, stroke=1, fill=1)
    c.circle(x + r, y - 0.7 * mm, r, stroke=1, fill=1)
    c.setFillColor(color)
    c.circle(x + r, y + 0.7 * mm, 0.18 * mm, stroke=0, fill=1)
    c.circle(x + r, y - 0.7 * mm, 0.18 * mm, stroke=0, fill=1)
    # короткие лезвия: сходятся сразу за кольцами и расходятся на 1.9 мм
    c.setLineWidth(0.55)
    c.line(x + 1.15 * mm, y + 0.38 * mm, x + 5.8 * mm, y - 1.55 * mm)
    c.line(x + 1.15 * mm, y - 0.38 * mm, x + 5.8 * mm, y + 1.55 * mm)
    c.restoreState()


def footer(c, page_no, label=""):
    c.saveState()
    c.setFont("PTSans", 7.2)
    c.setFillColor(HexColor("#A8A199"))
    c.drawCentredString(W / 2, 11 * mm, str(page_no))
    if label:
        c.drawString(M, 11 * mm, label)
    c.restoreState()


def new_page(c, fill=CREAM):
    c.setFillColor(fill)
    c.rect(0, 0, W, H, stroke=0, fill=1)


# ── картинки ────────────────────────────────────────────────────────────────
def extract_images() -> list[Path]:
    import base64
    import re

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    html = SRC_HTML.read_text(encoding="utf-8")
    pat = re.compile(r'src="data:image/(jpeg|png);base64,([^"]+)"')
    paths = []
    for i, m in enumerate(pat.finditer(html)):
        p = IMG_DIR / f"img_{i:02d}.{m.group(1)}"
        if not p.exists():
            p.write_bytes(base64.b64decode(m.group(2)))
        paths.append(p)
    return paths


def on_cream(path: Path) -> Path:
    """Сажает иллюстрацию на бумагу страницы — точно, а не «на глаз».

    У картинок из тетради своя бумага, чуть темнее фона. Считаем цвет этой
    бумаги по рамке кадра и сдвигаем весь кадр так, чтобы бумага стала ровно
    цвета страницы: out = cream + (v - paper). Белое становится кремовым,
    тени и линии остаются, прямоугольника на печати не видно.
    Картинка при этом не обрезается — меняется только подложка.
    """
    out = IMG_DIR / f"cream_{path.stem}.jpg"
    if out.exists():
        return out
    im = Image.open(path).convert("RGB")
    w, h = im.size
    k = max(2, int(min(w, h) * 0.02))  # рамка, по которой меряем бумагу
    px = im.load()
    samples = [px[x, k] for x in range(0, w, max(1, w // 40))]
    samples += [px[x, h - 1 - k] for x in range(0, w, max(1, w // 40))]
    samples += [px[k, y] for y in range(0, h, max(1, h // 40))]
    samples += [px[w - 1 - k, y] for y in range(0, h, max(1, h // 40))]
    paper = [max(1, sum(s[i] for s in samples) // len(samples)) for i in range(3)]
    cream = (247, 245, 240)
    lut = []
    for i in range(3):
        shift = cream[i] - paper[i]
        lut += [max(0, min(255, v + shift)) for v in range(256)]
    im.point(lut).save(out, quality=92, optimize=True)
    return out


def draw_plate(c, path: Path, x, y, width):
    """Иллюстрация в родной пропорции, без обрезки.

    В тетради арт не кадрируется: композиция нарисована целиком, и обрезка
    отрезает руки и лица. Поэтому в печати картинка ставится «плашкой»
    на своём соотношении сторон.
    """
    from reportlab.lib.utils import ImageReader

    im = Image.open(path)
    height = width * im.height / im.width
    src = on_cream(path)
    c.drawImage(ImageReader(str(src)), x, y - height, width, height, mask="auto")
    return height


# ─────────────────────────────────────────────────────────────────────────────
# Страницы
# ─────────────────────────────────────────────────────────────────────────────
def page_cover(c, imgs):
    new_page(c)
    from reportlab.lib.utils import ImageReader

    im0 = Image.open(imgs[0])
    cover_h = W * im0.height / im0.width
    c.drawImage(ImageReader(str(on_cream(imgs[0]))), 0, H - cover_h, W, cover_h,
                mask="auto")
    h = cover_h

    y = H - cover_h - 19 * mm
    kicker(c, "Тетрадь для пар · уровень 1", M, y, TERRA)
    y -= 11 * mm
    y = heading(c, "Как вовремя<br/>остановить ссору", M, y, CW, "h1_cover")
    y -= 5 * mm
    y = para(c, "Простая инструкция: нажать на паузу, остыть и не сказать того, "
                "о чём потом будет больно.", M, y, CW * 0.94, "lead")

    rule(c, M, 30 * mm, CW)
    c.saveState()
    c.setFont("PTSans", 8.2)
    c.setFillColor(MUTED)
    c.drawString(M, 22 * mm, "6 коротких шагов · 10 минут")
    c.drawRightString(M + CW, 22 * mm, "можно возвращаться")
    c.restoreState()


def page_how_to(c, imgs):
    new_page(c)
    footer(c, 2, "")
    kicker(c, "Перед началом", M, TOP)
    y = heading(c, "Как читать эту тетрадь", M, TOP - 9 * mm, CW)
    y -= 6 * mm

    y = numbered(c, 1, "Читайте в спокойный момент, а не в разгар ссоры. Это подготовка, "
                       "а не скорая помощь: в момент, когда накрыло, читать бесполезно.",
                 M, y, CW)
    y -= 3.4 * mm
    y = numbered(c, 2, "Держите рядом ручку. В тетради есть места для записи — "
                       "то, что вы напишете своей рукой, вспоминается легче.",
                 M, y, CW)
    y -= 3.4 * mm
    y = numbered(c, 3, "Возвращайтесь. Десять минут — ориентир, а не норматив. "
                       "К любому шагу можно вернуться позже.",
                 M, y, CW)

    y -= 4 * mm
    y = para(c, "Внутри — шесть коротких шагов: почему в ссоре отключается голова, "
                "правило 20 минут и шпаргалка, которую можно носить с собой.",
             M, y, CW, "body_small")

    # оглавление — в печатной книжке без него не найти нужный разворот
    y -= 12 * mm
    tracked(c, "СОДЕРЖАНИЕ", M, y, space=1.4)
    y -= 7.5 * mm
    rows = [
        (1, "Почему в ссоре отключается голова", 4),
        (2, "Правило 20 минут тишины", 5),
        (3, "Что сказать, чтобы партнёр не обиделся", 7),
        (4, "Репетиция в спокойный вечер", 8),
        (5, "Шпаргалка в карман", 9),
        (6, "Первая победа: куда двигаться дальше", 10),
    ]
    for num, title, page in rows:
        c.saveState()
        c.setFillColor(SAGE)
        c.setFont("PTSans-Bold", 7.0)
        c.drawString(M, y - 2.5 * mm, str(num))
        c.setFillColor(BODY)
        c.setFont("PTSerif", 8.8)
        c.drawString(M + 5.5 * mm, y - 2.7 * mm, title)
        tw = pdfmetrics.stringWidth(title, "PTSerif", 8.8)
        lx = M + 5.5 * mm + tw + 2 * mm
        c.setStrokeColor(HexColor("#CFC8BC"))
        c.setLineWidth(0.5)
        c.setDash(0.5, 2.3)
        c.line(lx, y - 1.3 * mm, M + CW - 7 * mm, y - 1.3 * mm)
        c.setDash()
        c.setFillColor(HexColor("#8E877D"))
        c.setFont("PTSans", 7.6)
        c.drawRightString(M + CW, y - 2.7 * mm, str(page))
        c.restoreState()
        y -= 6.2 * mm

    c.saveState()
    c.setFillColor(HexColor("#8E877D"))
    c.setFont("PTSans", 7.0)
    c.drawString(M, y - 1.8 * mm,
                 "Возврат после паузы — с. 6   ·   Заметки для себя — с. 11")
    c.restoreState()

    # безопасность
    rule(c, M, 48 * mm, CW)
    para(c, "Если в ссорах звучат угрозы, доходит до ударов или вам страшно оставаться "
            "рядом — это не решается техникой паузы. Здесь нужна помощь специалиста, "
            "и лучше найти её до следующего раза.",
         M, 44 * mm, CW, "note")


def page_intro(c, imgs):
    new_page(c)
    footer(c, 3, "")
    plate_w = 49 * mm
    h = draw_plate(c, imgs[1], (W - plate_w) / 2, H - 14 * mm, plate_w)
    y = H - 14 * mm - h - 7 * mm

    kicker(c, "Введение", M, y)
    y -= 10 * mm
    y = heading(c, "Почему пауза работает", M, y, CW)
    y -= 2.5 * mm
    y = para(c, "Что происходит с телом, когда ссора набирает ход, "
                "и почему короткая пауза не помогает.", M, y, CW, "lead")
    y -= 5 * mm

    # факт-бокс
    box_h = 33 * mm
    box_top = y
    card_bg(c, M, box_top, CW, box_h, TERRA_LIGHT)
    c.saveState()
    c.setFillColor(TERRA)
    c.rect(M, box_top - box_h, 1.6 * mm, box_h, stroke=0, fill=1)
    c.restoreState()
    yy = box_top - 8 * mm
    tracked(c, "У ПАУЗЫ ДВЕ ГРАНИЦЫ", M + 7 * mm, yy, space=1.2,
            color=HexColor("#A4603F"), size=8.0)
    para(c, "Короче двадцати минут она не работает: тело ещё не остыло, и разговор пойдёт "
            "по второму кругу. Дольше суток — это уже не пауза, а способ не возвращаться. "
            "Всё, что делает паузу паузой, живёт между этими двумя границами.",
         M + 7 * mm, yy - 6 * mm, CW - 12 * mm, "body_small")
    y = box_top - box_h - 6 * mm

    y = para(c, "Ссорятся абсолютно все пары. Но счастливые пары отличаются не тем, "
                "что у них нет разногласий, а тем, что они умеют вовремя "
                "<b>притормозить</b>, пока разговор не превратился в перестрелку.",
             M, y, CW)

    # запись
    y -= 6 * mm
    kicker(c, "Запишите · индивидуально", M, y, HexColor("#8E7A52"), size=6.8)
    y -= 5.5 * mm
    y = para(c, "Вспомните прошедшую неделю. Каким одним словом вы бы описали "
                "ваши отношения?", M, y, CW, "h3")
    y -= 5.5 * mm
    writing_lines(c, M, y, CW)


def page_step1(c, imgs):
    new_page(c)
    footer(c, 4, "")
    kicker(c, "Шаг 1 из 6 · Градусник эмоций", M, TOP)
    y = heading(c, "Почему в ссоре<br/>отключается голова", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "В сильном гневе наше тело думает, что на нас напал медведь. Пульс "
                "подскакивает выше 100 ударов, кровь отливает от зоны логики. В этот "
                "момент мы <b>физически не способны</b> слышать чужие доводы.",
             M, y, CW)

    # шкала
    y -= 8 * mm
    y = para(c, "Вспомните последнюю ссору и отметьте, на сколько баллов кипело:",
             M, y, CW, "h3")
    y -= 6 * mm
    seg_w = (CW - 9 * 1.1 * mm) / 10
    for i in range(10):
        x = M + i * (seg_w + 1.1 * mm)
        col = Z_GREEN if i < 4 else (Z_SAND if i < 7 else Z_RED)
        c.saveState()
        c.setFillColor(col)
        c.roundRect(x, y - 4.4 * mm, seg_w, 4.4 * mm, 0.9 * mm, stroke=0, fill=1)
        c.setFillColor(HexColor("#6E6862"))
        c.setFont("PTSans", 7.0)
        c.drawCentredString(x + seg_w / 2, y - 9.2 * mm, str(i + 1))
        c.restoreState()
    y -= 14 * mm

    zones = [
        (Z_GREEN, "1–4", "Голова ясная. Вы слышите партнёра, можете пошутить "
                         "и спокойно объяснить свою мысль."),
        (Z_SAND, "5–7", "Растёт напряжение. Дыхание чаще, фразы резче. Здесь ещё "
                        "можно притормозить — пока не вспыхнул скандал."),
        (Z_RED, "8–10", "Чайник кипит. В голове только обида и желание уколоть "
                        "побольнее. Любой разговор разрушителен — его лучше "
                        "остановить и взять 20 минут паузы."),
    ]
    for col, num, txt in zones:
        c.saveState()
        c.setFillColor(col)
        c.circle(M + 1.3 * mm, y - 2.6 * mm, 1.3 * mm, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont("PTSans-Bold", 8.0)
        c.drawString(M + 5.0 * mm, y - 3.6 * mm, num)
        c.restoreState()
        y = para(c, txt, M + 14 * mm, y, CW - 14 * mm, "body_small")
        y -= 2.4 * mm

    y -= 4 * mm
    kicker(c, "Запишите · индивидуально", M, y, HexColor("#8E7A52"), size=6.8)
    y -= 6 * mm
    y = para(c, "Какие сигналы тела предупреждают вас, что конфликт нарастает? "
                "Что вы заметили за минуту до того, как стало совсем горячо?",
             M, y, CW, "h3")
    y -= 7 * mm
    writing_lines(c, M, y, CW)


def page_step2(c, imgs):
    new_page(c)
    footer(c, 5, "")
    kicker(c, "Шаг 2 из 6 · Простое правило", M, TOP)
    y = heading(c, "Правило 20 минут тишины", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "Пауза — это <b>не наказание молчанием</b> (бойкот). Это договор "
                "разойтись по углам на 20 минут, чтобы защитить друг друга от лишних "
                "обид. Гормонам стресса нужно минимум 20 минут, чтобы схлынуть.",
             M, y, CW)

    # дыхание
    y -= 7 * mm
    card_bg(c, M, y, CW, 24 * mm, SAGE_LIGHT)
    tracked(c, "СБРОС НАПРЯЖЕНИЯ", M + 6 * mm, y - 7 * mm, size=7.2)
    c.saveState()
    c.setFillColor(TEXT)
    c.setFont("PTSerif-Bold", 11.5)
    c.drawString(M + 6 * mm, y - 12.5 * mm, "Сделайте 4 глубоких вдоха")
    c.restoreState()
    para(c, "Вдох носом — круг растёт. Выдох через рот — отпустите плечи и челюсть.",
         M + 6 * mm, y - 14.6 * mm, CW - 12 * mm, "body_small")
    y -= 29.5 * mm

    y = para(c, "Что делать в эти 20 минут:", M, y, CW, "h3")
    y -= 5 * mm
    y = bullet(c, "<b>Разойтись в разные комнаты.</b> Не стойте друг напротив друга.",
               M, y, CW)
    y = bullet(c, "<b>Не крутить в голове обвинения.</b> Мысленные монологи снова "
                  "разжигают злость.", M, y, CW)
    y = bullet(c, "<b>Телесный сброс.</b> Умойте лицо прохладной водой, выпейте стакан "
                  "воды мелкими глотками.", M, y, CW)

    y -= 3 * mm
    kicker(c, "Запишите · индивидуально", M, y, HexColor("#8E7A52"), size=6.8)
    y -= 6 * mm
    y = para(c, "Что уже помогало остывать именно вам? Перечислите способы, "
                "которые срабатывали.", M, y, CW, "h3")
    y -= 7 * mm
    writing_lines(c, M, y, CW)


def page_return(c, imgs):
    new_page(c)
    footer(c, 6, "")
    kicker(c, "Возврат после паузы", M, TOP)
    y = heading(c, "Вы вернулись —<br/>это половина дела", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "Пауза сработала наполовину, если разговор так и не продолжился. "
                "Вернуться — тоже шаг, и его лучше назвать вслух.",
             M, y, CW, "lead")
    y -= 7 * mm

    phrases = [
        "«Я вернулся, как обещал. Продолжим?»",
        "«Спасибо, что подождал. Мне важно договорить это спокойно.»",
        "«Я не хочу тебя переспорить. Я хочу, чтобы мы поняли друг друга.»",
    ]
    for ph in phrases:
        c.saveState()
        c.setFillColor(TERRA)
        c.circle(M + 1.2 * mm, y - 3.0 * mm, 1.1 * mm, stroke=0, fill=1)
        c.restoreState()
        y = para(c, ph, M + 6 * mm, y, CW - 6 * mm, "quote")
        y -= 3.5 * mm

    # если снова накрыло
    box_h = 36 * mm
    card_bg(c, M, y - 6 * mm, CW, box_h, TERRA_LIGHT)
    yy = y - 6 * mm - 9 * mm
    tracked(c, "ЕСЛИ СНОВА НАКРЫЛО", M + 7 * mm, yy, size=7.2,
            color=HexColor("#A4603F"))
    para(c, "Не дожимайте. Скажите «мне нужно ещё 20 минут» и назовите время. "
            "Если и второй раз не вышло — перенесите на завтра и договоритесь "
            "о часе. Дольше суток не откладывайте.",
         M + 7 * mm, yy - 6 * mm, CW - 12 * mm, "body_small")

    y = y - 6 * mm - box_h - 10 * mm
    para(c, "Возврат — это не продолжение спора с того же места. Это его перезапуск "
            "в спокойном тоне: сначала «я здесь», потом уже «давай разберёмся».",
         M, y, CW, "body_small")


def page_step3(c, imgs):
    new_page(c)
    footer(c, 7, "")
    kicker(c, "Шаг 3 из 6 · Собери свою фразу", M, TOP)
    y = heading(c, "Что сказать,<br/>чтобы партнёр не обиделся", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "Если просто бросить: «Я не хочу с тобой разговаривать!» — партнёр "
                "решит, что его бросают. Соберите мягкую фразу из трёх частей.",
             M, y, CW)

    parts = [
        ("1. Напомните, что человек вам дорог",
         "«Я люблю тебя» · «Ты очень дорог(а) мне» · «Вижу, как нам тяжело»"),
        ("2. Честно скажите о себе, без «ты виноват»",
         "«Я закипаю и боюсь обидеть» · «Слишком много эмоций, не слышу» · "
         "«Закрываюсь в глухую защиту»"),
        ("3. Назовите точное время, когда вернётесь",
         "«Помолчим 20 минут» · «Полчаса в тишине» · «Выйду на воздух и сделаю чай»"),
    ]
    y -= 6 * mm
    for title, opts in parts:
        y = para(c, title, M, y, CW, "h3")
        y -= 1.5 * mm
        y = para(c, opts, M + 4 * mm, y, CW - 4 * mm, "body_small")
        y -= 2.2 * mm

    # готовая фраза
    box_h = 28.5 * mm
    card_bg(c, M, y, CW, box_h, SAGE_LIGHT)
    tracked(c, "ВАША ГОТОВАЯ ФРАЗА", M + 7 * mm, y - 8 * mm, size=7.2)
    para(c, "«Я очень люблю тебя. Сейчас я закипаю и боюсь наговорить обидного. "
            "Давай помолчим 20 минут. Я подышу и вернусь к тебе.»",
         M + 7 * mm, y - 13.5 * mm, CW - 13 * mm,
         extra={"fontName": "PTSerif-Italic", "fontSize": 10.0, "leading": 14.2,
                "textColor": HexColor("#41544A")})
    y -= box_h + 8 * mm

    kicker(c, "Запишите · индивидуально", M, y, HexColor("#8E7A52"), size=6.8)
    y -= 6 * mm
    y = para(c, "Какую фразу вы скажете в следующий раз, когда почувствуете, "
                "что закипаете?", M, y, CW, "h3")
    y -= 7 * mm
    writing_lines(c, M, y, CW)


def page_step4(c, imgs):
    new_page(c)
    footer(c, 8, "")
    kicker(c, "Шаг 4 из 6 · Простая практика", M, TOP)
    y = heading(c, "Репетиция в спокойный вечер", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "Договариваться о правилах во время скандала бесполезно — все уже "
                "на взводе. Сделайте это заранее, за чашкой чая.",
             M, y, CW)

    y -= 7 * mm
    y = para(c, "План из трёх шагов", M, y, CW, "h3")
    y -= 5 * mm
    y = numbered(c, 1, "В спокойную минуту покажите эти слова: «Я хочу, чтобы мы "
                       "берегли друг друга и не ранили в спорах. Давай придумаем "
                       "общее стоп-слово».", M, y, CW)
    y -= 2.5 * mm
    y = numbered(c, 2, "Выберите смешное или простое слово: «Пауза», "
                       "«Чайник закипел», «Маяк».", M, y, CW)
    y -= 2.5 * mm
    y = numbered(c, 3, "Договоритесь: кто бы ни произнёс это слово — оба молча "
                       "расходятся на 20 минут без обид и споров.", M, y, CW)

    y -= 9 * mm
    kicker(c, "Запишите · вместе с партнёром", M, y, HexColor("#A4603F"), size=6.8)
    y -= 6 * mm
    y = para(c, "Обсудите это в спокойный вечер и запишите, к чему вы пришли.",
             M, y, CW, "h3")
    y -= 7 * mm
    writing_lines(c, M, y, CW, bottom=46 * mm)

    rule(c, M, 42 * mm, CW)
    para(c, "<b>Если вы проходите это сами.</b> Пауза — ваше действие, разрешение "
            "партнёра для неё не нужно: свою фразу можно сказать и без общего "
            "стоп-слова. Если обстановка спокойная, назовите время возврата — это "
            "забота, а не побег. Если в ответ можно услышать угрозу или вам страшно "
            "оставаться в комнате, ничего не объявляйте и не объясняйтесь — просто "
            "выйдите. Безопасность важнее вежливости.",
         M, 38 * mm, CW, "note")


def page_cheatsheet(c, imgs):
    new_page(c)
    footer(c, 9, "")
    kicker(c, "Шаг 5 из 6 · Памятка", M, TOP)
    y = heading(c, "Шпаргалка в карман", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "Когда накрывают эмоции, нужные слова вылетают из головы. Вырежьте "
                "карточку по пунктиру и положите в кошелёк или под чехол телефона.",
             M, y, CW)

    # карточка 85×54 мм
    cw, ch = 85 * mm, 54 * mm
    x = (W - cw) / 2
    top = y - 12 * mm
    c.saveState()
    c.setFillColor(HexColor("#FDFBF6"))
    c.roundRect(x, top - ch, cw, ch, 2.5 * mm, stroke=0, fill=1)
    c.setStrokeColor(DOTS)
    c.setLineWidth(0.7)
    c.setDash(2.2, 2.0)
    c.roundRect(x, top - ch, cw, ch, 2.5 * mm, stroke=1, fill=0)
    c.restoreState()
    c.saveState()
    c.setFillColor(TERRA)
    c.rect(x + 5 * mm, top - ch + 5 * mm, 0.9 * mm, ch - 10 * mm, stroke=0, fill=1)
    c.restoreState()

    tracked(c, "ЭКСТРЕННАЯ ПАУЗА", x + 9 * mm, top - 9 * mm, size=6.4,
            color=HexColor("#A4603F"), space=1.1)

    para(c, "«Я люблю тебя. Сейчас я чувствую, что закипаю. Мне нужно 20 минут "
            "тишины, чтобы остыть и услышать тебя спокойно. Я вернусь и договорим.»",
         x + 9 * mm, top - 14 * mm, cw - 18 * mm,
         extra={"fontName": "PTSerif-Italic", "fontSize": 9.2, "leading": 12.2,
                "textColor": TEXT})

    c.saveState()
    c.setFillColor(SAGE)
    c.setFont("PTSans", 6.8)
    c.drawString(x + 9 * mm, top - ch + 9 * mm,
                 "1. Медленный выдох · 2. Стакан воды · 3. Возврат через 20 минут")
    c.restoreState()

    # ножницы и подпись под карточкой
    scissors(c, x - 0.5 * mm, top - ch - 5.6 * mm)
    c.saveState()
    c.setFillColor(HexColor("#ABA398"))
    c.setFont("PTSans", 6.6)
    c.drawString(x + 8.2 * mm, top - ch - 6.4 * mm, "вырезать по пунктиру")
    c.restoreState()

    y = top - ch - 16 * mm
    kicker(c, "Запишите · индивидуально", M, y, HexColor("#8E7A52"), size=6.8)
    y -= 6 * mm
    y = para(c, "Какую фразу вы хотите себе напомнить в следующий конфликт?",
             M, y, CW, "h3")
    y -= 8 * mm
    writing_lines(c, M, y, CW, bottom=20 * mm)


def page_step6(c, imgs):
    new_page(c)
    footer(c, 10, "")
    kicker(c, "Шаг 6 из 6 · Тёплый финал", M, TOP)
    y = heading(c, "Первая победа:<br/>куда двигаться дальше", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "Вы освоили главный навык эмоциональной безопасности. Умение вовремя "
                "затормозить — это уже половина победы над ссорами.",
             M, y, CW)

    y -= 7 * mm
    box_h = 34 * mm
    card_bg(c, M, y, CW, box_h, HexColor("#F2EFE8"))
    c.saveState()
    c.setFillColor(TERRA)
    c.rect(M, y - box_h, 1.6 * mm, box_h, stroke=0, fill=1)
    c.restoreState()
    para(c, "«Пауза тушит пожар, но не убирает то, из-за чего загорелось. Следующий "
            "шаг — научиться говорить о своих желаниях и обидах так, чтобы партнёр "
            "не вставал в позу защиты».",
         M + 7 * mm, y - 7 * mm, CW - 13 * mm,
         extra={"fontName": "PTSerif-Italic", "fontSize": 10.2, "leading": 14.4,
                "textColor": HexColor("#41544A")})
    y -= box_h + 8 * mm

    y = para(c, "Следующий шаг — практикум второго уровня: 14 дней бережного диалога. "
                "Он про то, почему вы наступаете на одни и те же грабли в спорах, "
                "как просить без претензий и как вернуть нежность в общение. "
                "Практикум пока готовится — он выйдет отдельной тетрадью.",
             M, y, CW, "body_small")

    y -= 10 * mm
    kicker(c, "Запишите · индивидуально", M, y, HexColor("#8E7A52"), size=6.8)
    y -= 6 * mm
    y = para(c, "Оглянитесь на пройденный путь. Что вы хотите отметить у себя?",
             M, y, CW, "h3")
    y -= 7 * mm
    writing_lines(c, M, y, CW)


def page_notes(c, imgs):
    new_page(c)
    footer(c, 11, "")
    kicker(c, "Заметки", M, TOP)
    y = heading(c, "Сюда — всё, что не поместилось", M, TOP - 9 * mm, CW)
    y -= 5 * mm
    y = para(c, "Мысли, которые пришли по ходу чтения. Вопросы, которые хочется "
                "задать партнёру. Фразы, которые хочется попробовать.",
             M, y, CW, "body_small")
    y -= 10 * mm
    writing_lines(c, M, y, CW, gap=7.5 * mm)


def page_back(c, imgs):
    new_page(c)
    y = H - 26 * mm
    kicker(c, "Если это про вас", M, y, TERRA)
    y -= 10 * mm

    bw = CW - 14 * mm
    p1 = Paragraph("Если в ссорах звучат угрозы, доходит до ударов или вам страшно "
                   "оставаться рядом — это не решается техникой паузы.", STYLES["body"])
    p2 = Paragraph("Здесь нужна помощь специалиста, и лучше найти её до следующего раза.",
                   STYLES["body"])
    h1 = p1.wrapOn(c, bw, 2000)[1]
    h2 = p2.wrapOn(c, bw, 2000)[1]
    box_h = 10 * mm + h1 + 4 * mm + h2 + 10 * mm
    card_bg(c, M, y, CW, box_h, TERRA_LIGHT)
    c.saveState()
    c.setFillColor(TERRA)
    c.rect(M, y - box_h, 1.6 * mm, box_h, stroke=0, fill=1)
    c.restoreState()
    p1.drawOn(c, M + 8 * mm, y - 10 * mm - h1)
    p2.drawOn(c, M + 8 * mm, y - 10 * mm - h1 - 4 * mm - h2)

    plate_w = 72 * mm
    draw_plate(c, imgs[7], (W - plate_w) / 2, y - box_h - 22 * mm, plate_w)

    rule(c, M, 64 * mm, CW)
    para(c, "Тетрадь можно проходить заново. Пауза — навык, а не факт: "
            "он тренируется повторением, и с третьего раза получается лучше, "
            "чем с первого.", M, 58 * mm, CW, "body_small")

    c.saveState()
    c.setFillColor(HexColor("#9A938A"))
    c.setFont("PTSans", 7.6)
    c.drawString(M, 30 * mm, "Тетрадь для пар · Уровень 1")
    c.drawString(M, 24 * mm, "Как вовремя остановить ссору")
    c.drawRightString(M + CW, 30 * mm, "6 шагов · 10 минут")
    c.drawRightString(M + CW, 24 * mm, "можно возвращаться")
    c.restoreState()


# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    register_fonts()
    build_styles()
    imgs = extract_images()
    if len(imgs) < 8:
        raise SystemExit(f"В HTML найдено {len(imgs)} картинок, ожидалось 8")

    c = canvas.Canvas(str(OUT), pagesize=A5)
    c.setTitle("Как вовремя остановить ссору — рабочая тетрадь, уровень 1")
    c.setAuthor("PsyLab")
    c.setSubject("Тетрадь для пар · печатная версия")

    pages = [
        page_cover, page_how_to, page_intro,
        page_step1, page_step2, page_return,
        page_step3, page_step4, page_cheatsheet,
        page_step6, page_notes, page_back,
    ]
    for fn in pages:
        fn(c, imgs)
        c.showPage()
    c.save()
    print(f"Готово: {OUT} — {OUT.stat().st_size:,} байт".replace(",", " "))


if __name__ == "__main__":
    main()
