import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_H = 14 * mm
MARGIN_V = 14 * mm
CONTENT_WIDTH = 182 * mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.series_title = "СЕРИЯ 04 • ЗРЕЛАЯ САМООЦЕНКА И САМОЦЕННОСТЬ"
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
            self.setFillColor(colors.HexColor('#047857'))
            self.drawString(MARGIN_H, PAGE_HEIGHT - 10.5 * mm, self.series_title)
            self.setFont('DejaVu', 7)
            self.setFillColor(colors.HexColor('#475569'))
            self.drawRightString(PAGE_WIDTH - MARGIN_H, PAGE_HEIGHT - 10.5 * mm, "ПРАКТИКУМ")
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setLineWidth(0.6)
            self.line(MARGIN_H, PAGE_HEIGHT - 12 * mm, PAGE_WIDTH - MARGIN_H, PAGE_HEIGHT - 12 * mm)

        self.setFont('DejaVu', 7.5)
        self.setFillColor(colors.HexColor('#475569'))
        self.drawString(MARGIN_H, 9 * mm, "Психотерапевтическая рабочая тетрадь • Материал для безопасной личной практики")
        page_str = f"Страница {self._pageNumber} из {total_pages}"
        self.drawRightString(PAGE_WIDTH - MARGIN_H, 9 * mm, page_str)
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.6)
        self.line(MARGIN_H, 11.5 * mm, PAGE_WIDTH - MARGIN_H, 11.5 * mm)
        self.restoreState()

styles = getSampleStyleSheet()

title_style = ParagraphStyle('DocTitle', fontName='DejaVu-Bold', fontSize=13, leading=16.5, textColor=colors.HexColor('#0f172a'), spaceAfter=1.5*mm)
badge_style = ParagraphStyle('Badge', fontName='DejaVu-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#059669'))
h1_style = ParagraphStyle('H1', fontName='DejaVu-Bold', fontSize=9.5, leading=12.5, textColor=colors.HexColor('#065f46'), spaceAfter=1.5*mm)
body_style = ParagraphStyle('Body', fontName='DejaVu', fontSize=8, leading=10.5, textColor=colors.HexColor('#1e293b'))
body_bold = ParagraphStyle('BodyBold', fontName='DejaVu-Bold', fontSize=8, leading=10.5, textColor=colors.HexColor('#0f172a'))
small_style = ParagraphStyle('Small', fontName='DejaVu', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#475569'))

# Level 2 styles
badge_l2 = ParagraphStyle('BadgeL2', fontName='DejaVu-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#0284c7'))
h1_l2 = ParagraphStyle('H1L2', fontName='DejaVu-Bold', fontSize=9.5, leading=12.5, textColor=colors.HexColor('#0369a1'), spaceAfter=1.5*mm)

# Level 3 styles
badge_l3 = ParagraphStyle('BadgeL3', fontName='DejaVu-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#4f46e5'))
h1_l3 = ParagraphStyle('H1L3', fontName='DejaVu-Bold', fontSize=9.5, leading=12.5, textColor=colors.HexColor('#312e81'), spaceAfter=1.5*mm)

# ==================== L1: EXACTLY 3 PAGES ====================
doc1 = SimpleDocTemplate("therapy-workbooks/self_esteem_workbook_1_anchor.pdf", pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm)
s1 = []

# L1 Page 1: 10 test items
s1.append(Table([[Paragraph("<b>УРОВЕНЬ 1 • ЭКСПРЕСС-ИНТЕНСИВ (СТРАНИЦА 1 ИЗ 3)</b>", badge_style), Paragraph("Диагностика", small_style)],
                 [Paragraph("Внутренняя опора: Профиль устойчивости самооценки", title_style), Paragraph("Дата: _____________", body_style)]], colWidths=[135*mm, 47*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
s1.append(Spacer(1, 2*mm))

t1_items = [
    [Paragraph("<b>Клинический экспресс-тест (10 маркеров устойчивости)</b>", h1_style)],
    [Paragraph("[ ] 1. Мое настроение резко падает от чужой критики или сухого тона в переписке.<br/>"
               "[ ] 2. Мне трудно искренне похвалить себя за сделанное: кажется, что «можно было лучше».<br/>"
               "[ ] 3. Принимая комплимент, я испытываю неловкость и начинаю оправдываться.<br/>"
               "[ ] 4. Я постоянно сравниваю себя с коллегами в соцсетях и чувствую себя отстающим(ей).<br/>"
               "[ ] 5. Страх сделать ошибку настолько велик, что я долго откладываю начало важных дел.<br/>"
               "[ ] 6. При неудаче я ругаю себя жесткими словами, которых никогда не сказал(а) бы другу.<br/>"
               "[ ] 7. Мне трудно отказать в просьбе из-за страха показаться черствым(ой) или плохим(ой).<br/>"
               "[ ] 8. Мои успехи кажутся случайностью, а ошибки — доказательством моей некомпетентности.<br/>"
               "[ ] 9. Чтобы чувствовать уверенность, мне жизненно необходимо постоянное одобрение со стороны.<br/>"
               "[ ] 10. Мне тяжело отдыхать без чувства вины: кажется, что я трачу драгоценное время впустую.", body_style)],
    [Paragraph("<b>Интерпретация:</b> 0–3 совпадения — стабильная внутренняя опора; 4–7 — зависимость от внешних оценок; 8–10 — сильное давление критика, требуется регулярная поддержка.", small_style)]
]
t_t1 = Table(t1_items, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdfa')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')), ('PADDING', (0,0), (-1,-1), 4)])
s1.append(Table([[t_t1]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0d9488')), ('PADDING', (0,0), (-1,-1), 5)]))

s1.append(PageBreak())

# L1 Page 2: Self-compassion protocol & physical anchor
s1.append(Table([[Paragraph("<b>УРОВЕНЬ 1 • ЭКСПРЕСС-ИНТЕНСИВ (СТРАНИЦА 2 ИЗ 3)</b>", badge_style), Paragraph("Самопомощь", small_style)],
                 [Paragraph("Протокол перехвата самокритики и телесный якорь", title_style), Paragraph("Дата: _____________", body_style)]], colWidths=[135*mm, 47*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
s1.append(Spacer(1, 2*mm))

t2_proto = [
    [Paragraph("<b>3-шаговый алгоритм «Стоп-критика» (CFT)</b>", h1_style)],
    [Paragraph("<b>Шаг 1. Перехват и осознание:</b> Рука на груди. «Прямо сейчас мне тяжело. Во мне звучит привычная критика, но это лишь мысли, а не факты обо мне».", body_style)],
    [Paragraph("<b>Шаг 2. Проверка на человечность:</b> «Сказал(а) бы я эти жестокие слова другу в такой же ситуации? Почему я требую от себя абсолютного совершенства?»", body_style)],
    [Paragraph("<b>Шаг 3. Голос поддерживающего Защитника:</b> «Я имею право ошибаться, уставать и учиться. Я поддерживаю себя прямо сейчас».", body_style)]
]
t_t2 = Table(t2_proto, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)])
s1.append(Table([[t_t2]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))
s1.append(Spacer(1, 4*mm))

t2_body = [
    [Paragraph("<b>Телесный якорь уверенности (Физиология опоры)</b>", h1_style)],
    [Paragraph("• <b>Стопы:</b> плотно почувствовать пол, ощутить твердую опору под собой.<br/>"
               "• <b>Дыхание 4–6:</b> вдох носом на 4 счета — длинный выдох через рот на 6 счетов (снижение кортизола).<br/>"
               "• <b>Плечи:</b> мягко опустить плечи, разжать челюсти и снять зажим в диафрагме.", body_style)]
]
t_t2_body = Table(t2_body, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdfa')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')), ('PADDING', (0,0), (-1,-1), 4)])
s1.append(Table([[t_t2_body]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0d9488')), ('PADDING', (0,0), (-1,-1), 5)]))

s1.append(PageBreak())

# L1 Page 3: 3-day tracker & contract
s1.append(Table([[Paragraph("<b>УРОВЕНЬ 1 • ЭКСПРЕСС-ИНТЕНСИВ (СТРАНИЦА 3 ИЗ 3)</b>", badge_style), Paragraph("Интеграция", small_style)],
                 [Paragraph("3-дневный трекер внедрения и договор с собой", title_style), Paragraph("Дата: _____________", body_style)]], colWidths=[135*mm, 47*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
s1.append(Spacer(1, 2*mm))

t3_tracker = [
    [Paragraph("<b>Дневник присвоения ценности (3 дня практики)</b>", h1_style)],
    [Paragraph("<b>День 1:</b> Что сегодня получилось хорошо / где я проявил(а) устойчивость:<br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>День 2:</b> В какой момент я вовремя остановил(а) самобичевание и поддержал(а) себя:<br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>День 3:</b> За что я искренне уважаю себя независимо от чужого мнения:<br/>____________________________________________________________________________________________________", body_style)]
]
t_t3 = Table(t3_tracker, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)])
s1.append(Table([[t_t3]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))
s1.append(Spacer(1, 4*mm))

t3_contract = [
    [Paragraph("<b>Личный договор бережного отношения к себе</b>", h1_style)],
    [Paragraph("<i>«Я подтверждаю: моя ценность как личности безусловна. Она не становится меньше от ошибок, усталости или критики со стороны. Я учусь быть на своей стороне».</i><br/><br/>"
               "Личная подпись: ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Дата: ___________________", body_style)]
]
t_t3_c = Table(t3_contract, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdfa')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')), ('PADDING', (0,0), (-1,-1), 4)])
s1.append(Table([[t_t3_c]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0d9488')), ('PADDING', (0,0), (-1,-1), 5)]))

doc1.build(s1, canvasmaker=NumberedCanvas)
print("SUCCESS: PDF L1 (Exactly 3 pages)")

# ==================== L2: EXACTLY 6 PAGES ====================
badge_l2 = ParagraphStyle('Badge2', fontName='DejaVu-Bold', fontSize=7, leading=8, textColor=colors.HexColor('#0284c7'))
h1_l2 = ParagraphStyle('H12', fontName='DejaVu-Bold', fontSize=9, leading=11.5, textColor=colors.HexColor('#0369a1'), spaceAfter=1.5*mm)

doc2 = SimpleDocTemplate("therapy-workbooks/self_esteem_workbook_2_value.pdf", pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm)
s2 = []

def make_header(p_num, title, sub):
    return [
        Table([[Paragraph(f"<b>УРОВЕНЬ 2 • САМОСТОЯТЕЛЬНЫЙ ПРАКТИКУМ (СТРАНИЦА {p_num} ИЗ 6)</b>", badge_l2), Paragraph(sub, small_style)],
               [Paragraph(title, title_style), Paragraph("Дата: _____________", body_style)]], colWidths=[135*mm, 47*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]),
        Spacer(1, 2*mm)
    ]

# Page 1: Archetypes
s2.extend(make_header(1, "5 архетипов внутреннего самозванца", "Диагностика"))
arch_box = [
    [Paragraph("<b>Модуль 1. Диагностика личного паттерна самозванца</b>", h1_l2)],
    [Paragraph("<b>1. Перфекционист:</b> «Если сделано не на 100% идеально — это провал». <i>Противоядие:</i> стандарт достаточности.<br/>"
               "<b>2. Эксперт:</b> «Пока не прочитаю еще 5 книг, не имею права говорить». <i>Противоядие:</i> ценность практики.<br/>"
               "<b>3. Прирожденный гений:</b> «Если пришлось приложить усилие — значит, бездарен». <i>Противоядие:</i> мастерство требует опыта.<br/>"
               "<b>4. Солист:</b> «Обязан(а) справиться абсолютно один(на)». <i>Противоядие:</i> кооперация — сила.<br/>"
               "<b>5. Супермен:</b> «Должен быть идеален во всем одновременно». <i>Противоядие:</i> признание человеческих границ.", body_style)],
    [Paragraph("<b>Мой главный архетип самозванца:</b> __________________________________________________________________<br/>"
               "В каких рабочих или личных ситуациях он включается сильнее всего:<br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s2.append(Table([[Table(arch_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')), ('PADDING', (0,0), (-1,-1), 5)]))

s2.append(PageBreak())

# Page 2: Victory Ownership
s2.extend(make_header(2, "Дневник присвоения побед и опыта", "Практика"))
own_box = [
    [Paragraph("<b>Модуль 2. Деконструкция иллюзии «мне просто повезло»</b>", h1_l2)],
    [Paragraph("<b>Результат 1:</b> __________________________________________________________________________________<br/>"
               "Мысль самозванца: <i>«Это случайность, любой бы справился...»</i><br/>"
               "<b>Факты моих реальных усилий и навыков:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Результат 2:</b> __________________________________________________________________________________<br/>"
               "Мысль самозванца: <i>«Мне просто пошли навстречу...»</i><br/>"
               "<b>Факты моих реальных усилий и навыков:</b><br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s2.append(Table([[Table(own_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s2.append(PageBreak())

# Page 3: Perfectionism to Good Enough
s2.extend(make_header(3, "Переход к стандарту «Достаточно хорошо»", "Стандарты"))
perf_box = [
    [Paragraph("<b>Модуль 3. Матрица экологичных стандартов (Good Enough)</b>", h1_l2)],
    [Paragraph("<b>Дело, которое я долго откладываю из-за перфекционизма:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Что будет результатом «на 80%», который позволит завершить задачу:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Разрешение себе: что самое страшное произойдет без идеальной полировки:</b><br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s2.append(Table([[Table(perf_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')), ('PADDING', (0,0), (-1,-1), 5)]))

s2.append(PageBreak())

# Page 4: Self-Compassion
s2.extend(make_header(4, "Протокол сострадания к себе (К. Нефф)", "Самосострадание"))
comp_box = [
    [Paragraph("<b>Модуль 4. Исцеление вины и стыда в момент промаха</b>", h1_l2)],
    [Paragraph("<b>1. Осознанность (Mindfulness):</b> признать боль без драматизации: <i>«Прямо сейчас мне тяжело. Это неприятно, но это проходит».</i><br/>"
               "<b>2. Общая человечность (Common Humanity):</b> <i>«Все люди ошибаются. Ошибка не делает меня дефектным(ой)».</i><br/>"
               "<b>3. Доброта к себе (Self-Kindness):</b> <i>«Что я могу сделать для себя прямо сейчас, чтобы облегчить свое состояние?»</i>", body_style)],
    [Paragraph("<b>Мое личное поддерживающее послание себе в моменты неудач:</b><br/>"
               "____________________________________________________________________________________________________<br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s2.append(Table([[Table(comp_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s2.append(PageBreak())

# Page 5: Social Comparison
s2.extend(make_header(5, "Фильтр социальных сравнений", "Фокус"))
soc_box = [
    [Paragraph("<b>Модуль 5. Очищение фокуса внимания: выход из чужих витрин</b>", h1_l2)],
    [Paragraph("<b>1. За кем в соцсетях я слежу с тайным чувством неуверенности в себе:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>2. Реальность за чужим фасадом: о какой цене успеха я ничего не знаю:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>3. Сравнение с собой: в чем мой личный прогресс за последние 2–3 года:</b><br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s2.append(Table([[Table(soc_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')), ('PADDING', (0,0), (-1,-1), 5)]))

s2.append(PageBreak())

# Page 6: Manifest
s2.extend(make_header(6, "Личный манифест безусловной самоценности", "Кодекс"))
man_box = [
    [Paragraph("<b>Модуль 6. Неснижаемые правила уважения к себе на месяц</b>", h1_l2)],
    [Paragraph("<b>1. Мое безусловное право на отдых без оправданий:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>2. Мое право открыто говорить о своих потребностях:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>3. Мое право на неидеальность и обучение:</b><br/>"
               "____________________________________________________________________________________________________<br/><br/>"
               "<i>Личная подпись: ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Дата: ___________________</i>", body_style)]
]
s2.append(Table([[Table(man_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')), ('PADDING', (0,0), (-1,-1), 5)]))

doc2.build(s2, canvasmaker=NumberedCanvas)
print("SUCCESS: PDF L2 (Exactly 6 pages)")

# ==================== L3: EXACTLY 8 PAGES ====================
badge_l3 = ParagraphStyle('Badge3', fontName='DejaVu-Bold', fontSize=7, leading=8, textColor=colors.HexColor('#4f46e5'))
h1_l3 = ParagraphStyle('H13', fontName='DejaVu-Bold', fontSize=9, leading=11.5, textColor=colors.HexColor('#312e81'), spaceAfter=1.5*mm)

doc3 = SimpleDocTemplate("therapy-workbooks/self_esteem_workbook_3_depth.pdf", pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm)
s3 = []

def make_header3(p_num, title, sub):
    return [
        Table([[Paragraph(f"<b>УРОВЕНЬ 3 • КЛИНИЧЕСКИЙ ПРАКТИКУМ (СТРАНИЦА {p_num} ИЗ 8)</b>", badge_l3), Paragraph(sub, small_style)],
               [Paragraph(title, title_style), Paragraph("Дата: _____________", body_style)]], colWidths=[135*mm, 47*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]),
        Spacer(1, 2*mm)
    ]

# Page 1: Genesis
s3.extend(make_header3(1, "Генезис самооценки: Детские послания", "Анамнез"))
gen_box = [
    [Paragraph("<b>Модуль 1. Исследование раннего опыта формирования стыда</b>", h1_l3)],
    [Paragraph("<b>Родительские условия принятия: за что хвалили, а за что отвергали:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Школьные эпизоды сравнения и насмешек у доски:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Главное негласное правило выживания в детстве:</b><br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s3.append(Table([[Table(gen_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f3ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#4f46e5')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# Page 2: Schemas
s3.extend(make_header3(2, "Карта ранних дезадаптивных схем", "Схема-терапия"))
sch_box = [
    [Paragraph("<b>Модуль 2. Анализ глубинных убеждений о себе</b>", h1_l3)],
    [Paragraph("<b>Схема Дефективности: «Внутри меня есть изъян»</b><br/>"
               "В каких ситуациях сейчас поднимается страх разоблачения:<br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Схема Жестких Стандартов: «Любовь нужно заслуживать победами»</b><br/>"
               "В чем выражается перфекционизм и страх снизить планку требований к себе:<br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s3.append(Table([[Table(sch_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# Page 3: Critic Modes
s3.extend(make_header3(3, "Деконструкция режимов Критика", "Субличности"))
crit_box = [
    [Paragraph("<b>Модуль 3. Разделение субличностей: Требовательный vs Карающий</b>", h1_l3)],
    [Paragraph("<b>Монолог Требовательного критика («Ты должен(на) больше, быстрее, лучше»):</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Монолог Требовательного критика («Ты ничтожество, у тебя ничего не выйдет»):</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Чьи голоса и интонации из прошлого звучат в этих упреках:</b><br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s3.append(Table([[Table(crit_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f3ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#4f46e5')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# Page 4: Vulnerable Child
s3.extend(make_header3(4, "Контакт с Уязвимой частью (Ребенок)", "Защита"))
child_box = [
    [Paragraph("<b>Модуль 4. Диалог с Уязвимым ребенком</b>", h1_l3)],
    [Paragraph("<b>Чего больше всего боится моя детская часть при критике и оценке:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Слова утешения и защиты от моего Здорового Взрослого:</b><br/>"
               "<i>«Я рядом. Я больше не позволю никому унижать тебя. Твоя ценность в безопасности».</i><br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s3.append(Table([[Table(child_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# Page 5: Exp 1 & 2
s3.extend(make_header3(5, "Поведенческие эксперименты (Шаги 1–2)", "Экспозиция"))
exp12_box = [
    [Paragraph("<b>Модуль 5. Микро-эксперименты на смелость проявления</b>", h1_l3)],
    [Paragraph("<b>Эксперимент 1 (Легкий уровень, SUDS 3–4):</b> Сказать твердый отказ на мелкую просьбу.<br/>"
               "Прогноз тревоги: ____________________________________________________________________________________<br/>"
               "Фактический результат: ______________________________________________________________________________", body_style)],
    [Paragraph("<b>Эксперимент 2 (Средний уровень, SUDS 5–6):</b> Открыто высказать свое несогласие в группе.<br/>"
               "Прогноз тревоги: ____________________________________________________________________________________<br/>"
               "Фактический результат: ______________________________________________________________________________", body_style)]
]
s3.append(Table([[Table(exp12_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f3ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#4f46e5')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# Page 6: Exp 3 & 4
s3.extend(make_header3(6, "Поведенческие эксперименты (Шаги 3–4)", "Прорыв"))
exp34_box = [
    [Paragraph("<b>Модуль 6. Прорывные поведенческие эксперименты</b>", h1_l3)],
    [Paragraph("<b>Эксперимент 3 (Высокий уровень, SUDS 7–8):</b> Опубликовать свою мысль или проект без идеальной полировки.<br/>"
               "Реакция на страх критики: ___________________________________________________________________________<br/>"
               "Новый опыт безопасности: ____________________________________________________________________________", body_style)],
    [Paragraph("<b>Эксперимент 4 (Мастерство, SUDS 9–10):</b> Прямой разговор об увеличении оплаты труда / личной границе.<br/>"
               "Реакция на страх критики: ___________________________________________________________________________<br/>"
               "Новый опыт безопасности: ____________________________________________________________________________", body_style)]
]
s3.append(Table([[Table(exp34_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# Page 7: Session Roadmap
s3.extend(make_header3(7, "Повестка курса психотерапии (Roadmap)", "Альянс"))
road_box = [
    [Paragraph("<b>Модуль 7. Дорожная карта курса на 8 консультаций</b>", h1_l3)],
    [Paragraph("[  ] <b>Сессии 1–2:</b> Исследование детских посланий и обнаружение истоков критика.<br/>"
               "[  ] <b>Сессии 3–4:</b> Когнитивный рескриптинг и защита уязвимой части.<br/>"
               "[  ] <b>Сессии 5–6:</b> Преодоление синдрома самозванца и присвоение профессионального статуса.<br/>"
               "[  ] <b>Сессии 7–8:</b> Интеграция Здорового Взрослого и устойчивый жизненный контракт.", body_style)],
    [Paragraph("<b>Ключевой персональный запрос клиента на весь курс:</b><br/>"
               "____________________________________________________________________________________________________<br/>"
               "____________________________________________________________________________________________________", body_style)]
]
s3.append(Table([[Table(road_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f3ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#4f46e5')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# Page 8: Final Integration
s3.extend(make_header3(8, "Терапевтический протокол интеграции", "Финал"))
fin_box = [
    [Paragraph("<b>Модуль 8. Контракт безусловной самоценности на будущее</b>", h1_l3)],
    [Paragraph("<b>💡 Главные фундаментальные сдвиги клиента:</b><br/>"
               "____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>🎯 Рекомендации специалиста на случай рецидива самокритики:</b><br/>"
               "____________________________________________________________________________________________________<br/><br/>"
               "<i>Подпись клиента: ________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Подпись специалиста: ________________________</i>", body_style)]
]
s3.append(Table([[Table(fin_box, colWidths=[178*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')), ('PADDING', (0,0), (-1,-1), 4)])]], colWidths=[182*mm], style=[('BOX', (0,0), (-1,-1), 1, colors.HexColor('#4f46e5')), ('PADDING', (0,0), (-1,-1), 5)]))

doc3.build(s3, canvasmaker=NumberedCanvas)
print("SUCCESS: PDF L3 (Exactly 8 pages)")
