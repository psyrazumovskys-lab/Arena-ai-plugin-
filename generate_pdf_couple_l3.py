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

pdf_path = "therapy-workbooks/couple_workbook_3_clinical_cycle.pdf"

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
    textColor=colors.HexColor('#0284c7')
)

h1_style = ParagraphStyle(
    'H1',
    fontName='DejaVu-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#0369a1'),
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

# --- PAGE 1: DANCE & EMOTIONAL ICEBERG ---
header_data = [
    [
        Paragraph("<b>УРОВЕНЬ 3 • КЛИНИЧЕСКИЙ ПРАКТИКУМ ДЛЯ ПАРЫ</b>", badge_style),
        Paragraph("Семейная терапия", small_style)
    ],
    [
        Paragraph("Карта негативного цикла: Деконструкция парных ловушек", title_style),
        Paragraph("Дата сессии: _____________", body_style)
    ],
    [
        Paragraph("Картографирование цикла ссоры (ЭФТ), подводный айсберг уязвимостей и повестка сессии.", subtitle_style),
        Paragraph("Пара: _____________________", body_style)
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

# Block 1: The Dance (Cycle)
cycle_box = [
    [Paragraph("<b>МОДУЛЬ 1. Карта парного танца: «Преследователь — Отстраняющийся»</b>", h1_style)],
    [Paragraph("Проблема — не партнер, проблема — сам замкнутый повторяющийся цикл:", body_style)],
    [Spacer(1, 1*mm)]
]
table_cycle = [
    [Paragraph("<b>👤 Позиция А: «Атакующий / Требующий»</b>", body_bold), 
     Paragraph("<b>👤 Позиция Б: «Уходящий / В обороне»</b>", body_bold)],
    [Paragraph("Реакция на тревогу: повысить тон, потребовать немедленного ответа, стучаться в закрытую дверь.<br/><br/><i>«Чем больше ты молчишь, тем сильнее я:»</i><br/>________________________________________", body_style),
     Paragraph("Реакция на тревогу: замолчать, уйти в работу/экран, спрятаться от агрессии и критики.<br/><br/><i>«Чем громче ты требуешь, тем дальше я:»</i><br/>________________________________________", body_style)],
    [Paragraph("<b>Формула цикла:</b> <i>«Чем громче А атакует — тем глубже Б прячется; чем глубже Б прячется — тем сильнее паника у А».</i>", small_style),
     Paragraph("<b>Терапевтический фокус:</b> Увидеть этот цикл как общего внешнего врага, а не вину друг друга.", small_style)]
]
t_cycle_tab = Table(table_cycle, colWidths=[89*mm, 89*mm])
t_cycle_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0f2fe')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
cycle_box.append([t_cycle_tab])
t_cycle_container = Table(cycle_box, colWidths=[182*mm])
t_cycle_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#38bdf8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_cycle_container)
story.append(Spacer(1, 3.5*mm))

# Block 2: Iceberg
ice_box = [
    [Paragraph("<b>МОДУЛЬ 2. Айсберг эмоций: Вторичная защита vs Первичная боль привязанности</b>", h1_style)],
    [Paragraph("Над водой виден гнев или холод (защита). Под водой — глубинная уязвимость (тоска по связи):", body_style)],
    [Spacer(1, 1*mm)]
]
table_ice = [
    [Paragraph("<b>Уровень эмоции</b>", body_bold), 
     Paragraph("<b>👤 Партнер 1</b>", body_bold), 
     Paragraph("<b>👤 Партнер 2</b>", body_bold)],
    [Paragraph("<b>Над водой</b><br/>(вторичная защита:<br/>что видит партнер)", body_bold),
     Paragraph("Раздражение, критика, колкости или требовательный тон.<br/><br/>", body_style),
     Paragraph("Холодное молчание, равнодушный вид, рационализация.<br/><br/>", body_style)],
    [Paragraph("<b>Под водой</b><br/>(первичная уязвимость:<br/>что болит внутри)", body_bold),
     Paragraph("<i>«Мне невыносимо одиноко, я боюсь стать ненужным(ой) и брошенным(ой)»</i><br/><br/>", body_style),
     Paragraph("<i>«Я боюсь разочаровать, чувствую себя вечно 'недостаточно хорошим(ей)'»</i><br/><br/>", body_style)]
]
t_ice_tab = Table(table_ice, colWidths=[40*mm, 69*mm, 69*mm])
t_ice_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
ice_box.append([t_ice_tab])
t_ice_container = Table(ice_box, colWidths=[182*mm])
t_ice_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_ice_container)

story.append(PageBreak())

# --- PAGE 2: AGENDA & THERAPEUTIC PROTOCOL ---
header_p2 = [
    [
        Paragraph("<b>МОДУЛИ 3 и 4: ПОВЕСТКА СЕССИИ И ТЕРАПЕВТИЧЕСКИЙ ПРОТОКОЛ</b>", badge_style),
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

# Block 3: Couple Agenda
agenda_box = [
    [Paragraph("<b>МОДУЛЬ 3. Повестка совместной терапевтической сессии (Agenda)</b>", h1_style)],
    [Paragraph("Ключевые темы пары для разбора с семейным терапевтом на сессии:", body_style)],
    [Spacer(1, 1*mm)]
]
table_agenda = [
    [Paragraph("[  ] <b>Разбор застарелых обид:</b> не отпускающие прошлые эпизоды (ложь, холод в трудный момент).", body_style)],
    [Paragraph("[  ] <b>Интимность и охлаждение:</b> разница темпераментов, исчезновение физической ласки и флирта.", body_style)],
    [Paragraph("[  ] <b>Границы с третьими лицами:</b> навязчивое влияние родителей/родственников на жизнь семьи.", body_style)],
    [Paragraph("[  ] <b>Деньги и быт:</b> хроническое чувство несправедливости вклада в бюджет или домашние дела.", body_style)],
    [Paragraph("[  ] <b>Кризис будущего:</b> несовпадение долгосрочных целей, планов на детей или образ жизни.", body_style)],
    [Paragraph("<b>Индивидуальный вопрос пары к семейному психологу:</b><br/>____________________________________________________________________________________________________<br/>____________________________________________________________________________________________________", body_style)]
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

# Block 4: Couple Therapeutic Agreement
notes_box = [
    [Paragraph("<b>МОДУЛЬ 4. Совместный терапевтический протокол сессии</b>", h1_style)],
    [Paragraph("Фиксируется совместно с терапевтом в конце консультации:", body_style)],
    [Spacer(1, 1*mm)]
]
table_notes = [
    [Paragraph("<b>💡 Главный совместный инсайт пары</b>", body_bold), 
     Paragraph("<b>🎯 Терапевтическое домашнее микро-задание</b>", body_bold)],
    [Paragraph("Что мы увидели о наших триггерах и истинной привязанности друг к другу:<br/><br/><br/><br/><br/>", body_style),
     Paragraph("Конкретное соглашение пары до следующей сессии (например: 10 минут объятий / 1 свидание без быта):<br/><br/><br/><br/><br/>", body_style)],
    [Paragraph("<i>Подпись Партнера 1: ____________________________</i>", small_style),
     Paragraph("<i>Подпись Партнера 2: ____________________________</i>", small_style)]
]
t_notes_tab = Table(table_notes, colWidths=[89*mm, 89*mm])
t_notes_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0f2fe')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
notes_box.append([t_notes_tab])
t_notes_container = Table(notes_box, colWidths=[182*mm])
t_notes_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#38bdf8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_notes_container)

doc.build(story)
print("SUCCESS: Couple Level 3 PDF generated.")
