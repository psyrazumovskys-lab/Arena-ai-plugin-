import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

pdf_path = "therapy-workbooks/workbook_2_self_mastery.pdf"

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
    textColor=colors.HexColor('#1d4ed8')
)

h1_style = ParagraphStyle(
    'H1',
    fontName='DejaVu-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#1e293b'),
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

# --- PAGE 1: AUDIT & BODY SIGNALS ---
# Header
header_data = [
    [
        Paragraph("<b>УРОВЕНЬ 2 • САМОСТОЯТЕЛЬНЫЙ ПРАКТИКУМ</b>", badge_style),
        Paragraph("Личный экземпляр", small_style)
    ],
    [
        Paragraph("Искусство твердого «Нет»: Личные границы и ресурс", title_style),
        Paragraph("Дата: _____________", body_style)
    ],
    [
        Paragraph("Рабочая тетрадь углубленной саморефлексии. Модули 1 и 2: ревизия утечек энергии и телесный компас.", subtitle_style),
        Paragraph("", body_style)
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

# Block 1: Audit
audit_box = [
    [Paragraph("<b>МОДУЛЬ 1. Аудит утечек ресурса: кому и почему трудно отказывать</b>", h1_style)],
    [Paragraph("Вспомните 2 недавние ситуации, когда вы согласились вопреки внутреннему протесту или усталости.", body_style)],
    [Spacer(1, 1*mm)]
]
table_audit_rows = [
    [Paragraph("<b>Контекст ситуации и просьба</b>", body_bold), 
     Paragraph("<b>Что помешало отказать?</b>", body_bold), 
     Paragraph("<b>Реальная цена согласия (время, силы)</b>", body_bold)],
    [Paragraph("<i>Ситуация 1 (работа/коллеги):</i><br/><br/>", body_style),
     Paragraph("Опасение показаться ненадёжным / конфликт / долг", small_style),
     Paragraph("", body_style)],
    [Paragraph("<i>Ситуация 2 (семья/близкие):</i><br/><br/>", body_style),
     Paragraph("Чувство вины / страх расстроить близкого", small_style),
     Paragraph("", body_style)]
]
t_audit = Table(table_audit_rows, colWidths=[65*mm, 57*mm, 56*mm])
t_audit.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
audit_box.append([t_audit])
t_audit_container = Table(audit_box, colWidths=[182*mm])
t_audit_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 6),
]))
story.append(t_audit_container)
story.append(Spacer(1, 4*mm))

# Block 2: Somatic Compass
somatic_box = [
    [Paragraph("<b>МОДУЛЬ 2. Телесный компас: распознавание импульса до включения головы</b>", h1_style)],
    [Paragraph("Тело подает сигнал за доли секунды до того, как включается привычка быть «удобным». Зафиксируйте свои телесные маркеры.", body_style)],
    [Spacer(1, 1*mm)]
]
table_soma = [
    [Paragraph("<b>Зона тела</b>", body_bold), Paragraph("<b>Ощущение при согласии «из вины»</b>", body_bold), Paragraph("<b>Ощущение при спокойном отказе</b>", body_bold)],
    [Paragraph("<b>Горло / дыхание</b>", body_style), Paragraph("[ ] Ком в горле, задержка дыхания, сдавленность", body_style), Paragraph("[ ] Глубокий ровный выдох, свободное дыхание", body_style)],
    [Paragraph("<b>Плечи / шея</b>", body_style), Paragraph("[ ] Напряжение, втягивание головы, тяжесть", body_style), Paragraph("[ ] Плечи опущены, шея расслаблена", body_style)],
    [Paragraph("<b>Живот / солнечное сплетение</b>", body_style), Paragraph("[ ] Сжатие, холодок, тошнота, спазм", body_style), Paragraph("[ ] Тепло, устойчивость, опора внутри", body_style)],
    [Paragraph("<b>Мой главный личный маркер</b>", body_bold), Paragraph("Как именно моё тело кричит «я не хочу этого делать»:<br/><br/>", body_style), Paragraph("Моя опора: <i>«Я доверяю сигналам своего тела»</i>", small_style)]
]
t_soma_tab = Table(table_soma, colWidths=[45*mm, 70*mm, 63*mm])
t_soma_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
somatic_box.append([t_soma_tab])
t_soma_container = Table(somatic_box, colWidths=[182*mm])
t_soma_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 6),
]))
story.append(t_soma_container)

story.append(PageBreak())

# --- PAGE 2: CONSTRUCTOR, FIRST AID & CODE ---
header_p2 = [
    [
        Paragraph("<b>МОДУЛИ 3, 4 и 5: ПРАКТИКА И ЗАКРЕПЛЕНИЕ ГРАНИЦ</b>", badge_style),
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

# Block 3: Constructor
const_box = [
    [Paragraph("<b>МОДУЛЬ 3. Конструктор экологичного отказа: 3-шаговая формула</b>", h1_style)],
    [Paragraph("<b>Формула:</b> [1. Валидация важности] + [2. Чёткое «Нет» без оправданий] + [3. Альтернатива или точка].", body_style)],
    [Spacer(1, 1*mm)]
]
table_const = [
    [Paragraph("<b>Шаг формулы</b>", body_bold), Paragraph("<b>Пример формулировки</b>", body_bold), Paragraph("<b>Мой рабочий черновик для текущей ситуации</b>", body_bold)],
    [Paragraph("<b>1. Валидация</b>", body_style), Paragraph("<i>«Я понимаю, насколько срочная эта задача...»</i>", small_style), Paragraph("<br/>", body_style)],
    [Paragraph("<b>2. Прямой отказ</b>", body_style), Paragraph("<i>«...но я не смогу взять её на себя сегодня.»</i>", small_style), Paragraph("<br/>", body_style)],
    [Paragraph("<b>3. Альтернатива / точка</b>", body_style), Paragraph("<i>«Могу вернуться к ней в понедельник / Предлагаю обратиться к X.»</i>", small_style), Paragraph("<br/>", body_style)],
]
t_const_tab = Table(table_const, colWidths=[40*mm, 68*mm, 70*mm])
t_const_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
const_box.append([t_const_tab])
t_const_container = Table(const_box, colWidths=[182*mm])
t_const_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_const_container)
story.append(Spacer(1, 3.5*mm))

# Block 4: First Aid
aid_box = [
    [Paragraph("<b>МОДУЛЬ 4. Аптечка самопомощи: что делать, когда накрывает вина</b>", h1_style)],
    [Paragraph("Чувство вины после отказа — это не признак ошибки, а симптом ломки старого паттерна.", body_style)],
    [Spacer(1, 1*mm)]
]
table_aid = [
    [Paragraph("<b>Ложная установка (внутренний критик)</b>", body_bold), Paragraph("<b>Здоровая реальность (поддерживающий голос)</b>", body_bold)],
    [Paragraph("«Если я откажу, я испорчу отношения и человек обидится»", body_style), Paragraph("«Зрелые отношения выдерживают отказ. Если они держатся только на моём безотказном согласии — это не близость, а использование.»", body_style)],
    [Paragraph("«Отказывать эгоистично, хороший человек всегда выручает»", body_style), Paragraph("«Забота о своих границах — необходимое условие устойчивости. Отказывая чужой задаче, я говорю 'Да' своему здоровью и семье.»", body_style)],
    [Paragraph("«Мне обязательно нужно объяснить уважительную причину»", body_style), Paragraph("«'Нет' — это полноценное предложение. Моё право отказаться не зависит от того, насколько убедительным кажется моё оправдание.»", body_style)]
]
t_aid_tab = Table(table_aid, colWidths=[80*mm, 98*mm])
t_aid_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
aid_box.append([t_aid_tab])
t_aid_container = Table(aid_box, colWidths=[182*mm])
t_aid_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_aid_container)
story.append(Spacer(1, 3.5*mm))

# Block 5: Personal Code
code_box = [
    [Paragraph("<b>МОДУЛЬ 5. Личный кодекс неснижаемых границ на ближайший месяц</b>", h1_style)],
    [Paragraph("Сформулируйте 3 четких правила, которые защищают ваш сон, время и внутреннее спокойствие.", body_style)],
    [Spacer(1, 1*mm)]
]
table_code = [
    [Paragraph("<b>1. В работе:</b> Я говорю твердое «Нет», если ____________________________________________________________________", body_style)],
    [Paragraph("<b>2. В близком кругу:</b> Я не соглашаюсь на ____________________________________________________________________", body_style)],
    [Paragraph("<b>3. Правило паузы:</b> Перед любым решением я беру минимум ________________________ времени на подумать.", body_style)],
    [Paragraph("<i>Личная подпись и дата принятия: _________________________________________</i>", small_style)]
]
t_code_tab = Table(table_code, colWidths=[178*mm])
t_code_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
code_box.append([t_code_tab])
t_code_container = Table(code_box, colWidths=[182*mm])
t_code_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_code_container)

doc.build(story)
print("SUCCESS: Level 2 PDF generated.")
