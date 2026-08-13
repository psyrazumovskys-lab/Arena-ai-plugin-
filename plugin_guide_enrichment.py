"""Structured per-plugin practical guides for Plugin Navigator.

The module deliberately separates product-specific catalog facts from curated
starting points and family-level control models. It does not present a generic
family profile as a verified transcription of a product manual.
"""
from collections import defaultdict
import re
from beginner_plugin_copy import beginner_copy


def ctl(name, role, hear, start):
    return {'name': name, 'role': role, 'hear': hear, 'start': start,
            'evidence': 'Product-specific curated map'}


PRODUCT_CONTROLS = {
    'FabFilter Pro-Q 3': [
        ctl('Band / Filter Shape', 'Создаёт Bell, Shelf, Cut, Notch и другие формы.', 'Определяет тип и область коррекции.', 'Сначала выбрать Shape, затем Frequency.'),
        ctl('Frequency', 'Задаёт центральную или граничную частоту band.', 'Перемещает boost/cut по спектру.', 'Искать в контексте полного микса.'),
        ctl('Gain', 'Усиливает или ослабляет band.', 'Меняет tonal balance.', 'Обычно начать с ±0.5–3 dB.'),
        ctl('Q / Slope', 'Меняет ширину bell или крутизну cut.', 'Высокий Q звучит точечно, низкий — широко.', 'Q 0.7–4; узко только по диагнозу.'),
        ctl('Dynamic Range', 'Ограничивает динамическое изменение gain.', 'Band работает только при возникновении проблемы.', 'Начать с Range 1–3 dB.'),
        ctl('Threshold / Auto', 'Задаёт чувствительность dynamic band.', 'Ниже — band срабатывает чаще.', 'Добиться реакции только на проблемных местах.'),
        ctl('Stereo Placement', 'Выбирает Stereo, Left/Right или Mid/Side.', 'Меняет центр или края независимо.', 'M/S применять только после проверки причины.'),
        ctl('Processing Mode', 'Выбирает Zero Latency, Natural Phase или Linear Phase.', 'Меняет phase/latency и transient response.', 'Zero/Natural для tracks; Linear Phase только по задаче.'),
        ctl('Output / Auto Gain', 'Компенсирует общий уровень.', 'Позволяет честно сравнить bypass.', 'Сверять вручную при одинаковой loudness.'),
    ],
    'FabFilter Pro-C 2': [
        ctl('Style', 'Выбирает алгоритм compression.', 'Меняет envelope, color и плотность.', 'Сначала выбрать Style под задачу.'),
        ctl('Threshold', 'Определяет начало gain reduction.', 'Ниже — больше и чаще compression.', 'Настроить по целевому GR.'),
        ctl('Ratio', 'Определяет силу сжатия выше Threshold.', 'Выше — плотнее и жёстче.', '2:1–4:1 как консервативный старт.'),
        ctl('Attack', 'Задаёт скорость реакции detector.', 'Быстро срезает transient, медленно пропускает атаку.', '5–30 ms vocal; 10–40 ms bus.'),
        ctl('Release / Auto Release', 'Задаёт восстановление gain.', 'Коротко даёт movement, длинно — smooth leveling.', 'Вернуть GR до следующего значимого события.'),
        ctl('Knee / Range', 'Меняет плавность и максимальную глубину compression.', 'Soft Knee мягче; Range страхует от overcompression.', 'Range 2–6 dB по роли.'),
        ctl('Lookahead / Hold', 'Уточняет обработку коротких пиков.', 'Больше Lookahead чище, но мягче transient.', 'Использовать минимально необходимое.'),
        ctl('Side Chain / Audition', 'Фильтрует сигнал detector и позволяет его слушать.', 'Уменьшает pumping от ненужного low end.', 'HPF detector 60–150 Hz по материалу.'),
        ctl('Mix / Output / Auto Gain', 'Параллельная смесь и компенсация уровня.', 'Возвращает dry attack и убирает loudness bias.', 'Auto Gain проверить вручную; Output level-match.'),
    ],
    'FabFilter Pro-G': [
        ctl('Style', 'Выбирает Gate/Expander behavior.', 'Меняет скорость и естественность закрытия.', 'Для живого материала начать с мягкого Style.'),
        ctl('Threshold', 'Определяет уровень открытия.', 'Слишком высоко теряет тихие ноты и ghost notes.', 'Настраивать по самым тихим полезным событиям.'),
        ctl('Range', 'Ограничивает максимальное ослабление.', 'Небольшой Range звучит естественнее полного mute.', '6–15 dB как старт.'),
        ctl('Attack', 'Скорость открытия.', 'Медленная атака срезает начало.', '0–5 ms для drums; проверить click.'),
        ctl('Hold', 'Минимальное время открытого gate.', 'Сохраняет тело удара.', 'По длине полезного события.'),
        ctl('Release', 'Скорость закрытия.', 'Определяет естественность хвоста.', 'До следующего удара, без chatter.'),
        ctl('Ratio / Knee', 'Форма expander transition.', 'Мягкие значения меньше заметны.', 'Начать мягко и увеличивать только при необходимости.'),
        ctl('Side Chain / Audition', 'Фильтрует detector.', 'Помогает отличить нужный удар от bleed.', 'Настроить filters в Audition.'),
    ],
    'FabFilter Saturn 2': [
        ctl('Bands / Crossovers', 'Разделяет спектр на независимые зоны saturation.', 'Позволяет сохранить clean low end.', 'Начать с одной band; добавлять только по задаче.'),
        ctl('Style', 'Выбирает тип nonlinear processing.', 'Меняет harmonic profile и compression.', 'Сравнить 2–3 Style при одинаковом output.'),
        ctl('Drive', 'Уровень в saturation stage.', 'Добавляет harmonics, density и clipping.', 'Повышать до слышимого эффекта и немного вернуть.'),
        ctl('Dynamics', 'Меняет внутреннюю динамическую реакцию.', 'Добавляет punch или density.', 'Начать около neutral.'),
        ctl('Tone', 'Наклоняет tonal balance обработки.', 'Делает saturation темнее или ярче.', 'Не усиливать sibilance/harsh cymbals.'),
        ctl('Feedback', 'Возвращает обработанный сигнал.', 'Усиливает резонанс и агрессию.', 'Начать с нуля; контролировать пики.'),
        ctl('Mix / Output', 'Смешивает dry/wet и компенсирует level.', 'Parallel сохраняет transient.', '10–40% для сильного Drive; level-match.'),
        ctl('Modulation', 'Связывает параметры с envelope/LFO/XY.', 'Создаёт динамический color.', 'Одна понятная modulation-связь за раз.'),
    ],
    'Soundtoys Decapitator': [
        ctl('Style A / E / N / T / P', 'Выбирает модель analog saturation.', 'Меняет harmonic balance, bite и low-mid.', 'Сравнить Styles при одинаковых Drive/Output.'),
        ctl('Drive', 'Уровень перегруза.', 'Больше density, harmonics и compression.', 'Начать 1–3; на parallel можно выше.'),
        ctl('Punish', 'Включает экстремальный дополнительный drive.', 'Резко увеличивает distortion и level.', 'Использовать parallel и сначала снизить Output.'),
        ctl('Tone', 'Меняет яркость после/внутри saturation.', 'Сдвигает акцент от тёмного к яркому.', 'Компенсировать harshness после Drive.'),
        ctl('Low Cut / High Cut', 'Фильтрует обрабатываемый результат.', 'Освобождает sub и резкий верх.', 'Фильтровать по роли, особенно на send.'),
        ctl('Thump / Steep', 'Меняет low-frequency behavior фильтров.', 'Добавляет low resonance или более крутой cut.', 'Проверять headroom и mono.'),
        ctl('Mix', 'Смешивает исходный и distorted signal.', 'Возвращает punch и ясность.', '10–40% для aggressive processing.'),
        ctl('Output', 'Компенсирует громкость.', 'Убирает эффект «громче значит лучше».', 'Обязательный level-matched A/B.'),
    ],
    'Waves F6 Dynamic EQ': [
        ctl('Band Frequency', 'Задаёт центр каждой из шести bands.', 'Выбирает конфликтующую область.', 'Искать проблемный момент в контексте.'),
        ctl('Gain', 'Статический boost/cut band.', 'Меняет постоянный tonal balance.', 'Использовать мало, если нужна только динамика.'),
        ctl('Q', 'Ширина band.', 'Уже — точечнее, шире — естественнее.', 'Q 1–4 как старт.'),
        ctl('Range', 'Максимальный динамический boost/cut.', 'Ограничивает слышимость обработки.', 'Обычно ±1–4 dB.'),
        ctl('Threshold', 'Чувствительность dynamic processing.', 'Ниже — band работает чаще.', 'Только на проблемных фразах/ударах.'),
        ctl('Attack / Release', 'Envelope dynamic band.', 'Меняет transient и плавность возврата.', 'Attack сохраняет нужную атаку; Release по groove.'),
        ctl('External Sidechain', 'Управляет band внешним key signal.', 'Создаёт frequency-selective ducking.', 'Выбрать конфликтующую полосу, а не весь спектр.'),
        ctl('Global Output', 'Компенсирует уровень всего EQ.', 'Обеспечивает честный bypass.', 'Level match.'),
    ],
    'Purple Audio MC77': [
        ctl('Input', 'Одновременно задаёт вход и количество compression.', 'Выше — больше GR и color.', 'Поднять до нужного GR.'),
        ctl('Output', 'Компенсирует уровень после compression.', 'Не меняет detector как Input.', 'Level-match с bypass.'),
        ctl('Attack', 'Скорость FET attack.', 'Быстрее сильнее срезает transient.', 'Начать медленнее и ускорять по необходимости.'),
        ctl('Release', 'Скорость восстановления.', 'Быстро добавляет energy, медленно сглаживает.', 'Возврат по groove без distortion.'),
        ctl('Ratio', 'Выбирает 4:1, 8:1, 12:1, 20:1 behavior.', 'Выше — жёстче и агрессивнее.', '4:1 для control; выше для effect/parallel.'),
        ctl('Stereo Link / Channel mode', 'Определяет связь каналов в stereo operation.', 'Влияет на image stability.', 'На bus проверить center и low end.'),
    ],
    'dbx 160': [
        ctl('Threshold', 'Задаёт начало compression.', 'Ниже — больше GR.', 'Целиться в 1–4 dB GR.'),
        ctl('Compression / Ratio', 'Задаёт силу сжатия.', 'Выше — плотнее и жёстче.', 'Умеренно для leveling, выше для punch.'),
        ctl('Output Gain', 'Компенсирует уровень.', 'Позволяет честно оценить envelope.', 'Level-match.'),
        ctl('Mix', 'Параллельная смесь, если доступна в версии.', 'Возвращает dry transient.', '20–60% для aggressive drums.'),
        ctl('Noise / Analog mode', 'Моделирует дополнительные analog особенности, если доступны.', 'Может добавить шум/color.', 'Отключить, если не нужен.'),
    ],
    'elysia nvelope': [
        ctl('Full Range / Dual Band mode', 'Выбирает broadband или раздельную обработку.', 'Dual Band отделяет click от body.', 'Сначала Full Range; делить только по задаче.'),
        ctl('Attack', 'Усиливает или ослабляет transient.', 'Положительно — больше punch/click.', 'Начать ±1–3 деления.'),
        ctl('Sustain', 'Меняет хвост/room.', 'Положительно увеличивает size, отрицательно сушит.', 'Начать с малого.'),
        ctl('Freq A / Freq S', 'Задаёт частотную область Attack/Sustain.', 'Фокусирует обработку на click, body или room.', 'Настроить по источнику.'),
        ctl('Auto Gain / Output', 'Компенсирует изменение perceived level.', 'Облегчает A/B.', 'Проверить вручную.'),
    ],
    'Waves Smack Attack': [
        ctl('Attack', 'Меняет уровень начала события.', 'Плюс добавляет punch, минус смягчает.', 'Начать ±10–20%.'),
        ctl('Sustain', 'Меняет хвост.', 'Плюс добавляет room/body, минус делает tight.', 'Начать ±10–20%.'),
        ctl('Sensitivity', 'Определяет, какие события считаются transient.', 'Выше — процессор реагирует чаще.', 'Добиться стабильного detector.'),
        ctl('Duration', 'Задаёт длительность attack/sustain windows.', 'Отделяет короткий click от тела.', 'По envelope источника.'),
        ctl('Shape', 'Меняет кривую обработки.', 'Влияет на естественность envelope.', 'Начать мягко.'),
        ctl('Mix / Output', 'Parallel и gain compensation.', 'Сохраняет natural dynamics.', 'Level-match.'),
    ],
    'Waves InPhase': [
        ctl('Polarity', 'Инвертирует polarity выбранного канала.', 'Может восстановить или ослабить low end при суммировании.', 'Проверить первым.'),
        ctl('Delay', 'Сдвигает сигнал во времени.', 'Совмещает transients между микрофонами/слоями.', 'Искать около основной атаки.'),
        ctl('Phase Shift / Frequency', 'Вращает фазу частотно-зависимо.', 'Уточняет суммирование, когда простого delay недостаточно.', 'После polarity и delay.'),
        ctl('Gain', 'Выравнивает сравниваемые сигналы.', 'Убирает level bias при поиске alignment.', 'Согласовать до сравнения.'),
        ctl('Correlation / Waveform display', 'Показывает временную и фазовую связь.', 'Помогает найти конфликт, но не заменяет слух.', 'Подтвердить в mono и полном миксе.'),
        ctl('Monitor / Audition', 'Выбирает прослушиваемый сигнал/разность.', 'Позволяет локализовать cancellation.', 'Не оставлять service monitoring в export.'),
    ],
    'FabFilter Pro-L 2': [
        ctl('Style', 'Выбирает limiter algorithm.', 'Меняет punch, transparency и плотность.', 'Сравнить Styles на самых сложных пиках.'),
        ctl('Gain', 'Подаёт сигнал в limiting.', 'Увеличивает loudness и GR.', 'Поднимать до целевого, не по цифре любой ценой.'),
        ctl('Output Level', 'Задаёт финальный ceiling.', 'Ограничивает выходной пик.', 'Учитывать delivery и codec.'),
        ctl('Lookahead / Attack / Release', 'Настраивает envelope limiting.', 'Меняет transient, distortion и pumping.', 'Начать с Style defaults, затем корректировать.'),
        ctl('Channel Linking', 'Связывает transient и release между L/R.', 'Влияет на stereo stability.', 'Низ держать стабильным; проверять image.'),
        ctl('True Peak Limiting', 'Контролирует inter-sample peaks.', 'Безопаснее для lossy encoding.', 'Включать для финального delivery по задаче.'),
        ctl('Oversampling', 'Повышает внутреннюю sample rate.', 'Снижает aliasing/peak error, увеличивает CPU.', 'Высокое значение на final render.'),
        ctl('Unity Gain / Audition Limiting', 'Помогает сравнивать и слушать removed signal.', 'Выявляет повреждение transient/вокала.', 'Проверять регулярно.'),
    ],
    'FabFilter Pro-DS': [
        ctl('Detection', 'Выбирает vocal/широкополосное обнаружение.', 'Меняет, что считается sibilance.', 'Начать с режима под материал.'),
        ctl('Threshold', 'Чувствительность detector.', 'Ниже — чаще reduction.', 'Настроить на самые резкие S.'),
        ctl('Range', 'Максимальное подавление.', 'Ограничивает lisp и dullness.', '2–4 dB как старт.'),
        ctl('Wide Band / Split Band', 'Выбирает снижение всего сигнала или только highs.', 'Split прозрачнее, Wide иногда естественнее.', 'Сравнить level-matched.'),
        ctl('Lookahead', 'Позволяет заранее ловить согласные.', 'Чище обработка, больше latency.', 'Минимально необходимое.'),
        ctl('Audition', 'Слушает обнаруженную часть.', 'Помогает не удалять полезный vocal tone.', 'При настройке Threshold/Range.'),
    ],
    'FabFilter Pro-MB': [
        ctl('Bands / Crossovers', 'Создаёт независимые frequency ranges.', 'Разделяет динамику спектра.', 'Начать с одной band.'),
        ctl('Threshold / Range', 'Задаёт срабатывание и максимальное изменение.', 'Определяет частоту и глубину работы.', 'Range 1–3 dB для transparent control.'),
        ctl('Ratio / Knee', 'Форма compression/expansion.', 'Меняет жёсткость реакции.', 'Низкий Ratio и мягкий Knee для bus/master.'),
        ctl('Attack / Release', 'Envelope каждой band.', 'Меняет punch и tonal movement.', 'По событиям внутри band.'),
        ctl('Lookahead', 'Предварительно ловит пики.', 'Чище, но может смягчать attack.', 'Минимально необходимое.'),
        ctl('Stereo Link / Processing mode', 'Управляет L/R или M/S реакцией.', 'Влияет на image stability.', 'M/S только по диагнозу.'),
        ctl('Output', 'Компенсирует общий level.', 'Нужен для честного A/B.', 'Level-match.'),
    ],
    'FabFilter Timeless 3': [
        ctl('Delay Time / Sync', 'Задаёт время L/R repeats.', 'Формирует rhythm, slap или width.', 'Начать 1/8, 1/4 либо 70–140 ms.'),
        ctl('Feedback / Cross Feedback', 'Возвращает repeats в тот же или другой канал.', 'Определяет длину и stereo movement.', '10–30%; контролировать runaway.'),
        ctl('Drive / Diffusion', 'Насыщает и размывает repeats.', 'Отделяет delay от dry source.', 'Добавлять умеренно.'),
        ctl('Filters', 'Фильтрует delay path.', 'Освобождает место вокалу/инструменту.', 'HPF 150–500 Hz, LPF 3–10 kHz.'),
        ctl('Pitch / Modulation', 'Меняет высоту и движение repeats.', 'Создаёт chorus, detune и evolving echo.', 'Малая Depth для обычного delay.'),
        ctl('Freeze / Tap behavior', 'Удерживает или перестраивает feedback network.', 'Создаёт texture и transition.', 'Limiter на return.'),
        ctl('Mix / Output', 'Dry/wet и уровень.', 'На send отделяет routing.', '100% wet на return.'),
    ],
    'FabFilter Pro-R': [
        ctl('Space', 'Меняет воспринимаемый размер пространства.', 'От room к большому hall.', 'Выбрать до Decay.'),
        ctl('Decay Rate', 'Задаёт длину хвоста.', 'Дольше — глубже и плотнее.', 'По темпу и аранжировке.'),
        ctl('Brightness', 'Меняет high-frequency decay/тон.', 'Ярче ближе, темнее дальше.', 'Подстроить под source.'),
        ctl('Character', 'Меняет modulation и density хвоста.', 'От чистого к живому/chorused.', 'Начать нейтрально.'),
        ctl('Distance', 'Меняет отношение direct/early/tail.', 'Отодвигает source.', 'Не заменяет обычный send level.'),
        ctl('Pre-delay', 'Пауза до reverb.', 'Сохраняет ясность атаки/слов.', 'Vocal 20–80 ms.'),
        ctl('Decay Rate EQ / Post EQ', 'Меняет decay и output по частотам.', 'Убирает mud и лишний bright tail.', 'HPF/low decay по задаче.'),
        ctl('Stereo Width / Mix', 'Ширина и dry/wet.', 'Влияет на center и mono.', '100% wet на send; mono-check.'),
    ],
    'Soundtoys EchoBoy': [
        ctl('Echo Time / Sync', 'Задаёт delay time.', 'Формирует groove повторов.', '1/4, 1/8D либо ms.'),
        ctl('Style', 'Выбирает характер echo machine.', 'Меняет saturation, bandwidth и modulation.', 'Сначала выбрать Style.'),
        ctl('Feedback', 'Количество повторов.', 'Больше — длиннее и опаснее по уровню.', '10–30% как старт.'),
        ctl('Saturation', 'Добавляет nonlinear color repeats.', 'Делает delay плотнее и темнее.', 'Малый/средний Amount.'),
        ctl('Groove / Feel', 'Сдвигает timing повторов.', 'Создаёт swing или laid-back feel.', 'Настраивать с ритм-секцией.'),
        ctl('LowCut / HighCut', 'Ограничивает спектр repeats.', 'Уменьшает маскировку dry source.', 'Фильтровать сильнее, чем в solo.'),
        ctl('Mix / Output', 'Dry/wet и level.', 'Разделяет insert/send workflow.', '100% wet на send.'),
    ],
}


# 63 additional high-use products receive a product-informed map. The control
# model is adapted from the product's curated family profile and chain notes,
# and is explicitly NOT presented as a verbatim manual transcription.
PRODUCT_INFORMED_NAMES = {
'Newfangled Saturate','Room Service','Black Box Analog Design HG-2','SPL HawkEye','Soundtoys SuperPlate','bx_refinement / V3','Overloud Gem Dopamine','ADPTR Metric AB','Cactus Clipper','Soundtoys PanMan','Maag EQ4','Waves API 2500','Overloud Gem Comp LA','Soundtoys MicroShift','Soundtoys FilterFreak 2','AMEK EQ 200','Dangerous BAX EQ','Waves H-Reverb','CINEFELT','Erebos','UltraPump','Millennia TCL-2','Waves IR-1','DUEL LT','API 550B','Bus Ride','SPL Iron','Soundtoys Little Plate','API 550A','Waves PuigChild 670','Soundtoys Devil-Loc Deluxe','RESTRUKT','bx_townhouse Buss Compressor','Renaissance Vox','Waves Sibilance','Double Dare','Waves H-Delay','Greg Wells PianoCentric','Unfiltered Audio SILO','Abbey Road Chambers','Unfiltered Audio SpecOps','Waves J37 Tape','bx_control V2','Busboy','SubTec','bx_console SSL 4000 E','Lindell 50 Series','Abbey Road Reverb Plates','Waves Trans-X','Newfangled Punctuate','bx_console N','Waves Kramer Master Tape','Waves CLA-76 Black / Blue','Bass Rider','Waves CLA-2A','Ampeg SVT-VR Classic','Parallax','Waves RBass / Renaissance Bass','Sssh','HVX Chain','Slapshot','GilderVox','Waves Clarity Vx'
}

CATEGORY_SOUND = {
    'Cleanup и restoration': 'Результат должен восприниматься как более чистая запись, а не как слышимый эффект. Главный ориентир — отсутствие watery artifacts, lisp и потери полезных деталей.',
    'EQ и tone shaping': 'Меняет спектральный баланс: от незаметной коррекции до явного tonal character. Оценивайте не solo-красоту, а место источника в аранжировке.',
    'Dynamics': 'Меняет envelope, crest factor, стабильность и ощущение punch. Attack и Release важнее условно «правильной» цифры.',
    'Low-end processing': 'Работает с фундаментом, читаемостью баса и переводимостью на маленьких системах. Любое усиление sub необходимо проверять по headroom и в mono.',
    'Saturation и color': 'Добавляет гармоники, density и nonlinear compression. Даже небольшая прибавка уровня способна создать ложное ощущение улучшения.',
    'Channel strips и macros': 'Объединяет несколько стадий в один workflow. Его преимущество — скорость и связность, но не обязательное включение каждого модуля.',
    'Delay': 'Создаёт повторы, rhythmic depth и движение. На send repeats проще фильтровать, автоматизировать и отделять от dry source.',
    'Reverb': 'Формирует глубину, размер и общую акустическую среду. Читаемость обычно сохраняют Pre-delay, фильтрацией return и ducking.',
    'Modulation и stereo': 'Добавляет движение и ширину через time, pitch, level или phase различия. Проверка mono/correlation обязательна.',
    'Guitar и bass rigs': 'Формирует amp/cab/pedal tone. Cab/IR и input calibration обычно влияют сильнее, чем последующий радикальный EQ.',
    'Creative FX и sound design': 'Создаёт явно слышимую трансформацию. Безопаснее хранить dry source и печатать удачные random/feedback результаты в отдельный audio layer.',
    'Instruments': 'Генерирует исходный музыкальный сигнал. Patch лучше строить под роль в аранжировке, чем исправлять длинной insert-chain.',
    'Metering и utility': 'Помогает принимать и проверять решения, но обычно не должен печататься в master. Измерение подтверждает слух, а не заменяет его.',
}

TASK_META = {
    'Очистка / repair': ('Уменьшить техническую проблему без слышимой потери полезного сигнала.', 'Слушайте паузы, согласные и хвосты; остановитесь при metallic/watery artifacts.', 'Первым insert до EQ, saturation и upward compression.'),
    'Фаза / стерео': ('Согласовать слои и сохранить устойчивый центр.', 'Проверяйте фундамент, transient и mono; не максимизируйте correlation вслепую.', 'До dynamics и tonal processing.'),
    'Gate / expander': ('Ослабить bleed/noise, сохранив тихие полезные события.', 'Проверяйте ghost notes, начало и естественный хвост.', 'После грубой очистки, до тяжёлой compression.'),
    'EQ / тон': ('Исправить конфликт или сформировать tonal balance.', 'Слушайте источник в полном миксе и делайте level-matched bypass.', 'Corrective EQ рано; character EQ после dynamics по задаче.'),
    'Channel strip / macro': ('Быстро получить связный рабочий tone.', 'Проверяйте каждый модуль bypass и общий output.', 'Основная track/bus chain; не обязаны работать все modules.'),
    'Компрессия / уровень': ('Стабилизировать envelope, громкость или punch.', 'Следите за transient, groove, дыханием и восстановлением GR.', 'После corrective EQ либо до character EQ.'),
    'Транзиенты': ('Изменить соотношение attack и sustain.', 'Сравнивайте peak level и тело источника, не только click.', 'До/после compressor — выбрать лучший порядок.'),
    'Низ / фундамент': ('Сделать low end стабильнее и переводимее.', 'Проверяйте phase, mono, headroom и маленькие speakers.', 'После phase/EQ, до clipping/limiting.'),
    'Сатурация / цвет': ('Добавить harmonics, density или выраженный character.', 'Сравнивайте при одинаковом Output; слушайте low-mid и harsh верх.', 'До compressor для реакции, после для finishing density.'),
    'Amp / cabinet / pedal': ('Сформировать amp/cab tone и articulation.', 'Проверяйте input calibration, gain, cab и low-end conflict.', 'Source/amp stage до corrective post-EQ.'),
    'Модуляция / ширина': ('Добавить движение или stereo width.', 'Проверяйте mono, correlation и устойчивость центра.', 'Часто send/parallel, после основной tonal/dynamic обработки.'),
    'Delay / echo': ('Добавить rhythmic repeats и глубину.', 'Слушайте groove, окончания фраз и feedback peaks.', 'Обычно post-fader send, 100% wet return.'),
    'Reverb / пространство': ('Создать глубину и связать источник с пространством.', 'Слушайте diction, mud, длину хвоста и переход аккордов.', 'Обычно post-fader send, 100% wet return.'),
    'Creative FX': ('Создать отдельный слышимый texture/effect.', 'Сохраняйте dry source и контролируйте feedback/peaks.', 'Send, parallel или отдельный printed layer.'),
    'Limiter / clipper': ('Контролировать короткие пики или финальный ceiling.', 'Слушайте cymbals, consonants, snare и low end.', 'В конце processing chain; meter после limiter.'),
    'Контроль / анализ': ('Проверить level, spectrum, stereo и translation.', 'Не гонитесь за одной цифрой; сравнивайте релевантные секции.', 'Последним в Monitoring; не печатать в export.'),
}


def _sentence(text):
    text = (text or '').strip()
    return text if not text or text.endswith(('.', '!', '?')) else text + '.'


def _routing_for(task, category):
    if task in TASK_META:
        return TASK_META[task][2]
    if category in ('Delay', 'Reverb'):
        return 'Post-fader Send/Return; return обычно 100% wet.'
    if category == 'Metering и utility':
        return 'Monitoring после финального limiter; исключить из export.'
    if category == 'Instruments':
        return 'Source / Instrument перед audio inserts.'
    return 'Insert на source track или bus по задаче.'


def _parse_settings(text, fallback_values):
    text = (text or '').strip()
    values = []
    known = ['External SC', 'Sidechain HPF', 'Auto Gain', 'True Peak', 'Pre-delay',
             'Frequency', 'Threshold', 'Reduction', 'Feedback', 'Release', 'Attack',
             'Ratio', 'Range', 'Hold', 'Drive', 'Amount', 'Mix', 'Output', 'Input',
             'Ceiling', 'Decay', 'Damping', 'Size', 'Time', 'Sync', 'Filters', 'HPF',
             'LPF', 'Gain', 'GR', 'Q', 'Tone', 'Width', 'Oversampling', 'Mode',
             'Bands', 'Band', 'Sustain', 'Polarity', 'Delay', 'Phase']
    if text:
        controls_pattern = '|'.join(re.escape(x) for x in sorted(known, key=len, reverse=True))
        chunks = [x.strip(' .') for x in re.split(
            rf';|\.\s+(?=[А-ЯA-Z0-9])|,\s*(?=(?:{controls_pattern})\b)', text
        ) if x.strip(' .')]
        for i, chunk in enumerate(chunks[:7], 1):
            matched = None
            for name in sorted(known, key=len, reverse=True):
                if re.match(rf'^{re.escape(name)}\b', chunk, re.I):
                    matched = name
                    break
            if matched:
                value = chunk[len(matched):].strip(' :–—') or 'По материалу'
                values.append({'control': matched, 'value': value})
            elif ':' in chunk and not re.match(r'^\d+\s*:', chunk):
                left, right = chunk.split(':', 1)
                values.append({'control': left.strip(), 'value': right.strip()})
            else:
                values.append({'control': 'Starting point' if i == 1 else f'Шаг {i}', 'value': chunk})
    if not values:
        values = [dict(v) for v in fallback_values[:5]]
    present = {v['control'].casefold() for v in values}
    for item in fallback_values:
        if len(values) >= 4:
            break
        if item['control'].casefold() not in present:
            values.append(dict(item)); present.add(item['control'].casefold())
    return values


def _source_similarity(source, recipe_source):
    a = (source or '').casefold()
    b = (recipe_source or '').casefold()
    score = 0
    for token in re.findall(r'[a-zа-я0-9]+', b):
        if len(token) > 2 and token in a:
            score += 1
    return score


def _use_case(plugin, use, source_lookup, profile):
    row = source_lookup.get((use['source'], use['task']), {})
    goal, listen, route = TASK_META.get(use['task'], (profile.get('choose', ''), 'Проверяйте в контексте.', profile.get('position', '')))
    tier = 'Основная рекомендация' if use.get('primary') else 'Подходящая альтернатива'
    return {
        'source': use['source'], 'task': use['task'], 'tier': tier,
        'goal': goal,
        'why': row.get('choose') or profile.get('choose') or plugin.get('note', ''),
        'setup': row.get('how') or plugin.get('note', ''),
        'position': row.get('position') or route,
        'listenFor': listen,
    }


def _recipe_from_occurrence(plugin, occ, profile):
    base = profile['recipes'][0]
    goal, listen, route_default = TASK_META.get(occ['task'], (profile.get('choose', ''), 'Сравнивайте в контексте.', profile.get('position', '')))
    route = occ.get('bus') or route_default
    if occ.get('lane') == 'send':
        route = f"{route}: post-fader send, return 100% wet если это time-based effect."
    elif occ.get('lane') == 'monitor':
        route = 'Monitoring после final processing; не печатать в export.'
    elif occ.get('lane') == 'source':
        route = 'Source / Instrument перед inserts.'
    else:
        route = f"Main Inserts. {route_default}"
    values = _parse_settings(occ.get('settings', ''), base['values'])
    return {
        'title': f"{occ['source']} — {occ['style']}", 'source': occ['source'],
        'task': occ['task'], 'goal': goal, 'status': 'Curated preset occurrence',
        'routing': route, 'settingsText': occ.get('settings', ''), 'values': values,
        'order': [
            'Выставить Input/trim с запасом по headroom.',
            f"Настроить только задачу «{occ['task']}», не пытаться исправить всё одним stage.",
            'Вернуть Output к громкости bypass.',
            f"Проверить: {listen}",
        ],
        'why': occ.get('setup') or profile.get('choose', ''),
        'listenFor': listen,
        'stopWhen': profile['warnings'][0],
    }


def _recipe_from_use(plugin, use, profile, index):
    base = max(profile['recipes'], key=lambda r: _source_similarity(use['source'], r.get('source', ''))) if profile['recipes'] else None
    if not base:
        base = {'title': 'Старт', 'source': use['source'], 'values': [{'control': 'Amount', 'value': 'Начать мало'}], 'why': plugin['note']}
    goal, listen, route = TASK_META.get(use['task'], (profile.get('choose', ''), 'Сравнивайте в контексте.', profile.get('position', '')))
    values = [dict(v) for v in base['values']]
    return {
        'title': f"{use['source']} — {use['task']}", 'source': use['source'],
        'task': use['task'], 'goal': goal, 'status': 'Curated family-level adaptation',
        'routing': _routing_for(use['task'], plugin['category']),
        'settingsText': '; '.join(f"{v['control']}: {v['value']}" for v in values),
        'values': values,
        'order': [
            'Подготовить Input и отключить ненужные modules.',
            f"Начать с {values[0]['control']}: {values[0]['value']}.",
            'Настроить интенсивность по самому сложному фрагменту.',
            'Компенсировать Output и сделать level-matched bypass.',
            f"Проверить: {listen}",
        ],
        'why': base.get('why') or goal, 'listenFor': listen,
        'stopWhen': profile['warnings'][index % len(profile['warnings'])],
    }


def _fallback_recipe(plugin, profile, base, index):
    task = plugin['uses'][0]['task'] if plugin.get('uses') else plugin['family']
    listen = TASK_META.get(task, ('', 'Проверяйте в полном миксе и при одинаковой громкости.', ''))[1]
    values = [dict(v) for v in base['values']]
    return {
        'title': base['title'], 'source': base.get('source') or plugin['where'],
        'task': task, 'goal': base.get('why') or profile.get('choose', ''),
        'status': 'Family-level starting point',
        'routing': _routing_for(task, plugin['category']),
        'settingsText': '; '.join(f"{v['control']}: {v['value']}" for v in values),
        'values': values,
        'order': ['Проверить Input/headroom.', 'Начать с минимального Amount.', 'Настроить ключевые controls по материалу.', 'Компенсировать Output.', 'Сравнить в контексте и mono при необходимости.'],
        'why': base.get('why') or plugin['note'], 'listenFor': listen,
        'stopWhen': profile['warnings'][index % len(profile['warnings'])],
    }


def _workflow(plugin, controls, profile):
    names = [c['name'] for c in controls]
    first = names[0] if names else 'Input'
    second = names[1] if len(names) > 1 else 'Amount'
    return [
        f"1. Определите одну задачу для {plugin['name']}; bypass всё, что не помогает ей.",
        '2. Подготовьте gain staging: исключите случайный clipping и оставьте запас следующей стадии.',
        f"3. Настройте {first}, затем {second}; не начинайте с максимального Amount.",
        '4. Работайте на самом сложном участке, затем проверьте тихую/редкую часть материала.',
        '5. Компенсируйте Output и сделайте несколько level-matched bypass переключений.',
        '6. Проверьте источник в полном миксе; для stereo/low end дополнительно используйте mono.',
        '7. Сохраните настройку как стартовую только после проверки нескольких секций проекта.',
    ]


def enrich_plugins(plugins, profiles, source_records, chains):
    source_lookup = {}
    for source in source_records:
        for task in source['tasks']:
            source_lookup[(source['name'], task['task'])] = task

    occurrences = defaultdict(list)
    for chain in chains:
        for step in chain.get('steps', []):
            occurrences[step['name']].append({
                'source': chain['source'], 'style': chain.get('style') or chain.get('goal', ''),
                'setup': chain.get('setup', ''), **step,
            })

    by_name = {p['name']: p for p in plugins}
    assert PRODUCT_INFORMED_NAMES <= set(by_name), PRODUCT_INFORMED_NAMES-set(by_name)
    assert set(PRODUCT_CONTROLS) <= set(by_name), set(PRODUCT_CONTROLS)-set(by_name)
    for plugin in plugins:
        profile = profiles[plugin['familyKey']]
        product_specific = plugin['name'] in PRODUCT_CONTROLS
        product_informed = plugin['name'] in PRODUCT_INFORMED_NAMES
        controls = [dict(c) for c in PRODUCT_CONTROLS.get(plugin['name'], profile['controls'])]
        if product_informed and not product_specific:
            for c in controls: c['evidence'] = 'Product-informed curated map'
        elif not product_specific:
            for c in controls: c['evidence'] = 'Family-level control model'

        use_cases = [_use_case(plugin, u, source_lookup, profile) for u in plugin.get('uses', [])[:12]]
        if not use_cases:
            use_cases = [{
                'source': plugin['where'], 'task': plugin['family'], 'tier': 'Catalog use case',
                'goal': profile.get('use', ''), 'why': profile.get('choose', ''),
                'setup': plugin['note'], 'position': profile.get('position', ''),
                'listenFor': 'Сравнивайте в полном миксе и при одинаковом Output.',
            }]

        recipes = []
        seen = set()
        for occ in occurrences.get(plugin['name'], []):
            key = (occ['source'], occ['style'])
            if key in seen:
                continue
            recipes.append(_recipe_from_occurrence(plugin, occ, profile)); seen.add(key)
            if len(recipes) >= 4:
                break
        for idx, use in enumerate(plugin.get('uses', [])):
            key = (use['source'], use['task'])
            if key in seen:
                continue
            recipes.append(_recipe_from_use(plugin, use, profile, idx)); seen.add(key)
            if len(recipes) >= 4:
                break
        for idx, base in enumerate(profile['recipes']):
            if len(recipes) >= 4:
                break
            key = (base.get('source'), base['title'])
            if key in seen:
                continue
            recipes.append(_fallback_recipe(plugin, profile, base, idx)); seen.add(key)
        while len(recipes) < 3:
            recipes.append(_fallback_recipe(plugin, profile, profile['recipes'][len(recipes) % len(profile['recipes'])], len(recipes)))

        primary_sources = [u['source'] for u in plugin.get('uses', []) if u.get('primary')]
        all_sources = list(dict.fromkeys(primary_sources + [u['source'] for u in plugin.get('uses', [])]))
        source_phrase = ', '.join(all_sources[:6]) if all_sources else plugin['where']
        copy = beginner_copy(plugin, profile, all_sources)
        full_description = copy['full']

        variant_names = [x.strip() for x in plugin['name'].split(' / ')] if ' / ' in plugin['name'] else []
        variants = []
        if variant_names:
            variants = [{
                'name': name,
                'note': ('Более новая/расширенная редакция; проверьте дополнительные modes и oversampling в установленной версии.'
                         if re.search(r'v\d|plus|pro|classic', name, re.I)
                         else 'Близкий вариант объединён по функции; точные controls сверяйте с GUI установленной версии.')
            } for name in variant_names]

        comparisons = []
        for alt_name in plugin.get('analogues', [])[:5]:
            alt = by_name.get(alt_name)
            if not alt:
                continue
            comparisons.append({
                'name': alt_name,
                'chooseCurrent': f"Выбирать {plugin['name']}, когда нужен характер/процесс: {plugin['kind']}.",
                'chooseAlternative': f"Выбирать {alt_name}, когда лучше подходит: {alt['kind']}.",
            })

        evidence = [
            {'level': 'Curated', 'text': 'Описание, применение, routing и Starting settings подготовлены как консервативная практическая рекомендация.'},
            {'level': 'Product-specific curated map' if product_specific else 'Product-informed curated map' if product_informed else 'Family-level',
             'text': ('Controls привязаны к известной структуре этого продукта, но всё равно требуют сверки с установленной версией.' if product_specific else
                      'Controls адаптированы по роли продукта, curated chains и family profile; это не дословная карта manual/GUI.' if product_informed else
                      'Controls являются нормализованной моделью семейства и могут называться иначе или отсутствовать в GUI.')}, 
        ]
        if plugin.get('link'):
            evidence.append({'level': 'Official link', 'text': 'В карточке доступна официальная страница продукта; ссылка требует подключения к интернету.'})

        plugin['guide'] = {
            'simple': copy['simple'],
            'fullDescription': full_description,
            'sound': copy['sound'],
            'whyChoose': copy['why'],
            'bestFor': all_sources[:8] or [plugin['where']],
            'notFor': list(dict.fromkeys(profile['warnings'] + [
                'Не добавляйте processing только потому, что preset звучит громче.',
                'Если задача не сформулирована, сначала вернитесь к исходному балансу и аранжировке.',
            ]))[:5],
            'placement': profile.get('position', ''),
            'routing': _routing_for(plugin['uses'][0]['task'], plugin['category']) if plugin.get('uses') else _routing_for('', plugin['category']),
            'controls': controls,
            'controlStatus': 'Product-specific curated map' if product_specific else 'Product-informed curated map' if product_informed else 'Family-level control model',
            'controlNote': 'Сверено по известной структуре продукта; проверить установленную версию.' if product_specific else ('Адаптировано по роли продукта и curated use cases; названия Controls сверить с GUI/manual.' if product_informed else 'Нормализованная модель семейства, не карта конкретного GUI.'),
            'settings': recipes[:4],
            'workflow': _workflow(plugin, controls, profile),
            'techniques': profile['techniques'],
            'checks': list(dict.fromkeys([r['listenFor'] for r in recipes] + profile['warnings']))[:6],
            'useCases': use_cases,
            'variants': variants,
            'comparisons': comparisons,
            'evidence': evidence,
        }
        guide_terms = [full_description, plugin['guide']['simple'], plugin['guide']['whyChoose'], plugin['guide']['routing']]
        guide_terms += [u['source'] + ' ' + u['task'] + ' ' + u['goal'] for u in use_cases]
        guide_terms += [c['name'] + ' ' + c['role'] + ' ' + c['start'] for c in controls]
        guide_terms += [r['title'] + ' ' + r['settingsText'] for r in recipes]
        plugin['search'] = (plugin.get('search', '') + ' ' + ' '.join(guide_terms)).casefold()

    return plugins


from product_control_maps import EXTRA_INFORMED_NAMES, EXTRA_PRODUCT_CONTROLS
PRODUCT_CONTROLS = {**PRODUCT_CONTROLS, **EXTRA_PRODUCT_CONTROLS}
PRODUCT_INFORMED_NAMES = (PRODUCT_INFORMED_NAMES | EXTRA_INFORMED_NAMES) - set(PRODUCT_CONTROLS)
