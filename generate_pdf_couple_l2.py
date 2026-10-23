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

pdf_path = "therapy-workbooks/couple_workbook_2_safe_dialogue.pdf"

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
    textColor=colors.HexColor('#9333ea')
)

h1_style = ParagraphStyle(
    'H1',
    fontName='DejaVu-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#581c87'),
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

# --- PAGE 1: DECODER & 4 HORSEMEN ---
header_data = [
    [
        Paragraph("<b>УРОВЕНЬ 2 • САМОСТОЯТЕЛЬНЫЙ ПРАКТИКУМ ДЛЯ ПАРЫ</b>", badge_style),
        Paragraph("Домашний практикум", small_style)
    ],
    [
        Paragraph("Анатомия безопасного диалога: От взаимных упреков к пониманию", title_style),
        Paragraph("Дата: _____________", body_style)
    ],
    [
        Paragraph("Декодер претензий, 4 всадника Апокалипсиса, еженедельный чек-ин и Я-сообщения.", subtitle_style),
        Paragraph("Пара: _____________", body_style)
    ]
]
t_head = Table(header_data, colWidths=[135*mm, 47*mm])
t_head.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ('TOPPADDING', (0,0), (-1,-1), 1),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_head)
story.append(Spacer(1, 2*mm))

# Block 1: Decoder
dec_box = [
    [Paragraph("<b>МОДУЛЬ 1. Декодер претензий: с языка упрека на язык потребностей</b>", h1_style)],
    [Paragraph("За каждым обвинением («Ты вечно...») прячется скрытая потребность и боль одиночества:", body_style)],
    [Spacer(1, 1*mm)]
]
table_dec = [
    [Paragraph("<b>Привычный упрек (нападение)</b>", body_bold), 
     Paragraph("<b>Скрытая уязвимая потребность</b>", body_bold), 
     Paragraph("<b>Безопасная формулировка</b>", body_bold)],
    [Paragraph("<i>«Ты вечно торчишь в телефоне/играх, тебе плевать на семью!»</i>", body_style),
     Paragraph("Мне не хватает твоего взгляда, тепла и ощущения, что я важен(а).", small_style),
     Paragraph("<i>«Мне одиноко сегодня. Давай посидим 15 минут вдвоем без экранов?»</i>", body_style)],
    [Paragraph("<i>«Я тут как прислуга, от тебя никакой помощи не дождешься!»</i>", body_style),
     Paragraph("Я перегружен(а), чувствую себя брошенным(ой) с бытом.", small_style),
     Paragraph("<i>«Я очень устал(а). Пожалуйста, разгрузи меня: возьми ужин на себя».</i>", body_style)],
    [Paragraph("<i>Наш типичный упрек:<br/><br/></i>", small_style),
     Paragraph("Что на самом деле болит:<br/><br/>", small_style),
     Paragraph("Как сказать мягко:<br/><br/>", small_style)]
]
t_dec_tab = Table(table_dec, colWidths=[60*mm, 60*mm, 58*mm])
t_dec_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f3e8ff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d8b4fe')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
dec_box.append([t_dec_tab])
t_dec_container = Table(dec_box, colWidths=[182*mm])
t_dec_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#faf5ff')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#c084fc')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_dec_container)
story.append(Spacer(1, 3.5*mm))

# Block 2: 4 Horsemen
horse_box = [
    [Paragraph("<b>МОДУЛЬ 2. «4 всадника Апокалипсиса» и их антидоты (по Дж. Готтману)</b>", h1_style)],
    [Spacer(1, 0.5*mm)]
]
table_horse = [
    [Paragraph("<b>Токсичный паттерн</b>", body_bold), Paragraph("<b>✅ Здоровый антидот в диалоге</b>", body_bold)],
    [Paragraph("<b>1. Критика:</b> «Ты вечно забывчивый и неряшливый» (атака личности)", body_style),
     Paragraph("<b>Мягкое начало:</b> «Я расстраиваюсь, когда вещи не на месте. Пожалуйста, убери их»", body_style)],
    [Paragraph("<b>2. Презрение / сарказм:</b> «Ой, великий труженик нашелся» (насмешки)", body_style),
     Paragraph("<b>Культура уважения:</b> «Я ценю твои усилия на работе, но дома мне тоже тяжело»", body_style)],
    [Paragraph("<b>3. Защита:</b> «А ты сама/сам лучше? Вспомни свой косяк!» (контратака)", body_style),
     Paragraph("<b>Своя доля ответственности:</b> «Да, согласен(на), я забыл предупредить, прости»", body_style)],
    [Paragraph("<b>4. Стена молчания:</b> игнор, холодный уход, каменное лицо", body_style),
     Paragraph("<b>Бережный тайм-аут:</b> «Мне нужно 20 минут охладиться. Я вернусь, и мы продолжим»", body_style)],
]
t_horse_tab = Table(table_horse, colWidths=[89*mm, 89*mm])
t_horse_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
horse_box.append([t_horse_tab])
t_horse_container = Table(horse_box, colWidths=[182*mm])
t_horse_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_horse_container)

story.append(PageBreak())

# --- PAGE 2: 15-MIN CHECK-IN & I-STATEMENT BUILDER ---
header_p2 = [
    [
        Paragraph("<b>МОДУЛИ 3 и 4: РЕГУЛЯРНАЯ ГИГИЕНА И ПРАКТИКА Я-ВЫСКАЗЫВАНИЙ</b>", badge_style),
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

# Block 3: Weekly Check-in
check_box = [
    [Paragraph("<b>МОДУЛЬ 3. Протокол еженедельного 15-минутного «Парного чек-ина»</b>", h1_style)],
    [Paragraph("Регулярная 15-минутная сверка раз в неделю без телефонов и детей (говорит один, второй не перебивает):", body_style)],
    [Spacer(1, 1*mm)]
]
table_check = [
    [Paragraph("<b>Вопрос 1 (Признательность):</b> <i>«Что хорошего и ценного ты сделал(а) для меня на этой неделе, за что я благодарен(на)?»</i><br/>Ответ: ________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Вопрос 2 (Бережная уязвимость):</b> <i>«В какой момент на этой неделе ты почувствовал(а) грусть, обиду или отдаление со мной?»</i><br/>Ответ: ________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Вопрос 3 (Забота и поддержка):</b> <i>«Как я могу позаботиться о тебе и облегчить твою нагрузку на следующей неделе?»</i><br/>Ответ: ________________________________________________________________________________________________", body_style)]
]
t_check_tab = Table(table_check, colWidths=[178*mm])
t_check_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
]))
check_box.append([t_check_tab])
t_check_container = Table(check_box, colWidths=[182*mm])
t_check_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_check_container)
story.append(Spacer(1, 4*mm))

# Block 4: I-Statement Builder
i_box = [
    [Paragraph("<b>МОДУЛЬ 4. Конструктор безопасного «Я-сообщения» для пары</b>", h1_style)],
    [Paragraph("Формула решения сложного вопроса без вызова защитной реакции партнера:", body_style)],
    [Spacer(1, 1*mm)]
]
table_i = [
    [Paragraph("<b>1. Нейтральный факт без ярлыков:</b> <i>«Когда происходит _________________________________________________»</i>", body_style)],
    [Paragraph("<b>2. Мое уязвимое чувство:</b> <i>«...я чувствую (тревогу / грусть / одиночество / перегруз) ___________________»</i>", body_style)],
    [Paragraph("<b>3. Моя важная потребность:</b> <i>«...потому что для меня важно чувствовать (надежность / уважение / контакт) ___»</i>", body_style)],
    [Paragraph("<b>4. Конкретная просьба:</b> <i>«Пожалуйста, давай в следующий раз __________________________________________»</i>", body_style)],
    [Paragraph("<i>Наше соглашение: мы обязуемся использовать эту формулу вместо внезапных претензий. Подписи: ____________________</i>", small_style)]
]
t_i_tab = Table(table_i, colWidths=[178*mm])
t_i_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d8b4fe')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
]))
i_box.append([t_i_tab])
t_i_container = Table(i_box, colWidths=[182*mm])
t_i_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#faf5ff')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#c084fc')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_i_container)

doc.build(story)
print("SUCCESS: Couple Level 2 PDF generated.")
