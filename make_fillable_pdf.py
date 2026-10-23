import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

pdf_path = "therapy-workbooks/Pravo_Byt_Soboy_Interactive.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4 # 595.27 x 841.89 points

modules = [
    {
        "step": "Шаг 1. Где и почему я соглашаюсь во вред себе",
        "intro": "Спокойно и без самокритики замечаем ситуации, в которых мы говорим «да», хотя внутри всё просит отказаться.",
        "theory_title": "Откуда берется эта привычка:",
        "theory_text": "Стремление быть удобным — это выработанный защитный механизм. Когда-то он помогал сохранять мир и избегать ссор. Мы исследуем: где он полезен, а где отнимает слишком много сил.",
        "exp_title": "Простое упражнение недели:",
        "exp_text": "Не отвечайте на просьбы сразу «да». Возьмите паузу: «Мне нужно свериться с планами, отвечу позже». Почувствуйте, как пауза возвращает контроль.",
        "fields": [
            ("f1_1", "1. С кем произошла ситуация? (работа, семья, друзья, партнер, быт):", 20, False),
            ("f1_2", "2. Что произошло? (Опишите только факты, без осуждения себя):", 44, True),
            ("f1_3", "3. Что пугало в отказе? Какая мысль заставила согласиться?", 40, True),
            ("f1_4", "4. Какое решение здесь было бы честным и удобным для вас?", 40, True),
            ("f1_5", "5. Что вам стоила эта уступка? (время, силы, сорванные планы, обида):", 22, False),
        ],
        "q_therapy": "«Чье недовольство или обиду из прошлого я больше всего боюсь увидеть, когда хочу отказать этому человеку?»",
        "reqs": [
            ("chk1_1", "Разобрать эту ситуацию и понять, как поступить"),
            ("chk1_2", "Разобраться со страхом кого-то расстроить"),
            ("chk1_3", "Потренироваться брать паузу перед ответом"),
            ("chk1_4", "Снять тревогу перед сложным разговором")
        ],
        "notes_field": ("fn1", 32)
    },
    {
        "step": "Шаг 2. Как тело подсказывает, что силы на исходе",
        "intro": "Учимся слышать сигналы усталости и раздражения до того, как они перерастут в бессилие или эмоциональный срыв.",
        "theory_title": "О чем говорит раздражение:",
        "theory_text": "Злость и недовольство — это сторожа вашей батарейки. Они сообщают: «Мои силы закончились» или «Нарушена договоренность». Заметить сигнал — вернуть уважение к себе.",
        "exp_title": "Простое упражнение недели:",
        "exp_text": "Прислушайтесь к телу в момент любого предложения: почувствовало ли оно облегчение или всё сжалось? Этот первый физический отклик почти никогда не врет.",
        "fields": [
            ("f2_1", "1. Где в теле возник зажим, когда вы согласились через силу? (горло, челюсти, плечи):", 22, False),
            ("f2_2", "2. Что именно вызвало досаду или тихое раздражение? (какое действие задело):", 46, True),
            ("f2_3", "3. О чем просило ваше тело в этот момент? Какая была потребность?", 46, True),
            ("f2_4", "4. Как сказать об этой потребности спокойно и прямо?", 46, True),
        ],
        "q_therapy": "«Как в моей семье относились к злости? Можно ли было сказать 'мне это не нравится' без страха наказания?»",
        "reqs": [
            ("chk2_1", "Понять, почему тело так сильно зажимается при спорах"),
            ("chk2_2", "Научиться говорить «не подходит» спокойно"),
            ("chk2_3", "Перестать бояться, что несогласие разрушит контакт"),
            ("chk2_4", "Разрешить себе отдыхать без чувства вины")
        ],
        "notes_field": ("fn2", 34)
    },
    {
        "step": "Шаг 3. Как сказать «Нет» спокойно и без оправданий",
        "intro": "Учимся отказывать вежливо, понятно и твердо, не унижаясь избыточными извинениями.",
        "theory_title": "Почему длинные объяснения мешают:",
        "theory_text": "Чем подробнее мы оправдываемся, тем больше поводов даем спорить и давить. Простое «Спасибо за предложение, но сейчас я не смогу» звучит достойно и понятно.",
        "exp_title": "Простое упражнение недели:",
        "exp_text": "Потренируйтесь говорить «нет» в мелочах: откажитесь от чека на кассе, рекламной листовки или предложения по телефону. Мир от этого не рухнет.",
        "fields": [
            ("f3_1", "1. О чем вас попросили, на что хочется ответить отказом?", 22, False),
            ("f3_2", "2. Как вы обычно отвечали раньше (с кучей извинений и неловкостью):", 46, True),
            ("f3_3", "3. Простая, вежливая и твердая фраза отказа:", 46, True),
            ("f3_4", "4. Что ответить, если человек продолжит уговаривать («Ну пожалуйста, выручи!»)?", 46, True),
        ],
        "q_therapy": "«Почему мне кажется, что отказать взрослому человеку — это то же самое, что глубоко его ранить?»",
        "reqs": [
            ("chk3_1", "Отрепетировать сложный разговор по ролям"),
            ("chk3_2", "Найти правильные слова для родителей или начальства"),
            ("chk3_3", "Избавиться от привычки извиняться перед просьбой"),
            ("chk3_4", "Спокойно выдерживать чужую настойчивость")
        ],
        "notes_field": ("fn3", 34)
    },
    {
        "step": "Шаг 4. Что делать, если после отказа накрывает вина",
        "intro": "Как поддержать себя, когда вы поступили верно, но внутри навязчиво свербит мысль: «я поступил плохо».",
        "theory_title": "Откуда берется эта вина:",
        "theory_text": "После отказа мозгу тревожно от непривычного поведения. Это не значит, что вы совершили ошибку. Чувство вины быстро утихнет, если не бросаться всё спасать.",
        "exp_title": "Простое упражнение недели:",
        "exp_text": "Если после отказа хочется немедленно перезвонить и согласиться — сделайте медленный выдох и скажите себе: «Я взрослый человек. Я имею право беречь силы».",
        "fields": [
            ("f4_1", "1. В какой ситуации вас накрыло чувство вины или неловкости?", 22, False),
            ("f4_2", "2. В чем вы начали себя обвинять? Какая мысль крутится в голове?", 46, True),
            ("f4_3", "3. Трезвый взгляд на ситуацию (Факты вместо страхов):", 46, True),
            ("f4_4", "4. Что бы вы сказали в этой ситуации лучшему другу, если бы он мучился виной?", 46, True),
        ],
        "q_therapy": "«Чьим голосом говорит моя вина? Кто в детстве внушал мне ответственность за настроение взрослых?»",
        "reqs": [
            ("chk4_1", "Разобраться с внутренним критиком и самобичеванием"),
            ("chk4_2", "Перестать быть спасателем и тащить чужие эмоции"),
            ("chk4_3", "Научиться относиться к себе тепло и с поддержкой"),
            ("chk4_4", "Проработать детский страх быть отвергнутым")
        ],
        "notes_field": ("fn4", 34)
    },
    {
        "step": "Шаг 5. Чего на самом деле хочу я сам",
        "intro": "Когда мы перестаем тратить все силы на чужие ожидания, появляется время для своей настоящей жизни.",
        "theory_title": "Место для собственных желаний:",
        "theory_text": "Перестав угождать, мы сначала теряемся: «А чего хочу я сам?». Это радостный момент возвращения к своим вкусам, ценностям, спокойному ритму и отдыху.",
        "exp_title": "Простое упражнение недели:",
        "exp_text": "Выделите на этой неделе 45 минут на то, что приносит удовольствие лично вам, без пользы или чужого одобрения (прогулка в тишине, чай, любимая книга).",
        "fields": [
            ("f5_1", "1. Мои искренние «Я ХОЧУ» (то, что приносит мне радость и тепло):", 46, True),
            ("f5_2", "2. Мои категорические «Я БОЛЬШЕ НЕ ХОЧУ ЭТО ТЕРПЕТЬ»:", 46, True),
            ("f5_3", "3. Мое ежедневное разрешение себе (легализация отдыха и радости):", 22, False),
            ("f5_4", "4. Главное напоминание себе о самоуважении:", 22, False),
        ],
        "q_therapy": "«Каким человеком я становлюсь, когда перестаю под всех подстраиваться? Что в этом вдохновляет?»",
        "reqs": [
            ("chk5_1", "Составить постоянные правила общения с близкими"),
            ("chk5_2", "Научиться быть в близости, не теряя себя"),
            ("chk5_3", "Поверить в то, что мои желания ценны сами по себе"),
            ("chk5_4", "Подвести итоги работы и порадоваться успехам")
        ],
        "notes_field": ("fn5", 34)
    }
]

left_margin = 34
content_width = width - (left_margin * 2) # ~527 pt

def wrap_text(text, font, size, max_w):
    words = text.split()
    lines = []
    cur_line = []
    for w in words:
        test = " ".join(cur_line + [w])
        if c.stringWidth(test, font, size) <= max_w:
            cur_line.append(w)
        else:
            if cur_line:
                lines.append(" ".join(cur_line))
            cur_line = [w]
    if cur_line:
        lines.append(" ".join(cur_line))
    return lines

for m_idx, m in enumerate(modules):
    y = height - 32
    
    # 1. Top Document Header
    c.setFont("DejaVu", 7.5)
    c.setFillColor(colors.HexColor('#64748b'))
    c.drawString(left_margin, y, "ПРАВО БЫТЬ СОБОЙ  •  Интерактивная рабочая тетрадь бережных личных границ")
    
    y -= 18
    # 2. Step Title
    c.setFont("DejaVu-Bold", 12.5)
    c.setFillColor(colors.HexColor('#1e3a8a'))
    c.drawString(left_margin, y, m["step"])
    
    y -= 13
    # 3. Intro line
    c.setFont("DejaVu", 8)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(left_margin, y, m["intro"])
    
    y -= 10
    
    # 4. Top 2 columns: Theory + Exercise
    col_w = (content_width - 10) / 2 # ~258 pt
    box_h = 58
    
    # Theory box (Left)
    c.setFillColor(colors.HexColor('#f0fdfa'))
    c.setStrokeColor(colors.HexColor('#ccfbf1'))
    c.rect(left_margin, y - box_h, col_w, box_h, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#0f766e'))
    c.rect(left_margin, y - box_h, 3, box_h, fill=1, stroke=0)
    
    c.setFont("DejaVu-Bold", 7.5)
    c.drawString(left_margin + 7, y - 10, m["theory_title"])
    c.setFont("DejaVu", 7)
    c.setFillColor(colors.HexColor('#134e4a'))
    t_lines = wrap_text(m["theory_text"], "DejaVu", 7, col_w - 14)
    line_y = y - 21
    for tl in t_lines:
        c.drawString(left_margin + 7, line_y, tl)
        line_y -= 9
        
    # Exercise box (Right)
    rx = left_margin + col_w + 10
    c.setFillColor(colors.HexColor('#fffbeb'))
    c.setStrokeColor(colors.HexColor('#fef3c7'))
    c.rect(rx, y - box_h, col_w, box_h, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#d97706'))
    c.rect(rx, y - box_h, 3, box_h, fill=1, stroke=0)
    
    c.setFont("DejaVu-Bold", 7.5)
    c.drawString(rx + 7, y - 10, m["exp_title"])
    c.setFont("DejaVu", 7)
    c.setFillColor(colors.HexColor('#78350f'))
    e_lines = wrap_text(m["exp_text"], "DejaVu", 7, col_w - 14)
    line_y = y - 21
    for el in e_lines:
        c.drawString(rx + 7, line_y, el)
        line_y -= 9
        
    y -= (box_h + 12)
    
    # 5. Form Fields (Interactive Fillable Text Fields!)
    for f_name, f_label, f_h, is_multiline in m["fields"]:
        c.setFont("DejaVu-Bold", 7.8)
        c.setFillColor(colors.HexColor('#0f172a'))
        c.drawString(left_margin, y, f_label)
        y -= 13
        
        # Interactive Fillable Text Field
        c.acroForm.textfield(
            name=f_name,
            x=left_margin,
            y=y - f_h + 10,
            width=content_width,
            height=f_h,
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#0f172a'),
            borderWidth=0.5,
            borderColor=colors.HexColor('#94a3b8'),
            fillColor=colors.HexColor('#fafbfc'),
            fieldFlags='multiline' if is_multiline else ''
        )
        y -= (f_h + 6)
        
    y -= 2
    
    # 6. Therapy Section with Checkboxes and Notes
    th_box_h = 100
    c.setFillColor(colors.HexColor('#faf5ff'))
    c.setStrokeColor(colors.HexColor('#e9d5ff'))
    c.rect(left_margin, y - th_box_h, content_width, th_box_h, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#9333ea'))
    c.rect(left_margin, y - th_box_h, 3, th_box_h, fill=1, stroke=0)
    
    th_y = y - 11
    c.setFont("DejaVu-Bold", 8)
    c.setFillColor(colors.HexColor('#6b21a8'))
    c.drawString(left_margin + 8, th_y, "🛋 В фокус сессии с психологом")
    
    th_y -= 12
    c.setFont("DejaVu-Bold", 7.2)
    c.setFillColor(colors.HexColor('#581c87'))
    c.drawString(left_margin + 8, th_y, "Вопрос для размышления:")
    c.setFont("DejaVu", 7.2)
    c.drawString(left_margin + 124, th_y, m["q_therapy"])
    
    th_y -= 14
    c.setFont("DejaVu-Bold", 7)
    c.setFillColor(colors.HexColor('#581c87'))
    c.drawString(left_margin + 8, th_y, "Запрос на консультацию (отметьте галочками):")
    
    th_y -= 13
    # Checkbox items (2x2 grid)
    req_col_w = content_width / 2
    for r_idx, (chk_name, req_txt) in enumerate(m["reqs"]):
        cx = left_margin + 10 + (r_idx % 2) * req_col_w
        cy = th_y - (r_idx // 2) * 13
        
        # Interactive Checkbox
        c.acroForm.checkbox(
            name=chk_name,
            x=cx,
            y=cy - 1,
            size=10,
            borderColor=colors.HexColor('#7e22ce'),
            borderWidth=0.8,
            fillColor=colors.white,
            textColor=colors.HexColor('#7e22ce')
        )
        c.setFont("DejaVu", 7)
        c.setFillColor(colors.HexColor('#3b0764'))
        c.drawString(cx + 14, cy + 1, req_txt)
        
    # Therapy notes field
    notes_id, notes_h = m["notes_field"]
    th_y -= 26
    c.setFont("DejaVu-Bold", 6.8)
    c.setFillColor(colors.HexColor('#581c87'))
    c.drawString(left_margin + 8, th_y, "Заметки к встрече со специалистом:")
    th_y -= 6
    
    c.acroForm.textfield(
        name=notes_id,
        x=left_margin + 8,
        y=th_y - notes_h + 4,
        width=content_width - 16,
        height=notes_h,
        fontName='Helvetica',
        fontSize=7.5,
        textColor=colors.HexColor('#0f172a'),
        borderWidth=0.5,
        borderColor=colors.HexColor('#c084fc'),
        fillColor=colors.white,
        fieldFlags='multiline'
    )
    
    c.showPage()

c.save()
print("Interactive Fillable PDF workbook created successfully:", pdf_path)
