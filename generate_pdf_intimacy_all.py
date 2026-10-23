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
    textColor=colors.HexColor('#e11d48')
)

h1_style = ParagraphStyle(
    'H1',
    fontName='DejaVu-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#9f1239'),
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

# ----------------- BUILD L1 -----------------
doc1 = SimpleDocTemplate(
    "therapy-workbooks/intimacy_workbook_1_unfreeze.pdf",
    pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm
)
s1 = []
# P1
h_data1 = [
    [Paragraph("<b>УРОВЕНЬ 1 • ЭКСПРЕСС-ГАЙД ДЛЯ ПАРЫ</b>", badge_style), Paragraph("Бесплатный экспресс-гайд", small_style)],
    [Paragraph("Разморозка близости: Как перестать быть просто соседями", title_style), Paragraph("Дата: _____________", body_style)],
    [Paragraph("Диагностика отчуждения, 3 окситоциновых ритуала и цифровая граница в спальне.", subtitle_style), Paragraph("Пара: _____________", body_style)]
]
t_h1 = Table(h_data1, colWidths=[135*mm, 47*mm])
t_h1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 1)]))
s1.append(t_h1)
s1.append(Spacer(1, 2*mm))

box1_1 = [
    [Paragraph("<b>1. Тест: «Симптомы эмоционального охлаждения в паре»</b>", h1_style)],
    [Paragraph("Отметьте маркеры бытового отчуждения за последние 1–3 месяца:", body_style)],
    [Spacer(1, 1*mm)]
]
tab1_1 = [
    [Paragraph("[ ] Разговоры свелись только к быту, детям и покупкам («логистический кооператив»)<br/>[ ] Вечером каждый уходит в свой экран (телефон/сериал) без общения вдвоем<br/>[ ] Пропали спонтанные нежные прикосновения, объятия без повода и флирт<br/>[ ] Ощущение «одиночества вдвоем»: физически рядом, но эмоционально чужие<br/><i>📌 Если совпало от 2 пунктов: это не крах, а дефицит подпитки контакта.</i>", body_style)]
]
t_tab1_1 = Table(tab1_1, colWidths=[178*mm])
t_tab1_1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff5f6')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fecdd3')), ('PADDING', (0,0), (-1,-1), 4)]))
box1_1.append([t_tab1_1])
t_b1_1 = Table(box1_1, colWidths=[182*mm])
t_b1_1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f43f5e')), ('PADDING', (0,0), (-1,-1), 5)]))
s1.append(t_b1_1)
s1.append(Spacer(1, 3.5*mm))

box1_2 = [
    [Paragraph("<b>2. «Окситоциновый мост»: 3 пятиминутных ритуала воссоединения</b>", h1_style)],
    [Spacer(1, 0.5*mm)]
]
tab1_2 = [
    [Paragraph("<b>Ритуал 1. Правило 20-секундного объятия:</b>", body_bold), Paragraph("Обнять партнера ровно на 20 секунд полной грудью без слов. Именно через 20 секунд падает кортизол и активируется окситоцин.", body_style)],
    [Paragraph("<b>Ритуал 2. Минута мягкого взгляда:</b>", body_bold), Paragraph("Отложить телефоны и 60 секунд смотреть друг другу в глаза, сделав 3 глубоких выдоха. Это мгновенно возвращает контакт.", body_style)],
    [Paragraph("<b>Ритуал 3. Светящийся вопрос перед сном:</b>", body_bold), Paragraph("<i>«Что самое приятное случилось с тобой сегодня?»</i> или <i>«За что ты благодарен(на) сегодняшнему дню?»</i>.", body_style)]
]
t_tab1_2 = Table(tab1_2, colWidths=[55*mm, 123*mm])
t_tab1_2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 3.5), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box1_2.append([t_tab1_2])
t_b1_2 = Table(box1_2, colWidths=[182*mm])
t_b1_2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))
s1.append(t_b1_2)

s1.append(PageBreak())

# P2
s1.append(Table([[Paragraph("<b>ПРАКТИКА СБЛИЖЕНИЯ: КАРТА ТЕПЛА И ДОГОВОР СПАЛЬНИ</b>", badge_style), Paragraph("Страница 2 из 2", small_style)]], colWidths=[140*mm, 42*mm]))
s1.append(Spacer(1, 2*mm))

box1_3 = [
    [Paragraph("<b>3. Карта тепла: «Что возвращает мне ощущение любимости»</b>", h1_style)],
    [Paragraph("Отметьте проявления, которые зажигают тепло именно в вас:", body_style)],
    [Spacer(1, 1*mm)]
]
tab1_3 = [
    [Paragraph("<b>👤 Партнер 1: Я чувствую любовь, когда ты:</b>", body_bold), Paragraph("<b>👤 Партнер 2: Я чувствую любовь, когда ты:</b>", body_bold)],
    [Paragraph("[ ] Нежно обнимаешь / берешь за руку<br/>[ ] Внимательно слушаешь без советов<br/>[ ] Разгружаешь меня в быту без просьб<br/>[ ] Говоришь слова восхищения / комплимент<br/>Мой личный пункт: ______________________", body_style),
     Paragraph("[ ] Нежно обнимаешь / берешь за руку<br/>[ ] Внимательно слушаешь без советов<br/>[ ] Разгружаешь меня в быту без просьб<br/>[ ] Говоришь слова восхищения / комплимент<br/>Мой личный пункт: ______________________", body_style)]
]
t_tab1_3 = Table(tab1_3, colWidths=[89*mm, 89*mm])
t_tab1_3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box1_3.append([t_tab1_3])
t_b1_3 = Table(box1_3, colWidths=[182*mm])
t_b1_3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))
s1.append(t_b1_3)
s1.append(Spacer(1, 4*mm))

box1_4 = [
    [Paragraph("<b>4. Микро-договор пары: «Цифровой детокс в постели» и вечерний контакт</b>", h1_style)],
    [Spacer(1, 1*mm)]
]
tab1_4 = [
    [Paragraph("📵 <b>Правило спальни:</b> За 30 минут до сна все телефоны откладываются в беззвучном режиме экраном вниз. Кровать — пространство для сна, разговоров и ласки.", body_style)],
    [Paragraph("🤝 <b>Наше совместное микро-действие сегодня вечером:</b><br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<i>Подписи партнеров: __________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; __________________________</i>", small_style)]
]
t_tab1_4 = Table(tab1_4, colWidths=[178*mm])
t_tab1_4.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fecdd3')), ('PADDING', (0,0), (-1,-1), 4)]))
box1_4.append([t_tab1_4])
t_b1_4 = Table(box1_4, colWidths=[182*mm])
t_b1_4.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fff5f6')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f43f5e')), ('PADDING', (0,0), (-1,-1), 5)]))
s1.append(t_b1_4)

doc1.build(s1)
print("SUCCESS: Intimacy L1 PDF")

# ----------------- BUILD L2 -----------------
badge_l2 = ParagraphStyle('Badge2', fontName='DejaVu-Bold', fontSize=7, leading=8, textColor=colors.HexColor('#db2777'))
h1_l2 = ParagraphStyle('H12', fontName='DejaVu-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#9d174d'), spaceAfter=1.5*mm)

doc2 = SimpleDocTemplate(
    "therapy-workbooks/intimacy_workbook_2_tenderness.pdf",
    pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm
)
s2 = []
h_data2 = [
    [Paragraph("<b>УРОВЕНЬ 2 • САМОСТОЯТЕЛЬНЫЙ ПРАКТИКУМ ДЛЯ ПАРЫ</b>", badge_l2), Paragraph("Домашний практикум", small_style)],
    [Paragraph("Территория нежности: Практикум возрождения тепла и флирта", title_style), Paragraph("Дата: _____________", body_style)],
    [Paragraph("Свидание без быта, 12 глубоких вопросов и инвентаризация чистой тактильности.", subtitle_style), Paragraph("Пара: _____________", body_style)]
]
s2.append(Table(h_data2, colWidths=[135*mm, 47*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 1)]))
s2.append(Spacer(1, 2*mm))

box2_1 = [
    [Paragraph("<b>МОДУЛЬ 1. Конструктор «Свидания без быта и детей»</b>", h1_l2)],
    [Paragraph("Правила безопасного эмоционального пространства на 2 часа:", body_style)],
    [Spacer(1, 1*mm)]
]
tab2_1 = [
    [Paragraph("<b>Правило 1. «Красная зона тем»:</b> Запрещено обсуждать быт, ремонт, счета и детские кружки. Мягкий пароль возврата: <i>«Возвращаемся на свидание»</i>.", body_style)],
    [Paragraph("<b>Правило 2. Смена контекста:</b> Не дома на диване. Новая кофейня, вечерняя прогулка по набережной, пикник на полу при свечах.", body_style)],
    [Paragraph("<b>План нашего свидания на этой неделе:</b><br/>Место, день и время: ______________________________________________________________________________", body_style)]
]
t_tab2_1 = Table(tab2_1, colWidths=[178*mm])
t_tab2_1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fdf2f8')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fbcfe8')), ('PADDING', (0,0), (-1,-1), 3.5)]))
box2_1.append([t_tab2_1])
s2.append(Table(box2_1, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f472b6')), ('PADDING', (0,0), (-1,-1), 5)]))
s2.append(Spacer(1, 3.5*mm))

box2_2 = [
    [Paragraph("<b>МОДУЛЬ 2. 12 безопасных вопросов для разговора по душам</b>", h1_l2)],
    [Paragraph("Выберите 2–3 вопроса на вечер при свечах. Слушайте без критики и споров:", body_style)],
    [Spacer(1, 1*mm)]
]
tab2_2 = [
    [Paragraph("1. «Какое самое теплое воспоминание обо мне у тебя сохранилось за этот год?»<br/>2. «О чем ты мечтаешь прямо сейчас, но пока откладываешь?»<br/>3. «В какой момент ты чувствуешь себя самым(ой) красивым(ой) и желанным(ой)?»", body_style),
     Paragraph("4. «Какая моя привычка до сих пор тебя умиляет или радует?»<br/>5. «Если бы мы могли прямо сейчас улететь на уикенд — куда бы ты захотел(а)?»<br/>6. «Как я могу поддержать тебя в твоем личном увлечении на этой неделе?»", body_style)]
]
t_tab2_2 = Table(tab2_2, colWidths=[89*mm, 89*mm])
t_tab2_2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box2_2.append([t_tab2_2])
s2.append(Table(box2_2, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s2.append(PageBreak())

# L2 P2
s2.append(Table([[Paragraph("<b>МОДУЛЬ 3: ИНВЕНТАРИЗАЦИЯ ТАКТИЛЬНОСТИ И НЕЖНОСТИ</b>", badge_l2), Paragraph("Страница 2 из 2", small_style)]], colWidths=[140*mm, 42*mm]))
s2.append(Spacer(1, 2*mm))

box2_3 = [
    [Paragraph("<b>МОДУЛЬ 3. Инвентаризация тактильности: «Ласка без давления»</b>", h1_l2)],
    [Paragraph("Снятие тревоги: объятия и массаж с четкой договоренностью «без обязательного секса»:", body_style)],
    [Spacer(1, 1*mm)]
]
tab2_3 = [
    [Paragraph("<b>Практика «10 минут чистой нежности»:</b> Массаж плеч, поглаживание волос или держание за руки. Партнеры заранее знают: это только забота о теле, без требований продолжать интим. Это снимает страх и возвращает спонтанность прикосновений.", body_style)],
    [Paragraph("<b>👤 Пожелание Партнера 1:</b> Какое прикосновение сейчас нужно моему телу:<br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>👤 Пожелание Партнера 2:</b> Какое прикосновение сейчас нужно моему телу:<br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<i>Наше соглашение: мы возвращаем нежность в наш дом шаг за шагом. Подписи: __________________________</i>", small_style)]
]
t_tab2_3 = Table(tab2_3, colWidths=[178*mm])
t_tab2_3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fbcfe8')), ('PADDING', (0,0), (-1,-1), 4)]))
box2_3.append([t_tab2_3])
s2.append(Table(box2_3, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fdf2f8')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#f472b6')), ('PADDING', (0,0), (-1,-1), 5)]))

doc2.build(s2)
print("SUCCESS: Intimacy L2 PDF")

# ----------------- BUILD L3 -----------------
badge_l3 = ParagraphStyle('Badge3', fontName='DejaVu-Bold', fontSize=7, leading=8, textColor=colors.HexColor('#c026d3'))
h1_l3 = ParagraphStyle('H13', fontName='DejaVu-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#86198f'), spaceAfter=1.5*mm)

doc3 = SimpleDocTemplate(
    "therapy-workbooks/intimacy_workbook_3_reconnection.pdf",
    pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm
)
s3 = []
h_data3 = [
    [Paragraph("<b>УРОВЕНЬ 3 • КЛИНИЧЕСКИЙ ПРАКТИКУМ ДЛЯ ПАРЫ</b>", badge_l3), Paragraph("Семейная терапия", small_style)],
    [Paragraph("Реконструкция эмоциональной связи: Преодоление отчуждения", title_style), Paragraph("Дата сессии: _____________", body_style)],
    [Paragraph("Барьеры уязвимости, инвентаризация скрытых обид и терапевтический протокол.", subtitle_style), Paragraph("Пара: _____________________", body_style)]
]
s3.append(Table(h_data3, colWidths=[132*mm, 50*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 1)]))
s3.append(Spacer(1, 2*mm))

box3_1 = [
    [Paragraph("<b>МОДУЛЬ 1. Барьеры уязвимости: «Почему стало страшно открываться»</b>", h1_l3)],
    [Paragraph("Отчуждение наступает, когда открытость начинает казаться небезопасной:", body_style)],
    [Spacer(1, 1*mm)]
]
tab3_1 = [
    [Paragraph("<b>👤 Партнер 1: Что останавливает сделать шаг к теплу:</b>", body_bold), Paragraph("<b>👤 Партнер 2: Что останавливает сделать шаг к теплу:</b>", body_bold)],
    [Paragraph("Страх быть отвергнутым(ой), насмешки, холодный взгляд или усталость:<br/><br/>________________________________________", body_style),
     Paragraph("Обида на прошлые слова, чувство неоцененности, закрытость:<br/><br/>________________________________________", body_style)]
]
t_tab3_1 = Table(tab3_1, colWidths=[89*mm, 89*mm])
t_tab3_1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fae8ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e879f9')), ('PADDING', (0,0), (-1,-1), 4), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box3_1.append([t_tab3_1])
s3.append(Table(box3_1, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fdf4ff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#d946ef')), ('PADDING', (0,0), (-1,-1), 5)]))
s3.append(Spacer(1, 3.5*mm))

box3_2 = [
    [Paragraph("<b>МОДУЛЬ 2. Инвентаризация скрытых обид, блокирующих влечение</b>", h1_l3)],
    [Spacer(1, 0.5*mm)]
]
tab3_2 = [
    [Paragraph("<b>Эпизод или период, когда между нами выросла «ледяная стена» (рождение ребенка, кризис, холод в тяжелый момент):</b><br/>____________________________________________________________________________________________________<br/>____________________________________________________________________________________________________", body_style)]
]
t_tab3_2 = Table(tab3_2, colWidths=[178*mm])
t_tab3_2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)]))
box3_2.append([t_tab3_2])
s3.append(Table(box3_2, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# L3 P2
s3.append(Table([[Paragraph("<b>МОДУЛИ 3 и 4: ПОВЕСТКА СЕССИИ И ТЕРАПЕВТИЧЕСКИЙ ПРОТОКОЛ</b>", badge_l3), Paragraph("Страница 2 из 2", small_style)]], colWidths=[140*mm, 42*mm]))
s3.append(Spacer(1, 2*mm))

box3_3 = [
    [Paragraph("<b>МОДУЛЬ 3. Повестка совместной терапевтической сессии (Agenda)</b>", h1_l3)],
    [Spacer(1, 1*mm)]
]
tab3_3 = [
    [Paragraph("[  ] <b>Возврат тактильности и интимности:</b> снятие чувства вины и напряжения вокруг сексуальной сферы.", body_style)],
    [Paragraph("[  ] <b>Преодоление цифровой зависимости:</b> границы гаджетов и вечернего присутствия в спальне.", body_style)],
    [Paragraph("[  ] <b>Родительское выгорание:</b> как снова стать парой и любовниками, а не только «мамой и папой».", body_style)],
    [Paragraph("[  ] <b>Исцеление старой травмы:</b> честный разговор о ситуации, которая до сих пор отзывается болью.", body_style)],
    [Paragraph("<b>Индивидуальный запрос пары к семейному психологу:</b><br/>____________________________________________________________________________________________________", body_style)]
]
t_tab3_3 = Table(tab3_3, colWidths=[178*mm])
t_tab3_3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 3.5)]))
box3_3.append([t_tab3_3])
s3.append(Table(box3_3, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))
s3.append(Spacer(1, 4*mm))

box3_4 = [
    [Paragraph("<b>МОДУЛЬ 4. Совместный терапевтический протокол сессии</b>", h1_l3)],
    [Spacer(1, 1*mm)]
]
tab3_4 = [
    [Paragraph("<b>💡 Инсайт пары о нашем отчуждении:</b>", body_bold), Paragraph("<b>🎯 Микро-шаг к сближению до следующей встречи:</b>", body_bold)],
    [Paragraph("Что стало истинной причиной нашей дистанции:<br/><br/><br/><br/>", body_style),
     Paragraph("Конкретное простое действие тепла (1 свидание / вечер без экранов):<br/><br/><br/><br/>", body_style)],
    [Paragraph("<i>Подпись Партнера 1: ____________________________</i>", small_style),
     Paragraph("<i>Подпись Партнера 2: ____________________________</i>", small_style)]
]
t_tab3_4 = Table(tab3_4, colWidths=[89*mm, 89*mm])
t_tab3_4.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fae8ff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e879f9')), ('PADDING', (0,0), (-1,-1), 4), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box3_4.append([t_tab3_4])
s3.append(Table(box3_4, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fdf4ff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#d946ef')), ('PADDING', (0,0), (-1,-1), 5)]))

doc3.build(s3)
print("SUCCESS: Intimacy L3 PDF")
