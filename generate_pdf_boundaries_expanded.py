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

# Palette for Boundaries: Professional Teal / Blue Slate
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_H = 15 * mm
MARGIN_V = 15 * mm
CONTENT_WIDTH = 180 * mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.series_title = "СЕРИЯ 01 • СУВЕРЕНИТЕТ И ЛИЧНЫЕ ГРАНИЦЫ"
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

PRIMARY = colors.HexColor('#2563eb')
PRIMARY_DARK = colors.HexColor('#1d4ed8')
ACCENT = colors.HexColor('#0891b2')
BG_LIGHT = colors.HexColor('#f8fafc')
TEXT = colors.HexColor('#0f172a')
TEXT_MUTED = colors.HexColor('#475569')
LINE_COLOR = colors.HexColor('#cbd5e1')
HIGHLIGHT = colors.HexColor('#eff6ff')

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
    story.append(Paragraph("УРОВЕНЬ 1 • ЭКСПРЕСС-ИНТЕНСИВ: КАК СКАЗАТЬ «НЕТ» БЕЗ ВИНЫ", title_style))
    story.append(Paragraph("Клинический 3-дневный практикум экологичного отказа и защиты личных границ", subtitle_style))
    story.append(Paragraph("Раздел 1. Карта уязвимости личных границ (10 клинических маркеров)", h1_style))
    story.append(Paragraph("Оцените проявление каждого симптома от 0 (никогда) до 3 (почти всегда):", body_style))

    data_m = [
        [Paragraph("Маркер уязвимости границ", box_text_style), Paragraph("0-1-2-3", box_text_style)],
        [Paragraph("1. Соглашаюсь раньше, чем успеваю оценить свои реальные силы и время.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("2. Острое чувство вины или стыда при необходимости сказать кому-то «нет».", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("3. Долго и унизительно оправдываюсь, придумывая ложные причины для отказа.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("4. Беру на себя эмоциональное состояние окружающих («если он зол — я виноват»).", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("5. Терплю нарушение договоренностей, бестактные шутки или вторжение в пространство.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("6. Страх показаться грубым, эгоистичным или вызвать чужую обиду.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("7. Выполняю чужие просьбы в ущерб собственному сну, здоровью или семье.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("8. Глухое раздражение и фоновая злость на людей за то, что они «пользуются мной».", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("9. Телесные спазмы (ком в горле, сжатые челюсти, плечи вверх) при чужой просьбе.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("10. Желание проигнорировать звонок или исчезнуть, лишь бы не отказывать прямо.", box_text_style), Paragraph("[   ]", box_text_style)]
    ]
    story.append(make_table(data_m, [155*mm, 25*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 2. Психообразование: Границы как навигатор отношений", h1_style))
    story.append(make_box([
        Paragraph("<b>Терапевтический принцип:</b> Границы — это не крепостная стена и не агрессивный выпад. Это ясный дорожный знак, определяющий, где заканчиваетесь вы и начинается другой человек. Сказать спокойное «нет» внешнему требованию — это единственный способ сказать честное «да» собственному здоровью и сохранить искреннее уважение в контакте.", box_text_style)
    ]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<b>Интерпретация скрининга:</b> 0–9: сохранные границы; 10–19: ситуативная уязвимость и перегруз; 20–30: глубокий People-pleasing и синдром спасателя.", body_style))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 3. Пошаговый 4-шаговый протокол отказа в моменте", h1_style))
    story.append(Paragraph("Когда поступает обременительная просьба, остановите автоматизм угодничества алгоритмом:", body_style))

    data_proto = [
        [Paragraph("Шаг алгоритма", box_text_style), Paragraph("Психологическая задача", box_text_style), Paragraph("Речевая формула", box_text_style)],
        [Paragraph("<b>1. Пауза</b>", box_text_style), Paragraph("Остановить телесный импульс согласия и спасательства.", box_text_style), Paragraph("«Мне нужно свериться с расписанием, отвечу через час / к вечеру».", box_text_style)],
        [Paragraph("<b>2. Валидация</b>", box_text_style), Paragraph("Признать важность чужого запроса без принятия вины.", box_text_style), Paragraph("«Я понимаю, насколько этот проект/вопрос важен для тебя...»", box_text_style)],
        [Paragraph("<b>3. Прямое «Нет»</b>", box_text_style), Paragraph("Ясный отказ без оправданий, лжи и унизительных извинений.", box_text_style), Paragraph("«...но я не смогу взять это на себя / у меня нет ресурса помочь».", box_text_style)],
        [Paragraph("<b>4. Альтернатива</b>", box_text_style), Paragraph("Опциональный экологичный вариант вне ваших сверхусилий.", box_text_style), Paragraph("«Могу подсказать контакт другого специалиста / посмотреть позже».", box_text_style)]
    ]
    story.append(make_table(data_proto, [35*mm, 65*mm, 80*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 4. Готовые экологичные речевые шаблоны по сферам", h1_style))
    story.append(Paragraph("• <b>В работе:</b> «Мои приоритеты на сегодня сформированы. Взять новую задачу смогу, только сняв текущую».", bullet_style))
    story.append(Paragraph("• <b>В семье:</b> «Я ценю наши отношения и люблю тебя, но в эти выходные мне необходим полноценный отдых».", bullet_style))
    story.append(Paragraph("• <b>С друзьями:</b> «Спасибо за приглашение! К сожалению, я не присоединюсь. Давайте запланируем встречу позже».", bullet_style))
    story.append(Paragraph("• <b>На советы:</b> «Я благодарен за участие, но в этом вопросе я приму решение самостоятельно».", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 5. Практикум: Конструирование личного отказа", h1_style))
    story.append(make_box([
        Paragraph("<b>Ситуация актуального давления:</b> ____________________________________________________________________<br/>"
                  "<b>Мой отказ по 4 шагам:</b> ____________________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 6. 3-дневный трекер внедрения автономии", h1_style))
    story.append(Paragraph("Фиксируйте микроситуации отстаивания своих границ в течение ближайших 3 дней:", body_style))

    data_track = [
        [Paragraph("День", box_text_style), Paragraph("Ситуация / Просьба", box_text_style), Paragraph("Мой ответ / Действие", box_text_style), Paragraph("Уровень вины (0–10) и тело", box_text_style)],
        [Paragraph("<b>День 1</b>", box_text_style), Paragraph("Коллега / друг просит...", box_text_style), Paragraph("Взял паузу, отказал по шагам...", box_text_style), Paragraph("Вина: 6/10, ком в горле отпустил.", box_text_style)],
        [Paragraph("<b>День 2</b>", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style)],
        [Paragraph("<b>День 3</b>", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style)]
    ]
    story.append(make_table(data_track, [25*mm, 60*mm, 55*mm, 40*mm], bg_hdr=PRIMARY_DARK, is_compact=False))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("Раздел 7. Манифест базовых личных прав", h1_style))
    story.append(make_box([
        Paragraph("<b>Я признаю за собой неотъемлемые права взрослой личности:</b><br/>"
                  "1. Я имею право отказать без оправданий и объяснения уважительности причин.<br/>"
                  "2. Я не несу ответственности за чужие негативные эмоции и обиды в ответ на мой корректный отказ.<br/>"
                  "3. Моё время, энергия и покой — это моя зона ответственности и суверенная территория.", box_text_style),
    ], bg=colors.HexColor('#f0fdf4'), border_color=colors.HexColor('#166534')))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("Раздел 8. Интеграционный контракт с собой", h1_style))
    story.append(make_box([
        Paragraph("Я, ________________________________, обязуюсь в течение ближайшей недели сохранять верность своим границам. Моё ключевое правило отказа: ____________________________________________________________.<br/>"
                  "Дата: «____» ____________ 202__ г. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Подпись: ______________________", box_text_style)
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
    story.append(Paragraph("УРОВЕНЬ 2 • ПРАКТИКУМ: АРХИТЕКТУРА ЛИЧНЫХ ГРАНИЦ", title_style))
    story.append(Paragraph("14-дневная программа освобождения от синдрома славного человека (People-Pleasing)", subtitle_style))
    story.append(Paragraph("Модуль 1. Диагностическая типология нарушений психологических границ", h1_style))
    story.append(Paragraph("Границы определяют качество контакта с социумом. Исследуйте 4 базовых типа проницаемости:", body_style))

    data_t = [
        [Paragraph("Тип границы", box_text_style), Paragraph("Поведенческий паттерн", box_text_style), Paragraph("Психологическая цена", box_text_style)],
        [Paragraph("<b>Диффузная (размытая)</b>", box_text_style), Paragraph("Неспособность отказать, слияние с другими, синдром хронического спасателя.", box_text_style), Paragraph("Выгорание, истощение, потеря самоидентичности.", box_text_style)],
        [Paragraph("<b>Жесткая (стена)</b>", box_text_style), Paragraph("Тотальная дистанция, подозрительность, отказ от уязвимости и помощи.", box_text_style), Paragraph("Холод в отношениях, глубокое одиночество.", box_text_style)],
        [Paragraph("<b>Хаотичная</b>", box_text_style), Paragraph("Терпение до предела, сменяющееся яростными неконтролируемыми вспышками.", box_text_style), Paragraph("Непредсказуемость связей, вина и стыд после срывов.", box_text_style)],
        [Paragraph("<b>Гибкая (здоровая)</b>", box_text_style), Paragraph("Осознание ценностей, открытость контакту, спокойный твердый отказ.", box_text_style), Paragraph("Внутренняя стабильность, взаимное уважение.", box_text_style)]
    ]
    story.append(make_table(data_t, [40*mm, 75*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Картографирование проницаемости границ по сферам жизни", h2_style))
    story.append(make_box([
        Paragraph("1. Профессиональная сфера (переработки, поручения не по профилю): __________________________________<br/>"
                  "2. Семейная сфера (родители, родственники, непрошеные советы): ________________________________________<br/>"
                  "3. Близкие отношения (партнер, быт, личное время): ___________________________________________________<br/>"
                  "4. Друзья и знакомые (просьбы в долг, ночные звонки): _______________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Модуль 2. Когнитивная деконструкция токсической вины", h1_style))
    story.append(Paragraph("Иррациональная вина при отказе опирается на когнитивные искажения мышления:", body_style))

    data_c = [
        [Paragraph("Иррациональная мысль", box_text_style), Paragraph("Когнитивная ошибка", box_text_style), Paragraph("Рациональная терапевтическая альтернатива", box_text_style)],
        [Paragraph("«Если я откажу, меня бросят и возненавидят».", box_text_style), Paragraph("Катастрофизация, чтение мыслей.", box_text_style), Paragraph("«Зрелые отношения выдерживают отказ; уважение рождается из честности».", box_text_style)],
        [Paragraph("«Отказывать — это эгоистично и бессердечно».", box_text_style), Paragraph("Черно-белое мышление, навешивание ярлыков.", box_text_style), Paragraph("«Забота о своих базовых силах — обязанность взрослого человека».", box_text_style)],
        [Paragraph("«Я должен решать чужие проблемы, если могу».", box_text_style), Paragraph("Иллюзия грандиозного контроля.", box_text_style), Paragraph("«Другие взрослые обладают ресурсами, чтобы справиться со своей жизнью».", box_text_style)]
    ]
    story.append(make_table(data_c, [55*mm, 50*mm, 75*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум рефрейминга личных когнитивных искажений", h2_style))
    story.append(make_box([
        Paragraph("<b>Моя автоматическая мысль-обвинитель:</b> __________________________________________________________<br/>"
                  "<b>В чем логическая ошибка:</b> __________________________________________________________________________<br/>"
                  "<b>Мой новый рациональный ответ:</b> ____________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Модуль 3. Технологии экологичной конфронтации и защиты границ", h1_style))
    story.append(Paragraph("Четыре профессиональных метода ассертивного реагирования в сложных диалогах:", body_style))

    data_tech = [
        [Paragraph("Метод", box_text_style), Paragraph("Механизм действия", box_text_style), Paragraph("Пример формулировки", box_text_style)],
        [Paragraph("<b>Заезженная пластинка</b>", box_text_style), Paragraph("Повторение краткого отказа без аргументов и втягивания в спор.", box_text_style), Paragraph("«Я понимаю, но сегодня не смогу. Нет, сегодня не смогу».", box_text_style)],
        [Paragraph("<b>Сэндвич границ</b>", box_text_style), Paragraph("Теплое отношение + ясный отказ + позитивное пожелание.", box_text_style), Paragraph("«Ценю твоё доверие, но эту задачу не возьму. Уверен, ты справишься».", box_text_style)],
        [Paragraph("<b>Туманный ответ</b>", box_text_style), Paragraph("Согласие с частью критики без согласия на уступку.", box_text_style), Paragraph("«Да, ситуация сложная, и тем не менее я не выйду в выходной».", box_text_style)],
        [Paragraph("<b>Тайм-аут</b>", box_text_style), Paragraph("Остановка эмоционального манипулятивного давления.", box_text_style), Paragraph("«Давай вернемся к теме завтра, когда эмоции улягутся».", box_text_style)]
    ]
    story.append(make_table(data_tech, [40*mm, 70*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум отпора манипуляциям", h2_style))
    story.append(make_box([
        Paragraph("<b>Манипуляция (давление на жалость / стыд):</b> _______________________________________________________<br/>"
                  "<b>Мой ассертивный ответ:</b> __________________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Модуль 4. Соматический компас и телесная саморегуляция", h1_style))
    story.append(Paragraph("Тело подает сигналы нарушения границ задолго до включения рационального анализа:", body_style))

    data_som = [
        [Paragraph("Зона тела", box_text_style), Paragraph("Симптом сжатия / Реакция", box_text_style), Paragraph("Психологический смысл сигнала", box_text_style)],
        [Paragraph("<b>Горло и шея</b>", box_text_style), Paragraph("Ком, перехват дыхания, тихий голос.", box_text_style), Paragraph("Подавленный крик протеста, невысказанное «нет».", box_text_style)],
        [Paragraph("<b>Плечи и трапеции</b>", box_text_style), Paragraph("Подъем плеч, мышечный панцирь.", box_text_style), Paragraph("Ощущение тяжести чужой ноши, ожидание критики.", box_text_style)],
        [Paragraph("<b>Диафрагма</b>", box_text_style), Paragraph("Затаивание вдоха, замирание.", box_text_style), Paragraph("Реакция Freeze (замри), страх наказания.", box_text_style)],
        [Paragraph("<b>Живот и таз</b>", box_text_style), Paragraph("Спазм, тошнота, холод внутри.", box_text_style), Paragraph("Сигнал отторжения инвазии чужого присутствия.", box_text_style)]
    ]
    story.append(make_table(data_som, [40*mm, 70*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Соматический протокол центрирования «Земля — Дыхание — Опора»", h2_style))
    story.append(make_box([
        Paragraph("1. Почувствуйте плотный контакт подошв с полом (гравитация и устойчивость).<br/>"
                  "2. Разомкните зубы, опустите плечи, сделайте удлиненный выдох через сомкнутые губы.<br/>"
                  "3. Положите ладонь на живот: «Я в безопасности в границах своего тела прямо сейчас».<br/>"
                  "<b>Мои телесные наблюдения при защите суверенитета:</b> ________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Модуль 5. Градуированная иерархия поведенческих экспериментов", h1_style))
    story.append(Paragraph("Десенсибилизация тревоги отказа через последовательные реальные микродействия:", body_style))

    data_exp = [
        [Paragraph("Уровень", box_text_style), Paragraph("Поведенческий эксперимент", box_text_style), Paragraph("Дискомфорт (0–10)", box_text_style), Paragraph("Дата и статус", box_text_style)],
        [Paragraph("<b>1. Микро</b>", box_text_style), Paragraph("Отказать промоутеру на улице или спам-звонку без оправданий.", box_text_style), Paragraph("2 / 10", box_text_style), Paragraph("[  ] Сделано", box_text_style)],
        [Paragraph("<b>2. Бытовой</b>", box_text_style), Paragraph("Сказать «нет» в кафе на навязывание платных добавок/услуг.", box_text_style), Paragraph("4 / 10", box_text_style), Paragraph("[  ] Сделано", box_text_style)],
        [Paragraph("<b>3. Рабочий</b>", box_text_style), Paragraph("Отклонить несрочную просьбу коллеги («сегодня занят»).", box_text_style), Paragraph("6 / 10", box_text_style), Paragraph("[  ] Сделано", box_text_style)],
        [Paragraph("<b>4. Дружеский</b>", box_text_style), Paragraph("Отказаться от встречи при усталости без выдуманных болезней.", box_text_style), Paragraph("7 / 10", box_text_style), Paragraph("[  ] Сделано", box_text_style)],
        [Paragraph("<b>5. Семейный</b>", box_text_style), Paragraph("Обозначить границу близкому родственнику по непрошеным советам.", box_text_style), Paragraph("9 / 10", box_text_style), Paragraph("[  ] Сделано", box_text_style)]
    ]
    story.append(make_table(data_exp, [30*mm, 85*mm, 35*mm, 30*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Анализ результатов поведенческого эксперимента", h2_style))
    story.append(make_box([
        Paragraph("<b>Какой эксперимент был проведен:</b> ________________________________________________________________<br/>"
                  "<b>Что произошло в реальности (была ли катастрофа):</b> ________________________________________________<br/>"
                  "<b>Главный вывод для укрепления автономии:</b> ________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Модуль 6. 14-дневный трекер внедрения и Персональный кодекс границ", h1_style))
    story.append(Paragraph("Структурированный маршрут формирования устойчивой автономности:", body_style))

    data_m6 = [
        [Paragraph("Период", box_text_style), Paragraph("Терапевтический фокус", box_text_style), Paragraph("Критерий успеха", box_text_style)],
        [Paragraph("<b>Дни 1–4</b>", box_text_style), Paragraph("Пауза перед соглашением на любую просьбу.", box_text_style), Paragraph("Ни одного автоматического «да».", box_text_style)],
        [Paragraph("<b>Дни 5–8</b>", box_text_style), Paragraph("Отказ без длинных оправданий и лжи.", box_text_style), Paragraph("Использование лаконичных формулировок.", box_text_style)],
        [Paragraph("<b>Дни 9–11</b>", box_text_style), Paragraph("Соматическое выдерживание вины.", box_text_style), Paragraph("Снижение тревоги отказа до 3–4 баллов.", box_text_style)],
        [Paragraph("<b>Дни 12–14</b>", box_text_style), Paragraph("Закрепление стандартов в ключевых связях.", box_text_style), Paragraph("Стабильное чувство уважения к себе.", box_text_style)]
    ]
    story.append(make_table(data_m6, [35*mm, 85*mm, 60*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Персональный кодекс суверенной личности", h2_style))
    story.append(make_box([
        Paragraph("1. Я не обязан заслуживать любовь примерным поведением и самопожертвованием.<br/>"
                  "2. Моё тело, силы, личные финансы и время неприкосновенны.<br/>"
                  "3. Недовольство другого человека моим отказом — это естественная реакция, с которой он справится.<br/>"
                  "4. Я сохраняю доброжелательность к людям, одновременно оставаясь преданным себе.", box_text_style),
    ], bg=colors.HexColor('#f0fdf4'), border_color=colors.HexColor('#166534')))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Заключительное терапевтическое обязательство", h2_style))
    story.append(make_box([
        Paragraph("Я принимаю ответственность за свои границы и обязуюсь беречь свой суверенитет.<br/>"
                  "Дата: «____» ____________ 202__ г. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Подпись: ______________________", box_text_style)
    ]))

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
    story.append(Paragraph("УРОВЕНЬ 3 • КЛИНИЧЕСКОЕ РУКОВОДСТВО: СУВЕРЕНИТЕТ Я", title_style))
    story.append(Paragraph("Клинический альянс, схема-терапия дезадаптации и сепарация личности (8 сессий)", subtitle_style))
    story.append(Paragraph("Раздел 1. Концептуализация случая: Семейный генезис нарушений границ", h1_style))
    story.append(Paragraph("Деструкция автономии формируется в раннем детстве при подавлении субъектности ребенка:", body_style))

    data_p1 = [
        [Paragraph("Родительский паттерн", box_text_style), Paragraph("Детская интроекция", box_text_style), Paragraph("Взрослый дезадаптивный копинг", box_text_style)],
        [Paragraph("<b>Инвазивный контроль</b> (чтение личных дневников, вход без стука).", box_text_style), Paragraph("«У меня нет ничего своего, моё тело и мысли мне не принадлежат».", box_text_style), Paragraph("Утрата ощущения личного пространства, уязвимость к насилию.", box_text_style)],
        [Paragraph("<b>Условное принятие</b> («любим, только пока ты послушен и успешен»).", box_text_style), Paragraph("«Если я откажу или проявлю злость — меня разлюбят и бросят».", box_text_style), Paragraph("Хроническое угождение, подавление собственного голоса.", box_text_style)],
        [Paragraph("<b>Парентификация</b> (ребенок как контейнер для родительских бед).", box_text_style), Paragraph("«Я обязан спасать взрослых, их счастье — моя вина».", box_text_style), Paragraph("Гиперответственность за окружающих, пренебрежение собой.", box_text_style)]
    ]
    story.append(make_table(data_p1, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Клинический анамнез ранних предписаний", h2_style))
    story.append(make_box([
        Paragraph("<b>Ключевые директивы семьи («Не будь собой», «Не чувствуй», «Радуй других»):</b><br/>"
                  "____________________________________________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 2. Схема-терапевтический профиль автономии (Дж. Янг)", h1_style))
    story.append(Paragraph("Ранние дезадаптивные схемы сферы автономии и нарушенных границ:", body_style))

    data_p2 = [
        [Paragraph("Ранняя схема", box_text_style), Paragraph("Ядерное дисфункциональное убеждение", box_text_style), Paragraph("Поведение при триггере", box_text_style)],
        [Paragraph("<b>Подчинение (Subjugation)</b>", box_text_style), Paragraph("«Мои желания ничего не значат; если я не подчинюсь, последует наказание».", box_text_style), Paragraph("Автоматическая капитуляция перед авторитетами, пассивность.", box_text_style)],
        [Paragraph("<b>Самопожертвование (Self-Sacrifice)</b>", box_text_style), Paragraph("«Я обязан добровольно спасать других ценой собственного здоровья».", box_text_style), Paragraph("Хроническая перегрузка, токсическая вина за отдых.", box_text_style)],
        [Paragraph("<b>Слияние (Enmeshment)</b>", box_text_style), Paragraph("«Без одобрения близких я не существую; границы разрушают связь».", box_text_style), Paragraph("Неспособность к независимым решениям, страх автономии.", box_text_style)]
    ]
    story.append(make_table(data_p2, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Анализ активации ведущей схемы клиента", h2_style))
    story.append(make_box([
        Paragraph("<b>Доминирующая схема в отношениях:</b> ____________________________________________________________<br/>"
                  "<b>Копинг-реакция (капитуляция / избегание / гиперкомпенсация):</b> ___________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 3. Внутренние режимы: Критик, Уязвимый Ребенок и Взрослый", h1_style))
    story.append(Paragraph("Дифференциация режимов функционирования эго при защите границ:", body_style))

    data_p3 = [
        [Paragraph("Режим эго", box_text_style), Paragraph("Характерные проявления", box_text_style), Paragraph("Терапевтическая интервенция", box_text_style)],
        [Paragraph("<b>Карающий Критик</b>", box_text_style), Paragraph("«Ты эгоист! Ты разрушаешь отношения! Как не стыдно!».", box_text_style), Paragraph("Конфронтация и ограничение его влияния Здоровым Взрослым.", box_text_style)],
        [Paragraph("<b>Уязвимый Ребенок</b>", box_text_style), Paragraph("Ужас отвержения, страх наказания, ощущение беспомощности.", box_text_style), Paragraph("Эмоциональное валидирование, защита и утешение.", box_text_style)],
        [Paragraph("<b>Покорный Капитулянт</b>", box_text_style), Paragraph("Привычка соглашаться, улыбаться сквозь зубы, терпеть.", box_text_style), Paragraph("Обучение распознаванию гнева и безопасному отказу.", box_text_style)],
        [Paragraph("<b>Здоровый Взрослый</b>", box_text_style), Paragraph("Спокойная уверенность, уважение к себе и другому, твердость.", box_text_style), Paragraph("Укрепление руководящей роли во всех контактах.", box_text_style)]
    ]
    story.append(make_table(data_p3, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум разотождествления с Карающим Критиком", h2_style))
    story.append(make_box([
        Paragraph("<b>Атакующая фраза Критика:</b> ________________________________________________________________________<br/>"
                  "<b>Ответ Здорового Взрослого:</b> ______________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Раздел 4. Терапевтическая работа с токсической виной и злостью", h1_style))
    story.append(Paragraph("Гнев — это здоровая защитная энергия суверенитета. Подавленный гнев порождает аутоагрессию:", body_style))

    data_p4 = [
        [Paragraph("Паттерн реакции", box_text_style), Paragraph("Психосоматическое проявление", box_text_style), Paragraph("Ассертивная трансформация", box_text_style)],
        [Paragraph("<b>Подавление злости</b>", box_text_style), Paragraph("Хронические мышечные зажимы, мигрени, апатия, бессилие.", box_text_style), Paragraph("«Я разрешаю себе чувствовать раздражение, когда нарушают мои границы».", box_text_style)],
        [Paragraph("<b>Токсическая вина</b>", box_text_style), Paragraph("Бессонница, бесконечное мысленное самобичевание, тревога.", box_text_style), Paragraph("«Мой отказ — это нормальное ограничение, а не преступление».", box_text_style)],
        [Paragraph("<b>Пассивная агрессия</b>", box_text_style), Paragraph("Сарказм, саботаж сроков, намеренное забывание обещаний.", box_text_style), Paragraph("«Прямой спокойный отказ экологичнее скрытого саботажа».", box_text_style)]
    ]
    story.append(make_table(data_p4, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Интерактивная легализация защитного гнева", h2_style))
    story.append(make_box([
        Paragraph("<b>Ситуация, вызывающая скрытое возмущение:</b> ______________________________________________________<br/>"
                  "<b>Ассертивное заявление своей позиции:</b> __________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Раздел 5. Техника диалога субличностей на стульях (Chairwork)", h1_style))
    story.append(Paragraph("Клинический протокол интеграции автономии через работу с тремя позициями:", body_style))

    data_p5 = [
        [Paragraph("Позиция / Стул", box_text_style), Paragraph("Действие и высказывание", box_text_style), Paragraph("Терапевтический фокус", box_text_style)],
        [Paragraph("<b>Стул 1: Внутренний Критик</b>", box_text_style), Paragraph("Голос семейных интроектов: обвиняет в черствости, пугает одиночеством.", box_text_style), Paragraph("Взгляд со стороны вины наружу.", box_text_style)],
        [Paragraph("<b>Стул 2: Уязвимый Ребенок</b>", box_text_style), Paragraph("Озвучивает детский страх отвержения: «Мне страшно, что меня бросят».", box_text_style), Paragraph("Контакт с базовой детской болью.", box_text_style)],
        [Paragraph("<b>Стул 3: Здоровый Взрослый</b>", box_text_style), Paragraph("Встает между Критиком и Ребенком: «Я больше не позволю запугивать эту часть».", box_text_style), Paragraph("Установление внутренней защиты.", box_text_style)]
    ]
    story.append(make_table(data_p5, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Протокол фиксации сессии Chairwork", h2_style))
    story.append(make_box([
        Paragraph("<b>Какие чувства возникли в позиции Здорового Взрослого:</b> _________________________________________<br/>"
                  "<b>Как отреагировал телесный контур (дыхание, осанка):</b> ___________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Раздел 6. Комплексный протокол поведенческих экспериментов in vivo", h1_style))
    story.append(Paragraph("Проверка катастрофических ожиданий клиента в реальных социальных условиях:", body_style))

    data_p6 = [
        [Paragraph("Гипотеза страха", box_text_style), Paragraph("Поведенческий шаг", box_text_style), Paragraph("Фактический исход", box_text_style), Paragraph("Когнитивный сдвиг", box_text_style)],
        [Paragraph("«Если я откажу боссу в переработке — меня уволят».", box_text_style), Paragraph("Вежливый отказ со ссылкой на загрузку.", box_text_style), Paragraph("Руководитель перераспределил задачу.", box_text_style), Paragraph("«Катастрофы нет; руководство уважает загрузку».", box_text_style)],
        [Paragraph("«Если я попрошу не звонить после 21:00 — мама обидится».", box_text_style), Paragraph("Обозначение вечернего времени тишины.", box_text_style), Paragraph("Сначала было удивление, затем принятие.", box_text_style), Paragraph("«Близкие люди могут адаптироваться к правилам».", box_text_style)]
    ]
    story.append(make_table(data_p6, [50*mm, 45*mm, 45*mm, 40*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Проектирование индивидуального эксперимента клиента", h2_style))
    story.append(make_box([
        Paragraph("<b>Какую границу я протестирую на практике:</b> _______________________________________________________<br/>"
                  "<b>Катастрофический прогноз моего Критика:</b> _______________________________________________________<br/>"
                  "<b>Фактический результат и новый опыт:</b> ___________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 7
    story.append(Paragraph("Раздел 7. Дорожная карта терапевтического альянса на 8 сессий", h1_style))
    story.append(Paragraph("План систематической работы психолога и клиента по формированию автономности:", body_style))

    data_p7 = [
        [Paragraph("Сессия", box_text_style), Paragraph("Терапевтический фокус и интервенции", box_text_style), Paragraph("Критерий терапевтического сдвига", box_text_style)],
        [Paragraph("<b>Сессии 1–2</b>", box_text_style), Paragraph("Анамнез семьи, концептуализация деструктивных сценариев границ.", box_text_style), Paragraph("Осознание корней вины без самобичевания.", box_text_style)],
        [Paragraph("<b>Сессии 3–4</b>", box_text_style), Paragraph("Схема-терапия: выявление схем Подчинения и режимов Критика.", box_text_style), Paragraph("Разотождествление с чужими интроектами.", box_text_style)],
        [Paragraph("<b>Сессии 5–6</b>", box_text_style), Paragraph("Экспериенциальная работа (Chairwork), легализация защитного гнева.", box_text_style), Paragraph("Уверенная позиция защиты Уязвимого Ребенка.", box_text_style)],
        [Paragraph("<b>Сессии 7–8</b>", box_text_style), Paragraph("Поведенческие эксперименты, профилактика рецидивов, автономия.", box_text_style), Paragraph("Интегрированный навык твердого экологичного отказа.", box_text_style)]
    ]
    story.append(make_table(data_p7, [30*mm, 85*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Заметки для психолога и клиента", h2_style))
    story.append(make_box([
        Paragraph("<b>Ключевой фокус ближайшей терапевтической встречи:</b> ____________________________________________<br/>"
                  "<b>Домашнее задание между сессиями:</b> ______________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 8
    story.append(Paragraph("Раздел 8. Долгосрочный контракт суверенности и профилактика срывов", h1_style))
    story.append(Paragraph("Формирование устойчивой автономности и готовность к триггерным ситуациям:", body_style))

    data_p8 = [
        [Paragraph("Триггер рецидива спасательства", box_text_style), Paragraph("План превентивных мер Здорового Взрослого", box_text_style)],
        [Paragraph("Сильная усталость, упадок сил.", box_text_style), Paragraph("Брать паузу 24 часа перед любыми обязательствами.", box_text_style)],
        [Paragraph("Слезы или обида близкого человека.", box_text_style), Paragraph("Валидировать чувства другого, но не отменять свой отказ.", box_text_style)],
        [Paragraph("Давление со стороны авторитетного лица.", box_text_style), Paragraph("Опираться на заезженную пластинку и соматическое центрирование.", box_text_style)]
    ]
    story.append(make_table(data_p8, [70*mm, 110*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Терапевтический манифест суверенности личности", h2_style))
    story.append(make_box([
        Paragraph("<b>ДЕКЛАРАЦИЯ НЕОТЪЕМЛЕМОГО СУВЕРЕНИТЕТА</b><br/>"
                  "Я признаю, что моя личность, здоровье, время и силы принадлежат мне по праву рождения. Я выдерживаю чужое несогласие и выбираю искренность вместо разрушительного угодничества.<br/><br/>"
                  "Клиент: __________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Терапевт: __________________________<br/>"
                  "Дата заключения контракта: «____» ____________ 202__ г.", box_text_style),
    ], bg=colors.HexColor('#f0fdf4'), border_color=colors.HexColor('#166534')))

    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == '__main__':
    build_l1('therapy-workbooks/workbook_1_express_no.pdf')
    print("SUCCESS: Boundaries L1 (3 pages)")

    build_l2('therapy-workbooks/workbook_2_self_mastery.pdf')
    print("SUCCESS: Boundaries L2 (6 pages)")

    build_l3('therapy-workbooks/workbook_3_clinical_alliance.pdf')
    print("SUCCESS: Boundaries L3 (8 pages)")
