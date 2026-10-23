import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

pdf_path = "therapy-workbooks/workbook_3_clinical_alliance.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=14*mm,
    rightMargin=14*mm,
    topMargin=12*mm,
    bottomMargin=12*mm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    fontName='DejaVu-Bold',
    fontSize=13,
    leading=16,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=1.5*mm
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    fontName='DejaVu',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#475569'),
    spaceAfter=2.5*mm
)

badge_style = ParagraphStyle(
    'Badge',
    fontName='DejaVu-Bold',
    fontSize=7,
    leading=8,
    textColor=colors.HexColor('#4338ca')
)

h1_style = ParagraphStyle(
    'H1',
    fontName='DejaVu-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#1e1b4b'),
    spaceAfter=1.5*mm
)

body_style = ParagraphStyle(
    'Body',
    fontName='DejaVu',
    fontSize=7.5,
    leading=10,
    textColor=colors.HexColor('#334155')
)

body_bold = ParagraphStyle(
    'BodyBold',
    fontName='DejaVu-Bold',
    fontSize=7.5,
    leading=10,
    textColor=colors.HexColor('#1e293b')
)

small_style = ParagraphStyle(
    'Small',
    fontName='DejaVu',
    fontSize=6.8,
    leading=9,
    textColor=colors.HexColor('#64748b')
)

story = []

# --- PAGE 1: SCHEMAS & EXPERIMENTS ---
header_data = [
    [
        Paragraph("<b>УРОВЕНЬ 3 • КЛИНИЧЕСКИЙ ПРАКТИКУМ</b>", badge_style),
        Paragraph("Терапевтический альянс", small_style)
    ],
    [
        Paragraph("Границы и автономия: Работа с глубинными установками", title_style),
        Paragraph("Дата сессии: _____________", body_style)
    ],
    [
        Paragraph("Клиническая рабочая тетрадь: когнитивные схемы, поведенческий протокол и мост к сессии.", subtitle_style),
        Paragraph("Клиент: ___________________", body_style)
    ]
]
t_head = Table(header_data, colWidths=[132*mm, 50*mm])
t_head.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ('TOPPADDING', (0,0), (-1,-1), 1),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_head)
story.append(Spacer(1, 2*mm))

# Block 1: Deep Schemas
schema_box = [
    [Paragraph("<b>МОДУЛЬ 1. Глубинный аудит схем: «Цена отказа и плата за одобрение»</b>", h1_style)],
    [Paragraph("Исследование детских установок, блокирующих право говорить «Нет»:", body_style)],
    [Spacer(1, 1*mm)]
]
table_schemas = [
    [Paragraph("<b>Когнитивная схема и убеждение</b>", body_bold), 
     Paragraph("<b>Сила (0-10)</b>", body_bold), 
     Paragraph("<b>Ранний источник / опыт формирования</b>", body_bold)],
    [Paragraph("<b>1. Самопожертвование:</b> <i>«Если откажу, сделаю другому больно и буду плохим человеком»</i>", body_style),
     Paragraph("[ ] 0-3<br/>[ ] 4-7<br/>[ ] 8-10", small_style),
     Paragraph("От кого в семье/окружении звучало требование быть «удобным»:<br/><br/>", small_style)],
    [Paragraph("<b>2. Условное принятие:</b> <i>«Меня любят и ценят, только пока я полезен и не спорю»</i>", body_style),
     Paragraph("[ ] 0-3<br/>[ ] 4-7<br/>[ ] 8-10", small_style),
     Paragraph("Катастрофический страх при прекращении спасательства:<br/><br/>", small_style)],
    [Paragraph("<b>3. Страх конфликта:</b> <i>«Любое несогласие приведет к отвержению или скандалу»</i>", body_style),
     Paragraph("[ ] 0-3<br/>[ ] 4-7<br/>[ ] 8-10", small_style),
     Paragraph("Фактический реалистичный исход при спокойном отказе:<br/><br/>", small_style)],
]
t_schema_tab = Table(table_schemas, colWidths=[80*mm, 27*mm, 75*mm])
t_schema_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e7ff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
schema_box.append([t_schema_tab])
t_schema_container = Table(schema_box, colWidths=[182*mm])
t_schema_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_schema_container)
story.append(Spacer(1, 3.5*mm))

# Block 2: Behavioral Experiments Protocol
exp_box = [
    [Paragraph("<b>МОДУЛЬ 2. Протокол поведенческих микро-экспериментов (между сессиями)</b>", h1_style)],
    [Paragraph("Границы проверяются практикой. Зафиксируйте 2 микро-отказа и сравните прогноз с фактом:", body_style)],
    [Spacer(1, 1*mm)]
]
table_exp = [
    [Paragraph("<b>Ситуация микро-отказа</b>", body_bold), 
     Paragraph("<b>Катастрофический прогноз</b>", body_bold), 
     Paragraph("<b>Тревога до (0-10)</b>", body_bold),
     Paragraph("<b>Фактический результат</b>", body_bold),
     Paragraph("<b>Тревога после (0-10)</b>", body_bold)],
    [Paragraph("<i>Эксперимент 1 (работа/рутина):</i><br/><br/>", body_style),
     Paragraph("«Обидятся / посчитают наглым»<br/>", small_style),
     Paragraph("____ / 10", body_style),
     Paragraph("Реакция собеседника:<br/><br/>", small_style),
     Paragraph("____ / 10", body_style)],
    [Paragraph("<i>Эксперимент 2 (близкий круг):</i><br/><br/>", body_style),
     Paragraph("«Начнется ссора / охлаждение»<br/>", small_style),
     Paragraph("____ / 10", body_style),
     Paragraph("Реакция собеседника:<br/><br/>", small_style),
     Paragraph("____ / 10", body_style)],
]
t_exp_tab = Table(table_exp, colWidths=[46*mm, 44*mm, 24*mm, 44*mm, 24*mm])
t_exp_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
exp_box.append([t_exp_tab])
t_exp_container = Table(exp_box, colWidths=[182*mm])
t_exp_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_exp_container)

story.append(PageBreak())

# --- PAGE 2: AGENDA & THERAPEUTIC INTEGRATION ---
header_p2 = [
    [
        Paragraph("<b>МОДУЛИ 3 и 4: МОСТ К СЕССИИ И ИНТЕГРАЦИЯ ОПЫТА</b>", badge_style),
        Paragraph("Страница 2 из 2", small_style)
    ]
]
t_h2 = Table(header_p2, colWidths=[140*mm, 42*mm])
t_h2.setStyle(TableStyle([
    ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_h2)
story.append(Spacer(1, 2*mm))

# Block 3: Agenda Builder
agenda_box = [
    [Paragraph("<b>МОДУЛЬ 3. Тематический мост к сессии с психологом (Agenda)</b>", h1_style)],
    [Paragraph("Отметьте актуальные темы для глубокой проработки на предстоящей сессии:", body_style)],
    [Spacer(1, 1*mm)]
]
table_agenda = [
    [Paragraph("[  ] <b>Разбор вины и отката:</b> сильное эмоциональное самобичевание после недавнего отказа.", body_style)],
    [Paragraph("[  ] <b>Трудная фигура влияния:</b> сложность сказать «нет» конкретному человеку (родитель / босс / супруг).", body_style)],
    [Paragraph("[  ] <b>Телесный ступор:</b> ком в горле, задержка дыхания, неспособность выговорить отказ в моменте.", body_style)],
    [Paragraph("[  ] <b>Рабочие границы:</b> прекращение бесплатных переработок и спасательства коллег.", body_style)],
    [Paragraph("[  ] <b>Ролевая игра в кабинете:</b> моделирование спокойного отказа и отработка ответов на давление.", body_style)],
    [Paragraph("<b>Индивидуальный вопрос / запрос клиента на встречу:</b><br/>____________________________________________________________________________________________________<br/>____________________________________________________________________________________________________", body_style)]
]
t_agenda_tab = Table(table_agenda, colWidths=[178*mm])
t_agenda_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
agenda_box.append([t_agenda_tab])
t_agenda_container = Table(agenda_box, colWidths=[182*mm])
t_agenda_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_agenda_container)
story.append(Spacer(1, 4*mm))

# Block 4: Collaborative Session Notes
notes_box = [
    [Paragraph("<b>МОДУЛЬ 4. Совместные заметки и инсайты терапевтической сессии</b>", h1_style)],
    [Paragraph("Фиксируется во время или сразу после консультации для закрепления динамики:", body_style)],
    [Spacer(1, 1*mm)]
]
table_notes = [
    [Paragraph("<b>💡 Главные инсайты клиента</b>", body_bold), 
     Paragraph("<b>🎯 Фокус терапевтического контракта и фокус внимания</b>", body_bold)],
    [Paragraph("Что я понял(а) о себе, скрытых вторичных выгодах соглашаться или источнике страха:<br/><br/><br/><br/><br/><br/>", body_style),
     Paragraph("Ключевые гипотезы психолога, ресурсы устойчивости и фокус наблюдения до следующей встречи:<br/><br/><br/><br/><br/><br/>", body_style)],
    [Paragraph("<i>Домашний микро-шаг: ___________________________________________________________</i>", small_style),
     Paragraph("<i>Дата следующей консультации: ______________________</i>", small_style)]
]
t_notes_tab = Table(table_notes, colWidths=[89*mm, 89*mm])
t_notes_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
notes_box.append([t_notes_tab])
t_notes_container = Table(notes_box, colWidths=[182*mm])
t_notes_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_notes_container)

doc.build(story)
print("SUCCESS: Level 3 PDF generated.")
