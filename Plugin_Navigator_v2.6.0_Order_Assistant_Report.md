# Plugin Navigator 2.6.0 — Улучшение 1: Помощник порядка

Дата: 21.08.2026
Статус: **PASS**

## Что добавлено

### Расставить автоматически

Новая кнопка корректирует routing и порядок без удаления плагинов и без сброса Starting settings.

Правила:

- Instruments → Source;
- Melodyne / Pitch correction → первый Insert;
- Denoise / De-reverb / Cleanup → до основной dynamics;
- Phase / Polarity → до EQ и compression;
- Gate / Expander → до stages, которые могут поднять bleed;
- Amp / Cab / Pedal → до большинства post-EQ и Compressor stages;
- Corrective EQ → до Compressor;
- Rider / Leveler → до основного Compressor;
- Tone EQ → обычно после dynamics;
- Saturation → обычно после основного контроля;
- Modulation / Width → обычно Send или поздний flexible stage;
- Delay / Reverb → отдельные Sends;
- Parallel compression / saturation / Creative FX сохраняются на Parallel A;
- Clipper → перед финальным Limiter;
- Limiter → конец слышимой цепочки;
- Metering / Reference → Monitoring.

### Почему такой порядок

Новая кнопка показывает по каждому этапу:

- номер;
- маршрут;
- роль;
- причину положения;
- тип правила.

Типы:

- `РЕКОМЕНДУЕМЫЙ`;
- `ГИБКИЙ`;
- `ТВОРЧЕСКИЙ`;
- warning;
- technical error.

## Осознанные исключения

Помощник не считает ошибкой:

- Saturation перед Compressor;
- De-esser до Compressor при резком исходнике;
- Character EQ перед Compressor;
- Transient Shaper после Compressor;
- Modulation в Insert, если пользователь осознанно выбрал serial processing;
- несколько одинаковых плагинов с разными задачами.

Такие варианты получают объяснение и требуют level-matched A/B.

## Технические предупреждения

- Melodyne не первый;
- Denoise/De-reverb после Compressor;
- Reverb/Delay в Main Inserts;
- Metering среди audible processors;
- Limiter до последующих слышимых stages;
- processor в Monitoring;
- слишком много плагинов одного семейства;
- заметная инверсия рекомендуемого порядка.

## Интерфейс

Кнопки доступны в простом и экспертном конструкторах:

- `↕ Расставить автоматически`;
- `Объяснить порядок` / `Почему такой порядок`.

Добавлены:

- компактная формула порядка;
- numbered explanation rows;
- цветовые статусы;
- отдельное объяснение параллельных Sends;
- error и creative стили сообщений.

## Проверки

- Melodyne, вручную перемещённый после Pro-Q, определяется как ошибка: PASS;
- Auto-sort возвращает Melodyne первым: PASS;
- Pro-R остаётся на Send: PASS;
- explanation rows строятся для всех routes: PASS;
- Starting settings сохраняются: PASS;
- duplicate instances не удаляются: PASS;
- все 99 curated chains проходят прежний audit: PASS;
- JSDOM UI regression test: PASS;
- Chromium 1920×1080 visual smoke test: PASS;
- deterministic HTML build: PASS.

## Состав программы

- 366 плагинов;
- 68 семейств;
- 33 источника;
- 99 цепочек / 353 шага;
- 27 research sources;
- 350 exact official product pages.

## Контрольные суммы

- HTML: `7e820f9edc988f23cc1aae5f67ef041e6301ee4a234769eaec8ed5a455fdeba1`
- JSON: `86888e65684db73b18e9621ac6ec5f6b9977df7bf34e24248db6196a9f2334e1`
- Windows EXE внутри ZIP: `5038ab0021b367ad39bde90aa9cc15f28d8fc86d9e856b6d2f10acc5966d0ed0`
- Windows ZIP: `c25611e9b17bd4af4c8e988b6ab72631a994f79bac7ab628578b45c335b8136d`
- общий Download ZIP: `1b9d402561d24edcdc22ab253a136c963a115e9db7284d215c86e8e8174d8042`
