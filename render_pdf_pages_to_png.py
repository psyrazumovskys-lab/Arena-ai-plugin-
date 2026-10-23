import os
import fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    Image as RLImage, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Oblique', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))

pdf_path = "therapy-workbooks/couple_workbook_1_stop_escalation.pdf"

C_BG = colors.HexColor('#F7F5F0')
C_TEXT = colors.HexColor('#2C3539')
C_MUTED = colors.HexColor('#64748B')
C_SAGE = colors.HexColor('#5A7365')
C_SAGE_LIGHT = colors.HexColor('#EBF1ED')
C_TERRA = colors.HexColor('#C87D65')
C_TERRA_LIGHT = colors.HexColor('#FDF3E7')
C_TERRA_DEEP = colors.HexColor('#E3B09B')
C_BORDER = colors.HexColor('#E2DDD5')
C_WHITE = colors.white
C_GREEN_ZONE = colors.HexColor('#8FB8A8')
C_YELLOW_ZONE = colors.HexColor('#E2C99F')
C_RED_ZONE = colors.HexColor('#C87D65')
C_BORDER_DARK = colors.HexColor('#C9C0B4')

class MarkerBullet(Flowable):
    """Custom graphic marker instead of emoji"""
    def __init__(self, color=C_SAGE, label="", width=166*mm, height=6*mm, text_color=C_TEXT):
        super().__init__()
        self.color = color
        self.label = label
        self.width = width
        self.height = height
        self.text_color = text_color

    def draw(self):
        c = self.canv
        c.saveState()
        # Soft filled circle marker
        c.setFillColor(self.color)
        c.circle(12, self.height/2 - 1, 2.5, fill=1, stroke=0)
        c.setFont('DejaVu', 8.5)
        c.setFillColor(self.text_color)
        c.drawString(20, self.height/2 - 2, self.label)
        c.restoreState()

class ThermalScale(Flowable):
    """Графическая шкала закипания 1–10 с цветовыми зонами"""
    def __init__(self, width=166*mm, height=32*mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()
        bar_height = 7*mm
        bar_x = 0
        bar_y = 17*mm
        segments = 10
        seg_width = self.width / segments

        zone_colors = {
            0: C_GREEN_ZONE, 1: C_GREEN_ZONE, 2: C_GREEN_ZONE, 3: C_GREEN_ZONE,
            4: C_YELLOW_ZONE, 5: C_YELLOW_ZONE, 6: C_YELLOW_ZONE,
            7: C_RED_ZONE, 8: C_RED_ZONE, 9: C_RED_ZONE
        }

        for i in range(segments):
            x = bar_x + i * seg_width
            c.setFillColor(zone_colors.get(i, C_GREEN_ZONE))
            c.roundRect(x, bar_y, seg_width - 1.2, bar_height, 1.5, fill=1, stroke=0)

        # Номера внутри сегментов
        c.setFont('DejaVu-Bold', 7)
        c.setFillColor(colors.white)
        for i in range(segments):
            x_center = bar_x + i * seg_width + (seg_width - 1.2) / 2
            c.drawCentredString(x_center, bar_y + bar_height/2 - 2.4, str(i + 1))

        # Подписи зон — под шкалой, с запасом
        c.setFont('DejaVu-Bold', 6.5)
        c.setFillColor(C_SAGE)
        c.drawString(bar_x, bar_y - 5.5*mm, "ЗЕЛЁНАЯ ЗОНА · 1–4")
        c.setFillColor(colors.HexColor('#A8873F'))
        c.drawCentredString(bar_x + 5 * seg_width, bar_y - 5.5*mm, "ЖЁЛТАЯ · 5–7")
        c.setFillColor(C_TERRA)
        c.drawRightString(bar_x + self.width, bar_y - 5.5*mm, "КРАСНАЯ ЗОНА · 8–10")

        # Указатель "вы здесь"
        c.setFillColor(C_TERRA)
        c.setStrokeColor(C_TERRA)
        c.setLineWidth(1)
        px = bar_x + 4.5 * seg_width
        c.circle(px, bar_y + bar_height + 3*mm, 1.6, fill=1, stroke=0)
        c.line(px, bar_y + bar_height + 1.6*mm, px, bar_y + bar_height + 0.6*mm)

        c.restoreState()

class JournalLine(Flowable):
    """Пунктирная линия для записи от руки — строго в пределах карточки"""
    def __init__(self, width=142*mm, height=6*mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(C_BORDER_DARK)
        c.setLineWidth(0.6)
        c.setDash(1, 2)
        c.line(0, self.height/2, self.width, self.height/2)
        c.restoreState()


class BulbIcon(Flowable):
    """Печатный аналог иконки-лампочки из интерактивной версии"""
    def __init__(self, size=6*mm):
        super().__init__()
        self.width = size
        self.height = size

    def draw(self):
        c = self.canv
        c.saveState()
        cx, cy, r = 3.0*mm, 3.6*mm, 1.9*mm
        c.setLineWidth(1.0)
        c.setStrokeColor(C_TERRA)
        c.setFillColor(colors.HexColor('#FDF3E7'))
        c.circle(cx, cy, r, fill=1, stroke=1)
        # цоколь
        c.setFillColor(C_TERRA)
        c.rect(cx - 1.05*mm, cy - r - 1.4*mm, 2.1*mm, 1.5*mm, fill=1, stroke=0)
        # нить накала
        c.setStrokeColor(C_TERRA)
        c.setLineWidth(0.7)
        c.line(cx - 0.8*mm, cy + 0.5*mm, cx, cy - 0.6*mm)
        c.line(cx, cy - 0.6*mm, cx + 0.8*mm, cy + 0.5*mm)
        c.restoreState()

def draw_background_and_header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, 210*mm, 297*mm, fill=True, stroke=False)
    
    canvas.setFillColor(C_WHITE)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.8)
    canvas.roundRect(14*mm, 14*mm, 182*mm, 269*mm, 8, fill=True, stroke=True)

    canvas.setFont('DejaVu-Bold', 7.5)
    canvas.setFillColor(C_SAGE)
    canvas.drawString(22*mm, 275*mm, "PSYLAB · СТОП-ЭСКАЛАЦИЯ В ПАРЕ")
    canvas.setFont('DejaVu', 7.5)
    canvas.setFillColor(C_MUTED)
    canvas.drawRightString(188*mm, 275*mm, "ЭКСПРЕСС-ПРОТОКОЛ · УРОВЕНЬ 1")
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(22*mm, 272*mm, 188*mm, 272*mm)

    # Индикатор прохождения: точки-шаги, заполненные до текущей страницы
    total = 7
    dot_r = 1.15*mm
    gap = 5.2*mm
    start_x = 105*mm - (total - 1) * gap / 2
    dot_y = 27*mm
    for i in range(total):
        x = start_x + i * gap
        if i + 1 < doc.page:
            canvas.setFillColor(C_SAGE)
            canvas.setStrokeColor(C_SAGE)
        elif i + 1 == doc.page:
            canvas.setFillColor(C_TERRA)
            canvas.setStrokeColor(C_TERRA)
        else:
            canvas.setFillColor(colors.HexColor('#FFFFFF'))
            canvas.setStrokeColor(C_BORDER_DARK)
        canvas.setLineWidth(0.7)
        canvas.circle(x, dot_y, dot_r, fill=1, stroke=1)

    canvas.line(22*mm, 22*mm, 188*mm, 22*mm)
    canvas.setFont('DejaVu', 7.5)
    canvas.setFillColor(C_MUTED)
    canvas.drawString(22*mm, 18*mm, "Психологический практикум для двоих")
    canvas.drawRightString(188*mm, 18*mm, f"Страница {doc.page} из 7")
    canvas.restoreState()

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=22*mm,
    rightMargin=22*mm,
    topMargin=28*mm,
    bottomMargin=26*mm
)

styles = getSampleStyleSheet()

s_title = ParagraphStyle('TitleStyle', fontName='DejaVu-Bold', fontSize=17, leading=22, textColor=C_TEXT, spaceAfter=8)
s_badge = ParagraphStyle('BadgeStyle', fontName='DejaVu-Bold', fontSize=8.5, leading=11, textColor=C_TERRA, spaceAfter=5)
s_badge_sage = ParagraphStyle('BadgeSageStyle', fontName='DejaVu-Bold', fontSize=8.5, leading=11, textColor=C_SAGE, spaceAfter=5)
s_subtitle = ParagraphStyle('SubtitleStyle', fontName='DejaVu-Oblique', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#4A555B'), spaceAfter=10)
s_body = ParagraphStyle('BodyStyle', fontName='DejaVu', fontSize=9, leading=13.5, textColor=C_TEXT, spaceAfter=6)
s_body_bold = ParagraphStyle('BodyBoldStyle', fontName='DejaVu-Bold', fontSize=9, leading=13.5, textColor=C_TEXT, spaceAfter=5)
s_quote = ParagraphStyle('QuoteStyle', fontName='DejaVu-Oblique', fontSize=9, leading=13.5, textColor=colors.HexColor('#3D484D'))
s_field_label = ParagraphStyle('FieldLabel', fontName='DejaVu-Bold', fontSize=8.5, leading=11, textColor=C_SAGE, spaceAfter=3)
s_input_note = ParagraphStyle('InputNote', fontName='DejaVu-Oblique', fontSize=7.5, leading=9, textColor=C_MUTED, spaceBefore=2)
s_hint = ParagraphStyle('HintStyle', fontName='DejaVu-Oblique', fontSize=7.8, leading=10.5, textColor=colors.HexColor('#6B7378'))

def make_box(content_flowables, bg=colors.HexColor('#FAF8F5'), border=C_BORDER, pad=7):
    t = Table([[content_flowables]], colWidths=[166*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 1, border),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('TOPPADDING', (0,0), (-1,-1), pad),
        ('BOTTOMPADDING', (0,0), (-1,-1), pad),
        ('LEFTPADDING', (0,0), (-1,-1), pad),
        ('RIGHTPADDING', (0,0), (-1,-1), pad),
    ]))
    return t

def make_quote(text):
    p = Paragraph(f"«{text}»", s_quote)
    t = Table([[p]], colWidths=[166*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F1EA')),
        ('LINELEFT', (0,0), (-1,-1), 3, C_TERRA),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def make_input_field(height_mm=20):
    t = Table([[" "]], colWidths=[166*mm], rowHeights=[height_mm*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t

def make_journal_block(questions, hint="Пишите коротко и своими словами — места хватит на главное.", lines=2):
    """Печатный аналог блока записи: лампочка-подсказка + строки для записи"""
    header = Table([[BulbIcon(), Paragraph(hint, s_hint)]], colWidths=[7*mm, 135*mm])
    header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    inner = [header, Spacer(1, 8)]
    for q in questions:
        inner.append(Paragraph(q, s_field_label))
        inner.append(Spacer(1, 3))
        for _ in range(lines):
            inner.append(JournalLine(width=142*mm, height=7*mm))
        inner.append(Spacer(1, 6))

    t = Table([[inner]], colWidths=[166*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

story = []

# =========================================================================
# СТРАНИЦА 1: ОБЛОЖКА-МАНИФЕСТ
# =========================================================================
story.append(RLImage('therapy-workbooks/assets/cover_couples_l1.jpg', width=166*mm, height=72*mm))
story.append(Spacer(1, 8))
story.append(Paragraph("СКОРАЯ ПОМОЩЬ · УРОВЕНЬ 1", s_badge))
story.append(Paragraph("Как вовремя остановиться в ссоре", s_title))
story.append(Paragraph("Простая инструкция, как нажать на паузу, остыть и не наговорить слов, о которых потом больно вспоминать.", s_subtitle))
story.append(make_quote("Когда в комнате бушует буря, цель — не перекричать ветер, а вовремя укрыться в безопасной гавани. Каждый из вас имеет полное право сказать: „Мне нужно выдохнуть“"))
story.append(Spacer(1, 8))
safe_space = [
    Paragraph("Здесь вас никто не судит", s_body_bold),
    Paragraph("Ссорятся абсолютно все пары. Но счастливые пары отличаются не тем, что у них нет разногласий, а тем, что они умеют вовремя <b>притормозить</b>, пока разговор не превратился в перестрелку. Этот экспресс-протокол разработан на базе доказательной психотерапии пар и нейробиологии стресса.", s_body)
]
story.append(make_box(safe_space, bg=C_SAGE_LIGHT, border=C_SAGE))
story.append(make_journal_block([
    "Какое одно слово лучше всего описывает ваши отношения прямо сейчас?",
    "Что бы вы хотели сделать в первую очередь после прочтения этой тетради?",
], hint="Пишите первое, что приходит в голову. Правильного ответа здесь нет.", lines=2))
story.append(PageBreak())

# =========================================================================
# СТРАНИЦА 2: ТЕСТ НА ЗАКИПАНИЕ + ГРАФИЧЕСКАЯ ШКАЛА
# =========================================================================
story.append(RLImage('therapy-workbooks/assets/ill_boiling_scale.jpg', width=166*mm, height=72*mm))
story.append(Spacer(1, 6))
story.append(Paragraph("ШАГ 1 ИЗ 6 · ГРАДУСНИК ЭМОЦИЙ", s_badge_sage))
story.append(Paragraph("Почему в ссоре отключается голова", s_title))
story.append(Paragraph("В сильном гневе наше тело думает, что на нас напал хищник. Пульс подскакивает выше 100 ударов в минуту, кровь отливает от лобных долей мозга. В этот момент мы <b>физиологически не способны</b> слышать доводы партнера.", s_body))

# Визуальная шкала
story.append(Spacer(1, 4))
story.append(ThermalScale(width=166*mm, height=26*mm))
story.append(Spacer(1, 4))

scale_box = [
    Paragraph("Как ваше тело подаёт сигнал тревоги?", s_field_label),
    MarkerBullet(color=C_SAGE, label="Сжимаются челюсти, горит лицо, становится трудно дышать глубоко"),
    MarkerBullet(color=C_SAGE, label="Мысли крутятся по кругу, трудно сосредоточиться на чем-то одном"),
    MarkerBullet(color=C_SAGE, label="Появляется желание сделать паузу, уйти или крикнуть"),
]
story.append(make_box(scale_box, bg=C_SAGE_LIGHT, border=C_SAGE))
story.append(Spacer(1, 6))

story.append(make_journal_block([
    "Как вы обычно ведёте себя в «красной зоне» (8–10 баллов)?",
    "Что вы замечаете в теле в самый первый момент раздражения?",
], hint="Запишите первые телесные сигналы тревоги — то, что вы чувствуете в теле, когда начинаете закипать.", lines=2))
story.append(PageBreak())

# =========================================================================
# СТРАНИЦА 3: ПРАВИЛО 20 МИНУТ + ДЫХАНИЕ
# =========================================================================
story.append(RLImage('therapy-workbooks/assets/infographic_timeout_l1.jpg', width=166*mm, height=72*mm))
story.append(Spacer(1, 6))
story.append(Paragraph("ШАГ 2 ИЗ 6 · ПРОСТОЕ ПРАВИЛО", s_badge_sage))
story.append(Paragraph("Правило 20 минут тишины", s_title))
story.append(Paragraph("Пауза — это <b>не наказание молчанием</b> (бойкот). Это договор разойтись по углам на 20 минут, чтобы защитить друг друга от лишних обид. Гормонам стресса нужно ровно 20 минут, чтобы концентрация в крови снизилась.", s_body))

timeout_rules = [
    Paragraph("3 правила экологичного тайм-аута:", s_body_bold),
    Spacer(1, 2),
    Paragraph("Разойтись в разные комнаты: не стойте друг напротив друга, смените обстановку.", s_body),
    Paragraph("Не крутите в голове обвинения: не сочиняйте мысленные монологи — это снова разжигает злость.", s_body),
    Paragraph("Телесный сброс: умойте лицо холодной водой, сделайте 4 глубоких вдоха носом и длинных выдоха ртом.", s_body)
]
story.append(make_box(timeout_rules))
story.append(Spacer(1, 6))

story.append(make_journal_block([
    "Где в вашем доме или вне дома вы чувствуете себя в безопасности, чтобы остыть?",
    "Что вы будете делать эти 20 минут — по шагам?",
], hint="Что помогает вам остыть за 20 минут паузы? Перечислите свои способы.", lines=2))
story.append(PageBreak())

# =========================================================================
# СТРАНИЦА 4: КОНСТРУКТОР ФРАЗЫ
# =========================================================================
story.append(RLImage('therapy-workbooks/assets/ill_stop_phrase.jpg', width=166*mm, height=72*mm))
story.append(Spacer(1, 6))
story.append(Paragraph("ШАГ 3 ИЗ 6 · СОБЕРИ СВОЮ ФРАЗУ", s_badge))
story.append(Paragraph("Что сказать, чтобы партнер не обиделся", s_title))
story.append(Paragraph("Если просто бросить: «Я не хочу с тобой разговаривать!» — партнер решит, что его бросают. Экологичная фраза строится по формуле «Тепло + Я-сообщение + Время возвращения»:", s_body))

phrase_box = [
    Paragraph("Проверенные варианты формулы:", s_body_bold),
    Spacer(1, 2),
    Paragraph("«Я очень люблю тебя. Сейчас я закипаю и боюсь наговорить обидного. Давай помолчим 20 минут. Я подышу и вернусь к тебе».", s_body),
    Paragraph("«Ты очень дорог мне, и я не хочу ссориться. Внутри слишком много эмоций, мне трудно тебя слышать. Мне нужно ровно полчаса в тишине, в 20:00 продолжим».", s_body)
]
story.append(make_box(phrase_box, bg=C_TERRA_LIGHT, border=C_TERRA))
story.append(Spacer(1, 6))

story.append(make_journal_block([
    "Напишите свою фразу-стоп-слово своими словами:",
    "Когда и где вам удобнее всего обсудить это с партнером?",
], hint="Тепло + я-сообщение + время возвращения. Три части — и фраза звучит бережно.", lines=2))
story.append(PageBreak())

# =========================================================================
# СТРАНИЦА 5: РЕПЕТИЦИЯ В ТИХИЙ ВЕЧЕР
# =========================================================================
story.append(RLImage('therapy-workbooks/assets/ill_invivo_practice.jpg', width=166*mm, height=72*mm))
story.append(Spacer(1, 6))
story.append(Paragraph("ШАГ 4 ИЗ 6 · ПРОСТАЯ ПРАКТИКА", s_badge_sage))
story.append(Paragraph("Репетиция в спокойный вечер", s_title))
story.append(Paragraph("Договариваться о правилах во время скандала бесполезно — все уже на взводе. Сделайте это заранее, за чашкой чая в спокойный вечер.", s_body))

practice_steps = [
    Paragraph("План из 3 шагов:", s_body_bold),
    Spacer(1, 2),
    Paragraph("В спокойную минуту скажите: «Я хочу, чтобы мы берегли друг друга в спорах. Давай договоримся об общем стоп-слове».", s_body),
    Paragraph("Выберите простое или забавное слово (например: «Маяк», «Чайник закипел», «Пауза 20»).", s_body),
    Paragraph("Договоритесь: кто бы ни произнес это слово — оба молча расходятся на 20 минут без обид и споров.", s_body)
]
story.append(make_box(practice_steps))
story.append(Spacer(1, 6))

story.append(make_journal_block([
    "Какое стоп-слово вы выбрали?",
    "Когда вы обсудите это с партнером?",
], hint="Запишите выбранное стоп-слово и договорённость о его использовании.", lines=2))
story.append(PageBreak())

# =========================================================================
# СТРАНИЦА 6: ШПАРГАЛКА (VISIBLE SOS CARD)
# =========================================================================
story.append(RLImage('therapy-workbooks/assets/ill_sos_reconnect.jpg', width=166*mm, height=72*mm))
story.append(Spacer(1, 6))
story.append(Paragraph("ШАГ 5 ИЗ 6 · ПАМЯТКА", s_badge))
story.append(Paragraph("Шпаргалка для телефона (на случай ссоры)", s_title))
story.append(Paragraph("Когда накрывают эмоции, нужные слова вылетают из головы. Сохраните этот текст, чтобы отправить партнеру в мессенджер, если трудно сказать вслух:", s_body))

# Выразительная карточка-шпаргалка с контрастом
sos_card = [
    Paragraph("ЭКСТРЕННОЕ СООБЩЕНИЕ ДЛЯ ПАРТНЕРА", ParagraphStyle('H', fontName='DejaVu-Bold', fontSize=9.5, leading=12, textColor=C_TERRA)),
    Spacer(1, 4),
    Paragraph("«Я люблю тебя. Сейчас я чувствую, что закипаю. Мне нужно 20 минут тишины, чтобы остыть и услышать тебя спокойно. Я вернусь и мы договорим».", ParagraphStyle('Q', fontName='DejaVu', fontSize=9.5, leading=14, textColor=C_TEXT)),
    Spacer(1, 5),
    Paragraph("1. Медленный выдох · 2. Стакан воды · 3. Возврат через 20 минут", ParagraphStyle('F', fontName='DejaVu', fontSize=8, leading=10, textColor=C_MUTED)),
]
sos_table = Table([[sos_card]], colWidths=[166*mm])
sos_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FDF3E7')),
    ('BOX', (0,0), (-1,-1), 1.4, C_TERRA),
    ('LINEBELOW', (0,0), (-1,-1), 0.6, C_TERRA_DEEP),
    ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
]))
story.append(sos_table)
story.append(Spacer(1, 6))

story.append(make_journal_block([
    "Какую фразу вы скажете себе, чтобы остановиться?",
    "Что напомните себе о партнёре, когда злость накроет?",
], hint="Ваше главное напоминание себе — то, что вы хотите прошептать в момент сильного гнева.", lines=2))
story.append(PageBreak())

# =========================================================================
# СТРАНИЦА 7: МОСТИК КО 2 УРОВНЮ
# =========================================================================
story.append(RLImage('therapy-workbooks/assets/infographic_bridge_l1.jpg', width=166*mm, height=72*mm))
story.append(Spacer(1, 6))
story.append(Paragraph("ШАГ 6 ИЗ 6 · ТЕПЛЫЙ ФИНАЛ", s_badge))
story.append(Paragraph("Первая победа: Куда двигаться дальше", s_title))
story.append(Paragraph("Поздравляем! Вы освоили главный навык эмоциональной безопасности. Умение вовремя затормозить — это уже половина победы над ссорами.", s_body))
story.append(make_quote("Пауза тушит пожар, но не убирает то, из-за чего загорелось. Следующий шаг — научиться говорить о своих желаниях и обидах так, чтобы партнер не вставал в позу защиты."))
story.append(Spacer(1, 6))

bridge_box = [
    Paragraph("Практикум Уровня 2: 14 дней бережного диалога", ParagraphStyle('H2', fontName='DejaVu-Bold', fontSize=10.5, leading=13, textColor=C_SAGE)),
    Spacer(1, 3),
    Paragraph("Если вы хотите перейти от тушения пожаров к настоящей близости: понять, почему вы наступаете на одни и те же грабли в спорах, как просить без претензий и как вернуть нежность в общение.", s_body),
    Spacer(1, 1),
    Paragraph("Доступно в Telegram-боте @psy_workbook_bot", ParagraphStyle('L', fontName='DejaVu-Bold', fontSize=8.5, leading=11, textColor=C_TERRA))
]
story.append(make_box(bridge_box, bg=C_SAGE_LIGHT, border=C_SAGE))
story.append(Spacer(1, 6))

story.append(make_journal_block([
    "Маленькая благодарность себе за этот шаг:",
    "Что бы вы хотели перенести из этого протокола в повседневную жизнь?",
], hint="Не обесценивайте маленькие шаги — именно из них складывается перемена.", lines=2))

doc.build(story, onFirstPage=draw_background_and_header, onLaterPages=draw_background_and_header)
print(f"PDF successfully built: {pdf_path}")

pdf_doc = fitz.open(pdf_path)
os.makedirs("therapy-workbooks/page_previews", exist_ok=True)
for page_idx in range(len(pdf_doc)):
    page = pdf_doc[page_idx]
    pix = page.get_pixmap(dpi=150)
    out_file = f"therapy-workbooks/page_previews/page_{page_idx + 1}.png"
    pix.save(out_file)
    print(f"Rendered {out_file} ({pix.width}x{pix.height}px)")
