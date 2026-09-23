# Plugin Navigator 2.5.7 — аудит описаний всех плагинов

**Статус:** подтверждённые ошибки исправлены в версии 2.6.1. Подробности: `Plugin_Navigator_v2.6.1_Card_Fixes_Report.md`.

Дата: 18.08.2026

## Объём проверки

Автоматически проверены все 366 записей:

- `name`, `developer`, `category`, `family`;
- `kind`, `description`, `note`;
- короткое, полное и звуковое описание;
- Controls и уровень их происхождения;
- официальная ссылка;
- назначения по источникам и упоминания в цепочках;
- дубли, отрицания и фразы, ошибочно перенесённые между продуктами.

Результат структуры:

- пустых описаний: 0;
- уникальных коротких карточек: 366;
- уникальных полных описаний: 366;
- явных дублей исходного `description`: 2 группы;
- family-level Control maps: 38.

Подозрительные записи дополнительно сверены с официальными страницами и руководствами.

## Подтверждённые фактические ошибки

### 1. Soundtoys Sandman Pro — несуществующая запись

В каталоге одновременно находятся:

- `Soundtoys Sandman Pro`;
- `Unfiltered Audio Sandman Pro`.

Sandman Pro является продуктом Unfiltered Audio / Plugin Alliance. Страница Soundtoys из базы возвращает 404, а в официальном каталоге Soundtoys такого продукта нет.

Решение: удалить `Soundtoys Sandman Pro` как ошибочный дубль. Цепочки его не используют.

### 2. Ozone Spectral Denoiser — неверное название и suite

В официальном перечне модулей Ozone 11/12 нет Spectral Denoiser. `Spectral De-noise` относится к iZotope RX.

Текущие ошибки:

- неверное имя `Ozone Spectral Denoiser`;
- неверная ссылка на Ozone;
- неверная подпись «Ozone module»;
- неполная карта Controls.

Решение: переименовать в `iZotope RX Spectral De-noise`, указать RX и подготовить Controls: Learn, Threshold, Reduction, Quality, Artifact Control, Smoothing/Advanced параметры.

### 3. FabFilter Micro — Controls от компрессора

Описание Micro как фильтра верное, но вкладка Controls показывает:

- `Threshold / Ratio-style gain reduction`;
- `Release`;
- `Makeup`.

Это ошибочная компрессорная карта. Micro — однополосный low-pass/high-pass filter с envelope follower, Input/Output Gain и контролем насыщения.

Также неверна ссылка `micro-compressor-plug-in`. Правильная product page: `micro-mini-filter-plug-in`.

### 4. Waves dbx 160 — несуществующий OverEasy Control

В Controls указан `Over Easy / Hard`, а в заметке говорится об OverEasy. Waves dbx 160 моделирует hard-knee VCA compressor и не имеет такого переключателя.

Нужные основные Controls: Input, Threshold, Compression, Output, SC-HP, Mix, Noise и stereo mode.

### 5. H-Reverb — устаревшая 404-ссылка

Ссылка `/plugins/h-reverb` возвращает 404. Правильный URL:

`https://www.waves.com/plugins/h-reverb-hybrid-reverb`

Описание гибридного algorithmic/convolution/FIR-подхода в целом допустимо, но стоит явно назвать FIR engine и не смешивать его с cabinet IR.

## Ошибочные или вводящие в заблуждение Controls

### 6. Стерео-утилиты получили Controls модуляции

У следующих продуктов ошибочно показаны `Rate`, `Depth`, `Delay / Detune`, `Feedback`:

- `bx_control V2`;
- `bx_solo`;
- `The Util`;
- `Waves Center`;
- `Waves MS Matrix`;
- `Waves S1 Stereo Imager`.

Это разные stereo/M/S utilities, а не chorus/flanger.

Особенно явно неверна карта `The Util`. Официально он содержит Gain, Stereo Width, Phase Inversion, Pan и Bass Control / mono bass.

### 7. Session Inspector описан как insert/monitor utility

Session Inspector — не VST-плагин. Это отдельное HTML-приложение для macOS Safari, которое читает данные сессии без открытия DAW.

Текущая карточка не подчёркивает достаточно явно:

- только Mac/Safari;
- не загружается как insert;
- не является metering-плагином;
- generic Controls `Reference Level`, `Target`, `Codec`, `Bypass` к нему не относятся.

### 8. Ozone Vintage Compressor — неточная карта

Официально это feedback compressor с режимами Sharp, Balanced и Smooth, Detection Filter, Threshold, Ratio, Attack, Release, Gain и Auto Gain.

Текущая карта содержит объединённый `Mode / Mix`, хотя Mix не указан среди Controls модуля, и пропускает Detection Filter и три конкретных режима.

### 9. Chakra — слишком общий текст и неверные family Controls

Короткая карточка почти не отражает особенности продукта. Официально Chakra использует три настроенных harmonic colors, Tone EQ, THD/Input, Mix, Output Link, Delta и Bass/width логику.

Текущая family-map содержит `Bias / Flux / Speed`, что относится скорее к tape processing и не описывает Chakra.

### 10. Ultimate Snare — generic channel-strip Controls

Официальные основные секции:

- Heat;
- Body;
- Crack;
- Air;
- Punch;
- Plate;
- Bomb.

Текущие `Input / Preamp`, `HPF / LPF`, `EQ`, `Dynamics`, `Saturation / Character` слишком общие и не помогают работать с продуктом.

### 11. Mixing Cheat Sheet и Portable Mono Speaker Check

Их основные описания верны, но generic metering Controls не соответствуют реальному интерфейсу.

- Mixing Cheat Sheet: Frequency Map, frequency solo, instrument pages и guidance.
- Portable Mono Speaker Check: Bluetooth speaker mode, Pink Noise и level-matched reference workflow.

## Системная проблема происхождения Controls

### 12. Product-specific пометка завышена

154 карты помечены как `Product-specific curated map`, однако:

- 40 amp/bass suites используют одну и ту же карту;
- 7 Brainworx console strips используют одну общую карту;
- некоторые карты содержат модули, которых нет в конкретном продукте.

Например, общая amp-map утверждает наличие Noise Gate, Compressor, Delay/Reverb и Cab/IR у всех 40 продуктов. Это неверно для части отдельных amp-моделей и DI-плагинов.

До индивидуальной сверки эти карты правильнее пометить как `Product-informed curated map`.

## Проблемы качества текста без грубой фактической ошибки

### 13. Слишком общие короткие карточки

У 75 записей короткий текст почти не использует product-specific исходное описание. Чаще всего это:

- Waves signature macros;
- amp suites;
- channel strips;
- некоторые AudioLoom products;
- сложные multi-effects.

Текст не обязательно ложный, но пользователь не понимает, чем конкретный продукт отличается от семейства.

Примеры:

- Chakra;
- Ultimate Snare;
- Abbey Road TG Mastering Chain;
- Busboy;
- CLA Vocals;
- Archetype: Rabea;
- Smashburger Compressor.

### 14. Смешение русского и английского без первого объяснения

В ряде карточек используются слова `glue`, `forward`, `polished`, `density`, `character`, `workflow`, `translation` без короткого русского пояснения.

Для новичка лучше при первом упоминании давать перевод.

### 15. Session/source назначения требуют отдельной проверки

Есть назначения, которые возможны творчески, но выглядят нетипично:

- guitar macro на strings/brass;
- bass processor на synth lead;
- guitar amp на Bass Guitar;
- standalone Session Inspector в Monitoring lane.

Они не всегда являются ошибкой, но должны быть помечены как creative/conditional, а не как обычная рекомендация.

## Что уже проверено и выглядит корректно

- Melodyne и его порядок до основной обработки;
- LoAir как subharmonic generator;
- MaxxBass/RBass как psychoacoustic bass enhancers;
- Gem Dopamine как tape encoder enhancer, а не transient shaper;
- PuigTec MEQ-5 как midrange EQ;
- Renaissance Vox как vocal leveler/compressor/gate;
- Waves Torque как drum resonance pitch processor;
- Pro-Q 4 и его EQ Sketch / Spectral Dynamics;
- ADPTR Sculpt и Ozone Spectral Shaper не смешиваются с Pro-Q 4;
- H-Reverb не описывается как cabinet IR;
- основные descriptions AudioLoom: The Util, Chakra, Ultimate Snare, Mixing Cheat Sheet, Portable Mono Speaker Check и Session Inspector.

## Приоритет исправления

### Критично

1. удалить `Soundtoys Sandman Pro`;
2. исправить `Ozone Spectral Denoiser` на RX Spectral De-noise;
3. исправить FabFilter Micro Controls и ссылку;
4. убрать OverEasy из dbx 160;
5. исправить 404-ссылку H-Reverb.

### Высокий приоритет

6. исправить шесть stereo/M/S utility maps;
7. исправить Session Inspector;
8. исправить Ozone Vintage Compressor;
9. сделать точные карты Chakra и Ultimate Snare.

### Плановый аудит

10. понизить generic amp/console maps до Product-informed;
11. постепенно индивидуализировать 38 family-level карт;
12. сделать короткие карточки менее шаблонными.

## Источники сверки

- iZotope Ozone 12 modules: `https://docs.izotope.com/ozone12/en/getting-started.html`
- iZotope RX Spectral De-noise: `https://docs.izotope.com/rx11/en/spectral-de-noise.html`
- FabFilter Micro: `https://www.fabfilter.com/products/micro-mini-filter-plug-in`
- Waves dbx 160 manual: `https://assets.wavescdn.com/pdf/plugins/dbx-160.pdf`
- Waves H-Reverb: `https://www.waves.com/plugins/h-reverb-hybrid-reverb`
- Waves S1: `https://www.waves.com/plugins/s1-stereo-imager`
- The Util: `https://www.audioloom.com/cr8ive-audio/the-util`
- Session Inspector: `https://www.audioloom.com/smartaudiosolution/session-inspector`
- Chakra: `https://www.audioloom.com/styx-audio/chakra`
- Ultimate Snare: `https://www.audioloom.com/the-ultimate-production/ultimate-snare`
- Mixing Cheat Sheet: `https://www.audioloom.com/carve-audio/mixing-cheat-sheet`
- Portable Mono Speaker Check: `https://www.audioloom.com/styx-audio/portable-mono-speaker-check`
