"""Additional product-specific Control maps.

Names follow commonly documented official GUI labels. They are still a curated
map, not a verbatim manual dump of every version. Evidence stays
'Product-specific curated map'.
"""

def ctl(name, role, hear, start):
    return {'name': name, 'role': role, 'hear': hear, 'start': start,
            'evidence': 'Product-specific curated map'}


def cla_signature(extra):
    base = [
        ctl('Bass', 'Низкочастотный color/level модуля.', 'Добавляет вес или убирает тонкий низ.', 'Начать около noon, затем ±.'),
        ctl('Treble', 'Высокочастотный color/level модуля.', 'Добавляет air/bite или смягчает.', 'Начать около noon.'),
        ctl('Compress', 'Сила встроенной compression.', 'Плотнее и ровнее источник.', 'До 2–5 dB ощущаемого GR.'),
        ctl('Output / Trim', 'Компенсация уровня всей цепочки.', 'Нужен честный A/B.', 'Level-match с bypass.'),
    ]
    return extra + base


def neural_amp(extra=None):
    controls = [
        ctl('Input / Noise Gate', 'Калибрует DI и режет шум между нотами.', 'Слишком жёсткий Gate режет sustain.', 'Калибровать Input; Gate по паузам.'),
        ctl('Compressor', 'Сжимает сигнал до/внутри amp path.', 'Выравнивает attack и sustain.', 'Лёгкий GR; не душить dynamics.'),
        ctl('Amp Gain / Drive', 'Перегруз preamp выбранного amp.', 'Больше gain — меньше articulation.', 'Ниже, чем кажется в solo.'),
        ctl('Bass / Mid / Treble', 'Tone stack усилителя.', 'Сильно зависит от Cab/IR.', 'Настраивать вместе с кабинетом.'),
        ctl('Presence / Resonance', 'Яркость и низ power-amp.', 'Presence даёт bite, Resonance — weight.', 'Осторожно на bus/double tracks.'),
        ctl('Cab / IR / Mic', 'Кабинет, микрофон и позиция.', 'Обычно самое большое tonal изменение.', 'Выбрать до post-EQ.'),
        ctl('Delay / Reverb', 'Встроенные time effects.', 'Добавляют depth; могут маскировать dry.', 'Часто лучше внешний send.'),
        ctl('Output', 'Выходной уровень suite.', 'Нужен headroom следующей стадии.', 'Без клиппинга следующего insert.'),
    ]
    return (extra or []) + controls


def ozone_module(controls):
    return controls + [
        ctl('Solo / Bypass module', 'Слушает только этот Ozone module.', 'Помогает не копить обработку suite.', 'Проверять каждый module отдельно.'),
        ctl('Gain / Makeup', 'Компенсация уровня модуля.', 'Убирает loudness bias.', 'Level-match перед следующим module.'),
    ]


def bx_console():
    return [
        ctl('Input / THD / Drive', 'Gain staging и analog color канала.', 'Выше — больше harmonics и noise floor.', 'Оставить headroom до EQ/Dyn.'),
        ctl('Filters (HPF / LPF)', 'Срезает края спектра до/после EQ.', 'Чистит rumble и harsh air.', 'Только по задаче, не по привычке.'),
        ctl('Gate / Expander', 'Ослабляет сигнал ниже порога.', 'Убирает bleed, может резать ghost notes.', 'Range 6–15 dB; слушать хвост.'),
        ctl('Compressor / Limiter', 'Динамика канала консоли.', 'Меняет punch и density.', '1–4 dB GR как старт.'),
        ctl('EQ bands', 'Полосы консольного EQ.', 'Характер зависит от модели (E/G/N/Focusrite).', '±1–4 dB broad moves.'),
        ctl('TMT Channel', 'Выбирает допуск компонента канала.', 'Даёт мелкие отличия между tracks.', 'Разные Channel на double tracks.'),
        ctl('VCA / Fader / Output', 'Уровень канала и VCA group.', 'Влияет на saturation после обработки.', 'Level-match и проверить sum.'),
    ]


def waves_oneknob(name, role, hear):
    return [
        ctl(name, role, hear, 'Начать 20–40%; поднять только если слышно задачу.'),
        ctl('Output / Trim', 'Компенсирует громкость после макро.', 'Убирает эффект «громче лучше».', 'Обязательный level-match.'),
        ctl('Bypass / Compare', 'Сравнение с исходником.', 'Макро легко обманывает громкостью.', 'Level-matched A/B.'),
        ctl('Automation amount', 'Движение макро по секциям.', 'Один уровень редко подходит всей песне.', 'Автоматизировать между куплетом и припевом.'),
    ]


EXTRA_PRODUCT_CONTROLS = {
    'SSL E-Channel': [
        ctl('Input', 'Уровень в консольный канал.', 'Выше — больше analog/drive ощущения.', 'Без клиппинга Dynamics.'),
        ctl('Filters', 'HPF/LPF до Dynamics или EQ.', 'Чистит rumble и air.', 'HPF по источнику, не всегда On.'),
        ctl('Gate / Exp', 'Gate или expander канала.', 'Режет bleed между ударами.', 'Не убивать ghost notes.'),
        ctl('Compressor', 'VCA compressor канала.', 'Punch и контроль уровня.', '2–4 dB GR; Attack по transient.'),
        ctl('EQ (HF / HMF / LMF / LF)', 'Четыре полосы SSL E EQ.', 'HMF/LMF особенно характерны.', 'Сначала cut, потом small boost.'),
        ctl('DYN to EQ / Split', 'Порядок Dynamics и EQ.', 'Меняет, что попадает в detector.', 'Сравнить оба порядка.'),
        ctl('Output', 'Финальный уровень канала.', 'Нужен честный bypass.', 'Level-match.'),
    ],
    'SSL G-Channel': [
        ctl('Input', 'Уровень в G-series канал.', 'Влияет на плотность и drive.', 'Оставить запас.'),
        ctl('Filters', 'HPF/LPF консоли G.', 'Собирает спектр до EQ/Dyn.', 'По задаче.'),
        ctl('Dynamics', 'Compressor/Gate секции G.', 'Чуть иной glue, чем E.', '1–4 dB GR.'),
        ctl('EQ', 'G-series EQ curves.', 'Часто плотнее в midrange.', 'Broad ±1–3 dB.'),
        ctl('Output', 'Выход канала.', 'Компенсация loudness.', 'Level-match.'),
    ],
    'Waves CLA-76 Black / Blue': [
        ctl('Input', 'Одновременно уровень и количество GR.', 'Выше — больше compression и color.', 'Поднять до 3–8 dB GR.'),
        ctl('Output', 'Компенсация после FET.', 'Не меняет detector как Input.', 'Level-match.'),
        ctl('Attack', 'Скорость FET attack (1 быстро, 7 медленнее).', '1 режет transient, 4–6 сохраняет punch.', 'Начать 3–4.'),
        ctl('Release', 'Скорость восстановления.', 'Быстро добавляет energy.', 'В темп; избегать distortion.'),
        ctl('Ratio (All-Button)', '4/8/12/20 или All-button.', 'All-button — агрессивный эффект.', '4 или 8 для контроля; All parallel.'),
        ctl('Black / Blue', 'Две ревизии FET.', 'Blue быстрее/ярче, Black плотнее.', 'Сравнить на том же Input.'),
    ],
    'Waves CLA-2A': [
        ctl('Peak Reduction', 'Количество opto compression.', 'Плавное выравнивание без резкого attack.', '2–6 dB GR.'),
        ctl('Gain', 'Makeup после opto.', 'Возвращает уровень.', 'Level-match.'),
        ctl('Limit / Compress', 'Два режима степени сжатия.', 'Limit жёстче.', 'Compress как старт.'),
        ctl('HF / Sidechain filter', 'Облегчает реакцию на highs.', 'Меньше pumping от sibilance.', 'По вокалу.'),
    ],
    'Waves CLA-3A': [
        ctl('Peak Reduction', 'Сила solid-state leveling.', 'Быстрее и ярче, чем 2A.', '2–5 dB GR.'),
        ctl('Gain', 'Компенсация уровня.', 'Честный A/B.', 'Level-match.'),
        ctl('Comp / Limit', 'Степень сжатия.', 'Limit агрессивнее.', 'Comp для vocal/guitar.'),
    ],
    'Waves API 2500': [
        ctl('Threshold', 'Порог VCA bus compressor.', 'Ниже — больше glue.', '0.5–3 dB GR на bus.'),
        ctl('Ratio / Attack / Release', 'Форма и timing compression.', 'Меняет punch vs glue.', '2:1–4:1; Attack средне.'),
        ctl('Knee / Thrust', 'Плавность и тональный sidechain.', 'Thrust меняет, что управляет GR.', 'Med Knee; Thrust по низким.'),
        ctl('Type (Old / New)', 'Характер VCA path.', 'Old грязнее/плотнее.', 'Сравнить на bus.'),
        ctl('Mix / Output', 'Parallel и makeup.', 'Dry attack + compressed body.', 'Mix 40–80% на drums.'),
    ],
    'Waves SSL G-Master Buss Compressor': [
        ctl('Threshold', 'Порог mix-bus glue.', 'Ниже — сильнее склейка.', '0.5–2 dB GR.'),
        ctl('Ratio', '2:1 / 4:1 / 10:1.', '4:1 классический glue.', '4:1 как старт.'),
        ctl('Attack / Release', 'В том числе Auto release.', 'Auto следует материалу.', 'Attack 10–30 ms; Auto Release.'),
        ctl('Makeup', 'Компенсация bus.', 'Не должна маскировать GR.', 'Level-match.'),
        ctl('Mix', 'Dry/wet bus compression.', 'Оставляет transients.', '70–100% на mix bus.'),
    ],
    'Waves Vocal Rider': [
        ctl('Target', 'Целевой уровень вокала.', 'Выше — rider поднимает тихие фразы сильнее.', 'По среднему уровню куплета.'),
        ctl('Range', 'Максимальный автоматический ход.', 'Большой Range слышен как «ездит фейдер».', '±3–6 dB.'),
        ctl('Sensitivity', 'Насколько мелкие изменения ловятся.', 'Выше — больше движения.', 'Средне; не ловить каждый вздох.'),
        ctl('Vocal / Music', 'Отличает вокал от музыки в detector.', 'Неправильный режим даёт ложные ходы.', 'Vocal для lead.'),
        ctl('Attack / Release', 'Скорость фейдера.', 'Слишком быстро — pumping.', 'Медленнее, чем обычный compressor.'),
        ctl('Output', 'Итоговый уровень после rider.', 'Нужен запас до compressor/limiter.', 'Проверить пики.'),
    ],
    'Bass Rider': [
        ctl('Target', 'Целевой уровень баса.', 'Выравнивает ноты без сильного squash.', 'По тихим нотам.'),
        ctl('Range', 'Ход автоматического фейдера.', 'Слишком широко — слышны скачки.', '±3–6 dB.'),
        ctl('Sensitivity', 'Реакция на артикуляцию.', 'Высокая ловит ghost/ghosted notes.', 'Средне.'),
        ctl('Attack / Release', 'Скорость выравнивания.', 'Должна следовать фразам, не транsienтам.', 'Медленнее compressor.'),
        ctl('Output', 'Компенсация.', 'Честный A/B.', 'Level-match.'),
    ],
    'Renaissance Vox': [
        ctl('Gate', 'Простой порог шума.', 'Режет дыхания и room.', 'Только явный шум.'),
        ctl('Comp', 'Сила вокальной compression.', 'Быстрый vocal control.', 'До ровной фразы, без squashing.'),
        ctl('Energy', 'Верхняя плотность/presence.', 'Добавляет близость.', 'Мало; следить за sibilance.'),
        ctl('Output', 'Выход.', 'Level-match.', 'Обязательно.'),
    ],
    'Waves H-Comp': [
        ctl('Analog', 'Моделирует analog behavior.', 'Меняет punch и color.', 'Сравнить On/Off.'),
        ctl('Threshold / Ratio', 'Основная compression.', 'Классический VCA-like контроль.', '2–5 dB GR.'),
        ctl('Attack / Release', 'Включая Auto.', 'Punch vs leveling.', 'По groove.'),
        ctl('Punch', 'Подчёркивает transient до GR.', 'Больше click/attack.', 'Начать умеренно.'),
        ctl('Mix / Output', 'Parallel и makeup.', 'Возвращает dry.', 'Mix 50–80%.'),
    ],
    'Waves Renaissance Compressor': [
        ctl('Threshold / Ratio', 'Сила electro/opto compression.', 'Opto мягче, Electro быстрее.', '2–5 dB GR.'),
        ctl('Attack / Release / Auto', 'Envelope.', 'Auto удобен на vocal.', 'Сначала Auto, затем вручную.'),
        ctl('Electro / Opto', 'Два характера.', 'Меняет плотность и реакцию.', 'Opto vocal; Electro drums/bus.'),
        ctl('Warm / Smooth / Output', 'Тональный характер и makeup.', 'Warm добавляет низ/гармоники.', 'Output level-match.'),
    ],
    'Waves H-Delay': [
        ctl('Delay Time / Sync / Ping-Pong', 'Время и рисунок повторов.', 'Slap, 1/8, dotted, stereo bounce.', 'Сначала Time, потом Feedback.'),
        ctl('Feedback', 'Длина хвоста repeats.', 'Высокий Feedback опасен по уровню.', '10–35%.'),
        ctl('Analog / LoFi / Depth', 'Характер delay machine.', 'Грязнее и уже по спектру.', 'Analog On для vocal slap.'),
        ctl('LPF / HPF', 'Фильтры delay path.', 'Освобождают dry source.', 'HPF 150–400 Hz, LPF 4–8 kHz.'),
        ctl('Mod', 'Модуляция repeats.', 'Ширина и vintage movement.', 'Малая Depth.'),
        ctl('Mix / Output', 'Dry/wet.', 'На send 100% wet.', '100% на return.'),
    ],
    'Waves L2': [
        ctl('Threshold', 'Порог limiting.', 'Ниже — громче и больше GR.', '1–4 dB GR.'),
        ctl('Out Ceiling', 'Выходной потолок.', 'Для delivery/codec.', '-0.3 до -1.0 dBTP по задаче.'),
        ctl('Release / Auto', 'Восстановление limiter.', 'Короткий Release даёт pumping.', 'Auto или средне.'),
        ctl('IDR / Quantize / Dither', 'Финальный wordlength.', 'Нужен на последней стадии.', 'Только на финальном bounce.'),
    ],
    'Waves L1': [
        ctl('Threshold', 'Порог Ultramaximizer.', 'Сильнее — плотнее и громче.', '1–3 dB.'),
        ctl('Out Ceiling', 'Пиковый потолок.', 'Запас под codec.', '-0.3 dB как старт.'),
        ctl('Release', 'Скорость восстановления.', 'Влияет на punch.', 'По материалу.'),
        ctl('Quantize / Dither', 'Финализация разрядности.', 'Только в конце цепи.', 'Не оставлять на всех tracks.'),
    ],
    'Waves C6': [
        ctl('Bands / Freq / Q', 'Шесть динамических полос.', 'Делит спектр для точечного GR.', 'Начать 1–2 полосы.'),
        ctl('Range / Threshold', 'Глубина и чувствительность band.', 'Range ограничивает обработку.', '1–3 dB Range.'),
        ctl('Attack / Release', 'Envelope каждой полосы.', 'Меняет punch и pumping.', 'По событиям внутри band.'),
        ctl('Float / Internal/External SC', 'Боковые динамические bands и key.', 'Для de-ess/de-boom без статичного EQ.', 'Float на sibilance/boom.'),
        ctl('Mix / Output', 'Parallel multiband.', 'Возвращает microdynamics.', 'Level-match.'),
    ],
    'Waves C4': [
        ctl('Crossovers', 'Четыре частотные зоны.', 'Определяет, что считается low/low-mid/high.', 'Не дробить слишком мелко.'),
        ctl('Range / Threshold', 'Динамика каждой зоны.', 'Малый Range прозрачнее.', '1–3 dB.'),
        ctl('Attack / Release', 'Timing по band.', 'Низ обычно медленнее.', 'По groove.'),
        ctl('Output', 'Общий makeup.', 'Честный A/B.', 'Level-match.'),
    ],
    'Scheps Omni Channel': [
        ctl('Pre / Filters', 'Вход, HPF/LPF, phase.', 'Чистит и задаёт headroom.', 'HPF по rumble.'),
        ctl('Gate / Exp', 'Динамический noise/bleed control.', 'Может резать дыхания.', 'Мягкий Range.'),
        ctl('Focus / De-Ess', 'Точечный mid/high control.', 'Убирает harsh/sibilance.', 'Малый Range.'),
        ctl('Compressor 1 / 2', 'Два разных компрессора подряд.', 'Serial vocal/drum control.', 'По 1–3 dB на каждый.'),
        ctl('EQ', 'Полосы Scheps EQ.', 'Характерный mid punch.', '±1–4 dB.'),
        ctl('Saturation', 'Color до/после динамики.', 'Плотность и harmonics.', 'До слышимого, затем чуть назад.'),
        ctl('Output', 'Выход канала.', 'Level-match.', 'Обязательно.'),
    ],
    'CLA Vocals': cla_signature([
        ctl('Pitch', 'Короткий pitch/delay character.', 'Ширина и doubling.', 'Мало на lead; больше на layer.'),
        ctl('Reverb / Delay', 'Встроенные space sends.', 'Глубина вокала.', 'Сначала Delay slap, потом Reverb.'),
        ctl('Distortion', 'Легкий grit на вокале.', 'Близость и агрессия.', 'До появления hash на S.'),
    ]),
    'CLA Drums': cla_signature([
        ctl('Bass / Treble', 'Тональный баланс drum bus/track.', 'Вес vs cymbal bite.', 'По kick/snare в миксе.'),
        ctl('Compress', 'Плотность барабанов.', 'Glue и punch.', 'Не сплющить ghost notes.'),
        ctl('Reverb / Delay / Pitch', 'Пространство и width drums.', 'Размер комнаты.', 'Мало на bus, больше на snare send.'),
    ]),
    'CLA Bass': cla_signature([
        ctl('Sub / Bass / Treble', 'Низ и articulation баса.', 'Sub для веса, Treble для пальцев.', 'Проверить mono и phones.'),
        ctl('Compress', 'Выравнивание нот.', 'Ровнее уровень.', '3–6 dB ощущаемого контроля.'),
        ctl('Distortion', 'Grit баса.', 'Читаемость на маленьких системах.', 'Parallel-ощущение, не ломать sub.'),
    ]),
    'CLA Guitar': cla_signature([
        ctl('Bass / Treble', 'Вес и искристость гитары.', 'Конфликт с басом/вокалом.', 'Резать низ, если мешает bass.'),
        ctl('Compress', 'Устойчивость риффа.', 'Плотнее performance.', 'Сохранять pick attack.'),
        ctl('Reverb / Delay / Pitch', 'Пространство гитары.', 'Ширина и depth.', 'Часто лучше внешние sends.'),
    ]),
    'Waves DeEsser': [
        ctl('Frequency', 'Центр сибилянтов.', '4–8 kHz типично для S.', 'Искать самое резкое S.'),
        ctl('Threshold', 'Чувствительность.', 'Ниже — чаще reduction.', 'Только явные S.'),
        ctl('Mode Wide / Split', 'Весь сигнал или только highs.', 'Split прозрачнее.', 'Сравнить оба.'),
        ctl('Audio / Sidechain listen', 'Слушает detector.', 'Не вырезать полезный air.', 'Audition при настройке.'),
    ],
    'Waves Sibilance': [
        ctl('Detection', 'Находит sibilance по паттерну, не только по EQ.', 'Меньше ложных срабатываний на hats.', 'Vocal режим для вокала.'),
        ctl('Threshold / Range', 'Когда и насколько глушить S.', 'Большой Range даёт lisp.', '2–4 dB.'),
        ctl('Frequency / Mode', 'Область и характер reduction.', 'Split обычно естественнее.', 'Проверить слова с С/Ш.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'Waves Clarity Vx': [
        ctl('Ambience / Dialogue', 'Баланс речи и пространства.', 'Убирает room, может сделать watery.', 'Малый Amount; слушать согласные.'),
        ctl('Neural / Sensitivity', 'Насколько агрессивно отделяется голос.', 'Выше — больше artifacts.', 'Начать низко.'),
        ctl('Voice Focus', 'Удерживает полезный vocal/speech.', 'Слишком сильно — watery/lisp.', 'Проверять согласные и паузы.'),
        ctl('Output', 'Уровень после очистки.', 'Не маскировать artifacts громкостью.', 'Level-match.'),
    ],
    'API 550A': [
        ctl('Low / Mid / High bands', 'Три пропорциональных API полосы.', 'Proportional Q: больше gain — уже полоса.', '±2–4 dB.'),
        ctl('Frequency switches', 'Фиксированные частоты API.', 'Характерный mid punch.', 'Сначала найти нужную частоту.'),
        ctl('Recess / Peak', 'Cut или boost полосы.', 'Cut часто полезнее boost.', 'Сначала Recess проблем.'),
        ctl('Output', 'Уровень после EQ.', 'Честный A/B.', 'Level-match.'),
    ],
    'API 550B': [
        ctl('Four bands', 'Четыре API proportional-Q полосы.', 'Плотная середина.', '±1–4 dB.'),
        ctl('Frequency selectors', 'Дискретные частоты.', 'Быстрый musical workflow.', 'Не ставить все bands в boost.'),
        ctl('Peak / Shelf where available', 'Форма полосы.', 'Shelf для краёв, peak для mid.', 'По задаче.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'API 560': [
        ctl('10 graphic bands', 'Графический API EQ.', 'Быстрые тональные жесты.', '±1–3 dB, не рисовать «смайлик».'),
        ctl('Band Gain', 'Уровень каждой фиксированной полосы.', 'Сильно окрашивает mid.', 'Малые движения.'),
        ctl('Output', 'Выход.', 'Честный A/B.', 'Level-match.'),
    ],
    'Scheps 73': [
        ctl('Preamp / Drive', '1073-style input color.', 'Выше — harmonics и плотность.', 'До легкого окраса.'),
        ctl('HF / Mid / LF', 'Полосы Neve-подобного EQ.', 'Плотная mid и широкий low.', '±1–4 dB.'),
        ctl('HPF', 'Срез низа до/вместе с EQ.', 'Собирает rumble.', 'По источнику.'),
        ctl('Output', 'Компенсация после preamp/EQ.', 'Level-match.', 'Обязательно.'),
    ],
    'PuigTec EQP-1A': [
        ctl('Low Boost / Attenuate', 'Классический Pultec low trick.', 'Одновременный boost/cut даёт special curve.', 'Малые значения.'),
        ctl('High Boost / Attenuate / Bandwidth', 'Воздух и сглаживание верха.', 'Широкий boost + attenuate = musical top.', 'Не пересветить sibilance.'),
        ctl('Frequency selectors', 'Дискретные Pultec частоты.', 'Определяют характер кривой.', 'Сначала частоту, потом amount.'),
        ctl('Output', 'Уровень.', 'Level-match.', 'Обязательно.'),
    ],
    'Waves J37 Tape': [
        ctl('Tape Speed / Bias / Flux', 'Скорость ленты и насыщение.', '15 IPS ярче, 7.5 плотнее/темнее.', 'Сначала Speed, потом Bias/Flux.'),
        ctl('Wow / Flutter', 'Нестабильность высоты.', 'Vintage movement; много — раздражает.', 'Низко на vocal/lead.'),
        ctl('Noise', 'Уровень ленточного шума.', 'Аутентичность vs тишина.', 'Выключить, если мешает.'),
        ctl('Delay / Wow paths', 'Короткие tape delay режимы.', 'Slap и thickness.', 'По задаче, не всегда On.'),
        ctl('Input / Output', 'Уровень на ленту и компенсация.', 'Сильнее Input — больше tape compression.', 'Level-match Output.'),
    ],
    'Waves Kramer Master Tape': [
        ctl('Speed / Flux / Bias', 'Поведение ленты.', 'Меняет saturation и HF.', 'Сравнить 7.5 vs 15.'),
        ctl('Wow / Flutter / Noise', 'Механика и шум.', 'Характер vs чистота.', 'Минимум на master.'),
        ctl('Delay', 'Slap с ленты.', 'Короткая глубина.', 'Малый Mix.'),
        ctl('Input / Output', 'Насыщение и компенсация.', 'Честный A/B.', 'Level-match.'),
    ],
    'Waves Trans-X': [
        ctl('Duration', 'Длина окна атаки/хвоста.', 'Отделяет click от body.', 'Короче для kick click.'),
        ctl('Range', 'Сила изменения envelope.', 'Больше — явнее эффект.', 'Начать ±10–20%.'),
        ctl('Sensitivity', 'Какие события считаются transient.', 'Высокая ловит всё подряд.', 'По устойчивым ударам.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'dbx 160': [
        ctl('Threshold', 'Порог hard-knee VCA.', 'Ниже — больше GR и punch.', '2–6 dB GR.'),
        ctl('Compression', 'Сила сжатия (ratio-style).', 'Выше — плотнее и жёстче.', 'Умеренно на bass/drums.'),
        ctl('Output Gain', 'Makeup.', 'Честный A/B.', 'Level-match.'),
        ctl('Over Easy / Hard', 'Плавность входа, если доступна в версии.', 'Soft естественнее.', 'Сравнить на transient.'),
    ],
    'Waves InPhase': [
        ctl('Polarity', 'Инверсия выбранного канала.', 'Может вернуть низ при суммировании.', 'Проверить первым.'),
        ctl('Delay', 'Сдвиг во времени.', 'Совмещает атаки микрофонов.', 'По основной атаке.'),
        ctl('Phase Shift / Frequency', 'Частотно-зависимый phase.', 'Когда delay недостаточно.', 'После polarity/delay.'),
        ctl('Gain / Correlation display', 'Выравнивание и визуальный контроль.', 'Не заменяет слух и mono.', 'Подтвердить в моно.'),
    ],
    'Waves F6 Dynamic EQ': [
        ctl('Band Frequency / Q / Gain', 'Статическая часть каждой из 6 полос.', 'Обычный EQ плюс динамика.', 'Сначала найти проблему.'),
        ctl('Range / Threshold', 'Динамический ход полосы.', 'Полоса работает только на пике.', '±1–4 dB Range.'),
        ctl('Attack / Release', 'Envelope dynamic band.', 'Сохраняет или режет transient.', 'По событию.'),
        ctl('External Sidechain', 'Полоса слушает другой источник.', 'Frequency-selective ducking.', 'Kick→bass, vocal→pad.'),
        ctl('Output', 'Общий уровень.', 'Level-match.', 'Обязательно.'),
    ],
    'Soundtoys Little AlterBoy': [
        ctl('Drive', 'Сатурация до pitch/formant.', 'Грязнее vocal FX.', 'Мало на lead, больше на layer.'),
        ctl('Pitch', 'Сдвиг высоты в полутонах.', 'Грубый vocal/instrument transpose.', '±2–7 st для FX.'),
        ctl('Formant', 'Сдвиг резонаторов голоса.', 'Меняет «пол/размер» без pitch.', 'Отдельно от Pitch.'),
        ctl('Robot / Quantize', 'Притягивает pitch к сетке.', 'Hard-tune character.', 'По задаче, не всегда.'),
        ctl('Mix / Output', 'Dry/wet и уровень.', 'Parallel безопаснее.', '50–100% по роли.'),
    ],
    'Soundtoys Effect Rack': [
        ctl('Slot modules', 'Цепочка внутренних Soundtoys эффектов.', 'Порядок модулей критичен.', 'Не включать всё сразу.'),
        ctl('Input / Output / Mix', 'Общий уровень рэка.', 'Накопление loudness.', 'Bypass по модулю + level-match.'),
        ctl('Rhythm / Tap', 'Синхронизация time-based slots.', 'Общий groove рэка.', 'Сверить с темпом.'),
        ctl('Hot knobs / Recycle', 'Макро и feedback вокруг рэка.', 'Быстрые жесты и runaway.', 'Limiter после сильного Recycle.'),
    ],
    'Soundtoys Radiator': [
        ctl('Bass / Treble', 'Двухполосный analog color.', 'Вес и искристость.', 'Малые усиления.'),
        ctl('Heat', 'Насыщение схемы.', 'Плотность и harmonics.', 'До слышимого окраса.'),
        ctl('Mic / Mix', 'Характер входа и parallel.', 'Меняет плотность mid.', 'Mix 30–100%.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'Soundtoys PhaseMistress': [
        ctl('Tweak / Style', 'Алгоритм phaser.', 'От мягкого movement до metallic.', 'Сначала Style.'),
        ctl('Rate / Depth', 'Скорость и глубина sweeps.', 'Определяет заметность.', 'Медленно и мало на bus.'),
        ctl('Resonance / Stages', 'Острота и сложность notches.', 'Больше stages — сложнее спектр.', 'Не свистеть на vocal.'),
        ctl('Mix / Output', 'Dry/wet.', 'Parallel сохраняет центр.', '20–50% типично.'),
    ],
    'Soundtoys Tremolator': [
        ctl('Depth', 'Глубина амплитудной модуляции.', 'Сильнее — явнее тремоло.', 'Начать 20–40%.'),
        ctl('Rhythm / Rate', 'Сетка и скорость.', 'Должна сесть в groove.', 'Sync по темпу.'),
        ctl('Shape / Accent', 'Форма волны и акценты.', 'Меняет ощущение ритма.', 'Простые shapes сначала.'),
        ctl('Mix', 'Количество эффекта.', 'Сохраняет dry.', 'По роли.'),
    ],
    'Soundtoys Crystallizer': [
        ctl('Splice / Pitch', 'Гранулярный сдвиг кусков.', 'Pitch-up shimmer или darker slices.', 'Малый Mix на bus.'),
    ctl('Delay / Feedback', 'Время между slices и накопление.', 'Создаёт repeats/texture.', 'Контролировать пики.'),
        ctl('Smoothing / Gate', 'Стыки зёрен и порог.', 'Меньше кликов, меньше хвостов.', 'По материалу.'),
        ctl('Mix / Output', 'Parallel sound design.', 'Dry source обязателен.', '10–40% или send.'),
    ],
    'Soundtoys Devil-Loc': [
        ctl('Crush', 'Количество разрушительной компрессии.', 'Громко, грязно, мало динамики.', 'Parallel.'),
        ctl('Crunch', 'Сатурация/искажение.', 'Добавляет grit.', 'До появления hash.'),
        ctl('Mix / Output', 'Dry/wet.', 'Возвращает punch.', '10–40%.'),
    ],
    'Sie-Q': [
        ctl('Low / Mid / High', 'Простой трёхполосный EQ.', 'Быстрые musical moves.', '±1–3 dB.'),
        ctl('Drive', 'Легкий analog color.', 'Плотность.', 'Мало.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'EchoBoy Jr': [
        ctl('Time / Note', 'Время echo.', 'Slap или rhythmic.', '1/8 или 80–140 ms.'),
        ctl('Style', 'Характер junior EchoBoy.', 'Меняет saturation/bandwidth.', 'Сначала Style.'),
        ctl('Feedback / Mix', 'Длина и dry/wet.', 'На send 100% wet.', 'Feedback 10–30%.'),
    ],
    'FabFilter Micro': [
        ctl('Threshold / Ratio-style gain reduction', 'Очень простой compressor.', 'Быстрый vocal/track control.', '2–5 dB GR.'),
        ctl('Release', 'Восстановление.', 'По фразе.', 'Auto-ощущение вручную.'),
        ctl('Output', 'Makeup.', 'Level-match.', 'Обязательно.'),
    ],
    'FabFilter Simplon': [
        ctl('Cutoff / Peak', 'Частота и резонанс фильтра.', 'Движение тембра.', 'Peak низкий, пока не нужен свист.'),
        ctl('LP / HP / BP modes', 'Тип фильтра.', 'Разные роли в миксе.', 'LP для synth, HP для cleanup.'),
        ctl('Routing / Slope', 'Последовательность двух фильтров.', 'Круче — агрессивнее.', 'Сначала один фильтр.'),
    ],
    'FabFilter Volcano 3': [
        ctl('Filter bands / Routing', 'Несколько фильтров и схема.', 'Сложный motion design.', 'Начать с одного фильтра.'),
        ctl('Cutoff / Peak / Drive', 'Тон и насыщение фильтра.', 'Drive добавляет harmonics.', 'Peak контролировать.'),
        ctl('Modulation (XLFO / Envelope / XY)', 'Источники движения.', 'Оживляет cutoff.', 'Одна связь за раз.'),
        ctl('Mix / Output', 'Dry/wet.', 'Parallel безопаснее.', 'По задаче.'),
    ],
    'FabFilter One': [
        ctl('Waveform / Pulse Width', 'Источник осциллятора.', 'Определяет спектр.', 'Сначала волну, потом filter.'),
        ctl('Filter Cutoff / Peak', 'Тон синтеза.', 'Закрытый фильтр — темнее.', 'Автоматизировать cutoff.'),
        ctl('Amp Envelope', 'ADSR громкости.', 'Атака и длина ноты.', 'Под роль.'),
        ctl('Mod / Portamento', 'Вибрато и скольжение.', 'Movement и legato.', 'Малая глубина.'),
        ctl('Output', 'Уровень инструмента.', 'Headroom inserts.', 'Пики с запасом.'),
    ],
    'FabFilter Twin 3': [
        ctl('Oscillators / Unison', 'Несколько осцилляторов и голоса.', 'Плотность и ширина.', 'Unison проверить в mono.'),
        ctl('Filters / Routing', 'Фильтры синтеза.', 'Основной тон патча.', 'Один фильтр сначала.'),
        ctl('Envelopes / XLFO', 'Модуляция.', 'Движение патча.', 'Одна ясная связь.'),
        ctl('FX / Output', 'Встроенные эффекты и уровень.', 'Могут заменить внешнюю chain.', 'Отключать ненужный reverb.'),
    ],
    'Ozone Maximizer': ozone_module([
        ctl('Mode (IRC)', 'Алгоритм maximizer.', 'Меняет punch vs loudness.', 'Сравнить IRC на пиках.'),
        ctl('Threshold / Ceiling', 'Громкость и потолок.', 'Ниже Threshold — больше GR.', '1–3 dB; Ceiling по delivery.'),
        ctl('Character / Transient Emphasis', 'Сохранение атаки.', 'Меньше squash на drums/vocal.', 'Слушать snare и S.'),
        ctl('True Peak', 'Межсемпловые пики.', 'Безопаснее для codec.', 'On для финала.'),
    ]),
    'Ozone Equalizer': ozone_module([
        ctl('Band Shape / Freq / Gain / Q', 'Полосы mastering EQ.', 'Точная коррекция на bus/master.', '±0.3–1.5 dB.'),
        ctl('Mid/Side / Stereo', 'Независимый center/sides.', 'Ширина vs центр.', 'M/S только по диагнозу.'),
        ctl('Phase mode', 'Minimum / Linear / Mixed.', 'Linear может дать pre-ring.', 'Minimum для большинства случаев.'),
    ]),
    'Ozone Imager': ozone_module([
        ctl('Width / Stereoize', 'Ширина по полосам.', 'Слишком широко ломает mono.', 'Не расширять sub.'),
        ctl('Bands / Crossovers', 'Где меняется ширина.', 'Низ стабильный, верх шире.', '1–2 полосы.'),
        ctl('Vectorscope / Correlation', 'Визуальный контроль.', 'Не заменяет mono check.', 'Слушать mono.'),
    ]),
    'Ozone Exciter': ozone_module([
        ctl('Mode (Retro/Tape/Tube/Warm)', 'Тип гармоник.', 'Меняет цвет.', 'Сравнить при одном Output.'),
        ctl('Amount / Mix', 'Сила возбуждения.', 'Легко сделать harsh.', 'Мало на master.'),
        ctl('Post Filter', 'Ограничивает спектр гармоник.', 'Убирает hash сверху.', 'При необходимости.'),
    ]),
    'Ozone Dynamics': ozone_module([
        ctl('Threshold / Ratio / Attack / Release', 'Компрессия/лимитирование модуля.', 'Контроль шины.', '0.5–2 dB GR.'),
        ctl('Detection / Knee', 'Как считается уровень.', 'Влияет на незаметность.', 'Soft knee на master.'),
        ctl('Mix', 'Parallel dynamics.', 'Сохраняет microdynamics.', '70–100%.'),
    ]),
    'Ozone Vintage Compressor': ozone_module([
        ctl('Threshold / Ratio', 'Винтажная bus compression.', 'Плотность и glue.', '0.5–2 dB.'),
        ctl('Attack / Release', 'Характерный envelope.', 'Punch vs glue.', 'По материалу.'),
        ctl('Mode / Mix', 'Характер схемы и parallel.', 'Меняет color.', 'Сравнить режимы.'),
    ]),
    'Ozone Vintage Limiter': ozone_module([
        ctl('Mode', 'Характер vintage limiting.', 'От прозрачного к плотному.', 'Сравнить на cymbals.'),
        ctl('Threshold / Ceiling', 'Громкость и потолок.', 'Легко убить transients.', '1–3 dB.'),
        ctl('Character', 'Плотность/атака.', 'Слушать kick/snare.', 'Не гнаться за LUFS.'),
    ]),
    'Ozone Vintage EQ': ozone_module([
        ctl('Low / Mid / High bands', 'Винтажные кривые.', 'Широкие musical moves.', '±0.5–2 dB.'),
        ctl('Drive / Output', 'Окрас и компенсация.', 'Плотность сверху обработки.', 'Level-match.'),
    ]),
    'Ozone Low End Focus': ozone_module([
        ctl('Listen / Contrast', 'Показывает проблемный низ.', 'Помогает найти boom vs punch.', 'Сначала Listen.'),
        ctl('Action / Amount', 'Сглаживание или подчёркивание низа.', 'Слишком сильно — каша или дырка.', 'Малый Amount.'),
        ctl('Frequency range', 'Какой низ обрабатывается.', 'Не задеть вокал/гитары.', 'По фундаменту.'),
    ]),
    'Ozone Stabilizer': ozone_module([
        ctl('Amount / Speed', 'Насколько сильно выравнивается спектр.', 'Быстро может дышать.', 'Мало и медленно на master.'),
        ctl('Cutoff / Smoothing', 'Какие области трогает.', 'Не выгладить характер.', 'Исключить нужный character.'),
        ctl('Delta / Listen', 'Слышит, что меняется.', 'Ловит overprocessing.', 'Регулярно.'),
    ]),
    'Ozone Match EQ': ozone_module([
        ctl('Learn / Apply', 'Снимает спектр референса.', 'Легко скопировать чужой баланс слишком сильно.', '20–40% apply.'),
        ctl('Smoothing / Range', 'Грубость коррекции.', 'Узкие пики звучат искусственно.', 'Сильно сгладить.'),
        ctl('Amount', 'Глубина переноса спектра.', 'Главный контроль натуральности.', 'Начать 15–30%.'),
    ]),
    'Ozone Tonal Balance Control': [
        ctl('Target curve', 'Целевой жанровый баланс.', 'Ориентир, не закон.', 'Выбрать близкий референс.'),
        ctl('Broad / Fine view', 'Масштаб анализа.', 'Не править каждый пик.', 'Смотреть broad.'),
        ctl('Gain match / Bypass', 'Честное сравнение.', 'Громкость обманывает.', 'Всегда match.'),
        ctl('Monitoring only', 'Не печатать в export.', 'Это контроль, не процессор тона.', 'Исключить из render chain.'),
    ],
    'Ozone Spectral Shaper': ozone_module([
        ctl('Threshold / Speed', 'Сглаживание резких спектральных пиков.', 'Убирает harsh без широкого EQ.', 'Малый Amount.'),
        ctl('Frequency focus', 'Где искать sharpness.', '2–8 kHz типично.', 'По жалобе слуха.'),
        ctl('Listen', 'Слышит удаляемое.', 'Не вырезать air целиком.', 'При настройке.'),
    ]),
    'Ozone Spectral Denoiser': ozone_module([
        ctl('Threshold / Reduction', 'Насколько глушится шум.', 'Сильно — watery artifacts.', 'Только слышный шум.'),
        ctl('Learn / Profile', 'Профиль шума.', 'Нужен кусок без полезного сигнала.', 'Обучить на паузе.'),
        ctl('Tone / Artifact control', 'Баланс чистоты и артефактов.', 'Слушать хвосты и S.', 'Остановить при metallic.'),
    ]),
    'Ozone 12 suite': [
        ctl('Module chain / Bypass', 'Набор Ozone modules.', 'Порядок и лишние modules портят master.', 'Только нужные modules.'),
        ctl('Assistant / Targets', 'Стартовая цель громкости/тона.', 'Не финальный пресет.', 'После Assistant всё проверить ушами.'),
        ctl('I/O / Gain match', 'Вход/выход suite.', 'Честный A/B всего Ozone.', 'Всегда gain match.'),
        ctl('Dither / Codec preview', 'Финализация и preview доставки.', 'Только в конце.', 'Не на всех шинах.'),
    ],
    'bx_console SSL 4000 E': bx_console(),
    'bx_console SSL 4000 G': bx_console(),
    'bx_console SSL 9000 J': bx_console(),
    'bx_console N': bx_console(),
    'bx_console Focusrite SC': bx_console(),
    'bx_console AMEK 9099': bx_console(),
    'bx_console British Class A': bx_console(),
    'bx_digital V3': [
        ctl('M / S / L / R bands', 'Независимый Mid/Side EQ.', 'Центp vs края.', 'Сначала M, потом S.'),
        ctl('Dynamic EQ', 'Полоса работает по порогу.', 'Только на проблемных пиках.', 'Range 0.5–2 dB.'),
        ctl('Bass / Presence Shift', 'Широкие character сдвиги.', 'Быстрый mastering жест.', 'Очень мало.'),
        ctl('Solo EQ / Mono Maker', 'Слушает полосу; сужает низ в mono.', 'Низ стабильнее.', 'Mono Maker до 80–120 Hz.'),
        ctl('Output / Auto Listen', 'Компенсация и контроль.', 'Level-match.', 'Обязательно.'),
    ],
    'bx_opto': [
        ctl('Gain In / Gain Out', 'Уровень в opto и компенсация.', 'Выше In — больше GR и color.', '2–5 dB GR.'),
        ctl('Time', 'Скорость opto поведения.', 'Медленнее — мягче leveling.', 'По вокалу/басу.'),
        ctl('Peak / RMS feel', 'Как считается уровень.', 'Меняет реакцию на transients.', 'Сравнить.'),
        ctl('Mix', 'Parallel opto.', 'Возвращает dry.', '50–100%.'),
    ],
    'bx_townhouse Buss Compressor': [
        ctl('Threshold / Ratio', 'Bus glue.', 'Склейка группы.', '0.5–2 dB.'),
        ctl('Attack / Release', 'Включая Auto.', 'Punch vs glue.', 'Auto на mix bus часто уместен.'),
        ctl('Makeup / Mix', 'Компенсация и parallel.', 'Честный A/B.', 'Level-match.'),
    ],
    'AMEK EQ 200': [
        ctl('Bands / Proportional Q', 'Гибкий mastering/mix EQ.', 'Прозрачные broad moves.', '±0.5–2 dB.'),
        ctl('M/S', 'Раздельный центр/края.', 'Ширина и вокал.', 'По диагнозу.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'Dangerous BAX EQ': [
        ctl('Low / High Baxandall', 'Очень широкие полки.', 'Меняет весь баланс, не хирургия.', '±0.5–1.5 dB.'),
        ctl('Peq / Filters', 'Дополнительные точечные/фильтр секции.', 'Только если полки не хватает.', 'Минимум полос.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'Dangerous Compressor': [
        ctl('Threshold / Slope', 'Прозрачная bus compression.', 'Мало характера, много контроля.', '0.5–2 dB.'),
        ctl('Attack / Release', 'Timing.', 'Сохраняет transient.', 'Средний Attack.'),
        ctl('Smart / Auto', 'Помогает стабилизировать реакцию.', 'Меньше ручной борьбы.', 'Сравнить Off.'),
        ctl('Output', 'Makeup.', 'Level-match.', 'Обязательно.'),
    ],
    'elysia mpressor': [
        ctl('THD / Gain', 'Уровень и характер.', 'Добавляет плотность.', 'До легкого окраса.'),
        ctl('Attack / Release / Ratio', 'Агрессивный compressor behavior.', 'Может быть очень быстрым.', 'Сначала консервативно.'),
        ctl('Niveau / EQ', 'Тональный наклон при compression.', 'Меняет яркость под GR.', 'Мало.'),
        ctl('Gain Reduction Limiter', 'Ограничивает максимальный GR.', 'Страховка от squashing.', '2–6 dB.'),
        ctl('Mix / Output', 'Parallel.', 'Возвращает dry.', '40–80% creative.'),
    ],
    'elysia alpha compressor': [
        ctl('Threshold / Attack / Release', 'Мастеринг compressor.', 'Очень тонкий glue.', '0.3–1.5 dB.'),
        ctl('Feed Forward / Back', 'Тип детекции.', 'Меняет поведение GR.', 'Сравнить на материале.'),
        ctl('Niveau / EQ', 'Тон под компрессией.', 'Баланс при GR.', 'Минимум.'),
        ctl('M/S / Mix', 'Раздельная динамика и parallel.', 'Центр vs sides.', 'Осторожно с S.'),
    ],
    'elysia museq': [
        ctl('Bands / Gain / Freq', 'Музыкальный EQ elysia.', 'Широкие character curves.', '±1–3 dB.'),
        ctl('Warm / Pure', 'Окрас vs чистота.', 'Warm плотнее.', 'Сравнить.'),
        ctl('Output', 'Компенсация.', 'Level-match.', 'Обязательно.'),
    ],
    'elysia karacter': [
        ctl('Drive / Color', 'Сатурация/дисторшн.', 'От soft harmonics до fuzz.', 'Сначала soft.'),
        ctl('FET / Turbo', 'Более агрессивные режимы.', 'Сильно меняет density.', 'Parallel.'),
        ctl('Mix / Output', 'Dry/wet.', 'Сохраняет dry low.', '20–60%.'),
    ],
    'SPL Transient Designer': [
        ctl('Attack', 'Усиление/ослабление начала.', 'Punch или мягче.', '±1–3 деления.'),
        ctl('Sustain', 'Хвост/room.', 'Больше size или tighter.', '±1–3.'),
        ctl('Gain', 'Компенсация.', 'Level-match.', 'Обязательно.'),
        ctl('Output', 'Выход.', 'Headroom.', 'Без клиппинга.'),
    ],
    'SPL Iron': [
        ctl('Threshold / Attack / Release', 'Vari-mu mastering compressor.', 'Медленный дорогой glue.', '0.5–2 dB.'),
        ctl('Rectifier / Sidechain', 'Характер детекции.', 'Меняет реакцию на низ.', 'По материалу.'),
        ctl('EQ / AirBass', 'Тон под компрессией.', 'Воздух или вес.', 'Очень мало.'),
        ctl('Output', 'Makeup.', 'Level-match.', 'Обязательно.'),
    ],
    'SPL Vitalizer': [
        ctl('Process / Bass / Mid-Hi', 'Спектральное оживление.', 'Легко сделать harsh/boomy.', 'Малые значения.'),
        ctl('LC-EQ / Intensity', 'Акцент низ/верх.', 'Меняет perceived loudness.', 'Level-match обязателен.'),
        ctl('Stereo Expander', 'Ширина.', 'Проверить mono.', 'Мало.'),
        ctl('Output', 'Компенсация.', 'Честный A/B.', 'Обязательно.'),
    ],
    'SPL HawkEye': [
        ctl('Views (LUFS / TP / Spectrum / Phase)', 'Выбор измерителя.', 'Разные вопросы — разные виды.', 'Сначала level match.'),
        ctl('Reference / Integration', 'Окно измерения.', 'Short-term vs integrated.', 'Сбрасывать перед дублем.'),
        ctl('Bypass / Monitoring only', 'Не должен печататься.', 'Это контроль, не эффект.', 'Исключить из export.'),
    ],
    'Maag EQ4': [
        ctl('Sub / 160 / 400 / 2.5 / 4 / 10', 'Фиксированные полосы Maag.', 'Очень музыкальные частоты.', '±1–3 dB.'),
        ctl('Air Band', 'Фирменный верхний воздух.', 'Легко добавить sibilance/noise.', '0.5–2 dB.'),
        ctl('Input / Output', 'Headroom и компенсация.', 'Air Band поднимает уровень.', 'Level-match.'),
    ],
    'Newfangled Saturate': [
        ctl('Oversampling / Antialias', 'Чистый clip/sat без aliasing.', 'Важнее на ярком материале.', 'Высокое offline.'),
        ctl('Drive / Curve', 'Форма насыщения.', 'От soft sat до clip.', '1–3 dB.'),
        ctl('Output / Mix', 'Компенсация и parallel.', 'Честный A/B.', 'Level-match.'),
    ],
    'Newfangled Punctuate': [
        ctl('Bands / Amount', 'Многополосный transient designer.', 'Отделяет click от гула.', 'Малый Amount.'),
        ctl('Adaptive / Speed', 'Насколько следует материалу.', 'Слишком быстро — нервно.', 'Средне.'),
        ctl('Mix / Output', 'Parallel.', 'Сохраняет natural.', 'Level-match.'),
    ],
    'Newfangled Elevate': [
        ctl('Limiter / Adaptive', 'Mastering limiter с адаптацией.', 'Громкость без простого squash.', '1–3 dB.'),
        ctl('Transient / Clip', 'Сохранение атаки vs clip stage.', 'Слушать snare/S.', 'Не гнать LUFS.'),
        ctl('Ceiling / True Peak', 'Потолок доставки.', 'Codec safety.', 'On для финала.'),
    ],
    'ADPTR Metric AB': [
        ctl('References / Level Match', 'A/B с референсами на одной громкости.', 'Без match сравнение бесполезно.', 'Всегда Level Match.'),
        ctl('Filters / Mono / Dim', 'Слушать зоны и mono.', 'Быстрый диагноз.', 'Тихо + mono.'),
        ctl('Spectrum / Dynamics views', 'Визуальное сравнение.', 'Не копировать картинку вслепую.', 'Подтверждать слухом.'),
    ],
    'Waves OneKnob Louder': waves_oneknob('Louder', 'Одно движением поднимает perceived loudness.', 'Громче и плотнее, легко давит transients.'),
    'Waves OneKnob Brighter': waves_oneknob('Brighter', 'Макро на верхнюю яркость.', 'Air/presence; риск harsh и sibilance.'),
    'Waves OneKnob Wetter': waves_oneknob('Wetter', 'Макро пространства.', 'Больше reverb/space.'),
    'Waves OneKnob Driver': waves_oneknob('Driver', 'Макро перегруза.', 'Grit и harmonics.'),
    'Waves OneKnob Pressure': waves_oneknob('Pressure', 'Макро компрессии.', 'Плотность и squash.'),
    'Waves OneKnob Phatter': waves_oneknob('Phatter', 'Макро веса/низа.', 'Больше body; риск mud.'),
    'OneKnob Filter': [
        ctl('Filter', 'Однокнопочный filter sweep.', 'Открывает/закрывает спектр.', 'По автоматизации перехода.'),
        ctl('Mode если доступен', 'LP/HP характер.', 'Разные роли.', 'По задаче.'),
    ],
}

_PAD = [
    ctl('Bypass / Compare', 'Сравнение с исходником на той же громкости.', 'Без A/B легко переоценить эффект.', 'Level-matched bypass.'),
    ctl('Output / Trim', 'Компенсация уровня после обработки.', 'Громкость не должна решать за слух.', 'Сверить с bypass.'),
]
for _name, _ctrls in list(EXTRA_PRODUCT_CONTROLS.items()):
    if len(_ctrls) < 4:
        EXTRA_PRODUCT_CONTROLS[_name] = _ctrls + _PAD[:4 - len(_ctrls)]

for name in [
    'Archetype: Gojira', 'Archetype: Nolly', 'Archetype: Plini', 'Archetype: Petrucci',
    'Archetype: Abasi', 'Archetype: Rabea', 'Archetype: Tim Henson', 'Archetype: Cory Wong',
    'Archetype: Mateus Asato', 'Archetype: Tom Morello', 'Fortin Cali Suite',
    'Fortin Nameless Suite', 'Fortin NTS Suite', 'Omega Ampworks Granophyre',
    'Soldano SLO-100', 'Tone King Imperial MKII', 'Darkglass Ultra', 'Parallax',
    'Ampeg SVT-VR Classic', 'Ampeg B-15N', 'Ampeg SVT-3PRO', 'Ampeg SVT-4PRO',
    'Ampeg SVT-7PRO', 'Ampeg V-4B', 'Ampeg SGT-DI',
    'Friedman BE-100', 'Friedman Dirty Shirley', 'Friedman Buxom Betty',
    'Friedman Smallbox 50', 'Friedman JJ-100', 'Friedman Pink Taco',
    'Diezel VH4', 'Diezel Hagen', 'Diezel Herbert', 'Diezel Schmidt',
    'ENGL E646 VS', 'ENGL E765 Retro Tube', 'Suhr PT100', 'Suhr Badger 30',
    'bx_rockrack V3',
]:
    if name not in EXTRA_PRODUCT_CONTROLS:
        EXTRA_PRODUCT_CONTROLS[name] = neural_amp()

# Remaining well-known products get product-informed status via adapted family
# controls (not a full GUI transcription).
EXTRA_INFORMED_NAMES = {
    'UltraPump', 'Waves MV2', 'Waves MaxxVolume', 'Waves L3', 'Waves L3-16', 'Waves L3-LL',
    'Waves Linear Phase Multiband', 'Waves Linear Phase EQ', 'Waves Q10 / Q2 / Q1',
    'Waves Q-Clone', 'Waves Renaissance EQ 2/4/6', 'Waves Renaissance Reverb',
    'Waves RDeEsser', 'Waves Clarity Vx DeReverb', 'Waves DeBreath', 'Waves NS1',
    'Waves W43', 'Waves Tune', 'Waves Tune Real-Time', 'Waves Berzerk', 'Waves OVox',
    'Waves Morphoder', 'Waves SoundShifter', 'Waves UltraPitch', 'Waves SuperTap',
    'Waves Element 2.0', 'Waves StudioRack', 'Waves MetaFlanger', 'Waves MondoMod',
    'Waves Doubler', 'Waves PS22 Stereo Maker', 'Waves Center', 'Waves MS Matrix',
    'Waves S1 Stereo Imager', 'Waves TrueVerb', 'Waves IR-1', 'Waves Vitamin',
    'Waves Abbey Road Saturator', 'Waves Torque', 'Waves LoAir', 'Waves MaxxBass',
    'Waves RBass / Renaissance Bass', 'Waves Scheps Parallel Particles',
    'Abbey Road TG Mastering Chain', 'Abbey Road RS56', 'Abbey Road Studio 3',
    'Greg Wells MixCentric', 'Greg Wells PianoCentric', 'Greg Wells VoiceCentric',
    'Greg Wells ToneCentric', 'Maserati GRP', 'Maserati DRM', 'Maserati ACG',
    'Maserati B72', 'Maserati VX1', 'Maserati HMX', 'CLA MixDown', 'CLA Unplugged',
    'CLA Effects', 'Butch Vig Drums', 'Butch Vig Vocals', 'Eddie Kramer Drum Channel',
    'Eddie Kramer Bass Channel', 'Eddie Kramer Guitar Channel', 'Eddie Kramer Vocal Channel',
    'JJP Drums', 'JJP Bass', 'JJP Guitar', 'JJP Percussion', 'JJP Piano',
    'JJP Strings & Keys', 'JJP Vocals', 'Kramer HLS Channel', 'Kramer PIE Compressor',
    'Manny Marroquin Triple D', 'Manny Marroquin Delay', 'Manny Marroquin Reverb',
    'Manny Marroquin Distortion', 'PuigTec MEQ-5', 'V-EQ3 / V-EQ4',
    'Waves PuigChild 660', 'Waves C1 Gate/Expander', 'C1 Compressor/Gate',
    'Waves V-Comp', 'Renaissance Axx', 'Waves H-Reverb',
    'Soundtoys Effect Rack', 'Soundtoys Little PrimalTap', 'Soundtoys PrimalTap',
    'Soundtoys Sandman Pro', 'Soundtoys FilterFreak 1',
    'bx_masterdesk / Classic', 'bx_refinement / V3', 'bx_limiter', 'bx_2098',
    'bx_pultec / bx_pultec Pro', 'bx_greenscreamer', 'bx_boom / bx_boom V3',
    'bx_subfilter', 'bx_control V2', 'bx_solo', 'bx_saturator V2',
    'Lindell 50 Series', 'Lindell 80 Series', 'Lindell 6X-500', 'Lindell 7X-500',
    'Lindell SBC', 'Lindell MU-66', 'Suhr Koji Comp', 'ADPTR Sculpt',
    'Shadow Hills Mastering Compressor', 'Shadow Hills Dual Vandergraph',
    'Vertigo VSC-2', 'Vertigo VSM-3', 'Gyraf Gyratec X', 'Stealth Limiter',
    'Looptrotter SA2RATE', 'Millennia TCL-2', 'Phils Cascade',
    'SPL De-Esser', 'SPL Attacker', 'SPL Passeq', 'SPL EQ Ranger / Ranger Plus',
    'SPL TwinTube', 'Unfiltered Audio BYOME', 'Unfiltered Audio TRIAD',
    'Unfiltered Audio DENT', 'Unfiltered Audio Fault', 'Unfiltered Audio Sandman Pro',
    'Unfiltered Audio ZIP', 'Unfiltered Audio G8', 'Unfiltered Audio LION',
    'Gem Voice', 'Overloud Gem Comp 76', 'Overloud Gem Comp 670', 'Gem EQ550',
    'Gem EQ84', 'Gem EQP-1A', 'Mark Studio 2', 'TH-U / TH-U Premium', 'RIR',
    'Overloud Breverb 2', 'Overloud Gem Tapedesk', 'Newfangled Audio Generate',
    'Bettermaker Stereo Limiter', 'Bettermaker Mastering EQ', 'Bettermaker EQ232',
}
