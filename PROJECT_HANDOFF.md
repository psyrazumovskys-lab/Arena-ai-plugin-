# Plugin Navigator — текущее состояние проекта

**Дата:** 21 августа 2026
**Актуальная версия:** **2.6.0**
**Язык приложения и общения:** русский

## Инструкция следующему агенту

1. Считать этот файл и актуальные исходники источником текущего состояния.
2. Не менять интерфейс, базу, иконку или готовые цепочки без прямой команды пользователя.
3. Сохранять автономную офлайн-работу HTML и Windows-версии.
4. Объяснения писать по-русски, сохраняя оригинальные английские названия Controls.
5. Не выдавать family-level данные за точные элементы конкретного GUI/manual.

## Текущее состояние

- 366 плагинов;
- 68 смысловых семейств;
- 33 типа источников;
- 99 curated chains / 353 шага;
- 350 exact official product pages;
- 16 vendor hubs без выдуманных dedicated URL;
- 154 product-specific, 174 product-informed и 38 family-level Control maps;
- простой и экспертный режимы;
- быстрые и подробные карточки;
- Controls, Settings, Routing и сравнение;
- пользовательские цепочки, избранное и заметки;
- чеклист подготовки сессии;
- резервная копия и проверяемое восстановление пользовательских данных;
- поиск по карточкам, Controls, настройкам и аналогам;
- фильтр по производителю;
- Помощник порядка: auto-sort, explanations, warnings и creative exceptions;
- полностью автономный HTML;
- portable Windows x64 без Trial и ограничений.

Активной незавершённой задачи нет.

## Изменения 2.6.0

- Реализовано «Улучшение 1 — Помощник порядка плагинов» без ИИ и интернета.
- Добавлены кнопки «Расставить автоматически» и «Почему такой порядок».
- Pitch/timing correction ставится первой; cleanup/phase/gate — до основной dynamics.
- Amp/Cab располагается до post-EQ и большинства compressor stages.
- Delay/Reverb/типичная modulation направляются в Sends; meters/references — в Monitoring.
- Clipper/Limiter располагаются ближе к концу audible chain.
- Parallel compression/saturation сохраняются как отдельные Parallel returns.
- Различаются recommended, flexible, creative, warning и technical error.
- Автосортировка не удаляет плагины и не сбрасывает Starting settings.
- Добавлен подробный раздел в HTML/Markdown инструкции и новые UI regression tests.

## Финальные файлы

### Общий архив

- `Plugin_Navigator_v2.6.0_Download.zip`;
- содержит HTML, Windows x64, README, инструкцию в HTML/Markdown и checksums;
- SHA-256: `1b9d402561d24edcdc22ab253a136c963a115e9db7284d215c86e8e8174d8042`.

### Инструкция пользователя

- `Plugin_Navigator_User_Guide_RU.html` — автономная HTML-инструкция с оглавлением;
- SHA-256: `6bbfcb6886b7a06b1135453b8223a88df6a3308d89006c4b3fca805d8b190cd5`;
- `Plugin_Navigator_User_Guide_RU.md` — исходный текст;
- SHA-256: `3aac37cb0cfafcf69b9f09b3ae17943f4b21e2020a1f40d23120ad57070a51f4`.

### HTML

- `Plugin_Navigator_Full.html`
- `Plugin_Navigator_Full_v2.6.0.html`
- размер: 10 019 182 байта;
- SHA-256: `7e820f9edc988f23cc1aae5f67ef041e6301ee4a234769eaec8ed5a455fdeba1`;
- файлы и `Plugin_Navigator_Windows_Source/resources/index.html` побайтно совпадают.

### Windows x64

`Plugin_Navigator_Full_v2.6.0_Windows_x64.zip`

- ZIP SHA-256: `c25611e9b17bd4af4c8e988b6ab72631a994f79bac7ab628578b45c335b8136d`;
- EXE SHA-256: `5038ab0021b367ad39bde90aa9cc15f28d8fc86d9e856b6d2f10acc5966d0ed0`;
- Neutralinojs 6.9.0;
- Windows 10/11 x64;
- требуется Microsoft Edge WebView2 Runtime;
- цифровой подписи нет;
- HTML внутри EXE побайтно совпадает с HTML 2.6.0.

## Сборка и тесты

Установка зависимостей:

```bash
python3 -m pip install -r requirements.txt
cd test-runtime && npm ci && cd ..
```

HTML и все основные тесты:

```bash
python3 build_and_test.py
```

Опциональная проверка реальной вёрстки:

```bash
cd test-runtime
npx playwright install chromium
npm run test:browser
```

Windows:

```bash
cd Plugin_Navigator_Windows_Source && npm ci && cd ..
python3 build_windows.py
```

`build_windows.py` собирает ASAR, обновляет Windows VERSIONINFO, встраивает ресурс через postject, извлекает встроенный HTML для сравнения и формирует ZIP/checksums.

## Основные исходники

| Файл | Назначение |
|---|---|
| `plugin_usage_semantic_hybrid_corrected.xlsx` | Главная исходная таблица |
| `build_plugin_navigator.py` | Детерминированный генератор HTML и JSON |
| `plugin_guide_enrichment.py` | Карточки, Controls и настройки |
| `official_plugin_references.py` | Официальные источники и provenance |
| `official_product_pages.py` | Точные official product pages |
| `product_control_maps.py` | Product-specific Control maps |
| `curated_chain_presets.py` | 99 подготовленных цепочек |
| `chain_research_audit.py` | Аудит и обогащение цепочек |
| `build_and_test.py` | Единый запуск сборки и тестов |
| `build_windows.py` | Воспроизводимая Windows-сборка |
| `Plugin_Navigator_Windows_Source/` | Neutralino-конфигурация и Node-инструменты |

## Постоянные требования пользователя

- Сохранять максимальное количество валидных плагинов.
- Все AudioLoom-плагины должны оставаться включены, но не выделяться в отдельную экосистему.
- Использовать семантическую группировку.
- Для каждой карточки нужны простой и подробный режимы.
- Приложение должно оставаться автономным и офлайн.
- Конструктор должен быть понятным и предлагать готовые цепочки.
- Этапы цепочки делятся на базовые, условные, творческие и monitoring.
- Различать официальную информацию, практические рекомендации и family-level normalization.
- Иконку Windows, favicon и app icon без команды не менять.
- Windows-версия остаётся полной и без ограничений.

## Не реализовано

Lite/Trial/Pro, лицензирование, ключи и платный доступ не реализованы. Коммерческой подписи Windows нет. Исторические HTML/ZIP пока остаются в репозитории; перенос старых выпусков в GitHub Releases можно выполнить отдельной задачей.
