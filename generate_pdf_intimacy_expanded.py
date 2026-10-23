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

# Palette for Intimacy: Deep Purple / Violet / Magenta
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_H = 15 * mm
MARGIN_V = 15 * mm
CONTENT_WIDTH = 180 * mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.series_title = "СЕРИЯ 03 • ПРЕОДОЛЕНИЕ ДИСТАНЦИИ И ВОЗРОЖДЕНИЕ БЛИЗОСТИ"
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

PRIMARY = colors.HexColor('#9333ea')
PRIMARY_DARK = colors.HexColor('#7e22ce')
ACCENT = colors.HexColor('#db2777')
BG_LIGHT = colors.HexColor('#faf5ff')
TEXT = colors.HexColor('#0f172a')
TEXT_MUTED = colors.HexColor('#475569')
LINE_COLOR = colors.HexColor('#e9d5ff')
HIGHLIGHT = colors.HexColor('#faf5ff')

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
    story.append(Paragraph("УРОВЕНЬ 1 • ЭКСПРЕСС-ИНТЕНСИВ: РАЗМОРОЗКА БЛИЗОСТИ В ПАРЕ", title_style))
    story.append(Paragraph("3-дневный клинический практикум преодоления бытового отчуждения и возвращения нежности", subtitle_style))
    story.append(Paragraph("Раздел 1. Скрининг дефицита эмоционального и тактильного контакта (10 маркеров)", h1_style))
    story.append(Paragraph("Оцените выраженность признаков бытового охлаждения (0 — нет, 1 — иногда, 2 — часто, 3 — постоянно):", body_style))

    data_m = [
        [Paragraph("Маркер бытовой заморозки", box_text_style), Paragraph("0-1-2-3", box_text_style)],
        [Paragraph("1. Общение свелось исключительно к быту, детям, покупкам и логистике.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("2. Исчезли спонтанные касания мимоходом, нежные объятия и поцелуи.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("3. Параллельные вечера в смартфонах без живого зрительного контакта.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("4. Неловкость или напряжение при долгом взгляде глаза в глаза.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("5. Секс стал редким или воспринимается как утомительная обязанность.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("6. Ощущение «мы живем как хорошие соседи по квартире».", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("7. Страх открыться и показать уязвимость из-за риска равнодушия.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("8. Усталость и апатия при мысли о проявлении романтической инициативы.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("9. Мелкие застарелые обиды, создающие невидимую эмоциональную стену.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("10. Тоска по временам взаимного трепета, флирта и легкой игры.", box_text_style), Paragraph("[   ]", box_text_style)]
    ]
    story.append(make_table(data_m, [155*mm, 25*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 2. Психообразование: Синдром сожительства", h1_style))
    story.append(make_box([
        Paragraph("<b>Клинический принцип:</b> Близость не исчезает сама по себе — её вытесняет рутинный автопилот. Прикосновение — это базовый биологический проводник окситоцина и безопасности. Чтобы вернуть страсть, нужно снять груз ожиданий и вернуть телу право на неторопливую нежность.", box_text_style)
    ]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<b>Интерпретация:</b> 0–9: теплота сохранена; 10–19: фаза сожительства (нужна перезагрузка); 20–30: глубокое отчуждение.", body_style))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 3. 4-шаговый протокол нежного контакта «EYE-BREATHE-TOUCH»", h1_style))
    story.append(Paragraph("Практикуйте несексуализированный телесный контакт для снятия напряжения:", body_style))

    data_proto = [
        [Paragraph("Шаг", box_text_style), Paragraph("Психологический смысл", box_text_style), Paragraph("Практическое упражнение", box_text_style)],
        [Paragraph("<b>1. Взгляд</b>", box_text_style), Paragraph("Встреча двух людей без экранов и суеты.", box_text_style), Paragraph("Смотреть друг другу в глаза молча 60 секунд с доброй улыбкой.", box_text_style)],
        [Paragraph("<b>2. Дыхание</b>", box_text_style), Paragraph("Сонастройка вегетативной нервной системы.", box_text_style), Paragraph("Положить руку на грудь партнера и сделать 5 синхронных выдохов.", box_text_style)],
        [Paragraph("<b>3. Объятие</b>", box_text_style), Paragraph("Окситоциновый выброс безопасности.", box_text_style), Paragraph("Объятие «сердце к сердцу» 30–60 секунд, опираясь весом тела.", box_text_style)],
        [Paragraph("<b>4. Слово</b>", box_text_style), Paragraph("Вербальное подтверждение связи.", box_text_style), Paragraph("«Я так рад(а), что мы вместе сегодня».", box_text_style)]
    ]
    story.append(make_table(data_proto, [35*mm, 65*mm, 80*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 4. Меню ежедневных микроритуалов нежности", h1_style))
    story.append(Paragraph("• <b>6-секундный поцелуй:</b> Достаточное время для выброса гормонов привязанности при встрече/прощании.", bullet_style))
    story.append(Paragraph("• <b>Чайная пауза:</b> 10 минут совместного чаепития без смартфонов и новостей.", bullet_style))
    story.append(Paragraph("• <b>Массаж стоп/плеч:</b> Бережная забота без обязательства сексуального продолжения.", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 5. Практикум выбора микроритуала", h1_style))
    story.append(make_box([
        Paragraph("<b>Какой ритуал мы выбираем на сегодня:</b> ___________________________________________________________<br/>"
                  "<b>Наше согласованное время дня:</b> __________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 6. 3-дневный трекер возрождения тепла", h1_style))
    story.append(Paragraph("Фиксируйте микромоменты живого контакта в течение ближайших 3 дней:", body_style))

    data_track = [
        [Paragraph("День", box_text_style), Paragraph("Микродействие близости", box_text_style), Paragraph("Телесный отклик и ощущения", box_text_style), Paragraph("Уровень тепла (0–10)", box_text_style)],
        [Paragraph("<b>День 1</b>", box_text_style), Paragraph("6-секундный поцелуй...", box_text_style), Paragraph("Сначала смущение, потом улыбка...", box_text_style), Paragraph("7 / 10", box_text_style)],
        [Paragraph("<b>День 2</b>", box_text_style), Paragraph("Объятие 1 минуту...", box_text_style), Paragraph("Глубокий вздох, ушла суета...", box_text_style), Paragraph("8 / 10", box_text_style)],
        [Paragraph("<b>День 3</b>", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style)]
    ]
    story.append(make_table(data_track, [25*mm, 60*mm, 55*mm, 40*mm], bg_hdr=PRIMARY_DARK, is_compact=False))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 7. Терапевтический манифест доступности", h1_style))
    story.append(make_box([
        Paragraph("<b>Мы выбираем быть живыми друг для друга:</b><br/>"
                  "1. Прикосновение — это базовый язык любви и поддержки, а не только прелюдия к сексу.<br/>"
                  "2. Мы имеем право делиться сокровенным без страха критики или насмешки.<br/>"
                  "3. Близость создается нашими ежедневными маленькими шагами внимания.", box_text_style),
    ], bg=colors.HexColor('#faf5ff'), border_color=colors.HexColor('#7e22ce')))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 8. Пакт нежности в союзе", h1_style))
    story.append(make_box([
        Paragraph("Мы обязуемся беречь эмоциональный и тактильный мост нашей пары.<br/>"
                  "Партнер 1: ________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Партнер 2: ________________________<br/>"
                  "Дата: «____» ____________ 202__ г.", box_text_style)
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
    story.append(Paragraph("УРОВЕНЬ 2 • ПРАКТИКУМ: ТЕРРИТОРИЯ НЕЖНОСТИ", title_style))
    story.append(Paragraph("14-дневная программа чувственной сонастройки, доверия и преодоления тревоги", subtitle_style))
    story.append(Paragraph("Модуль 1. Карта пяти проводников близости пары", h1_style))
    story.append(Paragraph("Исследуйте субъективную иерархию языков интимности от 1 (мало) до 5 (жизненно важно):", body_style))

    data_l = [
        [Paragraph("Язык близости", box_text_style), Paragraph("Проявление в поведении", box_text_style), Paragraph("Партнер 1", box_text_style), Paragraph("Партнер 2", box_text_style)],
        [Paragraph("<b>1. Тактильный</b>", box_text_style), Paragraph("Поглаживания, объятия, массаж, касания мимоходом.", box_text_style), Paragraph("[  / 5]", box_text_style), Paragraph("[  / 5]", box_text_style)],
        [Paragraph("<b>2. Эмоциональный</b>", box_text_style), Paragraph("Искренние разговоры по душам о чувствах и страхах.", box_text_style), Paragraph("[  / 5]", box_text_style), Paragraph("[  / 5]", box_text_style)],
        [Paragraph("<b>3. Интеллектуальный</b>", box_text_style), Paragraph("Общие идеи, книги, дискуссии, совместные планы.", box_text_style), Paragraph("[  / 5]", box_text_style), Paragraph("[  / 5]", box_text_style)],
        [Paragraph("<b>4. Деятельностный</b>", box_text_style), Paragraph("Спорт, прогулки, путешествия, совместный досуг.", box_text_style), Paragraph("[  / 5]", box_text_style), Paragraph("[  / 5]", box_text_style)],
        [Paragraph("<b>5. Эротический</b>", box_text_style), Paragraph("Страсть, чувственная игра, взаимное влечение.", box_text_style), Paragraph("[  / 5]", box_text_style), Paragraph("[  / 5]", box_text_style)]
    ]
    story.append(make_table(data_l, [40*mm, 90*mm, 25*mm, 25*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Анализ профилей пары", h2_style))
    story.append(make_box([
        Paragraph("<b>Где наши потребности совпадают:</b> ________________________________________________________________<br/>"
                  "<b>В чем главное отличие и зона роста:</b> ___________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Модуль 2. Сенсорная фокусировка: Фаза I (Мастерс и Джонсон)", h1_style))
    story.append(Paragraph("Снятие тревоги сексуальной продуктивности через временный запрет на секс:", body_style))

    data_m2 = [
        [Paragraph("Правило протокола", box_text_style), Paragraph("Клиническая цель", box_text_style)],
        [Paragraph("<b>Категорическое табу на генитальный контакт</b>", box_text_style), Paragraph("Снимает синдром ожидания неудачи и страх «обязанности возбудиться».", box_text_style)],
        [Paragraph("<b>Разделение ролей Дающего и Принимающего</b>", box_text_style), Paragraph("Позволяет полностью погрузиться в ощущения без мыслей о взаимности.", box_text_style)],
        [Paragraph("<b>Фокус на текстурах, тепле и дыхании</b>", box_text_style), Paragraph("Переводит мозг из тревожного контроля в чистое чувственное восприятие.", box_text_style)]
    ]
    story.append(make_table(data_m2, [75*mm, 105*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Заметки после сеанса негенитального массажа", h2_style))
    story.append(make_box([
        Paragraph("<b>Ощущения Дающего (было ли трудно не спешить):</b> _________________________________________________<br/>"
                  "<b>Ощущения Принимающего (удалось ли отпустить мысли):</b> ____________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Модуль 3. Эмоциональное раздевание: глубокие уязвимые беседы", h1_style))
    story.append(Paragraph("Истинное влечение рождается там, где встречаются две открытые души:", body_style))

    story.append(Paragraph("• 1. «В какие моменты ты чувствуешь себя рядом со мной в абсолютной безопасности?»", bullet_style))
    story.append(Paragraph("• 2. «Какой детский страх до сих пор иногда поднимается в наших отношениях?»", bullet_style))
    story.append(Paragraph("• 3. «О каком проявлении нежности ты мечтаешь, но стесняешься попросить?»", bullet_style))
    story.append(Paragraph("• 4. «Что в нашей интимной истории ты вспоминаешь с самым сильным трепетом?»", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Интерактивный отклик пары", h2_style))
    story.append(make_box([
        Paragraph("<b>Главное открытие сегодняшнего доверительного разговора:</b> ________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Модуль 4. Преодоление сексуальной тревоги и зрительского синдрома", h1_style))
    story.append(Paragraph("Зрительский синдром (наблюдение за собой со стороны) блокирует спонтанность оргазма:", body_style))

    data_m4 = [
        [Paragraph("Симптом наблюдателя", box_text_style), Paragraph("Психологический барьер", box_text_style), Paragraph("Телесный соматический якорь", box_text_style)],
        [Paragraph("Оценка своего тела в постели.", box_text_style), Paragraph("Телесный стыд, страх критики.", box_text_style), Paragraph("Закрыть глаза, ощутить тепло ладоней партнера.", box_text_style)],
        [Paragraph("Контроль наступления оргазма.", box_text_style), Paragraph("Перфекционизм результата.", box_text_style), Paragraph("Медленный выдох через рот, фокус на процессе.", box_text_style)],
        [Paragraph("Спешка и мышечные зажимы.", box_text_style), Paragraph("Страх разочаровать другого.", box_text_style), Paragraph("Замедлить ласки в 3 раза, контакт дыхания.", box_text_style)]
    ]
    story.append(make_table(data_m4, [50*mm, 60*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум возврата в чувственность", h2_style))
    story.append(make_box([
        Paragraph("<b>Мой персональный соматический якорь (слово / выдох / прикосновение):</b> ___________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Модуль 5. Карта желаний: светофор интимных границ пары", h1_style))
    story.append(Paragraph("Безопасный инструмент согласования сексуальных практик без страха давления:", body_style))

    data_m5 = [
        [Paragraph("Цвет светофора", box_text_style), Paragraph("Значение зоны", box_text_style), Paragraph("Наши согласованные практики", box_text_style)],
        [Paragraph("<b>ЗЕЛЕНЫЙ</b>", box_text_style), Paragraph("Желанно и безопасно для обоих всегда.", box_text_style), Paragraph("Массаж, поцелуи, объятия, нежные прикосновения.", box_text_style)],
        [Paragraph("<b>ЖЕЛТЫЙ</b>", box_text_style), Paragraph("Интересно попробовать с правом на «стоп».", box_text_style), Paragraph("Новые локации, элементы ролевой игры, белье.", box_text_style)],
        [Paragraph("<b>КРАСНЫЙ</b>", box_text_style), Paragraph("Табу для любого из нас без уговоров.", box_text_style), Paragraph("Все практики, вызывающие дискомфорт или стыд.", box_text_style)]
    ]
    story.append(make_table(data_m5, [35*mm, 65*mm, 80*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Интимное стоп-слово безопасности", h2_style))
    story.append(make_box([
        Paragraph("<b>Наше слово мгновенной паузы в постели:</b> _________________________________________________________<br/>"
                  "<i>Правило: при его звуке ласка немедленно переходит в бережное согревающее объятие.</i>", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Модуль 6. 14-дневный план возрождения страсти и Кодекс пары", h1_style))
    story.append(Paragraph("Пошаговое закрепление устойчивой чувственной близости:", body_style))

    data_m6 = [
        [Paragraph("Период", box_text_style), Paragraph("Фокус практики", box_text_style), Paragraph("Критерий прогресса", box_text_style)],
        [Paragraph("<b>Дни 1–4</b>", box_text_style), Paragraph("Несексуальные прикосновения, поцелуи 6 сек.", box_text_style), Paragraph("Снятие напряжения и суеты.", box_text_style)],
        [Paragraph("<b>Дни 5–8</b>", box_text_style), Paragraph("Сенсорная фокусировка Фазы I при свечах.", box_text_style), Paragraph("Глубокое соматическое расслабление.", box_text_style)],
        [Paragraph("<b>Дни 9–11</b>", box_text_style), Paragraph("Уязвимые вечерние беседы и карта светофора.", box_text_style), Paragraph("Абсолютная безопасность желаний.", box_text_style)],
        [Paragraph("<b>Дни 12–14</b>", box_text_style), Paragraph("Спонтанная чувственная игра без ожиданий.", box_text_style), Paragraph("Возрождение радости и страсти.", box_text_style)]
    ]
    story.append(make_table(data_m6, [35*mm, 85*mm, 60*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Кодекс чувственной бережности союза", h2_style))
    story.append(make_box([
        Paragraph("1. Наше тело ценно само по себе, а не только как инструмент оргазма.<br/>"
                  "2. Мы имеем право на «не сейчас» или «чуть мягче» в любой момент без вины.<br/>"
                  "3. Мы выбираем неторопливость, любопытство и взаимное уважение.<br/>"
                  "4. Мы обязуемся быть чуткими хранителями страсти и тепла в нашем доме.", box_text_style),
    ], bg=colors.HexColor('#faf5ff'), border_color=colors.HexColor('#7e22ce')))

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
    story.append(Paragraph("УРОВЕНЬ 3 • КЛИНИЧЕСКОЕ РУКОВОДСТВО: ЭРОТИЧЕСКИЙ РЕКОННЕКТ", title_style))
    story.append(Paragraph("Клиническая сексология, дифференциация Д. Шнарха и диалектика Э. Перель (8 сессий)", subtitle_style))
    story.append(Paragraph("Раздел 1. Парадокс страсти и безопасности (Эстер Перель)", h1_style))
    story.append(Paragraph("Диалектическое противоречие между стремлением к привязанности и эротическим влечением:", body_style))

    data_p1 = [
        [Paragraph("Полюс привязанности (Любовь)", box_text_style), Paragraph("Полюс эротизма (Страсть)", box_text_style), Paragraph("Зрелая терапевтическая интеграция", box_text_style)],
        [Paragraph("Безопасность, надежность, слияние, предсказуемость.", box_text_style), Paragraph("Тайна, дистанция, влечение к непознанному, свобода.", box_text_style), Paragraph("«Я люблю тебя, но признаю твою суверенную отдельность».", box_text_style)],
        [Paragraph("Бытовые роли мамы и папы, партнерство по хозяйству.", box_text_style), Paragraph("Роли любовников, игра, чувственная дерзость.", box_text_style), Paragraph("Осознанное разграничение родительского и эротического пространств.", box_text_style)]
    ]
    story.append(make_table(data_p1, [55*mm, 55*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Исследование эротической дистанции", h2_style))
    story.append(make_box([
        Paragraph("<b>В какие моменты вы смотрите на партнера со стороны и чувствуете влечение:</b> _________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 2. Дифференциация личности в супружеской постели (Д. Шнарх)", h1_style))
    story.append(Paragraph("Сексуальное горнило брака: секс как глубочайшее испытание зрелости эго:", body_style))

    data_p2 = [
        [Paragraph("Уровень дифференциации", box_text_style), Paragraph("Реакция на отказ партнера", box_text_style), Paragraph("Внутреннее переживание", box_text_style)],
        [Paragraph("<b>Низкая (слияние)</b>", box_text_style), Paragraph("Обида, уход в молчание, злость: «Ты меня разлюбил(а)!».", box_text_style), Paragraph("Разрушение самооценки, паника отвержения.", box_text_style)],
        [Paragraph("<b>Высокая (зрелость)</b>", box_text_style), Paragraph("Спокойное принятие: «Я слышу твою усталость, отдохни».", box_text_style), Paragraph("Сохранение внутренней устойчивости и привлекательности.", box_text_style)]
    ]
    story.append(make_table(data_p2, [45*mm, 70*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Самодиагностика дифференциации пары", h2_style))
    story.append(make_box([
        Paragraph("<b>Насколько свободно каждый из нас переносит отказ без обид (0–10):</b> _______________________________<br/>"
                  "<b>Что помогает сохранять устойчивость:</b> ___________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 3. Сенсорная фокусировка: Фаза II (Генитальная ласка без оргазма)", h1_style))
    story.append(Paragraph("Клинический переход к исследованию интимных зон в контексте нежности и расслабления:", body_style))

    data_p3 = [
        [Paragraph("Шаг Фазы II", box_text_style), Paragraph("Терапевтический фокус", box_text_style), Paragraph("Инструкция для пары", box_text_style)],
        [Paragraph("<b>1. Включение интимных зон</b>", box_text_style), Paragraph("Снятие табу и стыда прикосновения.", box_text_style), Paragraph("Ласка всего тела, включая гениталии, мягкими касаниями.", box_text_style)],
        [Paragraph("<b>2. Запрет на оргазм</b>", box_text_style), Paragraph("Исключение целеполагания и спешки.", box_text_style), Paragraph("Не форсировать разрядку; дышать синхронно в момент возбуждения.", box_text_style)],
        [Paragraph("<b>3. Коррекция ладони</b>", box_text_style), Paragraph("Обучение точной обратной связи.", box_text_style), Paragraph("Принимающий мягко направляет руку партнера своей рукой.", box_text_style)]
    ]
    story.append(make_table(data_p3, [45*mm, 65*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Протокол фиксации сессии Фазы II", h2_style))
    story.append(make_box([
        Paragraph("<b>Главные соматические открытия (как тело реагировало на неспешность):</b> __________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Раздел 4. Преодоление сексуальных дисфункций и синдрома СТОСН", h1_style))
    story.append(Paragraph("Психотерапевтический протокол работы с тревогой ожидания сексуальной неудачи:", body_style))

    data_p4 = [
        [Paragraph("Дисфункция / Симптом", box_text_style), Paragraph("Психосоматический механизм", box_text_style), Paragraph("Клинический протокол помощи", box_text_style)],
        [Paragraph("Утрата эрекции / вазоконстрикция.", box_text_style), Paragraph("Адреналиновый всплеск тревоги блокирует парасимпатику.", box_text_style), Paragraph("Легализация паузы: прекратить движения, лечь рядом, глубокий выдох.", box_text_style)],
        [Paragraph("Аноргазмия / задержка эякуляции.", box_text_style), Paragraph("Зрительский синдром, гиперконтроль сознания.", box_text_style), Paragraph("Фокус на тактильном контакте кожи и звуках без ожидания оргазма.", box_text_style)]
    ]
    story.append(make_table(data_p4, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Партнерский протокол снятия тревоги", h2_style))
    story.append(make_box([
        Paragraph("<b>Слова партнера, мгновенно снимающие стыд и напряжение в спальне:</b> ______________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Раздел 5. Архитектура эротического пространства и тайны", h1_style))
    story.append(Paragraph("Создание границ между бытом семьи и священным пространством любовников:", body_style))

    data_p5 = [
        [Paragraph("Элемент среды", box_text_style), Paragraph("Бытовое загрязнение (Минус)", box_text_style), Paragraph("Эротическое святилище (Плюс)", box_text_style)],
        [Paragraph("<b>Постель и спальня</b>", box_text_style), Paragraph("Ноутбуки, счета, детские игрушки, работа.", box_text_style), Paragraph("Только сон, нежность, тишина и отдых.", box_text_style)],
        [Paragraph("<b>Сенсорный фон</b>", box_text_style), Paragraph("Яркий верхний свет, телевизор, шум.", box_text_style), Paragraph("Теплые свечи, приглушенный полумрак, ароматы.", box_text_style)],
        [Paragraph("<b>Индивидуация</b>", box_text_style), Paragraph("Слияние 24/7, отсутствие личных увлечений.", box_text_style), Paragraph("Личное время, возвращающее тайну и притяжение.", box_text_style)]
    ]
    story.append(make_table(data_p5, [40*mm, 70*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("План обустройства чувственного пространства", h2_style))
    story.append(make_box([
        Paragraph("<b>Конкретные шаги по очищению нашей спальни от быта:</b> ____________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Раздел 6. Интеграция эротических фантазий и взаимная безопасность", h1_style))
    story.append(Paragraph("Фантазия как язык бессознательного: интеграция желаний без страха осуждения:", body_style))

    data_p6 = [
        [Paragraph("Правило шеринга фантазий", box_text_style), Paragraph("Терапевтическое значение", box_text_style)],
        [Paragraph("<b>Абсолютная безоценочность и благодарность</b>", box_text_style), Paragraph("Создает ощущение тотального принятия сокровенных сторон личности.", box_text_style)],
        [Paragraph("<b>Фантазия не равна обязательному действию</b>", box_text_style), Paragraph("Снимает тревогу партнера: делиться образом безопасно.", box_text_style)],
        [Paragraph("<b>Сверка с картой светофора</b>", box_text_style), Paragraph("Гарантирует неприкосновенность границ обоих супругов.", box_text_style)]
    ]
    story.append(make_table(data_p6, [75*mm, 105*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум доверительного раскрытия", h2_style))
    story.append(make_box([
        Paragraph("<b>Образ или желание, озвученное в доверительном пространстве:</b> ___________________________________<br/>"
                  "<b>Благодарный поддерживающий ответ партнера:</b> ___________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 7
    story.append(Paragraph("Раздел 7. Дорожная карта сексологической терапии на 8 сессий", h1_style))
    story.append(Paragraph("Клинический план ведения пары по возрождению эротической витальности:", body_style))

    data_p7 = [
        [Paragraph("Сессии", box_text_style), Paragraph("Терапевтический фокус", box_text_style), Paragraph("Критерий прогресса", box_text_style)],
        [Paragraph("<b>Сессии 1–2</b>", box_text_style), Paragraph("Анамнез интимной истории, снятие вины за охлаждение влечения.", box_text_style), Paragraph("Нормализация кризиса дистанции.", box_text_style)],
        [Paragraph("<b>Сессии 3–4</b>", box_text_style), Paragraph("Сенсорная фокусировка Мастерс и Джонсон, снятие СТОСН.", box_text_style), Paragraph("Свободный контакт без тревоги.", box_text_style)],
        [Paragraph("<b>Сессии 5–6</b>", box_text_style), Paragraph("Дифференциация эротизма и родительства, шеринг фантазий.", box_text_style), Paragraph("Возрождение искры и флирта.", box_text_style)],
        [Paragraph("<b>Сессии 7–8</b>", box_text_style), Paragraph("Интеграция страсти и надежной привязанности, ритуалы огня.", box_text_style), Paragraph("Долгосрочная интимная гармония.", box_text_style)]
    ]
    story.append(make_table(data_p7, [30*mm, 85*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Заметки терапевтического союза", h2_style))
    story.append(make_box([
        Paragraph("<b>Главные достижения в раскрепощении и контакте:</b> ________________________________________________<br/>"
                  "<b>Индивидуальный вектор развития чувственности:</b> ________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 8
    story.append(Paragraph("Раздел 8. Долгосрочный эротический контракт и ритуалы страсти", h1_style))
    story.append(Paragraph("Опоры поддержания сексуальной витальности на годы совместной жизни:", body_style))

    data_p8 = [
        [Paragraph("Принцип долгосрочной страсти", box_text_style), Paragraph("Конкретное супружеское правило", box_text_style)],
        [Paragraph("<b>Регулярные свидания вдвоем</b>", box_text_style), Paragraph("Минимум раз в две недели выход в свет без детей и бытовых тем.", box_text_style)],
        [Paragraph("<b>Культура нежности в быту</b>", box_text_style), Paragraph("Ежедневные 6-секундные поцелуи и согревающие объятия.", box_text_style)],
        [Paragraph("<b>Право на автономию</b>", box_text_style), Paragraph("Уважение личных границ и отдельности внутреннего мира партнера.", box_text_style)]
    ]
    story.append(make_table(data_p8, [65*mm, 115*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Супружеский пакт вечной страсти и нежности", h2_style))
    story.append(make_box([
        Paragraph("<b>ДОЛГОСРОЧНЫЙ ЭРОТИЧЕСКИЙ ДОГОВОР</b><br/>"
                  "Мы признаем, что влечение — это живой сад, требующий внимания, игры, бережности и смелости. Мы выбираем оставаться желанными любовниками и преданными друзьями на нашем общем жизненном пути.<br/><br/>"
                  "Партнер 1: __________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Партнер 2: __________________________<br/>"
                  "Дата: «____» ____________ 202__ г.", box_text_style),
    ], bg=colors.HexColor('#faf5ff'), border_color=colors.HexColor('#7e22ce')))

    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == '__main__':
    build_l1('therapy-workbooks/intimacy_workbook_1_unfreeze.pdf')
    print("SUCCESS: Intimacy L1 (3 pages)")

    build_l2('therapy-workbooks/intimacy_workbook_2_tenderness.pdf')
    print("SUCCESS: Intimacy L2 (6 pages)")

    build_l3('therapy-workbooks/intimacy_workbook_3_reconnection.pdf')
    print("SUCCESS: Intimacy L3 (8 pages)")
