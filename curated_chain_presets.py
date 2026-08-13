"""Manually curated quick chains for Plugin Navigator.
These are conservative starting points, not mandatory processing recipes.
Lanes: insert, send, monitor.
"""
PRESETS=[]

def S(task,name,lane='insert',settings=''):
    return {'task':task,'name':name,'lane':lane,'settings':settings}

# Conservative fallbacks for the few manually authored steps that did not yet
# contain a setting note. These principles were cross-checked against the
# research registry in chain_research_audit.py. They remain starting points,
# never fixed prescriptions or claims about a product's factory presets.
def researched_setting(source,goal,step):
    task,name,lane=step['task'],step['name'],step['lane']
    s=(source+' '+goal).casefold()
    if task=='EQ / тон':
        if any(x in s for x in ['master','mix bus','stereo bus','orchestral','оркестр','stem']):
            return 'Только при необходимости: broad ±0.25–1 dB; corrective cut раньше dynamics; level-matched A/B.'
        if any(x in s for x in ['piano','strings','brass','woodwind','акустичес']):
            return 'Сначала broad strokes до 1–2 dB; узкие cuts только для слышимого resonance; не EQ по анализатору.'
        if any(x in s for x in ['speech','podcast','dialog','речь']):
            return 'Сначала убрать rumble/boom и явную harshness; dynamic cuts вместо постоянного затемнения; Output matched.'
        if any(x in s for x in ['backing','vocal']):
            return 'Corrective cuts до compression; освободить lead только по конфликту; bright boosts проверять по sibilance.'
        if any(x in s for x in ['bass','808','sub']):
            return 'Убрать только лишний rumble/конфликт kick; не срезать фундамент автоматически; проверить mono.'
        return 'Corrective moves обычно 1–3 dB; HPF только по слышимой проблеме; слушать в полном миксе.'
    if task=='Компрессия / уровень':
        if any(x in s for x in ['master','mix bus','stereo bus','bus','stem']):
            return 'Conservative glue: Ratio 1.5:1–2:1, Attack medium/slow, Release по tempo, GR 0.5–2 dB, level-match.'
        if any(x in s for x in ['orchestral','оркестр','strings','brass','woodwind']):
            return 'Только если нужна стабильность: Ratio 1.1:1–2:1, GR 0.5–2 dB; сохранить crescendos и articulation.'
        if any(x in s for x in ['speech','podcast','dialog','vocal','вокал']):
            return 'Ratio 2:1–4:1, Attack/Release по фразе, GR обычно 2–5 dB; automation/rider снижает нагрузку.'
        return 'Ratio 2:1–4:1, Attack сохраняет нужный transient, Release восстанавливается до следующего события, GR 1–3 dB.'
    if task=='Очистка / repair':
        return 'Reduction/Range минимально достаточные; для de-ess начать 2–4 dB и слушать detector; остановиться до artifacts/lisp.'
    if task=='Gate / expander':
        return 'Начать как expander: Range 6–15 dB; Attack сохраняет начало, Hold/Release — естественный хвост и ghost notes.'
    if task=='Фаза / стерео':
        return 'Только при нескольких mic/layers: polarity → time alignment → phase; затем mono/correlation check.'
    if task=='Транзиенты':
        return 'Attack/Sustain начать с ±10–20%; сравнить при одинаковом peak/output и не раздувать bleed или sub.'
    if task=='Низ / фундамент':
        return 'Сначала phase и balance; Amount 1–3 dB/минимально; проверять headroom, ноту, mono и small speakers.'
    if task=='Сатурация / цвет':
        return 'Drive до слышимого изменения, затем немного назад; Mix 10–40% для сильного color; Output обязательно matched.'
    if task=='Amp / cabinet / pedal':
        return 'Калибровать DI/Input; Gain ниже solo-ожидания; выбрать Cab/IR до post-EQ; clean low сохранить при bass split.'
    if task=='Модуляция / ширина':
        if lane=='send': return 'Отдельный return, 100% wet если плагин позволяет; Depth/Mix малые; dry center и mono-check.'
        return 'Depth/Mix начать мало; low end держать устойчивым; проверять correlation и mono.'
    if task=='Delay / echo':
        return 'Post-fader send, 100% wet; Feedback начать 10–30%; HPF/LPF repeats; Time/Sync и Release по groove.'
    if task=='Reverb / пространство':
        predelay='20–80 ms для ясности вокала' if any(x in s for x in ['vocal','speech','вокал','речь']) else 'по атаке и перспективе'
        return f'Post-fader send, 100% wet; Pre-delay {predelay}; Decay по tempo; HPF/LPF return против mud/harshness.'
    if task=='Creative FX':
        return 'Использовать parallel/send или printed copy; Amount 10–30% как старт; фильтровать return и страховать feedback peaks.'
    if task=='Limiter / clipper':
        if any(x in s for x in ['master','premaster']):
            return 'Финальная peak-stage: Ceiling/True Peak по delivery; начать с 1–2 dB GR и слушать transients/codec overs.'
        return 'Только редкие peaks: 0.5–2 dB reduction; oversampling на render; не заменять этим balance/gain staging.'
    if task=='Контроль / анализ':
        return 'После final limiter: LUFS/True Peak/stereo/mono и level-matched references; Monitoring не экспортировать.'
    if task=='Channel strip / macro':
        return 'Сначала Input; включать только нужные modules; broad EQ и GR умеренно; Output level-matched, limiter только peaks.'
    return 'Начать с минимального Amount, компенсировать Output и проверить результат в контексте.'

def P(pid,source,goal,steps,setup,alternatives='',control=''):
    for step in steps:
        if not step.get('settings','').strip():
            step['settings']=researched_setting(source,goal,step)
    labels={'source':'Источник','insert':'Inserts','send':'Sends','monitor':'Monitoring'}
    parts=[]
    for lane in ['source','insert','send','monitor']:
        names=[x['name'] for x in steps if x['lane']==lane]
        if names: parts.append(labels[lane]+': '+' → '.join(names))
    PRESETS.append({'id':'curated-'+pid,'source':source,'goal':'Curated / ручной стартовый preset · '+goal,'chain':' | '.join(parts),'setup':setup,'alternatives':alternatives,'control':control,'quickPreset':True,'verified':True,'steps':steps})

# 01 Kick
SRC='Бочка / kick'
P('kick-min',SRC,'Минимальный',[
 S('Фаза / стерео','Waves InPhase',settings='Только для слоёв/микрофонов: polarity → delay → phase.'),
 S('EQ / тон','FabFilter Pro-Q 3',settings='Убрать конфликт; обычно 1–3 dB, без лишнего HPF.'),
 S('Компрессия / уровень','FabFilter Pro-C 2',settings='Ratio 2:1–4:1, Attack 10–30 ms, GR 1–3 dB.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Срезать редкие пики примерно на 1–2 dB.')],
 'Прозрачная базовая цепь. InPhase включать только при нескольких слоях или микрофонах.','F6 Dynamic EQ, Smack Attack, Pro-L 2','Проверить с басом и в mono; сохранить punch.')
P('kick-modern',SRC,'Современный punch',[
 S('Фаза / стерео','Waves InPhase',settings='Выровнять слои до dynamics.'),
 S('EQ / тон','FabFilter Pro-Q 3',settings='Dynamic cut в мутной/гудящей зоне.'),
 S('Транзиенты','elysia nvelope',settings='Attack + умеренно; низ и click обрабатывать раздельно.'),
 S('Низ / фундамент','SubTec',settings='Настроить boost/attenuate на фундаменте.'),
 S('Limiter / clipper','Newfangled Saturate',settings='1–3 dB clipping, oversampling при render.')],
 'Для pop, hip-hop и electronic: сначала фаза, затем envelope и фундамент.','Smack Attack, bx_boom, SubMass, Cactus Clipper','Не добавлять sub, если проблема вызвана phase или arrangement.')
P('kick-rock',SRC,'Rock / metal',[
 S('Gate / expander','FabFilter Pro-G',settings='Expander Range 6–12 dB; сохранить естественный хвост.'),
 S('Channel strip / macro','bx_console SSL 4000 E',settings='Filters и broad EQ для body/click.'),
 S('Транзиенты','elysia nvelope',settings='Добавить attack без раздувания sub.'),
 S('Компрессия / уровень','Purple Audio MC77',settings='Attack не самый быстрый; GR 2–5 dB или parallel.'),
 S('Сатурация / цвет','Soundtoys Decapitator',settings='Level-match; Mix/parallel для сохранения атаки.')],
 'Напористая цепь для живой или sample-reinforced бочки.','CLA-76, Lindell 50 Series, Smashburger Compressor','Не делать solo-click слишком ярким; проверять под гитарами.')

# 02 Snare
SRC='Малый барабан / clap'
P('snare-min',SRC,'Минимальный',[
 S('Gate / expander','FabFilter Pro-G',settings='Range 6–15 dB, Hold/Release по хвосту.'),
 S('EQ / тон','FabFilter Pro-Q 3',settings='Убрать ring динамической полосой; сохранить body.'),
 S('Компрессия / уровень','dbx 160',settings='GR 2–4 dB; следить за crack.'),
 S('Reverb / пространство','Soundtoys SuperPlate','send',settings='100% wet, HPF return, decay по темпу.')],
 'Чистая цепь с plate на отдельном send.','Pro-C 2, Room Service, Abbey Road Reverb Plates','Не закрыть ghost notes gate-ом.')
P('snare-pop',SRC,'Pop / trap',[
 S('EQ / тон','Waves F6 Dynamic EQ',settings='Динамически укротить 3–10 kHz при резкости.'),
 S('Транзиенты','Waves Smack Attack',settings='Attack + умеренно, Sustain по длине sample.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Лёгкие harmonics; низ не перегружать.'),
 S('Limiter / clipper','Cactus Clipper',settings='1–2 dB clipping.'),
 S('Reverb / пространство','Soundtoys Little Plate','send',settings='Короткий/средний plate, low cut.')],
 'Для плотного современного snare/clap.','Trans-X, Newfangled Saturate, SuperPlate','Проверить верх в mono и вместе с hi-hat.')
P('snare-rock',SRC,'Rock character',[
 S('Channel strip / macro','Lindell 50 Series',settings='API-style broad EQ и preamp character.'),
 S('Компрессия / уровень','Purple Audio MC77',settings='2–5 dB GR или parallel crush.'),
 S('Сатурация / цвет','Soundtoys Decapitator',settings='Mix 10–40%, output matched.'),
 S('Reverb / пространство','Abbey Road Reverb Plates','send',settings='100% wet; pre-delay отделяет crack.')],
 'Характерная rock-цепь с параллельным plate.','CLA-76, API 550A, Devil-Loc Deluxe','Слушать bleed тарелок после saturation.')

# 03 Toms / percussion
SRC='Томы / перкуссия'
P('toms-min',SRC,'Живые томы',[
 S('Gate / expander','FabFilter Pro-G',settings='Range 6–15 dB; Hold/Release по sustain.'),
 S('EQ / тон','FabFilter Pro-Q 3',settings='Убрать boxiness и лишний rumble.'),
 S('Компрессия / уровень','dbx 160',settings='GR 2–4 dB, сохранить начало.'),
 S('Reverb / пространство','Room Service','send',settings='100% wet, короткий room.')],
 'Естественный контроль томов без жёсткого обрезания хвоста.','C1 Gate/Expander, TrueVerb, Pro-C 2','Проверить phase с overheads.')
P('toms-modern',SRC,'Современный punch',[
 S('Gate / expander','FabFilter Pro-G'),S('EQ / тон','API 550A',settings='Broad body/attack moves.'),
 S('Транзиенты','Waves Trans-X',settings='Attack + умеренно; sustain не раздувать.'),
 S('Компрессия / уровень','FabFilter Pro-C 2',settings='Ratio 3:1, GR 2–4 dB.'),
 S('Reverb / пространство','Waves H-Reverb','send',settings='Короткий room, фильтровать return.')],
 'Для плотных pop/rock томов и percussion.','Smack Attack, SSL E-Channel, Breverb 2','Не делать все томы одинаковыми по длине.')
P('perc-creative',SRC,'Creative percussion',[
 S('Транзиенты','Newfangled Punctuate',settings='Работать только нужными bands.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Multiband color умеренно.'),
 S('Модуляция / ширина','Soundtoys PanMan','send',settings='Tempo-sync, low end не панорамировать.'),
 S('Delay / echo','Soundtoys EchoBoy','send',settings='Filtered rhythmic repeats, 100% wet.')],
 'Ритмическое движение для дополнительной percussion.','Tremolator, ExoDelay, FilterFreak','Главный groove должен оставаться читаемым без FX.')

# 04 Overheads
SRC='Overheads / тарелки / hi-hat'
P('oh-min',SRC,'Чистые и мягкие',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='HPF только по необходимости; broad corrections.'),
 S('Очистка / repair','bx_refinement / V3',settings='Небольшой dynamic de-harsh.'),
 S('Компрессия / уровень','FabFilter Pro-C 2',settings='Ratio 2:1, GR 0.5–2 dB.')],
 'Минимальная обработка с сохранением stereo image.','F6 Dynamic EQ, Pro-DS, GilderComp','Проверить phase со snare/kick close mics.')
P('oh-vintage',SRC,'Vintage',[
 S('Channel strip / macro','bx_console N',settings='Лёгкий preamp color; фильтры по задаче.'),
 S('Сатурация / цвет','Waves Kramer Master Tape',settings='Небольшой drive, wow/flutter минимально.'),
 S('Компрессия / уровень','Waves PuigChild 670',settings='0.5–2 dB GR, time constant по groove.')],
 'Мягкий vintage tone для rock/retro.','J37 Tape, Gem Comp 670, V-Comp','Не потерять transient и центр snare.')
P('oh-bright',SRC,'Bright pop',[
 S('EQ / тон','Waves F6 Dynamic EQ',settings='Только проблемные пики.'),
 S('Очистка / repair','FabFilter Pro-DS',settings='Split-band, 1–3 dB reduction.'),
 S('EQ / тон','Maag EQ4',settings='Air Band после de-essing, очень умеренно.'),
 S('Сатурация / цвет','Overloud Gem Dopamine',settings='Малый Amount для presence.')],
 'Яркий, но контролируемый верх.','Sibilance, 8K, Chakra','Air не должен возвращать harshness.')

# 05 Room microphones
SRC='Room microphones / drum ambience'
P('room-natural',SRC,'Натуральная комната',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Удалить rumble/резонансы, сохранить характер room.'),
 S('Компрессия / уровень','FabFilter Pro-C 2',settings='Ratio 2:1–4:1, Release по groove, GR 1–4 dB.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Очень лёгкая density.')],
 'Сохраняет естественную комнату.','GilderComp, bx_console N','Сверить phase и время с close mics.')
P('room-crush',SRC,'Parallel crush',[
 S('Компрессия / уровень','Purple Audio MC77','send',settings='Сильный GR, затем подмешать.'),
 S('Сатурация / цвет','Soundtoys Devil-Loc Deluxe','send',settings='Crush/Crunch по вкусу, Mix через return.'),
 S('EQ / тон','FabFilter Pro-Q 3','send',settings='HPF/LPF на parallel return.')],
 'Отдельный parallel return для энергии, dry room сохраняется.','elysia mpressor, CLA-76, Decapitator','Проверить latency/phase parallel return.')
P('room-tight',SRC,'Tight / modern',[
 S('Creative FX','RESTRUKT',settings='Сначала sustain reduction, tape/shimmer минимально.'),
 S('Транзиенты','elysia nvelope',settings='Уменьшить sustain, сохранить attack.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Лёгкая density после envelope.')],
 'Для слишком длинной или захламлённой комнаты.','Trans-X, Pro-G expansion','Не делать room полностью безжизненным.')

# 06 Drum bus
SRC='Drum bus / группа барабанов'
P('dbus-min',SRC,'Минимальный glue',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Broad correction до 1–2 dB.'),
 S('Компрессия / уровень','bx_townhouse Buss Compressor',settings='Ratio 2:1/4:1, Attack 10–30 ms, GR 0.5–2 dB.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Срезать редкие пики 0.5–2 dB.')],
 'Классический punch/glue без лишних стадий.','SSL G-Master, Vertigo VSC-2, Pro-C 2','Если kick стал меньше — замедлить Attack или уменьшить GR.')
P('dbus-api',SRC,'API punch',[
 S('Компрессия / уровень','Waves API 2500',settings='Thrust/SC разгружает detector от sub; GR 1–3 dB.'),
 S('Сатурация / цвет','Black Box Analog Design HG-2',settings='Лёгкий parallel saturation.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Только короткие пики.')],
 'Напористая drum-bus цепь.','Lindell SBC, VSM-3, SA2RATE','Проверить stereo link и low-end stability.')
P('dbus-parallel',SRC,'Parallel New York',[
 S('Компрессия / уровень','Waves CLA-76 Black / Blue','send',settings='Сильный GR, fast release; подмешать return.'),
 S('Сатурация / цвет','Soundtoys Decapitator','send',settings='Drive на parallel return, output matched.'),
 S('EQ / тон','FabFilter Pro-Q 3','send',settings='Убрать лишний sub и brittle top.')],
 'Параллельная цепь для density при сохранении dry transients.','MC77, Devil-Loc Deluxe, mpressor','Parallel return не должен фазово уменьшать dry drums.')

# 07 Bass guitar
SRC='Бас-гитара'
P('bass-min',SRC,'Чистый bass',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Очистить rumble/mud и освободить kick.'),
 S('Компрессия / уровень','Bass Rider',settings='Сначала выровнять ноты без изменения attack.'),
 S('Компрессия / уровень','Waves CLA-2A',settings='Плавное leveling, GR 2–5 dB.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Лёгкие harmonics для маленьких систем.')],
 'Универсальная pop/rock цепь.','Gem Comp LA, Pro-C 2, RBass','Проверить ноты sub и отношение к kick.')
P('bass-rock',SRC,'Rock amp blend',[
 S('Amp / cabinet / pedal','Ampeg SVT-VR Classic',settings='Blend с clean DI; amp даёт midrange.'),
 S('EQ / тон','FabFilter Pro-Q 3',settings='Совместить DI/amp и убрать конфликт kick.'),
 S('Компрессия / уровень','Purple Audio MC77',settings='2–5 dB GR, сохранить pick/finger attack.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Ловить единичные пики.')],
 'Amp tone с контролируемым фундаментом.','V-4B, Darkglass Ultra, Mark Studio 2','Совместить phase DI и amp.')
P('bass-metal',SRC,'Modern metal',[
 S('Amp / cabinet / pedal','Parallax',settings='Clean compressed low, distorted mids/highs.'),
 S('EQ / тон','Waves F6 Dynamic EQ',settings='External sidechain от kick в зоне конфликта.'),
 S('Компрессия / уровень','FabFilter Pro-MB',settings='Только нестабильные bands, 1–3 dB GR.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Контролировать pick peaks.')],
 'Плотный bass для metal/prog.','Darkglass Ultra, C6, F6','Low band держать mono; слушать под гитарами.')

# 08 808 / synth bass
SRC='808 / synth bass / sub bass'
P('808-min',SRC,'Чистый 808',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Убрать инфраниз и resonant overs.'),
 S('Компрессия / уровень','FabFilter Pro-MB',settings='Стабилизировать только плавающие low bands.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Добавить harmonics, фундамент оставить clean.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Короткие пики 1–2 dB.')],
 'Чистый устойчивый 808 без лишнего stereo.','F6, C6, Low End Focus','Проверить mono и pitch каждой ноты.')
P('808-phone',SRC,'Слышно на телефоне',[
 S('EQ / тон','FabFilter Pro-Q 3'),
 S('Низ / фундамент','Waves RBass / Renaissance Bass',settings='Выбрать fundamental и добавить mid harmonics.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Лёгкая saturation выше sub.'),
 S('Limiter / clipper','FabFilter Pro-L 2',settings='Только peak control, не flatten.')],
 'Гармоники вместо простого увеличения sub.','MaxxBass, Scheps Parallel Particles, BodyLift','Сравнивать на band-limited speaker.')
P('808-kick',SRC,'Sidechain от kick',[
 S('Фаза / стерео','Waves InPhase',settings='Если kick и 808 слоятся — проверить phase.'),
 S('EQ / тон','Waves F6 Dynamic EQ',settings='External SC от kick; dip около kick fundamental.'),
 S('Компрессия / уровень','FabFilter Pro-MB',settings='При необходимости duck только low band.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Финальные пики.')],
 'Частотно-зависимое ducking обычно прозрачнее broadband pump.','C6, Pro-Q dynamic, H-Comp sidechain','Release настроить по groove; ducking не должен быть слышен.')

# 09 Lead vocal
SRC='Lead vocal / основной вокал'
P('vocal-min',SRC,'Базовый vocal',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Corrective EQ, убрать rumble/resonances.'),
 S('Компрессия / уровень','FabFilter Pro-C 2',settings='Ratio 2:1–3:1, GR 2–4 dB.'),
 S('Очистка / repair','FabFilter Pro-DS',settings='После brightening/compression, 2–4 dB reduction.'),
 S('Reverb / пространство','FabFilter Pro-R','send',settings='100% wet, pre-delay 30–80 ms, HPF return.')],
 'Минимальная профессиональная vocal chain.','F6, Sibilance, Room Service','Clip gain и tuning выполнить до processing.')
P('vocal-modern',SRC,'Modern pop',[
 S('EQ / тон','FabFilter Pro-Q 3'),
 S('Компрессия / уровень','Purple Audio MC77',settings='Peak catcher, GR 1–3 dB.'),
 S('Компрессия / уровень','Overloud Gem Comp LA',settings='Leveling 2–4 dB.'),
 S('Очистка / repair','FabFilter Pro-DS',settings='Финальный de-ess.'),
 S('Delay / echo','Soundtoys EchoBoy','send',settings='Filtered throw/slap, 100% wet.'),
 S('Reverb / пространство','Soundtoys SuperPlate','send',settings='Ducking/HPF для разборчивости.')],
 'Serial FET + opto и два отдельных send FX.','CLA-76 + CLA-2A, H-Delay, Pro-R','Автоматизация громкости до compression часто лучше дополнительного GR.')
P('vocal-fast',SRC,'Быстрый готовый vocal',[
 S('Очистка / repair','Sssh',settings='Лёгкий pre de-ess при резком исходнике.'),
 S('Channel strip / macro','HVX Chain',settings='Выставить input; включать только нужные stages.'),
 S('Delay / echo','Slapshot','send',settings='Короткий filtered slap.'),
 S('Reverb / пространство','Room Service','send',settings='Ducking и 100% wet.')],
 'Быстрая цепь с одним основным vocal macro.','GilderVox, VxBx, Gem Voice','Не добавлять второй полный channel strip поверх HVX.')

# 10 Backing vocals
SRC='Backing vocals / вокальные слои'
P('bvox-min',SRC,'Плотный stack',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Убрать лишний low-mid и место под lead.'),
 S('Компрессия / уровень','Renaissance Vox',settings='Плотнее lead, но без лишнего noise.'),
 S('Очистка / repair','FabFilter Pro-DS',settings='Групповой лёгкий de-ess.'),
 S('Модуляция / ширина','Soundtoys MicroShift','send',settings='Dry center не нужен для всех layers; mono-check.'),
 S('Reverb / пространство','FabFilter Pro-R','send',settings='Общий shared space.')],
 'Широкие, но контролируемые backing vocals.','Doubler, Double Dare, S1','Lead vocal должен оставаться впереди и в центре.')
P('bvox-clean',SRC,'Clean pop',[
 S('EQ / тон','Waves F6 Dynamic EQ'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='GR 3–6 dB для ровного stack.'),
 S('Очистка / repair','Waves Sibilance'),S('Модуляция / ширина','Double Dare','send'),S('Reverb / пространство','Room Service','send')],
 'Быстрый clean stack с отдельными width/room sends.','MicroShift, Pro-DS, SuperPlate','Низ backing-группы держать уже и тише lead.')
P('bvox-fast',SRC,'Быстрый macro',[
 S('Channel strip / macro','GilderVox',settings='Input по уровню, умеренный tone.'),
 S('Очистка / repair','FabFilter Pro-DS'),S('Модуляция / ширина','Double Dare','send'),S('Reverb / пространство','Room Service','send')],
 'Минимум окон и готовый backing tone.','HVX Chain, CLA Vocals','Не использовать macro для исправления отдельного резонанса.')

# 11 Speech / dialog
SRC='Речь / podcast / dialog'
P('speech-min',SRC,'Чистая речь',[
 S('Очистка / repair','Waves Clarity Vx',settings='Лёгкое denoise до artifacts.'),
 S('EQ / тон','FabFilter Pro-Q 3',settings='HPF/резонансы по голосу.'),
 S('Компрессия / уровень','FabFilter Pro-C 2',settings='Ratio 2:1–3:1, GR 2–4 dB.'),
 S('Очистка / repair','FabFilter Pro-DS'),S('Limiter / clipper','FabFilter Pro-L 2',settings='Peak control и delivery ceiling.'),
 S('Контроль / анализ','SPL HawkEye','monitor',settings='LUFS/TP после limiter.')],
 'Прозрачная narration chain.','NS1, Vocal Rider, MaxxVolume','Denoise всегда до compression.')
P('speech-fast',SRC,'One-click narration',[
 S('Channel strip / macro','SPEAKMIX',settings='Voice Timber и CLEAN; проверить artifacts.'),
 S('Контроль / анализ','SPL HawkEye','monitor',settings='Проверить итоговый loudness и True Peak.')],
 'Самый быстрый вариант для podcast/YouTube.','VxBx, GilderVox','SPEAKMIX уже содержит несколько stages — не дублировать их автоматически.')
P('speech-room',SRC,'Проблемная комната',[
 S('Очистка / repair','Waves Clarity Vx DeReverb',settings='Оставить немного естественной ambience.'),
 S('EQ / тон','Waves F6 Dynamic EQ'),S('Компрессия / уровень','Renaissance Vox',settings='Умеренно; следить за breaths.'),
 S('Очистка / repair','Waves Sibilance'),S('Limiter / clipper','FabFilter Pro-L 2'),S('Контроль / анализ','SPL HawkEye','monitor')],
 'Для домашней записи с выраженной комнатой.','Clarity Vx, NS1, Pro-DS','Остановиться до watery/phasey artifacts.')

# 12 Electric guitar
SRC='Электрогитара'
P('egtr-clean',SRC,'Clean / funk',[
 S('Amp / cabinet / pedal','Archetype: Cory Wong',settings='Clean/edge tone, умеренная compression.'),
 S('EQ / тон','API 550A',settings='Broad mid/presence moves.'),
 S('Компрессия / уровень','Waves CLA-3A',settings='GR 1–4 dB.'),
 S('Delay / echo','Waves H-Delay','send',settings='Slap/filtered delay.'),S('Reverb / пространство','Room Service','send')],
 'Читаемая clean-гитара с короткими sends.','Tone King Imperial MKII, Buxom Betty','Сохранить pick dynamics.')
P('egtr-rock',SRC,'Rock rhythm',[
 S('Amp / cabinet / pedal','Friedman BE-100',settings='Gain ниже solo-ожидания.'),
 S('EQ / тон','FabFilter Pro-Q 3',settings='HPF/LPF и конфликт с vocal.'),
 S('Очистка / repair','bx_refinement / V3',settings='Только fizz/harshness.'),
 S('Delay / echo','Soundtoys EchoBoy','send',settings='Короткий filtered ambience при необходимости.')],
 'Готовый rock rhythm без избыточного post-processing.','Soldano SLO-100, Friedman JJ-100','Двойные партии лучше реального widener.')
P('egtr-metal',SRC,'Modern metal',[
 S('Gate / expander','FabFilter Pro-G',settings='Сохранить sustain, не обрезать ноты.'),
 S('Amp / cabinet / pedal','bx_greenscreamer',settings='Drive low, Level high для tight low end.'),
 S('Amp / cabinet / pedal','Fortin Nameless Suite',settings='Gain умеренно, cab/IR в контексте.'),
 S('EQ / тон','FabFilter Pro-Q 3'),S('Очистка / repair','bx_refinement / V3',settings='Укротить fizz динамически.')],
 'Tight high-gain цепь.','Diezel VH4, Granophyre, Archetype: Gojira','Не делать две гитары шире phase-widener-ом.')

# 13 Acoustic guitar
SRC='Акустическая гитара'
P('agtr-min',SRC,'Натуральная',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='Ratio 2:1, GR 1–3 dB.'),
 S('Очистка / repair','bx_refinement / V3',settings='Укротить pick harshness.'),S('Reverb / пространство','FabFilter Pro-R','send',settings='Short room, 100% wet.')],
 'Минимальная natural chain.','CLA-3A, Gem Comp LA, Room Service','Не вырезать весь body 100–300 Hz.')
P('agtr-pop',SRC,'Яркая pop',[
 S('Channel strip / macro','Scheps Omni Channel',settings='Filters/EQ/dynamics только по задаче.'),
 S('EQ / тон','Maag EQ4',settings='Air после de-harsh.'),S('Сатурация / цвет','Overloud Gem Dopamine',settings='Малый Amount.'),
 S('Модуляция / ширина','Soundtoys MicroShift','send'),S('Reverb / пространство','Soundtoys Little Plate','send')],
 'Pop acoustic с controlled brightness.','Maserati ACG, CLA Unplugged','Следить за конфликтом с vocal 2–6 kHz.')
P('agtr-cinematic',SRC,'Cinematic / felt',[
 S('Creative FX','CINEFELT',settings='Warm/Clean, умеренный Felt amount.'),S('EQ / тон','FabFilter Pro-Q 3'),
 S('Reverb / пространство','Room Service','send',settings='Короткая общая комната.')],
 'Отдельный cinematic layer, а не обязательная обработка dry guitar.','Mixtape, Erebos','При сильном Felt лучше оставить dry-копию отдельно.')

# 14 Piano / keys
SRC='Piano / клавишные'
P('piano-min',SRC,'Натуральное piano',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','Overloud Gem Comp LA',settings='GR 1–3 dB.'),
 S('Reverb / пространство','FabFilter Pro-R','send',settings='Room/hall по перспективе.')],
 'Минимальная natural chain.','Millennia TCL-2, IR-1','Проверить stereo low end и pedal noise.')
P('piano-pop',SRC,'Pop forward',[
 S('Channel strip / macro','Greg Wells PianoCentric',settings='Начать с малого Amount.'),S('EQ / тон','FabFilter Pro-Q 3'),
 S('Компрессия / уровень','Waves V-Comp',settings='Малый GR для density.'),
 S('Модуляция / ширина','Soundtoys MicroShift','send'),S('Reverb / пространство','Soundtoys SuperPlate','send')],
 'Плотное piano под lead vocal.','JJP Piano, Maag EQ4','Не занимать весь midrange и stereo field.')
P('piano-cinematic',SRC,'Cinematic felt',[
 S('Creative FX','CINEFELT',settings='Felt amount по аранжировке.'),S('Компрессия / уровень','GilderComp',settings='Gentle leveling.'),
 S('Reverb / пространство','Erebos','send',settings='Dark layer отдельно от dry piano.')],
 'Intimate felt/cinematic texture.','Mixtape, Room Service','Long tail фильтровать и автоматизировать.')

# 15 Synths / pads
SRC='Synth / pads / textures'
P('synth-min',SRC,'Чистый synth',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='Только если нужна динамическая стабильность.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Лёгкий color.'),S('Reverb / пространство','FabFilter Pro-R','send')],
 'Минимальная обработка готового synth patch.','F6, Pro-MB, Room Service','Сначала исправить сам patch, потом добавлять plugins.')
P('synth-rhythm',SRC,'Rhythmic / sidechain',[
 S('EQ / тон','Soundtoys FilterFreak 2',settings='Tempo-synced filter movement.'),
 S('Компрессия / уровень','UltraPump',settings='External kick trigger, Release по groove.'),
 S('Сатурация / цвет','FabFilter Saturn 2'),S('Модуляция / ширина','Soundtoys PanMan','send',settings='Low end не панорамировать.')],
 'Ритмическая electronic chain.','Volcano 3, Pro-C 2 sidechain, Tremolator','Pump должен поддерживать groove, а не скрывать harmony.')
P('synth-ambient',SRC,'Ambient texture',[
 S('EQ / тон','FabFilter Volcano 3',settings='Медленная modulation.'),
 S('Delay / echo','FabFilter Timeless 3','send',settings='Filtered evolving repeats.'),
 S('Reverb / пространство','Unfiltered Audio SILO','send',settings='Granular tail, low cut.'),
 S('Модуляция / ширина','Ozone Imager',settings='Расширять только нужные bands.')],
 'Отдельные delay/reverb sends для evolving pad.','Erebos, Crystallizer, BYOME','Проверить mono и убрать лишний low-end tail.')

# 16 Strings / orchestral
SRC='Strings / orchestral / acoustic ensemble'
P('strings-min',SRC,'Натуральные strings',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','Millennia TCL-2',settings='GR 0.5–2 dB.'),
 S('Reverb / пространство','Waves IR-1','send',settings='Realistic hall/room, 100% wet.')],
 'Сохраняет естественную динамику.','AMEK EQ 200, Gem Comp LA, Pro-R','Не выравнивать orchestral dynamics до плоскости.')
P('strings-warm',SRC,'Warm cinematic',[
 S('EQ / тон','AMEK EQ 200',settings='Broad tonal moves.'),S('Компрессия / уровень','Waves PuigChild 670',settings='0.5–2 dB GR.'),
 S('Сатурация / цвет','Overloud Gem Dopamine',settings='Малый Amount.'),S('Reverb / пространство','Abbey Road Chambers','send')],
 'Тёплая cinematic цепь.','Gem Comp 670, J37, H-Reverb','Сохранять transient bows и depth секций.')
P('strings-dark',SRC,'Dark / intimate layer',[
 S('Creative FX','CINEFELT',settings='На копии или отдельном layer.'),S('Компрессия / уровень','DUEL LT',settings='Многоступенчатую dynamics использовать умеренно.'),
 S('Reverb / пространство','Erebos','send',settings='Dark spatial return.')],
 'Специальный layer для trailer/ambient, не замена natural strings.','Mixtape, RESTRUKT','Печатать layer отдельно и фильтровать под dry ensemble.')

# 17 FX / transitions
SRC='FX / transitions / sound design'
P('fx-transition',SRC,'Фильтрованный переход',[
 S('EQ / тон','Soundtoys FilterFreak 2',settings='Automation cutoff/resonance.'),
 S('Delay / echo','Soundtoys Crystallizer','send',settings='Pitch/reverse echo.'),S('Модуляция / ширина','Soundtoys PanMan','send'),
 S('Limiter / clipper','Cactus Clipper',settings='Страховка коротких peaks.')],
 'Управляемый riser/fall.','Volcano 3, Timeless 3','Feedback/resonance контролировать limiter-ом.')
P('fx-granular',SRC,'Granular / spectral',[
 S('Creative FX','Unfiltered Audio SpecOps',settings='Freeze/smear умеренно.'),
 S('Reverb / пространство','Unfiltered Audio SILO','send',settings='Granular space.'),S('Limiter / clipper','Prickly Clip',settings='Peak safety.')],
 'Печатать лучшие фрагменты в audio.','BYOME, Erebos, RESTRUKT','Spectral FX могут размыть transients.')
P('fx-random',SRC,'Быстрая генерация идеи',[
 S('Creative FX','Chance',settings='Сохранить удачный seed/preset.'),S('EQ / тон','FabFilter Pro-Q 3',settings='Освободить спектр под mix.'),
 S('Limiter / clipper','Cactus Clipper',settings='Ловить feedback peaks.')],
 'Простой random creative preset.','BYOME, Effect Rack','Не оставлять все random modules на максимуме.')

# 18 Instrument bus / stem
SRC='Instrument bus / stem'
P('stem-min',SRC,'Чистый stem',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Broad correction 0.5–2 dB.'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='GR 0.5–2 dB.'),
 S('Сатурация / цвет','FabFilter Saturn 2',settings='Лёгкая density.'),S('Limiter / clipper','Newfangled Saturate',settings='Только единичные peaks.')],
 'Прозрачная stem chain.','Pro-MB, Dangerous Compressor','Не дублировать heavy processing отдельных tracks.')
P('stem-analog',SRC,'Analog character',[
 S('EQ / тон','API 550B'),S('Компрессия / уровень','Waves API 2500',settings='GR 1–2 dB.'),
 S('Сатурация / цвет','Black Box Analog Design HG-2',settings='Лёгкий tube density.'),S('Limiter / clipper','Newfangled Saturate')],
 'Характерный stem/bus preset.','Lindell SBC, VSM-3, Forge','Level-match после каждой nonlinear стадии.')
P('stem-fast',SRC,'Быстрый finisher',[
 S('Channel strip / macro','Bus Ride',settings='Drive → compression → broad EQ; limiter только peaks.')],
 'Один all-in-one processor вместо длинной цепи.','Busboy, Epicizer','Не ставить второй bus finisher следом.')

# 19 Mix bus
SRC='Mix bus / стереошина'
P('mixbus-min',SRC,'Минимальный mix bus',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Broad ±0.5–1 dB.'),S('Компрессия / уровень','bx_townhouse Buss Compressor',settings='GR 0.5–2 dB.'),
 S('Limiter / clipper','Newfangled Saturate',settings='0.5–1.5 dB peak trim.'),S('Контроль / анализ','ADPTR Metric AB','monitor',settings='Level-matched references.')],
 'Минимальный glue и peak control.','SSL G-Master, Pro-C 2','Если будет отдельный mastering — сохранить clean pre-master.')
P('mixbus-clean',SRC,'Чистый и прозрачный',[
 S('EQ / тон','AMEK EQ 200',settings='Очень широкие малые moves.'),S('Компрессия / уровень','Dangerous Compressor',settings='GR 0.5–1.5 dB.'),
 S('Limiter / clipper','Newfangled Saturate',settings='Редкие peaks.'),S('Контроль / анализ','SPL HawkEye','monitor'),S('Контроль / анализ','ADPTR Metric AB','monitor')],
 'Прозрачная mix-bus chain без финального loudness limiting.','FabFilter Pro-Q 3, Vertigo VSC-2','Monitoring plugins не экспортировать.')
P('mixbus-analog',SRC,'Analog color',[
 S('EQ / тон','Dangerous BAX EQ',settings='Broad shelves ≤1 dB.'),S('Компрессия / уровень','SPL Iron',settings='GR 0.5–1.5 dB.'),
 S('Сатурация / цвет','Black Box Analog Design HG-2',settings='Очень мало.'),S('Контроль / анализ','ADPTR Metric AB','monitor')],
 'Один EQ, один compressor и одна color-stage.','elysia museq, Shadow Hills, VSM-3','Не складывать несколько analog emulations без причины.')

# 20 Mastering
SRC='Mastering / финальный мастер'
P('master-min',SRC,'Минимальный master',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='Broad ±0.25–1 dB.'),S('Limiter / clipper','FabFilter Pro-L 2',settings='True Peak по задаче; GR обычно до 1–3 dB.'),
 S('Контроль / анализ','SPL HawkEye','monitor'),S('Контроль / анализ','ADPTR Metric AB','monitor')],
 'EQ при необходимости и limiter в конце processing chain.','Ozone Maximizer, AMEK EQ 200','Сравнивать с референсами при одинаковой громкости.')
P('master-clean',SRC,'Чистый controlled master',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','Ozone Dynamics',settings='Single-band/малый GR; multiband только по проблеме.'),
 S('Limiter / clipper','Newfangled Saturate',settings='0.5–2 dB clip перед limiter.'),S('Limiter / clipper','Ozone Maximizer',settings='Финальный limiter/True Peak.'),
 S('Контроль / анализ','SPL HawkEye','monitor'),S('Контроль / анализ','Ozone Tonal Balance Control','monitor')],
 'Распределяет peak control между clipper и limiter.','Pro-L 2, Elevate','Не гнаться за LUFS ценой snare/vocal transients.')
P('master-analog',SRC,'Analog-style master',[
 S('EQ / тон','Dangerous BAX EQ',settings='Broad shelves, малые moves.'),S('Компрессия / уровень','SPL Iron',settings='GR 0.5–1.5 dB.'),
 S('Сатурация / цвет','Black Box Analog Design HG-2',settings='Очень лёгкая density.'),S('Limiter / clipper','FabFilter Pro-L 2',settings='Финальный ceiling/TP.'),
 S('Контроль / анализ','ADPTR Metric AB','monitor')],
 'Conservative analog color до прозрачного limiter.','elysia museq, Shadow Hills, Sage Velvet','Level-match после каждой стадии и сохранять динамику.')

# Rename the original 20 sources into the grouped taxonomy used by the app.
SOURCE_RENAME={
'Бочка / kick':'Бочка / Kick','Малый барабан / clap':'Малый барабан / Snare / Clap','Томы / перкуссия':'Toms',
'Overheads / тарелки / hi-hat':'Overheads','Room microphones / drum ambience':'Room Microphones','Drum bus / группа барабанов':'Drum Bus',
'Бас-гитара':'Bass Guitar','808 / synth bass / sub bass':'808 / Sub Bass','Lead vocal / основной вокал':'Lead Vocal',
'Backing vocals / вокальные слои':'Backing Vocals','Речь / podcast / dialog':'Speech / Podcast / Dialog','Электрогитара':'Electric Guitar',
'Акустическая гитара':'Acoustic Guitar','Piano / клавишные':'Acoustic Piano','Synth / pads / textures':'Pads / Textures',
'Strings / orchestral / acoustic ensemble':'Strings','FX / transitions / sound design':'FX / Transitions / Sound Design',
'Instrument bus / stem':'Instrument Stem','Mix bus / стереошина':'Mix Bus / Stereo Bus','Mastering / финальный мастер':'Premaster / Mastering'}
for preset in PRESETS:
    preset['source']=SOURCE_RENAME.get(preset['source'],preset['source'])

# Additional sources introduced by the revised hierarchy.
SRC='Hi-hat / Cymbals'
P('hihat-min',SRC,'Чистый hi-hat',[
 S('EQ / тон','FabFilter Pro-Q 3',settings='HPF/динамический cut только по проблеме.'),S('Очистка / repair','FabFilter Pro-DS',settings='1–3 dB split-band control.'),
 S('Компрессия / уровень','FabFilter Pro-C 2',settings='Если нужна стабильность: GR до 1–2 dB.')],
 'Минимальная обработка close hi-hat/cymbal.','F6, Sibilance, bx_refinement','Не делать hat шире и ярче автоматически.')
P('hihat-soft',SRC,'Мягкий верх',[
 S('EQ / тон','Waves F6 Dynamic EQ',settings='Укротить отдельные 6–12 kHz peaks.'),S('Очистка / repair','bx_refinement / V3',settings='Небольшой de-harsh.'),
 S('Сатурация / цвет','Waves J37 Tape',settings='Лёгкий smoothing, wow/flutter минимально.')],
 'Смягчает цифровой/колкий верх.','Pro-DS, Kramer Master Tape','Сравнивать при одинаковой громкости.')
P('hihat-character',SRC,'Character cymbals',[
 S('EQ / тон','Maag EQ4',settings='Air очень умеренно после de-harsh.'),S('Сатурация / цвет','Overloud Gem Dopamine',settings='Малый Amount.'),
 S('Фаза / стерео','bx_control V2',settings='Проверить width/mono, не расширять без причины.')],
 'Для controlled brightness и stereo check.','8K, Chakra','Следить за sibilance вокала в той же зоне.')

SRC='Percussion'
P('perc-min',SRC,'Натуральная percussion',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Транзиенты','Waves Smack Attack',settings='Attack/Sustain умеренно.'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='GR 1–3 dB.')],
 'Чистая цепь для congas, shakers и дополнительной percussion.','Trans-X, API 550A','Сохранять groove и различия ударов.')
P('perc-move',SRC,'Ритмическое движение',[
 S('EQ / тон','Soundtoys FilterFreak 2',settings='Tempo-synced movement.'),S('Модуляция / ширина','Soundtoys PanMan','send',settings='Low percussion не панорамировать слишком широко.'),
 S('Delay / echo','Soundtoys EchoBoy','send',settings='Filtered rhythmic repeats.')],
 'Для второстепенных percussion layers.','Tremolator, ExoDelay','Эффект не должен менять основной groove.')
P('perc-character',SRC,'Character percussion',[
 S('EQ / тон','API 560'),S('Сатурация / цвет','Soundtoys Decapitator',settings='Mix/parallel.'),S('Reverb / пространство','Room Service','send',settings='Короткий shared room.')],
 'Более плотная и выразительная percussion.','Radiator, Saturn 2','Контролировать brittle top после drive.')

SRC='Drum Loop'
P('loop-min',SRC,'Чистый loop',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='GR 1–3 dB, release по groove.'),S('Limiter / clipper','Newfangled Saturate',settings='Только peaks.')],
 'Минимальная обработка готового drum loop.','Pro-MB, C6','Не разрушать исходный groove.')
P('loop-tight',SRC,'Tight loop',[
 S('Creative FX','RESTRUKT',settings='Sustain reduction сначала.'),S('Транзиенты','Waves Trans-X',settings='Подстроить attack/sustain по groove.'),S('Сатурация / цвет','Mixtape',settings='Лёгкий color без лишнего drift/noise.')],
 'Для слишком room-heavy или размытого loop.','nvelope, Pro-G expansion','Не убирать весь ambience.')
P('loop-crush',SRC,'Parallel crush',[
 S('Компрессия / уровень','Soundtoys Devil-Loc Deluxe','send',settings='Сильный crush, подмешать return.'),S('Сатурация / цвет','Soundtoys Decapitator','send'),S('EQ / тон','FabFilter Pro-Q 3','send',settings='Фильтровать parallel return.')],
 'Параллельная агрессивная обработка.','MC77, mpressor','Проверить phase/latency параллельной ветки.')

SRC='Synth Bass'
P('sbass-min',SRC,'Чистый synth bass',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','bx_opto',settings='Gentle leveling 1–3 dB GR; сохранить envelope.'),S('Сатурация / цвет','FabFilter Saturn 2',settings='Harmonics выше sub.')],
 'Для обычного synth bass, не обязательно 808.','Pro-MB, F6','Низ держать mono и проверять с kick.')
P('sbass-sidechain',SRC,'Sidechain от kick',[
 S('EQ / тон','Waves F6 Dynamic EQ',settings='External SC, dip только в зоне kick.'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='Broadband duck только если нужен pump.'),S('Сатурация / цвет','FabFilter Saturn 2')],
 'Частотно-зависимое и broadband ducking по задаче.','C6, Pro-MB','Release настраивать по groove.')
P('sbass-character',SRC,'Distorted synth bass',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Сатурация / цвет','Soundtoys Decapitator',settings='Parallel; clean sub сохранить.'),S('Limiter / clipper','Newfangled Saturate')],
 'Для midrange grit без разрушения sub.','Violet Fuzz, Honeycomb Bass OD','Distorted ветку полезно high-pass.')

SRC='Bass Bus'
P('bbus-min',SRC,'Чистый bass bus',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','bx_opto',settings='Gentle leveling 1–3 dB GR, low end не раскачивать.'),S('Limiter / clipper','Newfangled Saturate',settings='Только peaks.')],
 'Собирает несколько bass layers.','Pro-MB, Dangerous Compressor','Проверить phase всех low layers.')
P('bbus-punch',SRC,'Punch / glue',[
 S('EQ / тон','API 550B'),S('Компрессия / уровень','Waves API 2500',settings='GR 1–2 dB.'),S('Сатурация / цвет','Black Box Analog Design HG-2',settings='Очень мало.')],
 'Character bus для rock/electronic low end.','Lindell SBC, VSM-3','Не раздувать low-mid.')
P('bbus-fast',SRC,'Быстрый finisher',[
 S('Channel strip / macro','Busboy',settings='Input → broad EQ → gentle compression; limiter только редкие peaks.')],
 'Один bus processor вместо длинной chain.','Busboy','Не добавлять второй finisher подряд.')

SRC='Vocal Bus'
P('vbus-min',SRC,'Чистый vocal bus',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='GR 0.5–2 dB.'),S('Очистка / repair','FabFilter Pro-DS',settings='Только общие S-peaks.')],
 'Лёгкий glue для lead/backing group.','F6, GilderComp','Не исправлять bus-ом проблему одной дорожки.')
P('vbus-character',SRC,'Character vocal bus',[
 S('EQ / тон','Maag EQ4',settings='Air после de-essing.'),S('Компрессия / уровень','The Josie TD3',settings='Gentle opto glue.'),S('Сатурация / цвет','Black Box Analog Design HG-2',settings='Минимальный drive.')],
 'Плотный polished vocal group.','bx_opto, Forge','Level-match и следить за sibilance.')
P('vbus-fast',SRC,'Быстрый bus',[
 S('Channel strip / macro','GilderVox',settings='Input по уровню; tone/compression умеренно, встроенные effects только по роли vocal bus.')],
 'All-in-one vocal-group finishing.','Busboy, Bus Ride','Не дублировать individual vocal chains.')

SRC='Guitar Bus'
P('gbus-min',SRC,'Чистый guitar bus',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','Vertigo VSC-2',settings='Bus glue 0.5–2 dB GR, Attack сохраняет pick.'),S('Сатурация / цвет','Forge',settings='Минимальный transformer/tube color, Output matched.')],
 'Glue для нескольких guitar tracks.','Vertigo VSC-2, Forge','Не исправлять общий fizz только bus EQ.')
P('gbus-rock',SRC,'Rock glue',[
 S('EQ / тон','API 550B'),S('Компрессия / уровень','Vertigo VSC-2',settings='GR 1–2 dB, medium Attack, Release по groove.'),S('Сатурация / цвет','Black Box Analog Design HG-2')],
 'Плотная rock-группа.','bx_townhouse, VSM-3','Слушать midrange под вокалом.')
P('gbus-fast',SRC,'Быстрый finisher',[
 S('Channel strip / macro','Maserati GRP',settings='Начать с neutral tone; compression/FX добавлять только по задаче guitar group.')],
 'Один processor для tone и glue.','Bus Ride, Busboy','Сохранить clean bus version.')

SRC='Electric Piano / Keys / Organ'
P('keys-min',SRC,'Чистые keys',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','Overloud Gem Comp LA',settings='GR 1–3 dB.'),S('Reverb / пространство','Room Service','send')],
 'Для Rhodes, Wurlitzer и organ.','CLA-3A, Pro-R','Не убирать характерные low-mids целиком.')
P('keys-vintage',SRC,'Vintage keys',[
 S('EQ / тон','Scheps 73'),S('Сатурация / цвет','Waves J37 Tape'),S('Модуляция / ширина','Soundtoys PhaseMistress','send',settings='Малый Mix.')],
 'Vintage color и движение.','Radiator, Mixtape, Tremolator','Mono-check при modulation.')
P('keys-pop',SRC,'Pop keys',[
 S('Channel strip / macro','Greg Wells PianoCentric'),S('EQ / тон','FabFilter Pro-Q 3'),S('Delay / echo','Waves H-Delay','send'),S('Reverb / пространство','Soundtoys SuperPlate','send')],
 'Быстрый polished keys sound.','JJP Piano, EchoBoy','Освободить место lead vocal.')

SRC='Synth Lead / Pluck / Arp'
P('slead-min',SRC,'Чистый lead/pluck',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','FabFilter Pro-C 2',settings='Если envelope нестабильна.'),S('Delay / echo','FabFilter Timeless 3','send')],
 'Фокусированный synth lead.','F6, EchoBoy','Низ и stereo не должны мешать vocal.')
P('slead-rhythm',SRC,'Rhythmic arp',[
 S('EQ / тон','Soundtoys FilterFreak 2'),S('Компрессия / уровень','UltraPump',settings='Kick sidechain по groove.'),S('Delay / echo','Soundtoys EchoBoy','send')],
 'Движение и pump для arp/pluck.','Volcano 3, H-Delay','Не размывать атаку длинным delay.')
P('slead-character',SRC,'Character lead',[
 S('Сатурация / цвет','FabFilter Saturn 2'),S('Модуляция / ширина','Soundtoys MicroShift','send'),S('Reverb / пространство','Soundtoys SuperPlate','send')],
 'Плотный широкий lead с dry center.','Decapitator, Double Dare','Проверить mono и сохранить центр.')

SRC='Synth / Keys Bus'
P('synthbus-min',SRC,'Чистый synth bus',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','Dangerous Compressor',settings='Transparent glue 0.5–2 dB GR; sidechain HPF при pumping.'),S('Сатурация / цвет','Waves J37 Tape',settings='Лёгкий tape density; wow/flutter почти zero, Output matched.')],
 'Glue для layers/keys.','Pro-MB, Vertigo VSC-2','Не выравнивать все layers до плоскости.')
P('synthbus-sidechain',SRC,'Kick-controlled bus',[
 S('EQ / тон','Waves F6 Dynamic EQ',settings='Частотный SC от kick.'),S('Компрессия / уровень','UltraPump',settings='Broad pump только по стилю.'),S('Фаза / стерео','bx_control V2',settings='Low end mono/width check.')],
 'Для electronic synth group.','Pro-C 2, C6','Сохранять groove и mono compatibility.')
P('synthbus-fast',SRC,'Быстрый finisher',[
 S('Channel strip / macro','CLA MixDown',settings='Использовать как быстрый preview/finisher: tone и glue малыми движениями, без loudness bias.')],
 'All-in-one finishing.','Busboy, Bus Ride','Не добавлять лишний limiter до mastering.')

SRC='Brass / Woodwinds'
P('brass-min',SRC,'Натуральный ensemble',[
 S('EQ / тон','AMEK EQ 200',settings='Broad tonal correction до 1 dB; harshness 1–5 kHz только по слуху.'),S('Компрессия / уровень','Overloud Gem Comp LA',settings='Gentle leveling 0.5–2 dB GR, сохранить breath и attack.'),S('Reverb / пространство','Abbey Road Chambers','send',settings='Natural chamber/hall, 100% wet, pre-delay по перспективе.')],
 'Сохраняет естественную динамику.','AMEK EQ 200, Pro-R','Не убирать breath/attack полностью.')
P('brass-cinematic',SRC,'Cinematic brass',[
 S('EQ / тон','AMEK EQ 200'),S('Компрессия / уровень','DUEL LT',settings='Multi-stage dynamics умеренно.'),S('Reverb / пространство','Waves H-Reverb','send')],
 'Плотный trailer/cinematic brass.','Ozone Dynamics, Erebos','Не делать brass постоянной стеной.')
P('woodwind-warm',SRC,'Warm woodwinds',[
 S('EQ / тон','Dangerous BAX EQ'),S('Компрессия / уровень','Overloud Gem Comp LA'),S('Сатурация / цвет','Overloud Gem Dopamine'),S('Reverb / пространство','Abbey Road Chambers','send')],
 'Мягкая intimate обработка.','GilderComp, Room Service','Сохранять articulation.')

SRC='Full Orchestral Ensemble'
P('orch-min',SRC,'Минимальный orchestral',[
 S('EQ / тон','AMEK EQ 200',settings='Broad ≤1 dB.'),S('Компрессия / уровень','Millennia TCL-2',settings='GR до 1 dB.'),S('Reverb / пространство','Waves IR-1','send')],
 'Минимальная обработка полного ensemble.','SPL Passeq, Pro-R','Не исправлять master-цепью проблемы секций.')
P('orch-cinematic',SRC,'Cinematic glue',[
 S('EQ / тон','Dangerous BAX EQ'),S('Компрессия / уровень','SPL Iron',settings='GR 0.5–1.5 dB.'),S('Сатурация / цвет','Sage Velvet',settings='Очень мало.'),S('Reverb / пространство','Waves H-Reverb','send')],
 'Осторожный cinematic finishing.','Shadow Hills, HG-2','Сохранять crest factor и depth.')
P('orch-dark',SRC,'Dark trailer layer',[
 S('Компрессия / уровень','DUEL LT'),S('Creative FX','Erebos','send')],
 'Специальный layer, не универсальный orchestral preset.','RESTRUKT, CINEFELT','Использовать параллельно с clean ensemble.')

SRC='Samples / Loops'
P('sample-min',SRC,'Чистый sample/loop',[
 S('EQ / тон','FabFilter Pro-Q 3'),S('Компрессия / уровень','Waves MaxxVolume',settings='Только если sample нестабилен: low-level/peak control умеренно, noise не поднимать.'),S('Limiter / clipper','Cactus Clipper',settings='Редкие peaks 0.5–2 dB, oversampling при render.')],
 'Минимальная подготовка sample.','F6, Pro-MB','Сначала проверить tempo, pitch и phase.')
P('sample-lofi',SRC,'Lo-fi sample',[
 S('Сатурация / цвет','Mixtape',settings='Quality/drift/noise умеренно.'),S('EQ / тон','Soundtoys FilterFreak 1'),S('Reverb / пространство','Room Service','send')],
 'Cassette/filtered texture.','J37, CINEFELT','Оставлять возможность вернуть dry sample.')
P('sample-chop',SRC,'Creative chop',[
 S('Creative FX','Unfiltered Audio SpecOps'),S('Delay / echo','Soundtoys PrimalTap','send'),S('Limiter / clipper','Cactus Clipper')],
 'Для resampling и transitions.','BYOME, Crystallizer','Печатать лучшие фрагменты в audio.')

assert len(PRESETS)==99, len(PRESETS)
