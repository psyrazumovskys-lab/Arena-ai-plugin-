import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

# Palette for Couple De-escalation: Warm Ruby / Berry / Indigo
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_H = 15 * mm
MARGIN_V = 15 * mm
CONTENT_WIDTH = 180 * mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.series_title = "СЕРИЯ 02 • ПРЕОДОЛЕНИЕ КОНФЛИКТОВ И ДИАЛОГ В ПАРЕ"
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        if self._pageNumber > 1:
            self.setFont('DejaVu-Bold', 7)
            self.setFillColor(PRIMARY_DARK)
            self.drawString(MARGIN_H, PAGE_HEIGHT - 10.5 * mm, self.series_title)
            self.setFont('DejaVu', 7)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(PAGE_WIDTH - MARGIN_H, PAGE_HEIGHT - 10.5 * mm, "ПРАКТИКУМ")
            self.setStrokeColor(LINE_COLOR)
            self.setLineWidth(0.6)
            self.line(MARGIN_H, PAGE_HEIGHT - 12 * mm, PAGE_WIDTH - MARGIN_H, PAGE_HEIGHT - 12 * mm)

        self.setFont('DejaVu', 7.5)
        self.setFillColor(TEXT_MUTED)
        self.drawString(MARGIN_H, 9 * mm, "Психотерапевтическая рабочая тетрадь • Материал для безопасной личной практики")
        page_str = f"Страница {self._pageNumber} из {total_pages}"
        self.drawRightString(PAGE_WIDTH - MARGIN_H, 9 * mm, page_str)
        self.setStrokeColor(LINE_COLOR)
        self.setLineWidth(0.6)
        self.line(MARGIN_H, 11.5 * mm, PAGE_WIDTH - MARGIN_H, 11.5 * mm)
        self.restoreState()

PRIMARY = colors.HexColor('#0d9488')
PRIMARY_DARK = colors.HexColor('#0f766e')
ACCENT = colors.HexColor('#e11d48')
BG_LIGHT = colors.HexColor('#f0fdfa')
TEXT = colors.HexColor('#0f172a')
TEXT_MUTED = colors.HexColor('#475569')
LINE_COLOR = colors.HexColor('#ccfbf1')
HIGHLIGHT = colors.HexColor('#f0fdfa')

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    fontName='DejaVu-Bold',
    fontSize=13.5,
    leading=17,
    textColor=PRIMARY_DARK,
    alignment=1,
    spaceAfter=3
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    fontName='DejaVu',
    fontSize=8.5,
    leading=11.5,
    textColor=TEXT_MUTED,
    alignment=1,
    spaceAfter=7
)

h1_style = ParagraphStyle(
    'SectionH1',
    fontName='DejaVu-Bold',
    fontSize=9.5,
    leading=12.5,
    textColor=PRIMARY_DARK,
    spaceBefore=3.5,
    spaceAfter=2.5
)

h2_style = ParagraphStyle(
    'SectionH2',
    fontName='DejaVu-Bold',
    fontSize=8.5,
    leading=11,
    textColor=ACCENT,
    spaceBefore=2.5,
    spaceAfter=2
)

body_style = ParagraphStyle(
    'BodyTextCustom',
    fontName='DejaVu',
    fontSize=8,
    leading=11,
    textColor=TEXT,
    spaceAfter=2.5
)

bullet_style = ParagraphStyle(
    'BulletCustom',
    fontName='DejaVu',
    fontSize=8,
    leading=10.5,
    textColor=TEXT,
    leftIndent=8,
    spaceAfter=2
)

box_text_style = ParagraphStyle(
    'BoxText',
    fontName='DejaVu',
    fontSize=7.8,
    leading=10.5,
    textColor=TEXT
)

def make_box(content_flowables, bg=HIGHLIGHT, border_color=PRIMARY):
    t = Table([[content_flowables]], colWidths=[180*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('LINELEFT', (0,0), (0,-1), 3.5, border_color),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def make_table(data, col_widths, bg_hdr=PRIMARY_DARK, is_compact=False):
    t = Table(data, colWidths=col_widths)
    pad = 3.5 if is_compact else 4.5
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_hdr),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), pad),
        ('TOPPADDING', (0,0), (-1,0), pad),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'DejaVu'),
        ('FONTSIZE', (0,1), (-1,-1), 7.8),
        ('BOTTOMPADDING', (0,1), (-1,-1), pad),
        ('TOPPADDING', (0,1), (-1,-1), pad),
        ('BOX', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    return t

# ==========================================
# LEVEL 1: EXACTLY 3 PAGES
# ==========================================
def build_l1(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=12*mm,
        bottomMargin=12*mm
    )
    story = []

    # Page 1
    story.append(Paragraph("УРОВЕНЬ 1 • ЭКСПРЕСС-ИНТЕНСИВ: СТОП-КРАН ДЛЯ ССОРЫ", title_style))
    story.append(Paragraph("Экстренная деэскалация, физиологическое охлаждение и безопасность в паре", subtitle_style))
    story.append(Paragraph("Раздел 1. Чек-лист эмоционального затопления (Flooding / DPA)", h1_style))
    story.append(Paragraph("Когда пульс превышает 100 уд/мин, диалог невозможен. Оцените симптомы перегруза (0–2):", body_style))

    data_m = [
        [Paragraph("Физиологический маркер затопления", box_text_style), Paragraph("0-1-2", box_text_style)],
        [Paragraph("1. Сердце колотится, пульсация в висках, перехват дыхания.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("2. Жар в лице, прилив крови к голове или ледяные руки.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("3. Сжатые челюсти, напряженные плечи, поза готовности к бою или бегству.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("4. Туннельный слух: слова партнера искажаются и воспринимаются как укол.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("5. Непреодолимый импульс ранить словом, хлопнуть дверью или замолчать.", box_text_style), Paragraph("[   ]", box_text_style)]
    ]
    story.append(make_table(data_m, [155*mm, 25*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 2. Психообразование: Базовый закон деэскалации", h1_style))
    story.append(make_box([
        Paragraph("<b>Клинический факт Дж. Готтмана:</b> Продолжение спора в состоянии затопления в 100% случаев ведет к эскалации, жестокости и тяжелым эмоциональным травмам. Взять тайм-аут — это не отвержение и не поражение, это спасение пары от взаимного саморазрушения.", box_text_style)
    ]))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("<b>Наше кодовое Стоп-слово для немедленного тайм-аута:</b> __________________________________", body_style))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 3. 4-шаговый протокол экологичного тайм-аута", h1_style))
    story.append(Paragraph("Если эмоции зашкаливают, примените пошаговую формулу выхода на паузу:", body_style))

    data_p = [
        [Paragraph("Шаг", box_text_style), Paragraph("Психологическая задача", box_text_style), Paragraph("Речевая формула", box_text_style)],
        [Paragraph("<b>1. Обозначение</b>", box_text_style), Paragraph("Озвучить факт своего перегруза без обвинений.", box_text_style), Paragraph("«Я чувствую, что меня переполняют эмоции, пульс зашкаливает».", box_text_style)],
        [Paragraph("<b>2. Заверение</b>", box_text_style), Paragraph("Снять тревогу отвержения у партнера.", box_text_style), Paragraph("«Ты важен мне, и я хочу решить этот вопрос бережно...»", box_text_style)],
        [Paragraph("<b>3. Время</b>", box_text_style), Paragraph("Назвать конкретную длительность перерыва (20–45 мин).", box_text_style), Paragraph("«...поэтому нам нужна пауза на 30 минут для остывания».", box_text_style)],
        [Paragraph("<b>4. Обязательство</b>", box_text_style), Paragraph("Гарантировать возвращение к диалогу.", box_text_style), Paragraph("«Я вернусь ровно в 19:30, и мы спокойно продолжим».", box_text_style)]
    ]
    story.append(make_table(data_p, [35*mm, 65*mm, 80*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 4. Правила поведения во время паузы", h1_style))
    story.append(Paragraph("• <b>Запрещено:</b> Накручивать себя мысленными спорами, писать сообщения, хлопать дверью.", bullet_style))
    story.append(Paragraph("• <b>Необходимо:</b> Умыться холодной водой (дайвинг-рефлекс), медленный выдох, выйти на воздух.", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 5. Практикум: Конструирование фразы паузы", h1_style))
    story.append(make_box([
        Paragraph("<b>Моя персональная фраза запроса на тайм-аут:</b> __________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 6. 3-дневный трекер микроперемирий", h1_style))
    story.append(Paragraph("Фиксируйте применение стоп-крана и шагов примирения в течение 3 дней:", body_style))

    data_track = [
        [Paragraph("День", box_text_style), Paragraph("Повод для вспышки", box_text_style), Paragraph("Что помогло остановиться", box_text_style), Paragraph("Уровень тепла (0–10)", box_text_style)],
        [Paragraph("<b>День 1</b>", box_text_style), Paragraph("Бытовой спор...", box_text_style), Paragraph("Стоп-слово, пауза 25 мин...", box_text_style), Paragraph("Тепло: 8/10", box_text_style)],
        [Paragraph("<b>День 2</b>", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style)],
        [Paragraph("<b>День 3</b>", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style)]
    ]
    story.append(make_table(data_track, [25*mm, 60*mm, 55*mm, 40*mm], bg_hdr=PRIMARY_DARK, is_compact=False))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 7. Четыре фразы ремонта контакта (Repair Attempts)", h1_style))
    story.append(Paragraph("1. «Я согласен с тобой в части..., прости за резкость тона».", bullet_style))
    story.append(Paragraph("2. «Похоже, мы оба устали. Можем ли мы начать этот разговор заново с теплотой?»", bullet_style))
    story.append(Paragraph("3. «Я люблю тебя больше, чем тему нашего спора. Давай найдем решение вместе».", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 8. Пакт эмоциональной безопасности пары", h1_style))
    story.append(make_box([
        Paragraph("Мы признаем право любого из нас объявить тайм-аут без обид и преследования. Мы табуируем мат, оскорбления и угрозы разрывом. Взявший паузу всегда возвращается к диалогу.<br/><br/>"
                  "Партнер 1: ________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Партнер 2: ________________________", box_text_style)
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)

# ==========================================
# LEVEL 2: EXACTLY 6 PAGES
# ==========================================
def build_l2(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=12*mm,
        bottomMargin=12*mm
    )
    story = []

    # Page 1
    story.append(Paragraph("УРОВЕНЬ 2 • ПРАКТИКУМ: БЕЗОПАСНЫЙ ДИАЛОГ В ПАРЕ", title_style))
    story.append(Paragraph("14-дневная программа трансформации конфликтов и нейтрализации «Четырех всадников»", subtitle_style))
    story.append(Paragraph("Модуль 1. Четыре всадника Апокалипсиса и их противоядия (Дж. Готтман)", h1_style))
    story.append(Paragraph("Четыре деструктивных паттерна, предсказывающих разрушение союза, и их замена:", body_style))

    data_h = [
        [Paragraph("Всадник", box_text_style), Paragraph("Токсичное проявление", box_text_style), Paragraph("Клиническое противоядие", box_text_style)],
        [Paragraph("<b>Критика</b>", box_text_style), Paragraph("Атака на личность («Ты вечно думаешь только о себе»).", box_text_style), Paragraph("Мягкое начало через «Я-послание» («Мне тяжело, я нуждаюсь в помощи»).", box_text_style)],
        [Paragraph("<b>Презрение</b>", box_text_style), Paragraph("Сарказм, насмешки, закатывание глаз, снисходительность.", box_text_style), Paragraph("Культура благодарности, уважение к партнеру.", box_text_style)],
        [Paragraph("<b>Защита</b>", box_text_style), Paragraph("Оправдания, встречные обвинения («А ты сам(а)?!»).", box_text_style), Paragraph("Принятие ответственности хотя бы за часть проблемы.", box_text_style)],
        [Paragraph("<b>Стена (Stonewalling)</b>", box_text_style), Paragraph("Ледяное молчание, игнорирование, уход в глухую оборону.", box_text_style), Paragraph("Физиологическое самоуспокоение и тайм-аут с возвратом.", box_text_style)]
    ]
    story.append(make_table(data_h, [35*mm, 75*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Самодиагностика пары", h2_style))
    story.append(make_box([
        Paragraph("<b>Мой ведущий всадник в ссоре:</b> ________________________________________________________________<br/>"
                  "<b>Ведущий всадник партнера:</b> ____________________________________________________________________<br/>"
                  "<b>Наше главное противоядие:</b> _____________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Модуль 2. Трансформатор: от упреков к истинным потребностям", h1_style))
    story.append(Paragraph("Претензия — это крик о помощи на языке войны. Исследуйте перевод упреков:", body_style))

    data_tr = [
        [Paragraph("Упрек (Язык войны)", box_text_style), Paragraph("Уязвимое чувство", box_text_style), Paragraph("Формула бережной просьбы", box_text_style)],
        [Paragraph("«Ты вечно сидишь в телефоне!»", box_text_style), Paragraph("Одиночество, тоска по близости.", box_text_style), Paragraph("«Мне не хватает твоего внимания. Давай побудем вместе 20 минут?»", box_text_style)],
        [Paragraph("«Тебе наплевать на порядок в доме!»", box_text_style), Paragraph("Усталость, бессилие, брошенность.", box_text_style), Paragraph("«Я сильно устала, помоги мне, пожалуйста, на кухне».", box_text_style)],
        [Paragraph("«Ты никогда меня не слушаешь!»", box_text_style), Paragraph("Ощущение своей неважности.", box_text_style), Paragraph("«Для меня очень важно почувствовать, что ты слышишь моё мнение».", box_text_style)]
    ]
    story.append(make_table(data_tr, [50*mm, 55*mm, 75*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум перевода личного упрека", h2_style))
    story.append(make_box([
        Paragraph("<b>Мой типичный упрек партнеру:</b> _________________________________________________________________<br/>"
                  "<b>Какая боль и потребность стоит за ним:</b> _________________________________________________________<br/>"
                  "<b>Моя новая бережная просьба:</b> ___________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Модуль 3. Технология Имаго-диалога (Х. Хендрикс)", h1_style))
    story.append(Paragraph("Структурированный трехшаговый алгоритм безопасной коммуникации в паре:", body_style))

    data_im = [
        [Paragraph("Шаг диалога", box_text_style), Paragraph("Действие слушателя", box_text_style), Paragraph("Ключевая фраза", box_text_style)],
        [Paragraph("<b>1. Зеркало</b>", box_text_style), Paragraph("Точное повторение слов без интерпретаций и возражений.", box_text_style), Paragraph("«Если я правильно слышу, ты говоришь, что... Я верно понял(а)?»", box_text_style)],
        [Paragraph("<b>2. Валидация</b>", box_text_style), Paragraph("Признание субъективной логики и правды партнера.", box_text_style), Paragraph("«В этом есть логика, и я понимаю, почему в этой ситуации ты так почувствовал(а)».", box_text_style)],
        [Paragraph("<b>3. Эмпатия</b>", box_text_style), Paragraph("Сопереживание уязвимой эмоции партнера.", box_text_style), Paragraph("«Я догадываюсь, что ты чувствовал(а) обиду и растерянность... Так ли это?»", box_text_style)]
    ]
    story.append(make_table(data_im, [35*mm, 70*mm, 75*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Отработка диалога на выбранной теме", h2_style))
    story.append(make_box([
        Paragraph("<b>Тема для безопасного обсуждения:</b> ______________________________________________________________<br/>"
                  "<b>Главный инсайт слушателя после отражения:</b> ______________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Модуль 4. Минное поле пары: карта эмоциональных триггеров", h1_style))
    story.append(Paragraph("Распознавание ранних травматических ран привязанности, обостряющих реакцию:", body_style))

    data_trig = [
        [Paragraph("Внешний триггер", box_text_style), Paragraph("Детская кнопка уязвимости", box_text_style), Paragraph("Бурная защитная реакция", box_text_style)],
        [Paragraph("Опоздание партнера на встречу.", box_text_style), Paragraph("«Я ничтожен, моё время ничего не значит».", box_text_style), Paragraph("Вспышка ярости, обвинения в черствости.", box_text_style)],
        [Paragraph("Усталый взгляд, вздох партнера.", box_text_style), Paragraph("«Мной недовольны, меня разлюбят».", box_text_style), Paragraph("Уход в глухую оборону, ледяное молчание.", box_text_style)],
        [Paragraph("Просьба о личном пространстве.", box_text_style), Paragraph("«Меня бросают, я останусь один».", box_text_style), Paragraph("Панический контроль, допросы, ревность.", box_text_style)]
    ]
    story.append(make_table(data_trig, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Паспорт личных уязвимых зон", h2_style))
    story.append(make_box([
        Paragraph("<b>Партнер 1 (моя главная детская кнопка):</b> ______________________________________________________<br/>"
                  "<b>Партнер 2 (моя главная детская кнопка):</b> ______________________________________________________<br/>"
                  "<b>Как мы договариваемся беречь эти зоны:</b> ________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Модуль 5. Сигналы ремонта контакта и ритуалы примирения", h1_style))
    story.append(Paragraph("Стабильность союза определяется способностью пары вовремя посылать и принимать сигналы мира:", body_style))

    data_rep = [
        [Paragraph("Тип сигнала мира", box_text_style), Paragraph("Конкретное проявление", box_text_style), Paragraph("Эффект для пары", box_text_style)],
        [Paragraph("<b>Вербальный</b>", box_text_style), Paragraph("«Давай притормозим», «Я сейчас нелепо защищаюсь, прости».", box_text_style), Paragraph("Снижение оборотов спора, возврат к логике.", box_text_style)],
        [Paragraph("<b>Телесный</b>", box_text_style), Paragraph("Прикосновение к руке, открытая поза, глубокий совместный выдох.", box_text_style), Paragraph("Соматическое успокоение нервной системы.", box_text_style)],
        [Paragraph("<b>Заботливый</b>", box_text_style), Paragraph("Принести стакан воды, молча обнять, накрыть пледом.", box_text_style), Paragraph("Подтверждение любви вопреки разногласиям.", box_text_style)]
    ]
    story.append(make_table(data_rep, [40*mm, 80*mm, 60*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Проектирование персонального ритуала выхода из ссоры", h2_style))
    story.append(make_box([
        Paragraph("<b>Наш совместный ритуал примирения:</b> ____________________________________________________________<br/>"
                  "____________________________________________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Модуль 6. 14-дневный план безопасной связи и Кодекс пары", h1_style))
    story.append(Paragraph("Пошаговое закрепление новых привычек общения:", body_style))

    data_m6 = [
        [Paragraph("Период", box_text_style), Paragraph("Фокус практики", box_text_style), Paragraph("Критерий успешности", box_text_style)],
        [Paragraph("<b>Дни 1–3</b>", box_text_style), Paragraph("Мониторинг 4 всадников, остановка сарказма.", box_text_style), Paragraph("Полное отсутствие насмешек и критики.", box_text_style)],
        [Paragraph("<b>Дни 4–7</b>", box_text_style), Paragraph("Мягкое начало диалога и перевод упреков в просьбы.", box_text_style), Paragraph("Снижение защитных реакций партнера.", box_text_style)],
        [Paragraph("<b>Дни 8–11</b>", box_text_style), Paragraph("Ежевечерний 15-минутный Имаго-диалог.", box_text_style), Paragraph("Укрепление взаимного доверия.", box_text_style)],
        [Paragraph("<b>Дни 12–14</b>", box_text_style), Paragraph("Закрепление ритуалов примирения и подведение итогов.", box_text_style), Paragraph("Стабильное чувство безопасности союза.", box_text_style)]
    ]
    story.append(make_table(data_m6, [35*mm, 85*mm, 60*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Кодекс безопасного супружеского союза", h2_style))
    story.append(make_box([
        Paragraph("1. Наш враг — это цикл ссоры, а не партнер.<br/>"
                  "2. Мы говорим о своих переживаниях без упреков и ярлыков.<br/>"
                  "3. Мы выбираем сохранение доверия превыше сиюминутной правоты в споре.<br/>"
                  "4. Мы обязуемся слышать боль друг друга и вовремя подавать сигналы примирения.", box_text_style),
    ], bg=colors.HexColor('#fff1f2'), border_color=colors.HexColor('#be123c')))

    doc.build(story, canvasmaker=NumberedCanvas)

# ==========================================
# LEVEL 3: EXACTLY 8 PAGES
# ==========================================
def build_l3(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=12*mm,
        bottomMargin=12*mm
    )
    story = []

    # Page 1
    story.append(Paragraph("УРОВЕНЬ 3 • КЛИНИЧЕСКОЕ РУКОВОДСТВО: ЭФТ-ДЕКОНСТРУКЦИЯ ЦИКЛА", title_style))
    story.append(Paragraph("Клинический протокол эмоционально-фокусированной супружеской терапии Сью Джонсон (8 сессий)", subtitle_style))
    story.append(Paragraph("Раздел 1. Концептуализация негативного цикла: «Танец ссоры»", h1_style))
    story.append(Paragraph("В ЭФТ конфликт рассматривается как самоподкрепляющаяся система «Преследование — Отстранение»:", body_style))

    data_p1 = [
        [Paragraph("Позиция в цикле", box_text_style), Paragraph("Вторичная реакция (верхушка айсберга)", box_text_style), Paragraph("Первичная уязвимость (глубина привязанности)", box_text_style)],
        [Paragraph("<b>Преследователь (Pursuer)</b>", box_text_style), Paragraph("Претензии, требование немедленного ответа, повышенный тон.", box_text_style), Paragraph("Паника одиночества: «Меня не замечают, связь разорвана!».", box_text_style)],
        [Paragraph("<b>Отстраняющийся (Withdrawer)</b>", box_text_style), Paragraph("Замыкание, уход в другую комнату, ледяное молчание.", box_text_style), Paragraph("Ужас своей несостоятельности: «Я всё порчу, я плохой партнер».", box_text_style)]
    ]
    story.append(make_table(data_p1, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Диагностика ролей пары в первичном цикле", h2_style))
    story.append(make_box([
        Paragraph("<b>Партнер А (Преследователь):</b> __________________________________________________________________<br/>"
                  "<b>Партнер Б (Отстраняющийся):</b> __________________________________________________________________<br/>"
                  "<b>Типичный сценарий развертывания конфликта:</b> ____________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 2. Дифференциация вторичных и первичных эмоций", h1_style))
    story.append(Paragraph("Вторичные эмоции защищают от уязвимости, но запускают ответную атаку партнера:", body_style))

    data_p2 = [
        [Paragraph("Ситуация триггера", box_text_style), Paragraph("Вторичная эмоция нападения", box_text_style), Paragraph("Первичная глубинная боль", box_text_style)],
        [Paragraph("Задержка на работе / молчание.", box_text_style), Paragraph("Ярость: «Тебе плевать на семью!»", box_text_style), Paragraph("Страх: «Я чувствую себя брошенной и одинокой».", box_text_style)],
        [Paragraph("Критическое замечание партнера.", box_text_style), Paragraph("Уход / Презрение: «С тобой невозможно».", box_text_style), Paragraph("Стыд: «Я снова не оправдал твоих ожиданий».", box_text_style)]
    ]
    story.append(make_table(data_p2, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Картирование скрытых первичных переживаний", h2_style))
    story.append(make_box([
        Paragraph("<b>Партнер 1 (моя первичная боль под гневом):</b> ____________________________________________________<br/>"
                  "<b>Партнер 2 (моя первичная боль под молчанием):</b> ________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 3. Взгляд со стороны негативного цикла пары", h1_style))
    story.append(Paragraph("Превращение циклического паттерна во внешнего общего противника союза:", body_style))

    data_p3 = [
        [Paragraph("Логика эскалации цикла", box_text_style), Paragraph("Формула замкнутого круга", box_text_style)],
        [Paragraph("Чем настойчивее партнер А требует контакта и кричит...", box_text_style), Paragraph("...тем глубже партнер Б уходит в защиту и молчание.", box_text_style)],
        [Paragraph("Чем холоднее и недоступнее становится партнер Б...", box_text_style), Paragraph("...тем сильнее нарастает паника и гнев партнера А.", box_text_style)]
    ]
    story.append(make_table(data_p3, [90*mm, 90*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Взгляд со стороны: имя для нашего цикла", h2_style))
    story.append(make_box([
        Paragraph("<b>Метафорическое имя нашего цикла («Вихрь», «Лед и пламя»):</b> _______________________________________<br/>"
                  "<b>Как мы понимаем, что попали в его ловушку:</b> ___________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Раздел 4. Стили привязанности и их столкновение в кризисе", h1_style))
    story.append(Paragraph("Ранние рабочие модели привязанности Дж. Боулби в контексте супружеского конфликта:", body_style))

    data_p4 = [
        [Paragraph("Стиль привязанности", box_text_style), Paragraph("Ядерная установка о себе и партнере", box_text_style), Paragraph("Копинг в конфликте", box_text_style)],
        [Paragraph("<b>Тревожный (Anxious)</b>", box_text_style), Paragraph("«Я ценен только в близости; другие ненадежны и могут бросить».", box_text_style), Paragraph("Гиперактивация: панический контроль, проверки, крик.", box_text_style)],
        [Paragraph("<b>Избегающий (Avoidant)</b>", box_text_style), Paragraph("«Полагаться на других опасно; я должен быть самодостаточным».", box_text_style), Paragraph("Деактивация: подавление чувств, изоляция, побег в работу.", box_text_style)],
        [Paragraph("<b>Надежный (Secure)</b>", box_text_style), Paragraph("«Я ценен, и партнер надежен; мы можем открыто говорить о боли».", box_text_style), Paragraph("Прямое обращение за поддержкой, умение утешать.", box_text_style)]
    ]
    story.append(make_table(data_p4, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Анализ профиля привязанности пары", h2_style))
    story.append(make_box([
        Paragraph("<b>Профиль привязанности Партнера 1:</b> ____________________________________________________________<br/>"
                  "<b>Профиль привязанности Партнера 2:</b> ____________________________________________________________<br/>"
                  "<b>Как наши стили взаимно триггерят друг друга:</b> _________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Раздел 5. Клинический протокол разворота (EFT Tango)", h1_style))
    story.append(Paragraph("Пять терапевтических движений ЭФТ для создания нового эмоционального опыта:", body_style))

    data_p5 = [
        [Paragraph("Движение Танго", box_text_style), Paragraph("Суть клинического шага", box_text_style), Paragraph("Задача терапевта и пары", box_text_style)],
        [Paragraph("<b>1. Отражение</b>", box_text_style), Paragraph("Фиксация момента запуска негативного цикла.", box_text_style), Paragraph("Остановить автоматическую ссору.", box_text_style)],
        [Paragraph("<b>2. Углубление</b>", box_text_style), Paragraph("Контакт с первичной болью и страхом привязанности.", box_text_style), Paragraph("Переход от злости к уязвимости.", box_text_style)],
        [Paragraph("<b>3. Разыгрывание</b>", box_text_style), Paragraph("Прямое озвучивание уязвимой потребности партнеру.", box_text_style), Paragraph("«Мне страшно потерять тебя».", box_text_style)],
        [Paragraph("<b>4. Обработка</b>", box_text_style), Paragraph("Исследование реакции принимающего партнера.", box_text_style), Paragraph("Обеспечить сочувствующий отклик.", box_text_style)],
        [Paragraph("<b>5. Интеграция</b>", box_text_style), Paragraph("Закрепление безопасного контакта.", box_text_style), Paragraph("Формирование нового опыта близости.", box_text_style)]
    ]
    story.append(make_table(data_p5, [40*mm, 75*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум уязвимого обращения", h2_style))
    story.append(make_box([
        Paragraph("<b>Моё искреннее послание партнеру из уязвимости:</b> ________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Раздел 6. Исцеление ран привязанности (Attachment Injuries)", h1_style))
    story.append(Paragraph("Протокол восстановления доверия после травмы оставления или предательства:", body_style))

    data_p6 = [
        [Paragraph("Фаза исцеления", box_text_style), Paragraph("Действия пострадавшего", box_text_style), Paragraph("Действия причинившего боль", box_text_style)],
        [Paragraph("<b>1. Экспликация раны</b>", box_text_style), Paragraph("Описание момента боли без сарказма и обобщений.", box_text_style), Paragraph("Слушать без оправданий и минимизации.", box_text_style)],
        [Paragraph("<b>2. Проживание горя</b>", box_text_style), Paragraph("Позволить себе слезы и печаль в присутствии партнера.", box_text_style), Paragraph("Искреннее сострадание: «Я вижу твою боль».", box_text_style)],
        [Paragraph("<b>3. Репарация</b>", box_text_style), Paragraph("Принятие эмоциональной доступности партнера.", box_text_style), Paragraph("Твердое подтверждение надежности союза.", box_text_style)]
    ]
    story.append(make_table(data_p6, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Протокол заживления раны в паре", h2_style))
    story.append(make_box([
        Paragraph("<b>Событие, оставившее травматический след:</b> _____________________________________________________<br/>"
                  "<b>Слова раскаяния и эмоциональной доступности:</b> __________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 7
    story.append(Paragraph("Раздел 7. Дорожная карта супружеской терапии на 8 сессий", h1_style))
    story.append(Paragraph("Клинический маршрут реструктуризации союза по методу Сью Джонсон:", body_style))

    data_p7 = [
        [Paragraph("Сессии", box_text_style), Paragraph("Терапевтическая фаза ЭФТ", box_text_style), Paragraph("Критерий перехода", box_text_style)],
        [Paragraph("<b>Сессии 1–2</b>", box_text_style), Paragraph("Альянс, деэскалация негативного цикла, картирование триггеров.", box_text_style), Paragraph("Пара объединена против цикла.", box_text_style)],
        [Paragraph("<b>Сессии 3–5</b>", box_text_style), Paragraph("Включение отстраняющегося партнера (Withdrawer Re-engagement).", box_text_style), Paragraph("Отстраняющийся партнер открыт и не сбегает.", box_text_style)],
        [Paragraph("<b>Сессии 6–7</b>", box_text_style), Paragraph("Смягчение преследующего партнера (Pursuer Softening).", box_text_style), Paragraph("Преследователь обращается из уязвимости.", box_text_style)],
        [Paragraph("<b>Сессия 8</b>", box_text_style), Paragraph("Консолидация надежной базы союза, новые ритуалы.", box_text_style), Paragraph("Стабильная эмоциональная безопасность.", box_text_style)]
    ]
    story.append(make_table(data_p7, [30*mm, 85*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Терапевтические заметки пары", h2_style))
    story.append(make_box([
        Paragraph("<b>Главные достижения в преодолении цикла:</b> _______________________________________________________<br/>"
                  "<b>Над чем предстоит работать в ближайшие недели:</b> ________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 8
    story.append(Paragraph("Раздел 8. Пакт надежной привязанности (Модель A.R.E.)", h1_style))
    story.append(Paragraph("Три фундаментальных опоры супружеской надежности (Сью Джонсон):", body_style))

    data_p8 = [
        [Paragraph("Опора ARE", box_text_style), Paragraph("Суть вопроса привязанности", box_text_style), Paragraph("Обязательство партнера", box_text_style)],
        [Paragraph("<b>Accessibility (Доступность)</b>", box_text_style), Paragraph("«Могу ли я достучаться до тебя в трудный миг?»", box_text_style), Paragraph("«Я откликаюсь и открываю своё сердце».", box_text_style)],
        [Paragraph("<b>Responsiveness (Отзывчивость)</b>", box_text_style), Paragraph("«Откликнешься ли ты на мою эмоциональную боль?»", box_text_style), Paragraph("«Я валидирую твои чувства и утешаю».", box_text_style)],
        [Paragraph("<b>Engagement (Вовлеченность)</b>", box_text_style), Paragraph("«Ценен ли я для тебя? Будешь ли ты рядом?»", box_text_style), Paragraph("«Я предан нашему союзу и ценю тебя».", box_text_style)]
    ]
    story.append(make_table(data_p8, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Супружеский терапевтический договор", h2_style))
    story.append(make_box([
        Paragraph("<b>ПАХТ БЕЗОПАСНОГО И ЛЮБЯЩЕГО СОЮЗА</b><br/>"
                  "Мы признаем ценность нашей связи превыше любых сиюминутных споров. Мы обязуемся беречь уязвимость друг друга, вовремя останавливать разрушительный цикл и хранить надежную привязанность.<br/><br/>"
                  "Партнер 1: __________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Партнер 2: __________________________<br/>"
                  "Дата: «____» ____________ 202__ г.", box_text_style),
    ], bg=colors.HexColor('#fff1f2'), border_color=colors.HexColor('#be123c')))

    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == '__main__':
    build_l1('therapy-workbooks/couple_workbook_1_stop_escalation.pdf')
    print("SUCCESS: Couple L1 (3 pages)")

    build_l2('therapy-workbooks/couple_workbook_2_safe_dialogue.pdf')
    print("SUCCESS: Couple L2 (6 pages)")

    build_l3('therapy-workbooks/couple_workbook_3_clinical_cycle.pdf')
    print("SUCCESS: Couple L3 (8 pages)")
