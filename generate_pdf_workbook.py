import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Register Unicode fonts
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

pdf_path = "therapy-workbooks/Pravo_Byt_Soboy_Workbook.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=12*mm,
    rightMargin=12*mm,
    topMargin=10*mm,
    bottomMargin=10*mm
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'DocTitle',
    fontName='DejaVu-Bold',
    fontSize=14,
    leading=17,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=2*mm
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    fontName='DejaVu',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#475569'),
    spaceAfter=3*mm
)

step_title_style = ParagraphStyle(
    'StepTitle',
    fontName='DejaVu-Bold',
    fontSize=11.5,
    leading=14,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=1*mm
)

step_intro_style = ParagraphStyle(
    'StepIntro',
    fontName='DejaVu',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#334155'),
    spaceAfter=2.5*mm
)

box_text_style = ParagraphStyle(
    'BoxText',
    fontName='DejaVu',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#1e293b')
)

field_label_style = ParagraphStyle(
    'FieldLabel',
    fontName='DejaVu-Bold',
    fontSize=8,
    leading=10,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=1*mm
)

therapy_title_style = ParagraphStyle(
    'TherapyTitle',
    fontName='DejaVu-Bold',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#6b21a8')
)

therapy_sub_style = ParagraphStyle(
    'TherapySub',
    fontName='DejaVu-Bold',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#581c87')
)

therapy_text_style = ParagraphStyle(
    'TherapyText',
    fontName='DejaVu',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#3b0764')
)

def make_callout(text, title=None, border_color='#0f766e', bg_color='#f8fafc', width=186*mm):
    content = []
    if title:
        content.append(Paragraph(f"<b>{title}</b>", box_text_style))
    content.append(Paragraph(text, box_text_style))
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('LINELEFT', (0,0), (-1,-1), 2.5, colors.HexColor(border_color)),
    ]))
    return t

def make_form_field(label_text, lines_count=2, width=186*mm):
    # Generates a label followed by an elegant lined box for handwriting/typing
    rows = [[Paragraph(label_text, field_label_style)]]
    for _ in range(lines_count):
        rows.append([''])
    
    t = Table(rows, colWidths=[width], rowHeights=[None] + [16 for _ in range(lines_count)])
    t.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LINEBELOW', (0,1), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    return t

modules_data = [
    {
        "num": "Шаг 1",
        "title": "Где и почему я соглашаюсь во вред себе",
        "intro": "Спокойно и без самокритики замечаем ситуации, в которых мы говорим «да», хотя внутри всё просит отказаться.",
        "theory": "<b>Откуда берется привычка:</b> Стремление быть удобным — это выработанный защитный механизм. Когда-то он помогал сохранять мир и избегать ссор. Мы исследуем: где он полезен, а где отнимает слишком много сил.",
        "exp": "<b>Простое упражнение:</b> Не отвечайте на просьбы сразу «да». Возьмите паузу: <i>«Мне нужно свериться с планами, отвечу позже»</i>. Почувствуйте, как пауза возвращает контроль.",
        "fields": [
            ("1. С кем произошла ситуация? (работа, семья, друзья, партнер, быт):", 1),
            ("2. Что произошло? (Опишите только факты, без осуждения себя):", 2),
            ("3. Что пугало в отказе? Какая мысль заставила согласиться?", 2),
            ("4. Какое решение здесь было бы честным и удобным для вас?", 2),
            ("5. Что вам стоила эта уступка? (время, силы, сорванные планы, обида):", 1),
        ],
        "q_therapy": "«Чье недовольство или обиду из прошлого я больше всего боюсь увидеть, когда хочу отказать этому человеку?»",
        "reqs": [
            "Разобрать эту ситуацию и понять, как поступить",
            "Разобраться со страхом кого-то расстроить",
            "Потренироваться брать паузу перед ответом",
            "Снять тревогу перед сложным разговором"
        ]
    },
    {
        "num": "Шаг 2",
        "title": "Как тело подсказывает, что силы на исходе",
        "intro": "Учимся слышать сигналы усталости и раздражения до того, как они перерастут в бессилие или эмоциональный срыв.",
        "theory": "<b>О чем говорит раздражение:</b> Злость — это сторож вашей батарейки. Она сообщает: <i>«Мои силы закончились»</i> или <i>«Нарушена договоренность»</i>. Заметить сигнал — вернуть уважение к себе.",
        "exp": "<b>Простое упражнение:</b> Прислушайтесь к телу в момент предложения: почувствовало ли оно облегчение или всё сжалось? Этот физический отклик никогда не обманывает.",
        "fields": [
            ("1. Где в теле возник зажим, когда вы согласились через силу? (горло, челюсти, плечи):", 1),
            ("2. Что именно вызвало досаду или тихое раздражение? (какое действие задело):", 2),
            ("3. О чем просило ваше тело в этот момент? Какая была потребность?", 2),
            ("4. Как сказать об этой потребности спокойно и прямо?", 2),
        ],
        "q_therapy": "«Как в моей семье относились к злости? Можно ли было сказать 'мне это не нравится' без страха наказания?»",
        "reqs": [
            "Понять, почему тело так сильно зажимается при спорах",
            "Научиться говорить «не подходит» спокойно",
            "Перестать бояться, что несогласие разрушит контакт",
            "Разрешить себе отдыхать без чувства вины"
        ]
    },
    {
        "num": "Шаг 3",
        "title": "Как сказать «Нет» спокойно и без оправданий",
        "intro": "Учимся отказывать вежливо, понятно и твердо, не унижаясь избыточными извинениями.",
        "theory": "<b>Почему длинные объяснения мешают:</b> Чем подробнее мы оправдываемся, тем больше поводов даем спорить и давить. Простое <i>«Спасибо за предложение, но сейчас я не смогу»</i> звучит достойно.",
        "exp": "<b>Простое упражнение:</b> Потренируйтесь говорить «нет» в мелочах: откажитесь от чека, рекламной листовки или предложения по телефону. Мир от этого не рухнет.",
        "fields": [
            ("1. О чем вас попросили, на что хочется ответить отказом?", 1),
            ("2. Как вы обычно отвечали раньше (с кучей извинений и неловкостью):", 2),
            ("3. Простая, вежливая и твердая фраза отказа:", 2),
            ("4. Что ответить, если человек продолжит уговаривать («Ну пожалуйста, выручи!»)?", 2),
        ],
        "q_therapy": "«Почему мне кажется, что отказать взрослому человеку — это то же самое, что глубоко его ранить?»",
        "reqs": [
            "Отрепетировать сложный разговор по ролям",
            "Найти правильные слова для родителей или начальства",
            "Избавиться от привычки извиняться перед просьбой",
            "Спокойно выдерживать чужую настойчивость"
        ]
    },
    {
        "num": "Шаг 4",
        "title": "Что делать, если после отказа накрывает вина",
        "intro": "Как поддержать себя, когда вы поступили верно, но внутри навязчиво свербит мысль: «я поступил плохо».",
        "theory": "<b>Откуда эта вина:</b> После отказа мозгу тревожно от непривычного поведения. Это не значит, что вы совершили ошибку. Чувство вины быстро утихнет, если не бросаться всё спасать.",
        "exp": "<b>Простое упражнение:</b> Если хочется немедленно перезвонить и согласиться — сделайте выдох и скажите себе: <i>«Я взрослый человек. Я имею право беречь силы. Со мной всё в порядке»</i>.",
        "fields": [
            ("1. В какой ситуации вас накрыло чувство вины или неловкости?", 1),
            ("2. В чем вы начали себя обвинять? Какая мысль крутится в голове?", 2),
            ("3. Трезвый взгляд на ситуацию (Факты вместо страхов):", 2),
            ("4. Что бы вы сказали в этой ситуации лучшему другу, если бы он мучился виной?", 2),
        ],
        "q_therapy": "«Чьим голосом говорит моя вина? Кто в детстве внушал мне ответственность за настроение взрослых?»",
        "reqs": [
            "Разобраться с внутренним критиком и самобичеванием",
            "Перестать быть спасателем и тащить чужие эмоции",
            "Научиться относиться к себе тепло и с поддержкой",
            "Проработать детский страх быть отвергнутым"
        ]
    },
    {
        "num": "Шаг 5",
        "title": "Чего на самом деле хочу я сам",
        "intro": "Когда мы перестаем тратить все силы на чужие ожидания, появляется время для своей настоящей жизни.",
        "theory": "<b>Место для собственных желаний:</b> Перестав угождать, мы сначала теряемся: <i>«А чего хочу я сам?»</i>. Это радостный момент возвращения к своим вкусам, ценностям и отдыху.",
        "exp": "<b>Простое упражнение:</b> Подарите себе 45 минут на то, что приносит удовольствие лично вам, без пользы или чужого одобрения (прогулка в тишине, чай, любимая книга).",
        "fields": [
            ("1. Мои искренние «Я ХОЧУ» (то, что приносит мне радость и тепло):", 2),
            ("2. Мои категорические «Я БОЛЬШЕ НЕ ХОЧУ ЭТО ТЕРПЕТЬ»:", 2),
            ("3. Мое ежедневное разрешение себе (легализация отдыха и радости):", 1),
            ("4. Главное напоминание себе о самоуважении:", 1),
        ],
        "q_therapy": "«Каким человеком я становлюсь, когда перестаю под всех подстраиваться? Что в этом вдохновляет?»",
        "reqs": [
            "Составить постоянные правила общения с близкими",
            "Научиться быть в близости, не теряя себя",
            "Поверить в то, что мои желания ценны сами по себе",
            "Подвести итоги работы и порадоваться успехам"
        ]
    }
]

story = []

# Build each module on its own exact A4 page
for idx, m in enumerate(modules_data):
    # Header
    story.append(Paragraph(f"<b>ПРАВО БЫТЬ СОБОЙ</b> &bull; Рабочая тетрадь бережных личных границ", subtitle_style))
    story.append(Paragraph(f"{m['num']}. {m['title']}", step_title_style))
    story.append(Paragraph(m['intro'], step_intro_style))
    
    # 2 columns: Theory + Experiment
    col_w = 91*mm
    t_theory = make_callout(m['theory'], title="Откуда это берется:", border_color='#0f766e', bg_color='#f0fdfa', width=col_w)
    t_exp = make_callout(m['exp'], title="Упражнение недели:", border_color='#d97706', bg_color='#fffbeb', width=col_w)
    
    grid_table = Table([[t_theory, t_exp]], colWidths=[col_w, col_w])
    grid_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 2*mm))
    
    # Form fields
    for label, lines in m['fields']:
        story.append(make_form_field(label, lines_count=lines, width=186*mm))
        story.append(Spacer(1, 1.5*mm))
    
    # Therapy block
    therapy_cells = [
        [Paragraph("<b>🛋 В фокус сессии с психологом</b>", therapy_title_style), ''],
        [Paragraph(f"<b>Вопрос для размышления:</b> {m['q_therapy']}", therapy_text_style), '']
    ]
    
    # Add check items 2 by 2
    r = m['reqs']
    therapy_cells.append([
        Paragraph(f"[  ] {r[0]}", therapy_text_style),
        Paragraph(f"[  ] {r[1]}", therapy_text_style)
    ])
    therapy_cells.append([
        Paragraph(f"[  ] {r[2]}", therapy_text_style),
        Paragraph(f"[  ] {r[3]}", therapy_text_style)
    ])
    
    therapy_table = Table(therapy_cells, colWidths=[93*mm, 93*mm])
    therapy_table.setStyle(TableStyle([
        ('SPAN', (0,0), (1,0)),
        ('SPAN', (0,1), (1,1)),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#faf5ff')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#d8b4fe')),
        ('LINELEFT', (0,0), (-1,-1), 2.5, colors.HexColor('#9333ea')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(therapy_table)
    
    if idx < len(modules_data) - 1:
        story.append(PageBreak())

doc.build(story)
print("PDF workbook successfully created at:", pdf_path)
