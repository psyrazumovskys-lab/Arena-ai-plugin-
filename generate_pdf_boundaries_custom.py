import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import pymupdf

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

PAGE_W, PAGE_H = A4
M_H = 13 * mm
M_V = 11.5 * mm
CW = PAGE_W - 2 * M_H

PRIMARY = colors.HexColor('#0f766e')      # Teal 700
PRIMARY_DARK = colors.HexColor('#115e59') # Teal 800
BG_LIGHT = colors.HexColor('#f0fdfa')     # Teal 50
TEXT = colors.HexColor('#0f172a')         # Slate 900
TEXT_MUTED = colors.HexColor('#475569')   # Slate 600
LINE_COLOR = colors.HexColor('#cbd5e1')   # Slate 300
HIGHLIGHT = colors.HexColor('#eff6ff')    # Blue 50
WARN_BG = colors.HexColor('#fff7ed')      # Amber 50
WARN_BORDER = colors.HexColor('#ea580c')  # Orange 600

class CustomNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        self.setFont('DejaVu-Bold', 7)
        self.setFillColor(PRIMARY_DARK)
        self.drawString(M_H, PAGE_H - 8 * mm, "СЕРИЯ 01 • СУВЕРЕНИТЕТ И ЛИЧНЫЕ ГРАНИЦЫ")
        self.setFont('DejaVu', 7)
        self.setFillColor(TEXT_MUTED)
        self.drawRightString(PAGE_W - M_H, PAGE_H - 8 * mm, "ПРАКТИКУМ САМОСТОЯТЕЛЬНОЙ ТЕРАПИИ")
        self.setStrokeColor(LINE_COLOR)
        self.setLineWidth(0.5)
        self.line(M_H, PAGE_H - 9.5 * mm, PAGE_W - M_H, PAGE_H - 9.5 * mm)

        self.setFont('DejaVu', 6.8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(M_H, 6.5 * mm, "Терапевтический протокол • Персональная психологическая практика • Автономия")
        page_str = f"Страница {self._pageNumber} из {total_pages}"
        self.drawRightString(PAGE_W - M_H, 6.5 * mm, page_str)
        self.setStrokeColor(LINE_COLOR)
        self.setLineWidth(0.5)
        self.line(M_H, 8.2 * mm, PAGE_W - M_H, 8.2 * mm)
        self.restoreState()

styles = getSampleStyleSheet()

s_title = ParagraphStyle('T1', fontName='DejaVu-Bold', fontSize=10.5, leading=13.5, textColor=PRIMARY_DARK, alignment=1)
s_sub = ParagraphStyle('TSub', fontName='DejaVu', fontSize=7.2, leading=9.5, textColor=TEXT_MUTED, alignment=1)
s_head = ParagraphStyle('TH_H', fontName='DejaVu-Bold', fontSize=8.5, leading=11, textColor=PRIMARY_DARK)
s_badge = ParagraphStyle('TH_B', fontName='DejaVu-Bold', fontSize=7, leading=9, textColor=PRIMARY, alignment=2)
s_bsub = ParagraphStyle('TH_BS', fontName='DejaVu', fontSize=6.2, leading=8, textColor=TEXT_MUTED, alignment=2)
s_body = ParagraphStyle('Body', fontName='DejaVu', fontSize=7, leading=9.5, textColor=TEXT)
s_body_b = ParagraphStyle('BodyB', fontName='DejaVu-Bold', fontSize=7, leading=9.5, textColor=TEXT)
s_muted = ParagraphStyle('Muted', fontName='DejaVu', fontSize=6.5, leading=8.5, textColor=TEXT_MUTED)
s_line = ParagraphStyle('Line', fontName='DejaVu', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#94a3b8'))

def timing_header(step_title, minutes, theory_min, practice_min):
    col1 = [Paragraph(f"📌 {step_title}", s_head)]
    col2 = [
        Paragraph(f"⏱ <b>Время: ~{minutes} мин</b>", s_badge),
        Paragraph(f"({theory_min} мин чтение • {practice_min} мин практика)", s_bsub)
    ]
    t = Table([[col1, col2]], colWidths=[122 * mm, 62 * mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-1), 0.75, PRIMARY),
    ]))
    return t

def card_box(items, bg=BG_LIGHT, border=PRIMARY, padding=2.5):
    flow = []
    for x in items:
        if isinstance(x, str):
            flow.append(Paragraph(x, s_body))
        else:
            flow.append(x)
    t = Table([[flow]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.6, border),
        ('TOPPADDING', (0,0), (-1,-1), padding),
        ('BOTTOMPADDING', (0,0), (-1,-1), padding),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def invivo_box(title, context, instruction, success_metric, lines=2):
    head_s = ParagraphStyle('IV_H', fontName='DejaVu-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#b45309'))
    txt_s = ParagraphStyle('IV_T', fontName='DejaVu', fontSize=6.8, leading=8.8, textColor=TEXT)
    b_s = ParagraphStyle('IV_B', fontName='DejaVu-Bold', fontSize=6.8, leading=8.8, textColor=TEXT)
    
    flow = [
        Paragraph(f"🎯 <b>ПОВЕДЕНЧЕСКИЙ ЭКСПЕРИМЕНТ В РЕАЛЬНОЙ ЖИЗНИ (IN VIVO): {title}</b>", head_s),
        Spacer(1, 0.8*mm),
        Paragraph(f"• <b>Где и когда:</b> {context}", txt_s),
        Paragraph(f"• <b>Что именно сделать:</b> {instruction}", txt_s),
        Paragraph(f"• <b>Критерий успеха:</b> {success_metric}", txt_s),
        Spacer(1, 0.6*mm),
        Paragraph("<b>Полевой отчёт (зафиксируйте реакцию тела и результат):</b>", b_s)
    ]
    for _ in range(lines):
        flow.append(Paragraph("____________________________________________________________________________________________________", s_line))
    t = Table([[flow]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WARN_BG),
        ('BOX', (0,0), (-1,-1), 0.75, WARN_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def make_table(data, widths, bg=BG_LIGHT):
    t_rows = []
    for r_i, r in enumerate(data):
        row_flow = []
        for c in r:
            st = s_body_b if r_i == 0 else s_body
            row_flow.append(Paragraph(c, st) if isinstance(c, str) else c)
        t_rows.append(row_flow)
    t = Table(t_rows, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

def write_lines(count=2, label="Моя рефлексия и записи:"):
    flow = [Paragraph(f"<b>{label}</b>", s_body_b)]
    for _ in range(count):
        flow.append(Paragraph("____________________________________________________________________________________________________", s_line))
    return flow

# ==========================================
# LEVEL 1: 5 PAGES
# ==========================================
def build_boundaries_l1(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=M_H, rightMargin=M_H, topMargin=M_V, bottomMargin=M_V)
    story = []

    # Page 1
    story.append(Paragraph("УРОВЕНЬ 1: ЭКСПРЕСС-ИНТЕНСИВ • СЕРИЯ 01", s_sub))
    story.append(Paragraph("Как сказать «НЕТ» без чувства вины и страха отвержения", s_title))
    story.append(Spacer(1, 1.5*mm))
    story.append(timing_header("Шаг 1: Экспресс-скрининг автоматического соглашательства", 8, 3, 5))
    story.append(Spacer(1, 1.5*mm))
    chk_data = [
        ["№", "Диагностический маркер автоматической реакции (People-Pleasing)", "Частота"],
        ["1", "Говорю «да» раньше, чем успеваю осознать, хочу ли соглашаться на самом деле.", "Часто / Редко"],
        ["2", "Испытываю вспышку тревоги или вины, если отказываю даже в незначительной просьбе.", "Часто / Редко"],
        ["3", "Беру на себя чужую ответственность из страха, что человек обидится или разочаруется.", "Часто / Редко"],
        ["4", "Оправдываюсь и придумываю длинные объяснения вместо спокойного короткого отказа.", "Часто / Редко"],
        ["5", "После вынужденного согласия ощущаю скрытое раздражение, упадок сил или злость на себя.", "Часто / Редко"],
    ]
    story.append(make_table(chk_data, [8*mm, 142*mm, 34*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(card_box([
        "💡 <b>Терапевтический ориентир:</b> Автоматическое «да» — это не доброта, а защитная реакция нервной системы («заискивание» / fawning). Наша задача — вернуть паузу выбора между стимулом и реакцией."
    ], bg=HIGHLIGHT, border=PRIMARY))
    story.append(Spacer(1, 2*mm))
    story.append(invivo_box(
        "Пауза перед соглашательством",
        "В течение дня при любых двух входящих вопросах или просьбах (дома, в мессенджере, на работе).",
        "Сделать вдох-выдох и физически выдержать молчание 5 секунд, прежде чем открыть рот для ответа.",
        "Заметить всплеск тревоги и не озвучивать автоматическое «да» в первые 5 секунд.",
        lines=2
    ))
    story.append(PageBreak())

    # Page 2
    story.append(timing_header("Шаг 2: Карта соматических маркеров соглашательства и Заземление", 10, 3, 7))
    story.append(Spacer(1, 1.5*mm))
    story.append(card_box([
        "🧠 <b>Нейробиология отказа:</b> При риске социального отказа миндалевидное тело посылает сигнал тревоги. Тело выдает спазм еще до включения логики. Заземление возвращает контроль префронтальной коре."
    ]))
    story.append(Spacer(1, 1.5*mm))
    soma_data = [
        ["Телесная зона", "Типичный спазм при нарушении границ", "Техника соматического снятия блока"],
        ["Горло / Голос", "Ком в горле, перехват дыхания, голос становится заискивающим.", "Глубокий сглатывающий вдох, расслабление челюсти, выдох со звуком «ха-а»."],
        ["Плечи и грудь", "Подтягивание плеч к ушам, сжатие груди, поверхностное дыхание.", "Опустить плечи, мягко свести лопатки, опереться спиной на спинку стула."],
        ["Живот", "Ощущение холода или спазма в солнечном сплетении.", "Положить теплую ладонь на живот, 3 цикла диафрагмального дыхания 4-6."],
        ["Стопы и ноги", "Потеря опоры, стремление суетливо уступить пространство.", "Вдавить обе подошвы в пол, почувствовать гравитацию и физическую устойчивость."],
    ]
    story.append(make_table(soma_data, [30*mm, 77*mm, 77*mm]))
    story.append(Spacer(1, 2*mm))
    story.extend(write_lines(2, "Мой доминирующий соматический маркер соглашательства (где в теле сжимается в первую очередь?):"))
    story.append(Spacer(1, 2*mm))
    story.append(invivo_box(
        "Соматическое заземление в разговоре",
        "При любом разговоре, где вы чувствуете нарастающее психологическое давление.",
        "Не отвечая сразу, физически вдавить стопы в пол и расслабить челюсть перед тем, как произнести фразу.",
        "Зафиксировать устойчивость в теле и отсутствие привычного суетливого оправдания.",
        lines=2
    ))
    story.append(PageBreak())

    # Page 3
    story.append(timing_header("Шаг 3: Формула ассертивного отказа (4-компонентная матрица)", 12, 4, 8))
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph("Золотой стандарт здоровой границы: отказ без встречной агрессии и без унизительных оправданий.", s_body))
    story.append(Spacer(1, 1.5*mm))
    mat_data = [
        ["Компонент", "Функция в диалоге", "Терапевтический речевой скрипт"],
        ["1. Валидация контакта", "Снижает защитную реакцию собеседника.", "«Спасибо за доверие ко мне...» / «Я понимаю важность задачи...»"],
        ["2. Ясный факт отказа", "Исключает ложные надежды и манипуляции.", "«Но в этот раз я не смогу взять это» / «Я вынужден отказаться»."],
        ["3. Краткая причина", "Без оправданий и чувства вины (1 предложение).", "«Мое расписание полностью заполнено» / «У меня другие приоритеты»."],
        ["4. Альтернатива (опция)", "Только если вы искренне готовы помочь иначе.", "«Могу подсказать коллегу» / «Можем вернуться к этому через месяц»."],
    ]
    story.append(make_table(mat_data, [38*mm, 52*mm, 94*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(card_box([
        "⚠️ <b>Опасная ошибка:</b> Длинные витиеватые объяснения («понимаешь, у меня кошка, пробки, голова...») считываются как слабость и приглашение продавить вас. Точка после отказа защищает отношения лучше оправданий."
    ], bg=WARN_BG, border=WARN_BORDER))
    story.append(Spacer(1, 2*mm))
    story.extend(write_lines(2, "Мой персональный шаблон отказа под актуальную ситуацию (сконструируйте по 4 компонентам):"))
    story.append(Spacer(1, 2*mm))
    story.append(invivo_box(
        "Тест короткого отказа без оправданий",
        "Бытовая просьба от коллеги, знакомого или продавца (дополнительная задача, навязчивое предложение).",
        "Сказать: «Спасибо, мне это не подходит» или «К сожалению, не смогу». И поставить точку, удерживая паузу.",
        "Удержать молчание после точки минимум 4 секунды, не заполняя паузу суетливыми оправданиями.",
        lines=2
    ))
    story.append(PageBreak())

    # Page 4
    story.append(timing_header("Шаг 4: Выдерживание вины и Техника «Буфер времени»", 10, 3, 7))
    story.append(Spacer(1, 1.5*mm))
    story.append(card_box([
        "⚡ <b>Клинический инсайт о вине:</b> Вина после установления границы — это не сигнал о том, что вы поступили плохо. Это лишь невротическая реакция непривычки. <b>«Лучше пережить 15 минут вины, чем 2 недели глухой злости за навязанные обязательства».</b>"
    ], bg=HIGHLIGHT, border=PRIMARY))
    story.append(Spacer(1, 2*mm))
    buf_data = [
        ["Контекст давления", "Опасная автоматическая реакция", "Ассертивный речевой буфер времени"],
        ["Коллега / Руководитель", "«Да, конечно, сделаю прямо сейчас...»", "«Мне нужно свериться с текущим пулом задач. Вернусь с точным ответом через 30 минут»."],
        ["Родственники / Близкие", "Спешное согласие, чтобы не обидеть.", "«Мне важно то, о чем ты говоришь. Подумаю до вечера и скажу, как мне комфортно»."],
        ["Продажи / Услуги", "Неловкое молчание и трата денег.", "«У меня железное правило: не принимать спонтанных решений. Если решу — свяжусь сам»."],
    ]
    story.append(make_table(buf_data, [38*mm, 54*mm, 92*mm]))
    story.append(Spacer(1, 2*mm))
    story.extend(write_lines(2, "Моя личная когнитивная опора при наплыве вины («Я имею право выбирать себя, потому что...»):"))
    story.append(Spacer(1, 2*mm))
    story.append(invivo_box(
        "Применение буфера времени на практике",
        "Следующее обращение любого человека с просьбой или предложением (личное или в мессенджере).",
        "Не отвечать сразу. Написать или сказать: «Мне нужно свериться с расписанием, отвечу через час».",
        "Использовать полученный час, чтобы спокойно решить, хотите ли вы согласиться, без внешнего давления.",
        lines=2
    ))
    story.append(PageBreak())

    # Page 5
    story.append(timing_header("Шаг 5: Карманная карточка дипломатичного отказа и Личный контракт", 8, 2, 6))
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph("✂️ Выносная карманная памятка (Pocket Reference Card): сфотографируйте в телефон", s_body_b))
    story.append(Spacer(1, 1.5*mm))
    pock_data = [
        ["Контекст границы", "Готовая дипломатичная формулировка (Pocket Script)"],
        ["1. Запрос на деньги / долг", "«Я ценю наши отношения, но у меня железный принцип: я не даю деньги в долг, чтобы не смешивать дружбу и финансы»."],
        ["2. Сверхурочная работа", "«Я готов взять задачу, но тогда нужно сдвинуть дедлайн по проекту Х. Что для нас в большем приоритете?»"],
        ["3. Непрошеные советы", "«Спасибо за участие, но в этом вопросе я хочу разобраться самостоятельно / опереться на свой опыт»."],
        ["4. Нарушение личных тем", "«Это пространство моей личной жизни, я предпочитаю не обсуждать его. Давай сменим тему»."],
        ["5. Навязчивые звонки", "«Сейчас я не могу говорить. Напиши суть сообщением, я прочитаю, когда освобожусь»."],
    ]
    story.append(make_table(pock_data, [44*mm, 140*mm]))
    story.append(Spacer(1, 2*mm))
    story.extend(write_lines(2, "Мой личный контракт с собой на 7 дней (Какую одну границу я обещаю себе защитить?):"))
    story.append(Spacer(1, 2*mm))
    story.append(invivo_box(
        "Финальный поведенческий эксперимент серии",
        "Главная «зависшая» ситуация недели (невыполнимая просьба, неприятный разговор, отложенный отказ).",
        "Используя одну из карточек выше, озвучить честное спокойное «нет» и зафиксировать факт освобождения ресурса.",
        "Осознать, что мир не рухнул, а самоуважение и энергия выросли кратно.",
        lines=2
    ))

    doc.build(story, canvasmaker=CustomNumberedCanvas)
    print("Boundaries L1 built successfully (5 pages).")

build_boundaries_l1('therapy-workbooks/workbook_1_express_no.pdf')
doc = pymupdf.open('therapy-workbooks/workbook_1_express_no.pdf')
print(f"Verified L1 pages: {len(doc)}")
