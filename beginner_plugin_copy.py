"""Beginner-facing Russian copy for plugin cards.

Keeps English control and product names. Does not invent official manual facts:
plugin-specific sentences are built from the catalog kind, description and note.
"""
import re

CATEGORY = {
    'Cleanup и restoration': {
        'tool': 'инструмент очистки записи',
        'what': 'Он убирает то, что мешает слушать: шум, резкие «с», колкий верх, дыхание или гул комнаты. Хороший результат звучит как более чистая запись, а не как эффект.',
        'hear': 'Проблема становится тише, а голос или инструмент остаются собой. Если появился «водянистый» призвук или шепелявость — обработки слишком много.',
        'when': 'Когда грязь слышна ещё до эквалайзера и компрессора.',
        'start': 'Сначала обработайте самый плохой кусок. Сравнивайте с выключенным плагином на одной громкости.',
    },
    'EQ и tone shaping': {
        'tool': 'эквалайзер',
        'what': 'Он меняет баланс частот: низ, середину или верх можно поднять или опустить. Звук становится темнее, светлее, толще или тоньше.',
        'hear': 'Источник занимает другое место в песне: меньше гула, больше ясности или другой характер середины. Слушайте не в solo, а в полном миксе.',
        'when': 'Когда на фейдерах картина уже есть, но источник мешает другому или звучит плоско.',
        'start': 'Сначала убирайте лишнее (cut), потом добавляйте. Всегда сравнивайте Bypass при одинаковой громкости.',
    },
    'Dynamics': {
        'tool': 'динамический процессор',
        'what': 'Он управляет разницей между тихим и громким: выравнивает фразу, добавляет удар или не даёт пикам вылезти.',
        'hear': 'Атака становится резче или мягче, хвост короче или длиннее, громкость ровнее. Цифры Attack и Release важнее «красивого» Gain Reduction.',
        'when': 'Когда уровень прыгает или удар пропадает в миксе, а баланс фейдерами уже сделан.',
        'start': 'Найдите 1–4 dB работы и верните Output к громкости Bypass. Иначе «громче» всегда покажется лучше.',
    },
    'Low-end processing': {
        'tool': 'обработка низа',
        'what': 'Он работает с фундаментом: бочка, бас, 808. Можно добавить вес, собрать хвост или сделать низ слышнее на маленькой колонке.',
        'hear': 'Низ становится плотнее или собраннее. Проверяйте mono и запас по уровню: лишний sub быстро съедает headroom.',
        'when': 'Когда низ либо не слышен, либо гудит и мешает другим инструментам.',
        'start': 'Сначала фаза и баланс kick/bass, потом этот плагин. Слушайте тихо и в mono.',
    },
    'Saturation и color': {
        'tool': 'сатурация или окраска',
        'what': 'Он добавляет гармоники и плотность, как лёгкий перегруз лампы, ленты или трансформатора. Звук ближе и «дороже», но это не замена баланса.',
        'hear': 'Появляется тепло, плотность или грязь. Если просто стало громче — сначала выровняйте Output.',
        'when': 'Когда источник чистый, но пустой, и нужна характерная плотность.',
        'start': 'Малый Drive, затем обязательный level-matched A/B. Слушайте низ середины и резкий верх.',
    },
    'Channel strips и macros': {
        'tool': 'готовая цепочка в одном окне',
        'what': 'Внутри сразу несколько стадий: фильтр, EQ, компрессия, иногда saturation и limiter. Удобно быстро получить рабочий тон.',
        'hear': 'Источник сразу звучит «собраннее». Но не каждый модуль обязан быть включён — лишние стадии только добавляют громкость.',
        'when': 'Когда нужен быстрый старт, а не тонкая хирургия одной проблемы.',
        'start': 'Выключите ненужные модули. Настройте Input без клипа и сравните с чистым сигналом на одной громкости.',
    },
    'Delay': {
        'tool': 'задержка',
        'what': 'Он повторяет звук через короткое или ритмичное время: slap, echo, рисунок доли.',
        'hear': 'Появляются повторы. На send их легче фильтровать и не заглушить сухой голос или гитару.',
        'when': 'Когда источнику нужна глубина или ритм, но не целое помещение reverb.',
        'start': 'Лучше Send, return 100% wet. Фильтруйте repeats сильнее, чем кажется в solo.',
    },
    'Reverb': {
        'tool': 'реверберация',
        'what': 'Он добавляет помещение: комнату, plate, hall или камеру. Источник получает глубину и общий воздух.',
        'hear': 'Появляется хвост и ощущение пространства. Если слова или атака смазались — увеличьте Pre-delay или уберите низ на return.',
        'when': 'Когда источник слишком сухой или не сидит в одной комнате с остальными.',
        'start': 'Обычно Send, return 100% wet. Сначала тип пространства, потом короткая длина.',
    },
    'Modulation и stereo': {
        'tool': 'модуляция или стерео-утилита',
        'what': 'Он двигает звук во времени, по панораме, фазе или ширине: chorus, doubler, M/S, mono check.',
        'hear': 'Появляется движение или ширина. В mono центр не должен провалиться.',
        'when': 'Когда нужно оживить статичный источник или проверить, что будет в одном канале.',
        'start': 'Малая глубина. Обязательно сравнение Stereo и Mono.',
    },
    'Guitar и bass rigs': {
        'tool': 'усилитель, кабинет или педаль',
        'what': 'Он красит гитару или бас как железный усилитель: преамп, кабинет, микрофон, иногда педали.',
        'hear': 'Меняется сам тон инструмента: чистый, хруст, высокий gain, характер кабинета. Кабинет и IR часто важнее, чем EQ после.',
        'when': 'Когда нужен amp-звук, а не коррекция уже готового тона.',
        'start': 'Сначала Input и выбор кабинета, потом gain. Проверяйте низ: гитара не должна есть бас.',
    },
    'Creative FX и sound design': {
        'tool': 'творческий эффект',
        'what': 'Он заметно меняет звук: granular, spectral, случайные цепочки, вокальные превращения. Это уже не «починить», а сделать новый слой.',
        'hear': 'Источник становится другим объектом. Сухой оригинал лучше оставить отдельно.',
        'when': 'Для акцентов, переходов и отдельных слоёв, не на весь микс постоянно.',
        'start': 'Копия дорожки или Send. Удачный случайный результат лучше записать в audio.',
    },
    'Instruments': {
        'tool': 'виртуальный инструмент',
        'what': 'Он сам создаёт звук: бас, лид, пэд. Это источник, а не обработка уже записанной дорожки.',
        'hear': 'Появляется новая партия. Её лучше сразу строить под роль в аранжировке.',
        'when': 'Когда нужен синтезаторный или спроектированный тембр, а не эффект на записи.',
        'start': 'Сначала тембр и огибающие, потом уже inserts. Не чините плохой патч десятью плагинами.',
    },
    'Metering и utility': {
        'tool': 'измеритель или служебная утилита',
        'what': 'Он помогает слышать и сравнивать: громкость, спектр, mono, маленький динамик, референс. Сам по себе микс обычно не украшает.',
        'hear': 'Вы лучше понимаете проблему. Если утилита меняет звук, её чаще нельзя печатать в export.',
        'when': 'Для проверки, обучения и сравнения, не как «красивый эффект».',
        'start': 'Держите в Monitoring. Перед render убедитесь, что служебный плагин выключен из экспорта.',
    },
}

FAMILY_HINT = {
    'De-essers': 'Специально ловит сибилянты — резкие «с», «ш», «ц».',
    'De-harsh и spectral repair': 'Сглаживает колкую середину и резкие призвуки, когда обычный EQ уже груб.',
    'Noise, breath и de-reverb': 'Убирает шум, лишние вдохи или хвост комнаты.',
    'Pitch correction': 'Подтягивает неточные ноты. Скорость Retune решает, будет ли натурально или как эффект.',
    'FET-компрессоры': 'Быстрые и напористые, часто в духе 1176: вокал, барабаны, бас.',
    'Opto-компрессоры': 'Плавные, как LA-2A: выравнивают фразу, не откусывая атаку сразу.',
    'VCA и bus-компрессоры': 'Точный glue на группах и mix bus: небольшая работа, общая склейка.',
    'Vari-mu и tube compression': 'Мягкое ламповое округление и плотность.',
    'Чистые и универсальные компрессоры': 'Прозрачное выравнивание уровня без сильного характера.',
    'Brickwall limiters': 'Жёсткий потолок пиков. Обычно в конце цепи или на мастере.',
    'Clippers': 'Срезает самые короткие пики и добавляет плотность, сильнее чем мягкий компрессор.',
    'Gate и expander': 'Тише делает то, что ниже порога: bleed барабана или шум гитары.',
    'Broadband transient shaping': 'Меняет удар и хвост, почти не трогая «компрессорный» характер.',
    'Leveling, riders и upward compression': 'Подтягивает тихие места, вместо того чтобы давить громкие.',
    'API и proportional-Q EQ': 'Напористая середина и punch в духе API.',
    'Neve и British EQ': 'Плотная, тёплая середина в британском консольном вкусе.',
    'Pultec и passive EQ': 'Широкие музыкальные полки; классический одновременный boost и cut низа.',
    'Чистый parametric и dynamic EQ': 'Точная коррекция. Dynamic EQ трогает частоту только когда она вылезает.',
    'Linear-phase и mastering EQ': 'Аккуратный тон на шине/мастере; linear phase берегите из‑за pre-ringing.',
    'High-gain guitar amps и suites': 'Набор гитарных усилителей: от плотного crunch до сильного Gain.',
    'Clean, crunch и boutique guitar amps': 'Чистый или слегка хрустящий гитарный amp.',
    'Bass amps, DI и multiband rigs': 'Басовый усилитель или DI: фундамент плюс читаемый верх.',
    'Pedals, cabinets и IR': 'Педаль, кабинет или проигрыватель IR — тон кабинета часто решает всё.',
    'Kick, bass и body processors': 'Собрать или подчеркнуть тело бочки и баса.',
    'Subharmonic и psychoacoustic bass': 'Добавляет слышимые гармоники, чтобы низ читался на маленькой акустике.',
    'Tube и transformer saturation': 'Ламповая или трансформаторная плотность и тепло.',
    'Tape machine': 'Ленточная компрессия, мягкий верх и плотность.',
    'Vocal chains': 'Готовая вокальная стойка: несколько стадий в одном окне.',
    'Console channel strips': 'Канал большого пульта: фильтры, EQ и динамика вместе.',
    'Bus и mastering finishers': 'Быстрый финиш группы или шины. Чистый premaster лучше сохранить отдельно.',
    'Algorithmic reverbs': 'Считанное помещение: room, hall, plate без записи реальной комнаты.',
    'Plate и chamber reverbs': 'Классические plate и камерные пространства, часто для вокала и малого.',
    'Doubling и widening': 'Имитация второго дубля или расширение, сухой центр лучше оставить.',
    'M/S, stereo matrix и mono control': 'Работа с центром и краями, либо проверка mono.',
    'Phase и time alignment': 'Совмещение микрофонов по polarity и времени, до EQ.',
}

KEYWORD_HINTS = [
    (r'de-ess|sibil|сибилянт|S-sound', 'убирает резкие «с» и «ш», стараясь не сделать голос шепелявым'),
    (r'de-harsh|harsh', 'сглаживает колкую верхнюю середину'),
    (r'de-reverb|dereverb', 'укорачивает комнатный хвост записи'),
    (r'denoise|noise reduc|шумопод', 'убирает постоянный шум и гул'),
    (r'pro-q 4|spectral dynamics|eq sketch', 'dynamic и spectral EQ плюс EQ Sketch: можно нарисовать кривую и точечно давить вылезающие частоты'),
    (r'crystallizer|reverse pitch|pitch-shifted reverse', 'делает обратные повторы со сдвигом высоты — текстура, не обычный delay'),
    (r'(?<![a-z])pitch correction|autotune|retune', 'подтягивает высоту нот'),
    (r'flip-top|B-15', 'тёплый округлый тон маленького винтажного басового комбо'),
    (r'\bSVT\b', 'плотный громкий басовый amp-характер'),
    (r'rockrack', 'восемь amp в одном окне: от clean Marshall до metal; не только высокий Gain'),
    (r'decapitator|punish', 'аналоговая сатурация пяти характеров: от лёгкой плотности до сильного перегруза'),
    (r'sidechain|ducking|UltraPump', 'ритмично приседает по внешнему ключу — классический pump, не автоматический фейдер'),
    (r'nameless|granophyre|extremely tight high gain', 'плотный современный перегруз с сильным Gain'),
    (r'clean/crunch|boutique clean|pedal-platform', 'чистый или слегка хрустящий тон, удобный под педали'),
    (r'LA-2A|opto|оптическ', 'сжимает плавно, как оптический компрессор'),
    (r'1176|FET|CLA-76', 'сжимает быстро и напористо'),
    (r'vari-mu|vari mu', 'мягко округляет и уплотняет по-ламповому'),
    (r'glue|VCA|bus compress', 'слегка склеивает группу, чтобы дорожки звучали вместе'),
    (r'brickwall|maximizer|true-peak limiter', 'держит пики у потолка и поднимает общую громкость'),
    (r'clipper|клиппер', 'срезает самые короткие пики и добавляет плотность'),
    (r'transient|attack/sustain|attack и sustain', 'меняет удар начала и длину хвоста'),
    (r'gate|expander', 'тише делает то, что ниже порога'),
    (r'pultec', 'широкие музыкальные полки и характерный трюк boost+cut низа'),
    (r'proportional-Q|API 55', 'напористый API-тон: узкий boost звучит острее'),
    (r'linear phase', 'минимальный сдвиг фазы; на транзиентах возможен pre-ringing'),
    (r'dynamic eq|dynamic band', 'трогает частоту только когда она вылезает'),
    (r'plate', 'металлический плотный хвост, частый выбор для вокала и малого'),
    (r'convolution|IR-1|impulse', 'помещение из записи реального пространства или кабинета'),
    (r'doubler|MicroShift|Double Dare', 'имитирует второй дубль небольшой разницей по времени и высоте'),
    (r'widener|widening|width', 'делает сигнал шире; проверяйте mono'),
    (r'chorus|flanger|phaser', 'добавляет движение через расстройку, гребёнку или фазовые провалы'),
    (r'tape|кассет|J37|Kramer Master Tape', 'ленточная плотность, мягкий верх и лёгкая компрессия'),
    (r'cassette|lo-fi|felt', 'ностальгическая грязь, мягкость и нестабильность'),
    (r'subharmonic|psychoacoustic|RBass', 'добавляет гармоники, чтобы низ читался на маленькой акустике'),
    (r'EchoBoy|echo boy', 'delay с характером разных эхо-машин: от slap до грязного analog repeat'),
    (r'multi-tap|taps для|SuperTap', 'ставит несколько повторов в разных долях — ритмический рисунок, а не одно эхо'),
    (r'IR player|cabinet IR|SuperCabinet', 'подставляет кабинет из импульса; тон кабинета важнее EQ после'),
    (r'reference|Metric AB', 'сравнивает ваш микс с референсом на одной громкости'),
    (r'mono speaker|translation', 'показывает, как микс сядет на маленькой моно-колонке'),
    (r'Vocal Rider|Bass Rider', 'едет по уровню как автоматический фейдер, а не как обычный компрессор'),
]


def _cyr_ratio(text):
    text = text or ''
    cyr = sum(('а' <= ch.lower() <= 'я') or ch.lower() == 'ё' for ch in text)
    return cyr / max(1, len(text))


def _sentence(text):
    text = re.sub(r'\s+', ' ', (text or '').strip())
    if not text:
        return ''
    return text if text.endswith(('.', '!', '?')) else text + '.'


def _keyword_hint(plugin):
    blob = f'{plugin.get("name", "")} {plugin.get("kind", "")}'.casefold()
    for pattern, hint in KEYWORD_HINTS:
        if re.search(pattern, blob, re.I):
            return hint
    return ''


def _family_hint_for(plugin):
    family = plugin.get('family') or ''
    kind = (plugin.get('kind') or '').casefold()
    name = (plugin.get('name') or '').casefold()
    if 'sidechain' in kind or 'ducking' in kind or 'ultrapump' in name:
        return 'Ритмичный sidechain-pump: место под удар, не автоматический фейдер.'
    if 'rockrack' in name:
        return 'Восемь amp от clean до metal плюс кабинеты; не один high-gain пресет.'
    if family == 'Leveling, riders и upward compression' and 'rider' not in name and 'rider' not in kind:
        return 'Выравнивает громкость: подтягивает тихое или слегка давит громкое.'
    if family == 'High-gain guitar amps и suites' and re.search(r'clean|crunch|jazz|multi-amp|suite', kind):
        return 'Несколько каналов amp: не только высокий Gain.'
    return FAMILY_HINT.get(family, '')


def _this_one_does(plugin):
    desc = (plugin.get('description') or '').strip()
    kind = (plugin.get('kind') or '').strip()
    hint = _keyword_hint(plugin)
    if _cyr_ratio(desc) >= 0.18 and len(desc) >= 36:
        core = desc.rstrip('.')
        if hint and hint[:18].casefold() not in core.casefold():
            return f'{core}: {hint}'
        return core
    if hint:
        return hint
    if kind and _cyr_ratio(kind) >= 0.18:
        return kind.rstrip('.')
    family_hint = _family_hint_for(plugin)
    if family_hint:
        return family_hint.rstrip('.')
    if kind:
        return f'в каталоге его роль записана как {kind}'
    return 'меняет звук в рамках своего семейства'


def _source_phrase(sources):
    names = [s for s in sources if s][:4]
    if not names:
        return 'тех дорожках, где он указан в каталоге'
    if len(names) == 1:
        return names[0]
    return ', '.join(names[:-1]) + ' и ' + names[-1]


def beginner_copy(plugin, profile, sources):
    cat = CATEGORY.get(plugin.get('category'), {
        'tool': 'плагин обработки',
        'what': 'Он меняет звук под конкретную задачу.',
        'hear': 'Слушайте разницу с выключенным плагином на одной громкости.',
        'when': 'Когда задача уже слышна без стойки.',
        'start': 'Начните с малого Amount и сравните Bypass.',
    })
    family_hint = _family_hint_for(plugin)
    does = _this_one_does(plugin)
    src = _source_phrase(sources)
    name = plugin['name']
    dev = plugin.get('developer') or 'разработчика'
    note = (plugin.get('note') or '').strip()

    many_sources = len(sources or []) >= 6
    catalog_line = (
        'В каталоге он встречается на разных источниках — это карта базы, не официальное «типичное применение».'
        if many_sources else
        f'В каталоге он встречается в том числе на {src}. Это карта этой базы, не официальный список типичных задач.'
    )
    simple = ' '.join(filter(None, [
        _sentence(f'{name} — {cat["tool"]}'),
        _sentence(does[0].upper() + does[1:] if does and does[0].islower() else does),
        _sentence(family_hint) if family_hint and family_hint[:24].casefold() not in does.casefold() else '',
        _sentence(catalog_line),
    ]))

    sound = ' '.join(filter(None, [
        _sentence(cat['hear']),
        _sentence(f'Именно у {name} это звучит так: {does}'),
        _sentence(cat['start']),
    ]))

    why_bits = [
        _sentence(cat['when']),
    ]
    if note and len(note) > 20:
        why_bits.append(_sentence(f'Практическая пометка по этому плагину: {note.rstrip(".")}'))
    choose = (profile or {}).get('choose') or ''
    if choose and _cyr_ratio(choose) >= 0.12:
        why_bits.append(_sentence(choose))
    why = ' '.join(why_bits)

    full = ' '.join(filter(None, [
        _sentence(f'{name} разработан {dev}. Это {cat["tool"]}'),
        _sentence(cat['what']),
        _sentence(f'Чем этот экземпляр отличается в каталоге: {does}'),
        _sentence(family_hint),
        _sentence(f'В картах этой базы он встречается в том числе на {src}. Это порядок каталога, не официальное типичное применение'),
        _sentence(cat['hear']),
        _sentence(cat['start']),
        _sentence(f'Пометка: {note.rstrip(".")}') if note else '',
        _sentence('Названия ручек оставляйте английскими, как на панели. Если Controls помечены как модель семейства, сверяйте их с вашим GUI — это не дословный manual.'),
    ]))

    return {
        'simple': simple,
        'sound': sound,
        'why': why,
        'full': full,
    }
