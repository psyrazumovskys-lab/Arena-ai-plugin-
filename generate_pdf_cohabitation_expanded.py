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

# Palette for Cohabitation & Home Harmony: Warm Emerald / Sage / Amber
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_H = 15 * mm
MARGIN_V = 15 * mm
CONTENT_WIDTH = 180 * mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.series_title = "СЕРИЯ 05 • МОЛОДАЯ ПАРА: АРХИТЕКТУРА БЫТА И РОМАНТИКА"
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

PRIMARY = colors.HexColor('#0284c7')
PRIMARY_DARK = colors.HexColor('#0369a1')
ACCENT = colors.HexColor('#ea580c')
BG_LIGHT = colors.HexColor('#f0f9ff')
TEXT = colors.HexColor('#0f172a')
TEXT_MUTED = colors.HexColor('#475569')
LINE_COLOR = colors.HexColor('#bae6fd')
HIGHLIGHT = colors.HexColor('#f0f9ff')

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
    story.append(Paragraph("УРОВЕНЬ 1 • ЭКСПРЕСС-ИНТЕНСИВ: СЪЕХАЛИСЬ", title_style))
    story.append(Paragraph("Экспресс-адаптация под одной крышей, синхронизация привычек и сохранение романтики", subtitle_style))
    story.append(Paragraph("Раздел 1. Чек-лист 10 скрытых бытовых мин", h1_style))
    story.append(Paragraph("Оцените уровень бытового трения в паре от 0 (не беспокоит) до 3 (постоянный триггер):", body_style))

    data_m = [
        [Paragraph("Бытовой триггер напряжения", box_text_style), Paragraph("0-1-2-3", box_text_style)],
        [Paragraph("1. Разбросанная одежда, вещи не на своих местах, открытые дверцы.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("2. Посуда в раковине («помыть сразу» vs «пусть постоит до утра»).", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("3. Несовпадающие биоритмы («сова» не спит, «жаворонок» встает ни свет ни заря).", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("4. Разные стандарты чистоты поверхностей и частоты мытья полов.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("5. Невидимый быт (кто помнит про покупку бытовой химии, мусор и оплату счетов).", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("6. Удаленная работа в одной квартире (шум от созвонов, сбитый фокус).", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("7. Внезапные гости и родственники без согласования с партнером.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("8. Нехватка личного пространства и невозможность побыть в одиночестве.", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("9. Туалетный стыд и гигиенические неловкости (запахи, открытые двери).", box_text_style), Paragraph("[   ]", box_text_style)],
        [Paragraph("10. Пропажа романтики: пара в трениках 24/7, свидания исчезли.", box_text_style), Paragraph("[   ]", box_text_style)]
    ]
    story.append(make_table(data_m, [155*mm, 25*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 2. Психообразование: Закон двух культур", h1_style))
    story.append(make_box([
        Paragraph("<b>Главный закон адаптации:</b> Бытовое трение — это не признак несовместимости, а закономерная притирка двух разных семейных укладов. Носок на полу — это просто носок, а не тайный знак обесценивания. Задача первого года — выработать свои собственные правила дома.", box_text_style)
    ]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("<b>Интерпретация:</b> 0–9: легкая притирка; 10–19: накопление невысказанных обид; 20–30: острый бытовой кризис сожительства.", body_style))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 3. 4-шаговый протокол экологичной бытовой просьбы", h1_style))
    story.append(Paragraph("Откажитесь от демонстративных вздохов и сарказма в пользу чистого алгоритма:", body_style))

    data_proto = [
        [Paragraph("Шаг", box_text_style), Paragraph("Психологическая задача", box_text_style), Paragraph("Речевая формула", box_text_style)],
        [Paragraph("<b>1. Факт</b>", box_text_style), Paragraph("Описать действие без слов «вечно» и «никогда».", box_text_style), Paragraph("«На столе осталась посуда после ужина...»", box_text_style)],
        [Paragraph("<b>2. Чувство</b>", box_text_style), Paragraph("Озвучить своё состояние через «Я-послание».", box_text_style), Paragraph("«...я сильно устал(а) сегодня и мне тяжело убирать одному(ой)...»", box_text_style)],
        [Paragraph("<b>3. Просьба</b>", box_text_style), Paragraph("Назвать конкретное действие со сроком.", box_text_style), Paragraph("«...пожалуйста, помой тарелки до того, как мы пойдем спать».", box_text_style)],
        [Paragraph("<b>4. Тепло</b>", box_text_style), Paragraph("Подкрепить союз благодарностью.", box_text_style), Paragraph("«Для меня это будет огромной заботой, спасибо тебе».", box_text_style)]
    ]
    story.append(make_table(data_proto, [35*mm, 65*mm, 80*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 4. Правила сохранения уюта в быту", h1_style))
    story.append(Paragraph("• <b>Никаких мыслей на расстоянии:</b> Не ждите догадок — говорите прямо и мягко.", bullet_style))
    story.append(Paragraph("• <b>Табу на критику качества:</b> Если партнер взялся за дело, не критикуйте его способ.", bullet_style))
    story.append(Paragraph("• <b>Разделение кухни:</b> Один готовит — второй убирает со стола (баланс сил).", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 5. Практикум перевода претензии", h1_style))
    story.append(make_box([
        Paragraph("<b>Бытовая мелочь, вызывающая раздражение:</b> ____________________________________________________<br/>"
                  "<b>Моя чистая просьба по 4 шагам:</b> __________________________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 6. 3-дневный трекер сонастройки привычек", h1_style))
    story.append(Paragraph("Фиксируйте микродоговоренности и решения бытовых ситуаций в течение 3 дней:", body_style))

    data_track = [
        [Paragraph("День", box_text_style), Paragraph("Бытовой вопрос", box_text_style), Paragraph("Как решили", box_text_style), Paragraph("Уровень уюта (0–10)", box_text_style)],
        [Paragraph("<b>День 1</b>", box_text_style), Paragraph("Ужин и посуда...", box_text_style), Paragraph("Один готовит, второй моет...", box_text_style), Paragraph("8 / 10", box_text_style)],
        [Paragraph("<b>День 2</b>", box_text_style), Paragraph("Режим сна и свет...", box_text_style), Paragraph("Наушники + ночник...", box_text_style), Paragraph("9 / 10", box_text_style)],
        [Paragraph("<b>День 3</b>", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style), Paragraph("", box_text_style)]
    ]
    story.append(make_table(data_track, [25*mm, 60*mm, 55*mm, 40*mm], bg_hdr=PRIMARY_DARK, is_compact=False))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 7. Домашний манифест молодой пары", h1_style))
    story.append(make_box([
        Paragraph("<b>НАШИ ПРАВИЛА ЖИЗНИ ПОД ОДНОЙ КРЫШЕЙ:</b><br/>"
                  "1. Мы выбираем радость общения превыше стерильного порядка.<br/>"
                  "2. Право на личное время священно: уединение не означает обиду.<br/>"
                  "3. Наш дом — это тихая гавань и убежище, а не казарма с проверками.", box_text_style),
    ], bg=colors.HexColor('#ecfdf5'), border_color=colors.HexColor('#047857')))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Раздел 8. Пакт первого года совместной жизни", h1_style))
    story.append(make_box([
        Paragraph("Мы обязуемся беречь тепло и романтику в нашем общем доме.<br/>"
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
    story.append(Paragraph("УРОВЕНЬ 2 • ПРАКТИКУМ: АРХИТЕКТУРА СОВМЕСТНОГО ДОМА", title_style))
    story.append(Paragraph("14-дневная программа распределения быта, зонирования пространства и спасения романтики", subtitle_style))
    story.append(Paragraph("Модуль 1. Столкновение двух семейных культур", h1_style))
    story.append(Paragraph("Исследуйте родительские сценарии, определяющие ваши бессознательные бытовые ожидания:", body_style))

    data_m1 = [
        [Paragraph("Сфера быта", box_text_style), Paragraph("Уклад в семье Партнера 1", box_text_style), Paragraph("Уклад в семье Партнера 2", box_text_style)],
        [Paragraph("<b>Уборка дома</b>", box_text_style), Paragraph("«Генеральная уборка по субботам, стерильность».", box_text_style), Paragraph("«Уборка по мере загрязнения, творческий хаос».", box_text_style)],
        [Paragraph("<b>Приготовление еды</b>", box_text_style), Paragraph("«Горячее первое и второе каждый день».", box_text_style), Paragraph("«Быстрые перекусы, полуфабрикаты, доставка».", box_text_style)],
        [Paragraph("<b>Гости и друзья</b>", box_text_style), Paragraph("«Дом всегда полон друзей и родственников».", box_text_style), Paragraph("«Крепость только для своих, никаких визитов».", box_text_style)],
        [Paragraph("<b>Траты на быт</b>", box_text_style), Paragraph("«Строгая экономия, учет каждого чека».", box_text_style), Paragraph("«Свободные покупки для комфорта без отчета».", box_text_style)]
    ]
    story.append(make_table(data_m1, [40*mm, 70*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Формирование нашего уникального уклада", h2_style))
    story.append(make_box([
        Paragraph("<b>От какого родительского правила мы сознательно отказываемся:</b> ___________________________________<br/>"
                  "<b>Какое наше собственное правило мы внедряем:</b> __________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Модуль 2. Матрица невидимого труда (Mental Load & Fair Play)", h1_style))
    story.append(Paragraph("Быт состоит из физических действий и мыслительной нагрузки. Закрепите хозяев сфер:", body_style))

    data_m2 = [
        [Paragraph("Бытовой сектор", box_text_style), Paragraph("Невидимая нагрузка (Mental Load)", box_text_style), Paragraph("Ответственный партнер", box_text_style)],
        [Paragraph("<b>Продукты и меню</b>", box_text_style), Paragraph("Ревизия холодильника, составление списка, заказ.", box_text_style), Paragraph("Партнер 1 / Партнер 2", box_text_style)],
        [Paragraph("<b>Посуда и раковина</b>", box_text_style), Paragraph("Посудомойка, таблетки, вынос мусора, раковина.", box_text_style), Paragraph("Партнер 1 / Партнер 2", box_text_style)],
        [Paragraph("<b>Стирка и текстиль</b>", box_text_style), Paragraph("Сортировка, стирка, сушка, глажка, постельное белье.", box_text_style), Paragraph("Партнер 1 / Партнер 2", box_text_style)],
        [Paragraph("<b>ЖКХ и бытовая химия</b>", box_text_style), Paragraph("Оплата счетов, заказ химии, вызов сантехника.", box_text_style), Paragraph("Партнер 1 / Партнер 2", box_text_style)]
    ]
    story.append(make_table(data_m2, [45*mm, 85*mm, 50*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Принцип «Один хозяин задачи»", h2_style))
    story.append(make_box([
        Paragraph("Тот, кто отвечает за сферу, сам решает, когда и как её выполнять. Второй партнер не контролирует и не критикует способ выполнения. Доверие — основа партнерства.", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Модуль 3. Зонирование личного пространства в общем доме", h1_style))
    story.append(Paragraph("Даже в однокомнатной квартире важно иметь автономию и суверенные границы:", body_style))

    story.append(Paragraph("• <b>«Правило наушников»:</b> Надевание наушников — сигнал «я в отдельной комнате, не беспокоить».", bullet_style))
    story.append(Paragraph("• <b>Право на 45 минут тишины:</b> Обязательный декомпрессионный буфер после рабочего дня.", bullet_style))
    story.append(Paragraph("• <b>Неприкосновенный уголок:</b> Личный рабочий стол или кресло, где вещи партнера не трогают.", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Проектирование зон автономии в квартире", h2_style))
    story.append(make_box([
        Paragraph("<b>Зона уединения Партнера 1:</b> ____________________________________________________________________<br/>"
                  "<b>Зона уединения Партнера 2:</b> ____________________________________________________________________<br/>"
                  "<b>Как мы сигнализируем о потребности в тишине:</b> __________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Модуль 4. Преодоление ролей опекуна и обороняющегося", h1_style))
    story.append(Paragraph("Опаснейшая ловушка совместной жизни — регресс в родительско-детскую динамику:", body_style))

    data_m4 = [
        [Paragraph("Ловушка роли", box_text_style), Paragraph("Поведенческий маркер", box_text_style), Paragraph("Взрослый терапевтический выход", box_text_style)],
        [Paragraph("<b>«Опекающий контролер»</b>", box_text_style), Paragraph("Нотации, вздохи, «ты надел шапку?», переделывание.", box_text_style), Paragraph("Передать 100% ответственности и принять неидеальность.", box_text_style)],
        [Paragraph("<b>«Обороняющийся партнер»</b>", box_text_style), Paragraph("«Забыл», «потом», демонстративное игнорирование.", box_text_style), Paragraph("Соблюдать договоренности взрослого мужчины.", box_text_style)]
    ]
    story.append(make_table(data_m4, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум разрыва родительского сценария", h2_style))
    story.append(make_box([
        Paragraph("<b>Слова-стопперы при скатывании в нотации:</b> «Стоп, мы равные взрослые любовники, а не мама с сыном».<br/>"
                  "<b>Моё личное обязательство:</b> _____________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Модуль 5. Спасение романтики: закон внешних свиданий", h1_style))
    story.append(Paragraph("Чтобы не превратиться в соседей по коммуналке, введите жесткие правила для двоих:", body_style))

    story.append(Paragraph("• <b>Табу на быт под одеялом:</b> Никаких счетов, ремонта и претензий в постели перед сном.", bullet_style))
    story.append(Paragraph("• <b>Закон внешнего свидания:</b> Раз в неделю нарядный выход за пределы квартиры только вдвоем.", bullet_style))
    story.append(Paragraph("• <b>Эстетичный домашний дресс-код:</b> Запрет на старые рваные футболки и растянутые треники.", bullet_style))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("План романтического выхода на эту неделю", h2_style))
    story.append(make_box([
        Paragraph("<b>Куда мы идем (новое место):</b> __________________________________________________________________<br/>"
                  "<b>Запрещенные темы за ужином:</b> Быт, уборка, счета, рабочие проблемы.<br/>"
                  "<b>О чем мы мечтаем поговорить:</b> _________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Модуль 6. 14-дневный маршрут уюта и Домашний кодекс", h1_style))
    story.append(Paragraph("Пошаговое закрепление комфортной жизни под одной крышей:", body_style))

    data_m6 = [
        [Paragraph("Период", box_text_style), Paragraph("Фокус практики", box_text_style), Paragraph("Критерий успеха", box_text_style)],
        [Paragraph("<b>Дни 1–4</b>", box_text_style), Paragraph("Внедрение матрицы Fair Play по быту.", box_text_style), Paragraph("Четкое разделение без напоминаний.", box_text_style)],
        [Paragraph("<b>Дни 5–8</b>", box_text_style), Paragraph("Освоение «правила наушников» и тишины.", box_text_style), Paragraph("Отсутствие обид на уединение.", box_text_style)],
        [Paragraph("<b>Дни 9–11</b>", box_text_style), Paragraph("Отказ от избыточного контроля и опеки.", box_text_style), Paragraph("Равный взрослый диалог.", box_text_style)],
        [Paragraph("<b>Дни 12–14</b>", box_text_style), Paragraph("Внешнее романтическое свидание.", box_text_style), Paragraph("Возвращение взаимной искры и трепета.", box_text_style)]
    ]
    story.append(make_table(data_m6, [35*mm, 85*mm, 60*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Домашний кодекс молодой пары", h2_style))
    story.append(make_box([
        Paragraph("1. Мы ценим любовь и радость выше идеальной чистоты на полках.<br/>"
                  "2. Мы благодарим друг друга за бытовой вклад каждый день.<br/>"
                  "3. Мы строим наше гнездо по собственным правилам, а не по лекалам родителей.<br/>"
                  "4. Мы остаемся нежными любовниками в любых бытовых обстоятельствах.", box_text_style),
    ], bg=colors.HexColor('#ecfdf5'), border_color=colors.HexColor('#047857')))

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
    story.append(Paragraph("УРОВЕНЬ 3 • КЛИНИЧЕСКОЕ РУКОВОДСТВО: СИСТЕМНАЯ ИНТЕГРАЦИЯ", title_style))
    story.append(Paragraph("Клинический протокол системной адаптации пары: переход от «Я» к «МЫ» (8 сессий)", subtitle_style))
    story.append(Paragraph("Раздел 1. Системная трансформация: интеграция зрелого «МЫ»", h1_style))
    story.append(Paragraph("Психологический переход от холостяцкого эгоцентризма к зрелому супружескому союзу:", body_style))

    data_p1 = [
        [Paragraph("Сфера жизни", box_text_style), Paragraph("Холостяцкая позиция («Я»)", box_text_style), Paragraph("Зрелая интеграция («МЫ»)", box_text_style)],
        [Paragraph("<b>Бытовой уклад</b>", box_text_style), Paragraph("«Я живу так, как привык; подстраиваться не хочу».", box_text_style), Paragraph("«Мы создаем наши правила с чистого листа».", box_text_style)],
        [Paragraph("<b>Планы и график</b>", box_text_style), Paragraph("Спонтанные решения в одиночку, партнер перед фактом.", box_text_style), Paragraph("Координация расписаний, уважение планов другого.", box_text_style)],
        [Paragraph("<b>Конфликт быта</b>", box_text_style), Paragraph("«Ты пытаешься сломать мои границы!».", box_text_style), Paragraph("«У нас разные привычки, давай найдем середину».", box_text_style)]
    ]
    story.append(make_table(data_p1, [45*mm, 65*mm, 70*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Исследование индекса интеграции пары", h2_style))
    story.append(make_box([
        Paragraph("<b>В чем каждому труднее всего поступиться холостяцкими привычками:</b> ______________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 2
    story.append(Paragraph("Раздел 2. Схема-терапевтический профиль бытовых триггеров", h1_style))
    story.append(Paragraph("Почему невымытая кружка воспринимается как глубинная атака на личность:", body_style))

    data_p2 = [
        [Paragraph("Бытовой триггер", box_text_style), Paragraph("Активированная детская схема", box_text_style), Paragraph("Скрытая глубинная боль", box_text_style)],
        [Paragraph("Партнер забыл купить продукты.", box_text_style), Paragraph("<b>Страх непринятия / Неуверенность</b>", box_text_style), Paragraph("«Мои просьбы ничего не значат, я пустой звук».", box_text_style)],
        [Paragraph("Замечание по поводу уборки.", box_text_style), Paragraph("<b>Жесткие стандарты / Стыд</b>", box_text_style), Paragraph("«Я плохая(ой), меня отвергнут за ошибку».", box_text_style)],
        [Paragraph("Партнер закрылся в комнате.", box_text_style), Paragraph("<b>Покинутость (Abandonment)</b>", box_text_style), Paragraph("«Меня бросили, я остался в одиночестве».", box_text_style)]
    ]
    story.append(make_table(data_p2, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Анализ глубинных корней бытовых ссор", h2_style))
    story.append(make_box([
        Paragraph("<b>Когда мы ругаемся из-за быта, о чем на самом деле наш страх:</b> __________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("Раздел 3. Преодоление скрытого напряжения и обид", h1_style))
    story.append(Paragraph("Деконструкция скрытых форм выражения гнева в совместном проживании:", body_style))

    data_p3 = [
        [Paragraph("Форма пассивной агрессии", box_text_style), Paragraph("Скрытое послание", box_text_style), Paragraph("Ассертивная терапевтическая замена", box_text_style)],
        [Paragraph("<b>Демонстративный грохот посудой</b>", box_text_style), Paragraph("«Посмотри, как я страдаю, а ты не видишь!».", box_text_style), Paragraph("«Я устал(а). Пожалуйста, помой посуду сегодня».", box_text_style)],
        [Paragraph("<b>Систематическая «забывчивость»</b>", box_text_style), Paragraph("«Мне тяжело от избыточного контроля».", box_text_style), Paragraph("«Я не хочу это делать, давай передоговоримся».", box_text_style)],
        [Paragraph("<b>Бытовой сарказм и подколы</b>", box_text_style), Paragraph("«Мне страшно сказать прямо, я уколю исподтишка».", box_text_style), Paragraph("«Мне неприятно, когда вещи лежат на полу».", box_text_style)]
    ]
    story.append(make_table(data_p3, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Практикум чистого диалога", h2_style))
    story.append(make_box([
        Paragraph("<b>Моя привычная скрытая реакция на напряжение:</b> ____________________________________________________<br/>"
                  "<b>Как я обязуюсь выражать эту потребность словами:</b> _____________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 4
    story.append(Paragraph("Раздел 4. Защита сексуальности и либидо от бытовой рутины", h1_style))
    story.append(Paragraph("Сохранение эротического влечения в условиях общего санузла и кухни:", body_style))

    data_p4 = [
        [Paragraph("Фактор бытовой эрозии", box_text_style), Paragraph("Влияние на эротическое поле", box_text_style), Paragraph("Терапевтический протокол защиты", box_text_style)],
        [Paragraph("Открытые двери в туалет/ванную.", box_text_style), Paragraph("Уничтожение эротической тайны тела.", box_text_style), Paragraph("Строгая приватность гигиенических процедур.", box_text_style)],
        [Paragraph("Хроническая усталость от порядка.", box_text_style), Paragraph("Секс начинает восприниматься как обязанность.", box_text_style), Paragraph("Снижение планки перфекционизма: отдых важнее.", box_text_style)],
        [Paragraph("Бытовая одежда в спальне.", box_text_style), Paragraph("Стирание сексуального образа партнера.", box_text_style), Paragraph("Эстетичная и привлекательная домашняя одежда.", box_text_style)]
    ]
    story.append(make_table(data_p4, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Протокол сенсорного оздоровления спальни", h2_style))
    story.append(make_box([
        Paragraph("<b>Что мы убираем из спальни (ноутбуки, сушилки с бельем):</b> _________________________________________<br/>"
                  "<b>Что мы добавляем для чувственности (свет, свечи, запахи):</b> ______________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 5
    story.append(Paragraph("Раздел 5. Работа с тупиковыми спорами о чистоте (Дж. Готтман)", h1_style))
    story.append(Paragraph("69% разногласий в паре неразрешимы. Протокол сосуществования с разницей стандартов:", body_style))

    data_p5 = [
        [Paragraph("Шаг метода Готтмана", box_text_style), Paragraph("Суть клинического действия", box_text_style)],
        [Paragraph("<b>1. Поиск мечты за позицией</b>", box_text_style), Paragraph("Понять, что порядок значит для партнера (Безопасность? Уважение?).", box_text_style)],
        [Paragraph("<b>2. Разделение суверенных зон</b>", box_text_style), Paragraph("Рабочий стол одного — его хаос; общие зоны — нейтральная чистота.", box_text_style)],
        [Paragraph("<b>3. Юмор и принятие различий</b>", box_text_style), Paragraph("Воспринимать привычку как милую особенность, а не повод для развода.", box_text_style)]
    ]
    story.append(make_table(data_p5, [65*mm, 115*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Наш компромисс по вечному спору", h2_style))
    story.append(make_box([
        Paragraph("<b>Наш главный неразрешимый спор о чистоте:</b> _______________________________________________________<br/>"
                  "<b>Наше соглашение взаимного уважения:</b> ___________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 6
    story.append(Paragraph("Раздел 6. Поведенческий эксперимент «Смена ролей на 48 часов»", h1_style))
    story.append(Paragraph("Глубинная десенсибилизация претензий через проживание быта партнера:", body_style))

    data_p6 = [
        [Paragraph("Партнер", box_text_style), Paragraph("Временная новая роль", box_text_style), Paragraph("Главный эмпатический инсайт", box_text_style)],
        [Paragraph("<b>Партнер 1</b> (обычно готовит еду)", box_text_style), Paragraph("Полное освобождение от мыслей о кухне.", box_text_style), Paragraph("Ощущение глубокого отдыха и заботы.", box_text_style)],
        [Paragraph("<b>Партнер 2</b> (не готовил ранее)", box_text_style), Paragraph("Меню, закупка продуктов, готовка 2 дня.", box_text_style), Paragraph("«Я понял, какой это огромный невидимый труд».", box_text_style)]
    ]
    story.append(make_table(data_p6, [50*mm, 65*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Результаты и выводы эксперимента", h2_style))
    story.append(make_box([
        Paragraph("<b>Главное взаимное открытие после смены ролей:</b> ___________________________________________________<br/>"
                  "____________________________________________________________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 7
    story.append(Paragraph("Раздел 7. Дорожная карта адаптации пары на 8 сессий", h1_style))
    story.append(Paragraph("Клинический маршрут психотерапевтической помощи молодой паре:", body_style))

    data_p7 = [
        [Paragraph("Сессии", box_text_style), Paragraph("Терапевтический фокус", box_text_style), Paragraph("Критерий прогресса", box_text_style)],
        [Paragraph("<b>Сессии 1–2</b>", box_text_style), Paragraph("Анамнез родительских семей, деконструкция сценариев быта.", box_text_style), Paragraph("Снятие взаимных упреков и обид.", box_text_style)],
        [Paragraph("<b>Сессии 3–4</b>", box_text_style), Paragraph("Схема-терапия: выявление скрытых детских ран в быту.", box_text_style), Paragraph("Переход от скрытых обид к открытому диалогу.", box_text_style)],
        [Paragraph("<b>Сессии 5–6</b>", box_text_style), Paragraph("Зонирование автономии, внедрение матрицы Fair Play.", box_text_style), Paragraph("Справедливое разделение без контроля.", box_text_style)],
        [Paragraph("<b>Сессии 7–8</b>", box_text_style), Paragraph("Интеграция зрелого «МЫ», укрепление романтической базы.", box_text_style), Paragraph("Стабильный уют и взаимная страсть.", box_text_style)]
    ]
    story.append(make_table(data_p7, [30*mm, 85*mm, 65*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Заметки семейного терапевта и пары", h2_style))
    story.append(make_box([
        Paragraph("<b>Ключевой фокус ближайшей сессии:</b> _______________________________________________________________<br/>"
                  "<b>Домашнее задание для пары между сессиями:</b> ____________________________________________________", box_text_style)
    ]))
    story.append(PageBreak())

    # Page 8
    story.append(Paragraph("Раздел 8. Супружеская хартия гармоничного дома", h1_style))
    story.append(Paragraph("Фундаментальные опоры зрелого, комфортного и любящего союза:", body_style))

    data_p8 = [
        [Paragraph("Принцип союза", box_text_style), Paragraph("Практическое правило пары", box_text_style)],
        [Paragraph("<b>Свобода в границах «МЫ»</b>", box_text_style), Paragraph("Право на личные увлечения, отдельных друзей и время наедине с собой.", box_text_style)],
        [Paragraph("<b>Культура благодарности</b>", box_text_style), Paragraph("Ежедневно замечать заботу партнера и говорить «спасибо» за быт вслух.", box_text_style)],
        [Paragraph("<b>Командное единство</b>", box_text_style), Paragraph("Бытовые проблемы снаружи — мы вдвоем нерушимы внутри.", box_text_style)]
    ]
    story.append(make_table(data_p8, [65*mm, 115*mm], bg_hdr=PRIMARY_DARK, is_compact=True))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Хартия нашего совместного дома", h2_style))
    story.append(make_box([
        Paragraph("<b>ХАРТИЯ СОВМЕСТНОГО ДОМА МОЛОДОЙ ПАРЫ</b><br/>"
                  "Мы строим наш общий дом как пространство безопасности, вдохновения, нежности и взаимного уважения. Мы обязуемся беречь чувства друг друга, не позволять бытовой рутине убивать любовь и всегда помнить, почему мы выбрали быть вместе.<br/><br/>"
                  "Партнер 1: __________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Партнер 2: __________________________<br/>"
                  "Дата заключения союза: «____» ____________ 202__ г.", box_text_style),
    ], bg=colors.HexColor('#ecfdf5'), border_color=colors.HexColor('#047857')))

    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == '__main__':
    build_l1('therapy-workbooks/cohabitation_workbook_1_adaptation.pdf')
    print("SUCCESS: Cohabitation L1 (3 pages)")

    build_l2('therapy-workbooks/cohabitation_workbook_2_architecture.pdf')
    print("SUCCESS: Cohabitation L2 (6 pages)")

    build_l3('therapy-workbooks/cohabitation_workbook_3_integration.pdf')
    print("SUCCESS: Cohabitation L3 (8 pages)")
