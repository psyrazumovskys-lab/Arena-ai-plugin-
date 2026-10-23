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

title_style = ParagraphStyle('DocTitle', fontName='DejaVu-Bold', fontSize=12.5, leading=15.5, textColor=colors.HexColor('#0f172a'), spaceAfter=1.5*mm)
subtitle_style = ParagraphStyle('DocSubtitle', fontName='DejaVu', fontSize=8, leading=10.5, textColor=colors.HexColor('#475569'), spaceAfter=2.5*mm)
badge_style = ParagraphStyle('Badge', fontName='DejaVu-Bold', fontSize=7, leading=8, textColor=colors.HexColor('#0d9488'))
h1_style = ParagraphStyle('H1', fontName='DejaVu-Bold', fontSize=9, leading=11.5, textColor=colors.HexColor('#115e59'), spaceAfter=1.5*mm)
body_style = ParagraphStyle('Body', fontName='DejaVu', fontSize=7.2, leading=9.5, textColor=colors.HexColor('#334155'))
body_bold = ParagraphStyle('BodyBold', fontName='DejaVu-Bold', fontSize=7.2, leading=9.5, textColor=colors.HexColor('#1e293b'))
small_style = ParagraphStyle('Small', fontName='DejaVu', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#64748b'))

# ==================== L1 (1 PAGE ONLY) ====================
doc1 = SimpleDocTemplate(
    "therapy-workbooks/self_esteem_workbook_1_anchor.pdf",
    pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=10*mm, bottomMargin=10*mm
)
s1 = []
h1_tab = [
    [Paragraph("<b>УРОВЕНЬ 1 • ЭКСПРЕСС-ГАЙД (1 СТРАНИЦА)</b>", badge_style), Paragraph("Бесплатный гайд", small_style)],
    [Paragraph("Внутренняя опора: Скорая помощь при самокритике", title_style), Paragraph("Дата: _____________", body_style)],
    [Paragraph("Экспресс-тест самооценки, техника Защитника и 3 факта о вашей ценности.", subtitle_style), Paragraph("Имя: _____________", body_style)]
]
t_h1 = Table(h1_tab, colWidths=[135*mm, 47*mm])
t_h1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0.5)]))
s1.append(t_h1)
s1.append(Spacer(1, 2*mm))

box1_1 = [
    [Paragraph("<b>1. Экспресс-тест: «На чем держится моя самооценка?»</b>", h1_style)],
    [Paragraph("Отметьте привычные реакции на похвалу и критику:", body_style)],
    [Spacer(1, 0.5*mm)]
]
t1_items = [
    [Paragraph("[ ] Если хвалят — я на высоте; если нейтральны или критикуют — чувствую себя никчемным(ой)<br/>[ ] Сложно сказать себе «я молодец», пока результат не идеален на 100%<br/>[ ] Постоянно сравниваю свои будни с чужими успехами в соцсетях не в свою пользу<br/>[ ] Трудно принимать комплименты: неловко, хочется оправдаться или отмахнуться<br/><i>💡 Совпадение 2 и более пунктов говорит о смещении опоры на внешнюю оценку.</i>", body_style)]
]
t_t1 = Table(t1_items, colWidths=[178*mm])
t_t1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdfa')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')), ('PADDING', (0,0), (-1,-1), 3.5)]))
box1_1.append([t_t1])
s1.append(Table(box1_1, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0d9488')), ('PADDING', (0,0), (-1,-1), 4)]))
s1.append(Spacer(1, 3*mm))

box1_2 = [
    [Paragraph("<b>2. Техника «Голос Защитника против Критика»</b>", h1_style)],
    [Spacer(1, 0.5*mm)]
]
t2_items = [
    [Paragraph("<b>Критик:</b> «Ты опять ошибся(лась), ничего нормально сделать не можешь!»", body_style),
     Paragraph("<b>Защитник:</b> «Ошибаться нормально. Ошибка показывает, что я пробую новое. Я сделаю вывод и пойду дальше».", body_style)],
    [Paragraph("<b>Критик:</b> «Посмотри на других — они успевают в два раза больше тебя!»", body_style),
     Paragraph("<b>Защитник:</b> «У каждого свой темп и ресурс. Я двигаюсь со своей здоровой скоростью и уважаю свои силы».", body_style)]
]
t_t2 = Table(t2_items, colWidths=[89*mm, 89*mm])
t_t2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 3.5), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box1_2.append([t_t2])
s1.append(Table(box1_2, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 4)]))
s1.append(Spacer(1, 3*mm))

box1_3 = [
    [Paragraph("<b>3. Моя внутренняя опора сегодня (Практика 3 минут)</b>", h1_style)],
    [Spacer(1, 0.5*mm)]
]
t3_items = [
    [Paragraph("<b>1. Трудность, с которой я успешно справился(лась) в жизни:</b><br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>2. Ценное качество моего характера, за которое меня уважают:</b><br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>3. За что я искренне благодарен(на) себе сегодня (даже за отдых):</b><br/>____________________________________________________________________________________________________", body_style)]
]
t_t3 = Table(t3_items, colWidths=[178*mm])
t_t3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')), ('PADDING', (0,0), (-1,-1), 3.5)]))
box1_3.append([t_t3])
s1.append(Table(box1_3, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdfa')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0d9488')), ('PADDING', (0,0), (-1,-1), 4)]))

doc1.build(s1)
print("SUCCESS: Self-Esteem L1 (1 page)")

# ==================== L2 (2 PAGES) ====================
badge_l2 = ParagraphStyle('BadgeL2', fontName='DejaVu-Bold', fontSize=7, leading=8, textColor=colors.HexColor('#0284c7'))
h1_l2 = ParagraphStyle('H1L2', fontName='DejaVu-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#0369a1'), spaceAfter=1.5*mm)

doc2 = SimpleDocTemplate(
    "therapy-workbooks/self_esteem_workbook_2_value.pdf",
    pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm
)
s2 = []
h2_tab = [
    [Paragraph("<b>УРОВЕНЬ 2 • САМОСТОЯТЕЛЬНЫЙ ПРАКТИКУМ (2 СТРАНИЦЫ)</b>", badge_l2), Paragraph("Практикум самооценки", small_style)],
    [Paragraph("Право на ценность: Преодоление синдрома самозванца", title_style), Paragraph("Дата: _____________", body_style)],
    [Paragraph("Дневник присвоения побед, стандарт «достаточно хорошо» и манифест самоценности.", subtitle_style), Paragraph("Имя: _____________", body_style)]
]
s2.append(Table(h2_tab, colWidths=[135*mm, 47*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 1)]))
s2.append(Spacer(1, 2*mm))

box2_1 = [
    [Paragraph("<b>МОДУЛЬ 1. Дневник присвоения побед: «Это не просто везение»</b>", h1_l2)],
    [Paragraph("Деконструкция обесценивания — возвращение авторства своим результатам:", body_style)],
    [Spacer(1, 1*mm)]
]
tab2_1 = [
    [Paragraph("<b>Мой результат или успех</b>", body_bold), Paragraph("<b>Обесценивание («самозванец»)</b>", body_bold), Paragraph("<b>Реальный личный вклад (факты)</b>", body_bold)],
    [Paragraph("<i>«Успешно сдал сложный проект»</i>", body_style), Paragraph("«Просто повезло с темой, любой бы смог»", small_style), Paragraph("Я работал 3 недели, применил свои навыки и опыт.", body_style)],
    [Paragraph("<i>Мое недавнее достижение:<br/><br/></i>", small_style), Paragraph("Как ум пытается обесценить:<br/><br/>", small_style), Paragraph("Мой реальный труд, время и знания:<br/><br/>", small_style)],
]
t_tab2_1 = Table(tab2_1, colWidths=[58*mm, 60*mm, 60*mm])
t_tab2_1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0f2fe')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')), ('PADDING', (0,0), (-1,-1), 4), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box2_1.append([t_tab2_1])
s2.append(Table(box2_1, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')), ('PADDING', (0,0), (-1,-1), 5)]))
s2.append(Spacer(1, 3.5*mm))

box2_2 = [
    [Paragraph("<b>МОДУЛЬ 2. Матрица перехода: от перфекционизма к «Достаточно хорошо»</b>", h1_l2)],
    [Paragraph("Перфекционизм парализует. Здоровый стандарт (Good Enough) возвращает энергию:", body_style)],
    [Spacer(1, 1*mm)]
]
tab2_2 = [
    [Paragraph("<b>Ловушка перфекционизма (страх ошибки)</b>", body_bold), Paragraph("<b>✅ Стандарт «Достаточно хорошо» (Good Enough)</b>", body_bold)],
    [Paragraph("• «Либо идеально, либо я неудачник»<br/>• Ошибка воспринимается как личный позор<br/>• Хроническое откладывание из-за страха критики", body_style),
     Paragraph("• «Сделанное на 80% лучше идеального в голове»<br/>• Ошибка = обычная рабочая обратная связь<br/>• Сохранение сил, уверенности и легкости", body_style)]
]
t_tab2_2 = Table(tab2_2, colWidths=[89*mm, 89*mm])
t_tab2_2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box2_2.append([t_tab2_2])
s2.append(Table(box2_2, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s2.append(PageBreak())

# L2 P2
s2.append(Table([[Paragraph("<b>МОДУЛЬ 3: МАНИФЕСТ БЕЗУСЛОВНОЙ САМОЦЕННОСТИ</b>", badge_l2), Paragraph("Страница 2 из 2", small_style)]], colWidths=[140*mm, 42*mm]))
s2.append(Spacer(1, 2*mm))

box2_3 = [
    [Paragraph("<b>МОДУЛЬ 3. Личный манифест безусловной самоценности на месяц</b>", h1_l2)],
    [Paragraph("Сформулируйте ваши внутренние правила бережного отношения к себе:", body_style)],
    [Spacer(1, 1*mm)]
]
tab2_3 = [
    [Paragraph("<b>1. Мое право на ошибку:</b><br/><i>«Я разрешаю себе ошибаться, потому что: ______________________________________________________________»</i>", body_style)],
    [Paragraph("<b>2. Мое право на отдых без оправданий:</b><br/><i>«Отдых — это базовое право, а не награда. Я не обязан(а) заслуживать паузу через изнеможение».</i>", body_style)],
    [Paragraph("<b>3. Фильтр сравнений:</b><br/><i>«Когда я ловлю себя на сравнении с другими в сети, я перевожу фокус на свой путь: _________________________»</i>", body_style)],
    [Paragraph("<i>Личная подпись: _________________________________________ Дата: ______________________</i>", small_style)]
]
t_tab2_3 = Table(tab2_3, colWidths=[178*mm])
t_tab2_3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')), ('PADDING', (0,0), (-1,-1), 4)]))
box2_3.append([t_tab2_3])
s2.append(Table(box2_3, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')), ('PADDING', (0,0), (-1,-1), 5)]))

doc2.build(s2)
print("SUCCESS: Self-Esteem L2 (2 pages)")

# ==================== L3 (3 PAGES) ====================
badge_l3 = ParagraphStyle('BadgeL3', fontName='DejaVu-Bold', fontSize=7, leading=8, textColor=colors.HexColor('#4f46e5'))
h1_l3 = ParagraphStyle('H1L3', fontName='DejaVu-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#312e81'), spaceAfter=1.5*mm)

doc3 = SimpleDocTemplate(
    "therapy-workbooks/self_esteem_workbook_3_depth.pdf",
    pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm
)
s3 = []

# L3 P1: SCHEMAS
h3_tab = [
    [Paragraph("<b>УРОВЕНЬ 3 • КЛИНИЧЕСКИЙ ПРАКТИКУМ (3 СТРАНИЦЫ)</b>", badge_l3), Paragraph("Психотерапия", small_style)],
    [Paragraph("Архитектура глубинного «Я»: Исцеление стыда и опора", title_style), Paragraph("Дата сессии: _____________", body_style)],
    [Paragraph("Исследование ранних схем, поведенческий эксперимент и терапевтический протокол.", subtitle_style), Paragraph("Клиент: ___________________", body_style)]
]
s3.append(Table(h3_tab, colWidths=[132*mm, 50*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 1)]))
s3.append(Spacer(1, 2*mm))

box3_1 = [
    [Paragraph("<b>МОДУЛЬ 1. Аудит ранних схем: «Откуда взялось недоверие к себе»</b>", h1_l3)],
    [Paragraph("Глубинная неуверенность — это эхо родительских и школьных установок:", body_style)],
    [Spacer(1, 1*mm)]
]
tab3_1 = [
    [Paragraph("<b>Схема дефективности: «Со мной что-то не так»</b><br/>Убеждение: <i>«Если люди узнают меня настоящего(ую), они разочаруются».</i><br/>Чей критикующий голос звучит за этой мыслью? В каких ситуациях детства возникал стыд:<br/><br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>Схема жестких стандартов: «Любовь нужно заслужить»</b><br/>Убеждение: <i>«Я ценен(на) только тогда, когда достигаю побед и безупречен(на)».</i><br/>Какие правила успеха и критики ошибок транслировались в семье:<br/><br/>____________________________________________________________________________________________________", body_style)]
]
t_tab3_1 = Table(tab3_1, colWidths=[178*mm])
t_tab3_1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')), ('PADDING', (0,0), (-1,-1), 4)]))
box3_1.append([t_tab3_1])
s3.append(Table(box3_1, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f3ff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#4f46e5')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# L3 P2: EXPERIMENT
s3.append(Table([[Paragraph("<b>МОДУЛЬ 2: ПРОТОКОЛ ПОВЕДЕНЧЕСКОГО ЭКСПЕРИМЕНТА</b>", badge_l3), Paragraph("Страница 2 из 3", small_style)]], colWidths=[140*mm, 42*mm]))
s3.append(Spacer(1, 2*mm))

box3_2 = [
    [Paragraph("<b>МОДУЛЬ 2. Поведенческий эксперимент: «Право проявиться»</b>", h1_l3)],
    [Paragraph("Самооценка растет не от размышлений, а от реального нового опыта проявления:", body_style)],
    [Spacer(1, 1*mm)]
]
tab3_2 = [
    [Paragraph("<b>1. Запланированное действие проявления (выбрать с терапевтом):</b><br/><i>(Например: высказать свое мнение на совещании, выложить свою работу, назвать честную цену)</i><br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>2. Катастрофический прогноз внутреннего критика:</b><br/><i>(«Они решат, что я глупый(ая) / надо мной посмеются / отвернутся»)</i><br/>____________________________________________________________________________________________________", body_style)],
    [Paragraph("<b>3. Фактический результат и новый вывод о себе:</b><br/><i>(Что произошло на самом деле? Какой новый опыт безопасности я получил(а)?)</i><br/>____________________________________________________________________________________________________", body_style)]
]
t_tab3_2 = Table(tab3_2, colWidths=[178*mm])
t_tab3_2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 4)]))
box3_2.append([t_tab3_2])
s3.append(Table(box3_2, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 5)]))

s3.append(PageBreak())

# L3 P3: AGENDA & THERAPIST CONTRACT
s3.append(Table([[Paragraph("<b>МОДУЛИ 3 и 4: ПОВЕСТКА СЕССИИ И ИНТЕГРАЦИЯ</b>", badge_l3), Paragraph("Страница 3 из 3", small_style)]], colWidths=[140*mm, 42*mm]))
s3.append(Spacer(1, 2*mm))

box3_3 = [
    [Paragraph("<b>МОДУЛЬ 3. Повестка сессии с психологом (Agenda)</b>", h1_l3)],
    [Paragraph("Отметьте актуальные темы для глубокой проработки со специалистом:", body_style)],
    [Spacer(1, 1*mm)]
]
tab3_3 = [
    [Paragraph("[  ] <b>Исцеление токсичного стыда:</b> переработка детских воспоминаний отвержения и критики.", body_style)],
    [Paragraph("[  ] <b>Страх публичности и оценки:</b> ступор перед высказыванием своего мнения в коллективе.", body_style)],
    [Paragraph("[  ] <b>Синдром самозванца:</b> неспособность признать свой профессиональный уровень.", body_style)],
    [Paragraph("[  ] <b>Укрепление позиции Здорового Взрослого:</b> формирование устойчивого доброго голоса внутри.", body_style)],
    [Paragraph("<b>Индивидуальный вопрос клиента к терапевту:</b> ____________________________________________________", body_style)]
]
t_tab3_3 = Table(tab3_3, colWidths=[178*mm])
t_tab3_3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c7d2fe')), ('PADDING', (0,0), (-1,-1), 3.5)]))
box3_3.append([t_tab3_3])
s3.append(Table(box3_3, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f3ff')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#4f46e5')), ('PADDING', (0,0), (-1,-1), 4)]))
s3.append(Spacer(1, 3*mm))

box3_4 = [
    [Paragraph("<b>МОДУЛЬ 4. Совместные терапевтические заметки</b>", h1_l3)],
    [Spacer(1, 0.5*mm)]
]
tab3_4 = [
    [Paragraph("<b>💡 Главный инсайт клиента:</b>", body_bold), Paragraph("<b>🎯 Опоры до следующей встречи:</b>", body_bold)],
    [Paragraph("Что я понял(а) о своей самоценности:<br/><br/><br/><br/>", body_style),
     Paragraph("Договоренности и фокус внимания:<br/><br/><br/><br/>", body_style)],
    [Paragraph("<i>Подпись клиента: ________________________</i>", small_style), Paragraph("<i>Дата следующей встречи: ________________</i>", small_style)]
]
t_tab3_4 = Table(tab3_4, colWidths=[89*mm, 89*mm])
t_tab3_4.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('PADDING', (0,0), (-1,-1), 3.5), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
box3_4.append([t_tab3_4])
s3.append(Table(box3_4, colWidths=[182*mm], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')), ('PADDING', (0,0), (-1,-1), 4)]))

doc3.build(s3)
print("SUCCESS: Self-Esteem L3 (3 pages)")
