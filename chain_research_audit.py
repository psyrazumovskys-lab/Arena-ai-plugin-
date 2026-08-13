"""Web-research audit metadata and conservative routing normalization for chains.

The URLs are authoritative educational material from manufacturers and
Sound On Sound. The app embeds the principles and links for offline reference;
settings remain starting points that must be auditioned on the user's audio.
"""
from collections import defaultdict

RESEARCH_SOURCES = [
    {'id':'signal-order','title':'Signal chain: order of operations','publisher':'iZotope','url':'https://www.izotope.com/community/blog/signal-chain-order-of-operations','principle':'Plugin order changes the result. Corrective EQ before compression is conventional, but the best order depends on the source and purpose.'},
    {'id':'eq-compression','title':'Which Comes First: EQ or Compressor?','publisher':'iZotope','url':'https://www.izotope.com/en/learn/eq-before-or-after-compression.html','principle':'Technical cleanup EQ before compression prevents unwanted energy from driving the detector; creative EQ may follow compression.'},
    {'id':'send-return','title':'How To Use Reverb Like A Pro: 1','publisher':'Sound On Sound','url':'https://www.soundonsound.com/techniques/how-use-reverb-pro-1','principle':'Shared reverb/delay normally uses a post-fader send and a 100% wet return.'},
    {'id':'send-routing','title':'Using Aux Sends & Returns','publisher':'Sound On Sound','url':'https://www.soundonsound.com/techniques/using-aux-sends-returns','principle':'Aux returns allow independent filtering and processing; parallel compression blends a heavily processed return with the dry signal.'},
    {'id':'reverb-filter','title':'How To Optimise Your Reverb Treatments','publisher':'Sound On Sound','url':'https://www.soundonsound.com/techniques/how-optimise-your-reverb-treatments','principle':'Filter reverb returns to reduce low/low-mid mud; ducking and de-essing can preserve clarity.'},
    {'id':'compression-controls','title':'Basic compressor controls','publisher':'FabFilter','url':'https://www.fabfilter.com/learn/compression/basic-compressor-controls','principle':'Attack and release must follow the transient and groove; too-fast attack removes impact and too-slow release may not recover.'},
    {'id':'sidechain','title':'Side chain compression','publisher':'FabFilter','url':'https://www.fabfilter.com/learn/compression/side-chain-compression','principle':'Kick-triggered bass ducking is valid; detector filtering improves targeting, while overly fast processing can distort bass-rich signals.'},
    {'id':'kick-bass','title':'How to Mix Kick and Bass to Perfection','publisher':'Waves','url':'https://www.waves.com/how-to-mix-kick-bass-perfection','principle':'Balance and tuning come first; use complementary EQ, restrained sidechain compression, saturation for translation, and low-end referencing.'},
    {'id':'kick-808','title':'Mix 808 and Kick Like a Hip Hop Pro','publisher':'Waves','url':'https://www.waves.com/mix-808-and-kick-like-a-pro','principle':'Assign kick and 808 distinct roles; frequency-selective external sidechain can duck only the conflicting 808 band.'},
    {'id':'drum-compression','title':'Ultimate Drum Compression Guide','publisher':'iZotope','url':'https://www.izotope.com/en/learn/drum-compression.html','principle':'Compression is optional on revealing overheads, room crush is a character choice, and parallel compression can add punch while retaining dry transients.'},
    {'id':'drum-phase','title':'2 Approaches to Mixing Live Drums','publisher':'iZotope','url':'https://izotope.com/en/learn/2-approaches-to-mixing-live-drums','principle':'Check polarity/phase relationships before detailed processing; judge spot mics, overheads and rooms as one kit.'},
    {'id':'parallel','title':'6 parallel compression mistakes in mixing','publisher':'iZotope','url':'https://www.izotope.com/en/learn/parallel-compression-mistakes','principle':'Parallel processing must be level-matched and checked for phase/timing, unwanted frequency reinforcement and groove changes.'},
    {'id':'vocal-chain','title':'Crafting a basic vocal chain','publisher':'iZotope','url':'https://www.izotope.com/en/learn/crafting-a-basic-vocal-chain','principle':'A conservative vocal path uses corrective EQ, compression, de-essing as needed, then delay/reverb; order remains source-dependent.'},
    {'id':'vocal-reverb','title':'Essential tips for using reverb on vocals','publisher':'iZotope','url':'https://izotope.com/en/learn/essential-tips-for-using-reverb-on-vocals','principle':'Use a 100% wet aux, choose pre-delay/decay for clarity and tempo, and EQ frequencies that mask the dry vocal.'},
    {'id':'backing-vocals','title':'How to produce background vocals that complement a lead','publisher':'iZotope','url':'https://www.izotope.com/en/learn/background-vocals.html','principle':'De-ess stacked vocals, unmask the lead, use panning/depth effects, and compress the background group only as much as its role needs.'},
    {'id':'guitar','title':'Understanding guitar compression: a beginner’s guide','publisher':'iZotope','url':'https://www.izotope.com/en/learn/guitar-compression','principle':'A useful starting order is subtractive EQ, compression, then creative tone shaping; exceptions should be chosen by listening.'},
    {'id':'piano','title':'How to mix piano','publisher':'iZotope','url':'https://izotope.com/en/learn/how-to-mix-piano','principle':'Use broad EQ and as little processing as possible; align multi-mic recordings and compress subtly.'},
    {'id':'acoustic-eq','title':'Choosing the right EQ for your mix','publisher':'iZotope','url':'https://izotope.com/en/learn/choosing-the-right-eq','principle':'Acoustic guitars, pianos and strings expose over-EQ easily, so subtle broad moves are safer than aggressive surgery.'},
    {'id':'pads','title':'5 Tips for Mixing Pads','publisher':'iZotope','url':'https://www.izotope.com/en/learn/5-tips-for-mixing-pads','principle':'Pads often arrive too wide and wet; remove low-end buildup from both source and effects and narrow when clarity requires it.'},
    {'id':'podcast','title':'How to Edit Podcasts','publisher':'iZotope','url':'https://www.izotope.com/community/blog/how-to-edit-podcasts','principle':'Repair noise first, then apply corrective/dynamic EQ, de-essing and compression; final loudness processing follows track cleanup.'},
    {'id':'orchestral','title':'How do I compress my orchestral recordings?','publisher':'Sound On Sound','url':'https://www.soundonsound.com/sound-advice/q-how-do-compress-my-orchestral-recordings','principle':'Preserve orchestral dynamics; use automation or very gentle compression and avoid pumping.'},
    {'id':'orchestral-samples','title':'How should I treat my sample-library orchestral parts?','publisher':'Sound On Sound','url':'https://www.soundonsound.com/sound-advice/q-how-should-treat-my-sample-library-orchestral-parts','principle':'Sample-library parts may need contextual EQ/compression, and filtered shared reverb can reduce clutter.'},
    {'id':'mix-bus','title':'Essential tips for mix bus processing','publisher':'iZotope','url':'https://www.izotope.com/en/learn/tips-for-mix-bus-processing','principle':'EQ, compression and saturation are typical but should be subtle; do not rely on a limiter to repair mix peaks.'},
    {'id':'mix-bus-compression','title':'Mix Bus Compression 101','publisher':'iZotope','url':'https://www.izotope.com/community/blog/mix-bus-compression','principle':'Use conservative ratio and gain reduction, time release to the track, consider sidechain HPF, and always level-match.'},
    {'id':'mastering','title':'What is an ideal mastering signal chain?','publisher':'iZotope','url':'https://www.izotope.com/en/learn/what-is-an-ideal-mastering-signal-chain.html','principle':'Listen and plan first, perform corrective work before sweetening as needed, and use the fewest stages that solve the problem.'},
    {'id':'limiter','title':'Getting to know brickwall limiters','publisher':'iZotope','url':'https://www.izotope.com/community/blog/brickwall-limiters','principle':'A brickwall limiter normally ends mastering processing; True Peak is a delivery-dependent choice and limiting should be judged for transient damage.'},
]


def _source_keys(source):
    s=source.casefold()
    keys=[]
    if any(x in s for x in ['kick','bass','808','sub']): keys += ['kick-bass','sidechain']
    if '808' in s or 'sub bass' in s: keys += ['kick-808']
    if any(x in s for x in ['kick','snare','tom','drum','overhead','room microphone','hi-hat','cymbal','percussion']): keys += ['drum-phase','drum-compression']
    if 'lead vocal' in s: keys += ['vocal-chain','vocal-reverb']
    if 'backing' in s or 'vocal bus' in s: keys += ['backing-vocals','vocal-chain']
    if any(x in s for x in ['speech','podcast','dialog']): keys += ['podcast']
    if 'guitar' in s: keys += ['guitar']
    if 'piano' in s: keys += ['piano','acoustic-eq']
    if any(x in s for x in ['strings','brass','woodwind','orchestral']): keys += ['orchestral','orchestral-samples','acoustic-eq']
    if any(x in s for x in ['pad','synth','keys']): keys += ['pads']
    if any(x in s for x in ['bus','stem']): keys += ['mix-bus','mix-bus-compression']
    if any(x in s for x in ['premaster','mastering']): keys += ['mastering','limiter']
    return keys


STEP_GUIDANCE = {
    'Очистка / repair': ('Удаляет или ослабляет конкретную проблему записи до того, как её усилят следующие stages.', 'Слышны noise, room, breaths, sibilance или harshness.', 'Исходник уже чистый либо появляются lisp, watery/metallic artifacts и потеря деталей.', 'Паузы, согласные, атака и естественная ambience.'),
    'Фаза / стерео': ('Согласует polarity/time/phase нескольких microphones или layers и проверяет устойчивость stereo.', 'Есть несколько mic/layers одного события либо слышна cancellation.', 'Один чистый mono source или изменение не улучшает body/transient в mono.', 'Фундамент, центр, transient и mono correlation.'),
    'Gate / expander': ('Ослабляет bleed, noise и слишком длинный хвост между полезными событиями.', 'Close mic содержит bleed/noise либо хвост мешает groove.', 'Чистый sample, полезная room ambience или пропадают тихие удары/ghost notes.', 'Начало удара, тихие события, sustain и chatter на закрытии.'),
    'EQ / тон': ('Исправляет слышимый частотный конфликт или задаёт аккуратный tonal balance.', 'Есть rumble, resonance, masking или осознанная tonal-задача.', 'Коррекция основана только на analyzer либо source уже занимает нужное место.', 'Тон в полном миксе, headroom и реакция следующего compressor.'),
    'Channel strip / macro': ('Объединяет несколько базовых stages для быстрого связного результата.', 'Нужен быстрый workflow и понятна задача каждого включённого module.', 'Отдельные проблемы требуют точного repair либо macro дублирует уже работающие stages.', 'Input, вклад каждого module и Output при level-matched bypass.'),
    'Компрессия / уровень': ('Контролирует envelope/уровень либо добавляет punch, density или glue.', 'Динамика нестабильна или нужен определённый envelope/character.', 'Уровень уже стабилен либо compression уменьшает punch, groove и natural dynamics.', 'Gain reduction, transient, recovery до следующего события и breaths/noise.'),
    'Транзиенты': ('Меняет соотношение attack и sustain без обязательного broadband compression.', 'Нужно больше/меньше attack, body, room или длины хвоста.', 'Envelope уже правильная либо усиливаются click, bleed и sub.', 'Peak level, attack, body и хвост в полном миксе.'),
    'Низ / фундамент': ('Фокусирует fundamental или добавляет слышимые harmonics для переводимости.', 'Низу не хватает определённости после balance и phase-check.', 'Проблема вызвана arrangement/phase либо растут mud и headroom demand.', 'Нота, kick/bass separation, mono и маленькие speakers.'),
    'Сатурация / цвет': ('Добавляет harmonics, density, мягкое peak rounding или выраженный характер.', 'Нужны color, presence или переводимость на небольших системах.', 'Source уже достаточно плотный либо накапливаются harshness и low-mid mud.', 'Output-matched tone, transient, sibilance и low end.'),
    'Amp / cabinet / pedal': ('Формирует amp/cab/pedal tone и основную артикуляцию DI-сигнала.', 'Исходник является DI или нужен намеренный amp character.', 'Уже записан законченный amp tone либо stage дублирует другой rig.', 'Input calibration, gain, cab/IR, fizz и конфликт с bass/vocal.'),
    'Модуляция / ширина': ('Добавляет движение, doubling или stereo width через time/pitch/level различия.', 'Нужна ширина или движение и dry center остаётся устойчивым.', 'Mono теряет источник, correlation ухудшается или low end становится нестабильным.', 'Центр, mono compatibility, low band и perceived level.'),
    'Delay / echo': ('Создаёт slap, rhythmic repeats, depth или автоматизированные throws.', 'Аранжировке нужны repeats/depth, которые не закрывают новые события.', 'Delay размывает groove, diction или заполняет ненужные паузы.', 'Feedback peaks, tempo, фильтрация return и окончания фраз.'),
    'Reverb / пространство': ('Создаёт перспективу, общий room или характерный хвост на отдельном return.', 'Источнику нужна глубина/связь с пространством.', 'Запись уже содержит нужную ambience либо теряется clarity.', 'Pre-delay, decay, mud, diction и переходы аккордов.'),
    'Creative FX': ('Создаёт отдельную слышимую трансформацию, texture или transition.', 'Creative-результат является частью аранжировки и сохранён dry source.', 'Эффект отвлекает, непредсказуем по level или не переживает mono/render.', 'Feedback, peaks, repeatability и место эффекта в arrangement.'),
    'Limiter / clipper': ('Срезает редкие пики или задаёт финальный delivery ceiling.', 'Пики мешают headroom либо это последняя mastering stage.', 'Используется вместо исправления balance/dynamics или заметно портит transient.', 'Снятый сигнал/delta, cymbals, consonants, snare и True Peak.'),
    'Контроль / анализ': ('Проверяет loudness, peaks, spectrum, stereo и references без изменения export.', 'Нужна техническая или сравнительная проверка.', 'Никогда не пропускать финальную проверку, но monitoring processors не печатать.', 'LUFS, True Peak, mono, correlation и level-matched references.'),
}


def _step_meta(chain, step):
    purpose,condition,skip,listen=STEP_GUIDANCE.get(step['task'],('Выполняет указанную задачу обработки.','Есть слышимая задача.','Stage не улучшает материал.','Сравнение в контексте.'))
    goal=(chain.get('style','')+' '+chain.get('goal','')).casefold()
    creative_chain=any(x in goal for x in ['creative','character','dark','lo-fi','ambient','crush','cinematic'])
    conditional_tasks={'Очистка / repair','Фаза / стерео','Gate / expander','Транзиенты','Низ / фундамент','Модуляция / ширина','Delay / echo','Reverb / пространство','Creative FX'}
    if step['lane']=='monitor': necessity,label='monitor','MONITORING — НЕ EXPORT'
    elif creative_chain and step['task'] in {'Сатурация / цвет','Модуляция / ширина','Delay / echo','Reverb / пространство','Creative FX'}: necessity,label='creative','CREATIVE — ПРОСЛУШАТЬ'
    elif step['task'] in conditional_tasks or (step['task']=='Limiter / clipper' and chain['source']!='Premaster / Mastering'):
        necessity,label='conditional','ЕСЛИ ТРЕБУЕТСЯ'
    else: necessity,label='start','БАЗОВЫЙ СТАРТ — НЕ ОБЯЗАТЕЛЬНО'
    if step['task']=='Limiter / clipper' and chain['source']=='Premaster / Mastering':
        audible=[x for x in chain['steps'] if x['lane']!='monitor']
        if audible and step is audible[-1]: necessity,label='start','ФИНАЛЬНАЯ LIMITER-STAGE'
        else: necessity,label='conditional','ЕСЛИ ТРЕБУЕТСЯ — PEAK SHAPING'
    return {'necessity':necessity,'necessityLabel':label,'purpose':purpose,'condition':condition,'skipWhen':skip,'listenFor':listen,'how':step.get('settings','')}


def _preflight(chain):
    s=chain['source'].casefold();items=['Сначала выставить balance/Input и сформулировать одну слышимую задачу для каждого stage.']
    if any(x in s for x in ['kick','snare','tom','overhead','room microphone','drum']):
        items.append('Если используются несколько microphones/layers, проверить polarity, time alignment и mono до Gate/EQ/Compression.')
    if any(x in s for x in ['bass','808','sub']): items.append('Проверить роль kick и bass, tuning/phase и headroom до sidechain или усиления sub.')
    if any(x in s for x in ['vocal','speech','podcast','dialog']): items.append('Сделать clip gain/editing и убрать явные clicks/noise до dynamics; оставить естественные breaths по задаче.')
    if any(x in s for x in ['piano','acoustic','strings','brass','woodwind','orchestral']): items.append('Сначала оценить естественную динамику и перспективу; broad/subtle moves предпочтительнее обработки по analyzer.')
    if chain['source']=='Mix Bus / Stereo Bus': items.append('Собрать статический mix и headroom до bus processing; сохранить clean pre-master без peak trim.')
    if chain['source']=='Premaster / Mastering': items.append('Сначала прослушать весь mix, сделать notes и определить delivery; limiter оставить последней слышимой stage.')
    return items


def _rebuild_route(chain):
    parts=[]
    source_steps=[s['name'] for s in chain['steps'] if s['lane']=='source']
    inserts=[s['name'] for s in chain['steps'] if s['lane']=='insert']
    monitors=[s['name'] for s in chain['steps'] if s['lane']=='monitor']
    if source_steps: parts.append('Source: '+' → '.join(source_steps))
    if inserts: parts.append('Inserts: '+' → '.join(inserts))
    buses=defaultdict(list)
    order=[]
    for step in chain['steps']:
        if step['lane']!='send': continue
        bus=step.get('bus') or 'Send A'
        if bus not in buses: order.append(bus)
        buses[bus].append(step['name'])
    for bus in order: parts.append(bus+': '+' → '.join(buses[bus]))
    if monitors: parts.append('Monitoring: '+' → '.join(monitors))
    chain['chain']=' | '.join(parts)


def audit_chains(chains):
    source_ids={x['id'] for x in RESEARCH_SOURCES}
    for chain in chains:
        changes=[]
        goal=(chain.get('style','')+' '+chain.get('goal','')).casefold()
        sends=[s for s in chain['steps'] if s['lane']=='send']
        parallel='parallel' in goal
        if parallel and sends:
            for step in sends:
                if step.get('bus')!='Parallel A': changes.append('Parallel processors grouped into one serial return.')
                step['bus']='Parallel A'
                if 'parallel return' not in step.get('settings','').casefold():
                    step['settings']=(step.get('settings','').rstrip(' .')+'; serial stage on the same Parallel A return.').strip('; ')
        else:
            send_n=0
            for step in sends:
                send_n+=1;step['bus']=f'Send {chr(64+send_n)}'

        for step in chain['steps']:
            text=step.get('settings','')
            low=text.casefold()
            if step['lane']=='send' and step['task'] in {'Delay / echo','Reverb / пространство'}:
                additions=[]
                if '100% wet' not in low: additions.append('return 100% wet')
                if 'post-fader' not in low: additions.append('обычно post-fader send')
                if additions:
                    step['settings']=text.rstrip(' .')+'; '+', '.join(additions)+'.';changes.append('Time effect routing normalized to post-fader/100% wet.')
            if step['lane']=='monitor' and 'не экспорт' not in low:
                step['settings']=text.rstrip(' .')+'; Monitoring после final processing, не экспортировать.';changes.append('Monitoring exclusion from export made explicit.')
            if step['task']=='Фаза / стерео' and 'только' not in low and 'несколь' not in low:
                step['settings']=text.rstrip(' .')+'; применять только при нескольких mic/layers и подтвердить в mono.';changes.append('Phase stage made conditional.')
        if chain['source']=='Mix Bus / Stereo Bus':
            for step in chain['steps']:
                if step['task']=='Limiter / clipper' and 'optional' not in step['settings'].casefold() and 'не замен' not in step['settings'].casefold():
                    step['settings']=step['settings'].rstrip(' .')+'; optional peak trim, сохранить clean pre-master с headroom.';changes.append('Mix-bus clipping marked optional.')

        keys=['signal-order','eq-compression','compression-controls']+_source_keys(chain['source'])
        if sends: keys += ['send-return','send-routing','reverb-filter']
        if parallel: keys += ['parallel']
        if any('sidechain' in s.get('settings','').casefold() or s.get('sidechain') for s in chain['steps']): keys += ['sidechain']
        keys=list(dict.fromkeys(k for k in keys if k in source_ids))

        checks=['Удалить любой stage, который не решает слышимую задачу; сравнивать при одинаковом уровне.']
        if sends: checks.append('Проверить wet return отдельно: фильтры, peak level, post-fader behavior и 100% wet для delay/reverb.')
        if parallel: checks.append('Проверить delay compensation/phase и не принимать прибавку громкости за улучшение.')
        if any(x in chain['source'].casefold() for x in ['kick','bass','808','sub']): checks.append('Сначала balance/tuning/phase, затем EQ или sidechain; проверить low end в mono и на маленькой системе.')
        if any(x in chain['source'].casefold() for x in ['vocal','speech','podcast','dialog']): checks.append('Проверить breaths, sibilance и intelligibility после compression и bright EQ.')
        if any(x in chain['source'].casefold() for x in ['orchestral','strings','brass','woodwind','piano','acoustic']): checks.append('Сохранить natural dynamics и timbre; broad/subtle processing предпочтительнее обработки по анализатору.')
        if chain['source']=='Mix Bus / Stereo Bus': checks.append('Не использовать clipper/limiter как замену исправлению peaks внутри mix; сохранить clean pre-master.')
        if chain['source']=='Premaster / Mastering': checks.append('Limiter должен завершать слышимую processing-chain; meters/references находятся только после него в Monitoring.')

        chain['preflight']=_preflight(chain)
        for step in chain['steps']:
            meta=_step_meta(chain,step)
            if len(step.get('settings','').strip())<70:
                base=step.get('settings','').rstrip(' .')
                step['settings']=f"{base}. Контроль: {meta['listenFor']} Пропустить/ослабить, если: {meta['skipWhen']}"
                meta['how']=step['settings']
            step.update(meta)
        creative=any(x in goal for x in ['creative','character','dark','lo-fi','ambient','crush','cinematic'])
        chain['webAudit']={
            'status':'WEB-RESEARCH AUDITED · 12.08.2026',
            'risk':'Creative / audition essential' if creative else 'Conservative starting point',
            'summary':'Порядок, routing и стартовые диапазоны сверены с рекомендациями iZotope, FabFilter, Waves и Sound On Sound.',
            'sourceKeys':keys,
            'checks':checks,
            'normalizations':list(dict.fromkeys(changes)),
        }
        _rebuild_route(chain)

    # Hard validation after normalization.
    for chain in chains:
        assert chain.get('webAudit') and chain['webAudit']['sourceKeys'], chain['id']
        assert all(s.get('settings','').strip() for s in chain['steps']), (chain['id'],'empty settings')
        assert chain.get('preflight')
        assert all(all(s.get(k) for k in ('necessity','necessityLabel','purpose','condition','skipWhen','listenFor','how')) for s in chain['steps']), chain['id']
        for step in chain['steps']:
            if step['lane']=='send' and step['task'] in {'Delay / echo','Reverb / пространство'}:
                assert '100% wet' in step['settings'], (chain['id'],step['name'])
            if step['lane']=='monitor':
                assert 'не экспорт' in step['settings'].casefold(), (chain['id'],step['name'])
        if chain['source']=='Premaster / Mastering':
            audible=[s for s in chain['steps'] if s['lane']!='monitor']
            assert audible[-1]['task']=='Limiter / clipper', chain['id']
    return chains
