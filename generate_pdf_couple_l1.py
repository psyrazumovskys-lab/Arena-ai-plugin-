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

pdf_path = "therapy-workbooks/couple_workbook_1_stop_escalation.pdf"

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
    textColor=colors.HexColor('#be185d')
)

h1_style = ParagraphStyle(
    'H1',
    fontName='DejaVu-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#831843'),
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

# --- PAGE 1: PHYSIOLOGY, TIMEOUT & PHRASES ---
header_data = [
    [
        Paragraph("<b>УРОВЕНЬ 1 • ЭКСПРЕСС-ПРАКТИКУМ ДЛЯ ПАРЫ</b>", badge_style),
        Paragraph("Бесплатный экспресс-гайд", small_style)
    ],
    [
        Paragraph("Стоп-кран для ссоры: Как остановить эскалацию за 3 минуты", title_style),
        Paragraph("Дата: _____________", body_style)
    ],
    [
        Paragraph("Физиология эмоционального шторма, алгоритм безопасной паузы и шпаргалка фраз.", subtitle_style),
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

# Block 1: Flooding Test
flood_box = [
    [Paragraph("<b>1. Шкала эмоционального затопления (Flooding)</b>", h1_style)],
    [Paragraph("При пульсе >100 уд/мин мозг переходит в режим «бей или беги», и диалог физиологически блокируется:", body_style)],
    [Spacer(1, 1*mm)]
]
table_flood = [
    [Paragraph("<b>Физиологические маркеры (отметьте, если чувствуете прямо сейчас):</b>", body_bold)],
    [Paragraph("[ ] Учащенное сердцебиение, жар в груди или лице &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] Поверхностное или сдавленное дыхание", body_style)],
    [Paragraph("[ ] Туннельное зрение: партнер воспринимается как враг &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] Желание крикнуть или хлопнуть дверью", body_style)],
    [Paragraph("<i>⚠️ Если совпало 2 и более признака у любого из партнеров — продолжать спор запрещено: вы травмируете связь.</i>", small_style)]
]
t_flood_tab = Table(table_flood, colWidths=[178*mm])
t_flood_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fbcfe8')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
flood_box.append([t_flood_tab])
t_flood_container = Table(flood_box, colWidths=[182*mm])
t_flood_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff5f8')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f472b6')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_flood_container)
story.append(Spacer(1, 3.5*mm))

# Block 2: Timeout Protocol
time_box = [
    [Paragraph("<b>2. Протокол бережного тайм-аута (Без чувства брошенности)</b>", h1_style)],
    [Paragraph("Не хлопайте дверью. Здоровый тайм-аут состоит из трех шагов:", body_style)],
    [Spacer(1, 1*mm)]
]
table_time = [
    [Paragraph("<b>Шаг 1. Подтверждение ценности:</b>", body_bold), Paragraph("<i>«Я люблю тебя, наши отношения для меня очень важны...»</i>", body_style)],
    [Paragraph("<b>Шаг 2. Признание перегрузки:</b>", body_bold), Paragraph("<i>«...но прямо сейчас я перегружен(а) эмоциями и боюсь наговорить лишнего...»</i>", body_style)],
    [Paragraph("<b>Шаг 3. Точное время возвращения:</b>", body_bold), Paragraph("<i>«...давай сделаем паузу на 20 минут. Я умоюсь/подышу и вернусь ровно в ____:____, чтобы спокойно продолжить».</i>", body_style)],
    [Paragraph("<b>Правило паузы:</b>", body_bold), Paragraph("20 минут прохладной воды, дыхания и тишины. Запрещено мысленно репетировать обвинения.", small_style)]
]
t_time_tab = Table(table_time, colWidths=[55*mm, 123*mm])
t_time_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
time_box.append([t_time_tab])
t_time_container = Table(time_box, colWidths=[182*mm])
t_time_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_time_container)
story.append(Spacer(1, 3.5*mm))

# Block 3: Emergency Phrases
phrase_box = [
    [Paragraph("<b>3. Шпаргалка фраз-огнетушителей (Мгновенное снижение накала)</b>", h1_style)],
    [Spacer(1, 0.5*mm)]
]
table_phrase = [
    [Paragraph("<b>🗣️ Если накатывает злость и претензии:</b>", body_bold), Paragraph("<b>🛡️ Если хочется закрыться и замолчать:</b>", body_bold)],
    [Paragraph("• «Я злюсь не на тебя, я очень устал(а) от ситуации»<br/>• «Мне важно то, что ты говоришь. Помоги мне понять»<br/>• «Кажется, мы воюем друг с другом, хотя проблема общая»", body_style),
     Paragraph("• «Я не ухожу от тебя, мне нужно 5 минут тишины»<br/>• «Я слышу твою боль. Давай снизим тон, чтобы я услышал(а)»<br/>• «Ты мне очень дорог(а). Я хочу найти решение вместе»", body_style)]
]
t_phrase_tab = Table(table_phrase, colWidths=[89*mm, 89*mm])
t_phrase_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fdf2f8')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fbcfe8')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
phrase_box.append([t_phrase_tab])
t_phrase_container = Table(phrase_box, colWidths=[182*mm])
t_phrase_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f472b6')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_phrase_container)

story.append(PageBreak())

# --- PAGE 2: TRIGGER MAP & FAIR FIGHT CONTRACT ---
header_p2 = [
    [
        Paragraph("<b>ИНТЕРАКТИВНАЯ ПРАКТИКА: КАРТА ТРИГГЕРОВ И КОНТРАКТ БЕЗОПАСНОСТИ</b>", badge_style),
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

# Block 4: Dual Trigger Map
trig_box = [
    [Paragraph("<b>4. Индивидуальная карта триггеров: «Что взрывает нас быстрее всего»</b>", h1_style)],
    [Paragraph("Отметьте реакции и действия партнера, которые мгновенно выводят вас из равновесия:", body_style)],
    [Spacer(1, 1*mm)]
]
table_trig = [
    [Paragraph("<b>👤 Партнер 1</b>", body_bold), Paragraph("<b>👤 Партнер 2</b>", body_bold)],
    [Paragraph("[ ] Закатывание глаз / глубокие вздохи<br/>[ ] Перебивание на полуслове<br/>[ ] Сарказм, насмешки или повышенный тон<br/>[ ] Припоминание прошлых ошибок и обид<br/>Мой личный триггер: ________________________", body_style),
     Paragraph("[ ] Закатывание глаз / глубокие вздохи<br/>[ ] Перебивание на полуслове<br/>[ ] Сарказм, насмешки или повышенный тон<br/>[ ] Припоминание прошлых ошибок и обид<br/>Мой личный триггер: ________________________", body_style)]
]
t_trig_tab = Table(table_trig, colWidths=[89*mm, 89*mm])
t_trig_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
trig_box.append([t_trig_tab])
t_trig_container = Table(trig_box, colWidths=[182*mm])
t_trig_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_trig_container)
story.append(Spacer(1, 4*mm))

# Block 5: Fair Fight Contract
contract_box = [
    [Paragraph("<b>5. Парный контракт безопасности: «Правила боя» и Стоп-слово</b>", h1_style)],
    [Paragraph("Три нерушимых правила для любого разногласия в нашей паре:", body_style)],
    [Spacer(1, 1*mm)]
]
table_contract = [
    [Paragraph("🚫 <b>Табу 1:</b> Никаких оскорблений личности и обобщений («Ты вечно...», «Ты никогда...»).", body_style)],
    [Paragraph("🚫 <b>Табу 2:</b> Запрет на угрозы расставанием, разводом или сбором вещей во время ссоры.", body_style)],
    [Paragraph("🚫 <b>Табу 3:</b> Никаких демонстративных уходов без точного времени возвращения.", body_style)],
    [Paragraph("🛑 <b>Наше общее стоп-слово для немедленной паузы:</b> ________________________________________<br/><i>(При произнесении этого слова спор останавливается обоими без споров и условий)</i>", body_bold)],
    [Paragraph("🤝 <b>Наш ритуал примирения после бури (микро-действие сегодня):</b><br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<i>Подписи партнеров: __________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; __________________________</i>", small_style)]
]
t_contract_tab = Table(table_contract, colWidths=[178*mm])
t_contract_tab.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fbcfe8')),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
]))
contract_box.append([t_contract_tab])
t_contract_container = Table(contract_box, colWidths=[182*mm])
t_contract_container.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff5f8')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f472b6')),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_contract_container)

doc.build(story)
print("SUCCESS: Couple Level 1 PDF generated.")
