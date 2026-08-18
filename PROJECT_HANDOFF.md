# Plugin Navigator — текущее состояние проекта

**Дата:** 15 августа 2026
**Актуальная версия:** **2.5.7**
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
- полностью автономный HTML;
- portable Windows x64 без Trial и ограничений.

Активной незавершённой задачи нет.

## Изменения 2.5.7

- Исправлена Windows-упаковка: предыдущий EXE открывал стандартную страницу Neutralinojs вместо приложения.
- `resources.neu` теперь содержит обязательный `neutralino.config.json` в корне архива.
- HTML упакован по правильному пути `/resources/index.html`, соответствующему `documentRoot: /resources/`.
- Проверка Windows-сборки извлекает и валидирует и конфигурацию, и HTML до создания ZIP.
- Сохранены Celemony Melodyne, 366 плагинов, 99 цепочек и все улучшения 2.5.6.
- Windows FileVersion/ProductVersion соответствует 2.5.7.0.

## Финальные файлы

### Общий архив

- `Plugin_Navigator_v2.5.7_Download.zip`;
- содержит HTML, Windows x64, README, инструкцию в HTML/Markdown и checksums;
- SHA-256: `1b6070cb7d082ef37ec97adcb28a21959742b8efec10e0dc75c201fd9abf66c1`.

### Инструкция пользователя

- `Plugin_Navigator_User_Guide_RU.html` — автономная HTML-инструкция с оглавлением;
- SHA-256: `d6529a22ff895f2dbddf07af673630850715d476dd7b59e71db3d66992f55e8e`;
- `Plugin_Navigator_User_Guide_RU.md` — исходный текст;
- SHA-256: `66147eca63c276d92d22da8c4a767afc187427723bcbaf6c7bc7dedcb5deb269`.

### HTML

- `Plugin_Navigator_Full.html`
- `Plugin_Navigator_Full_v2.5.7.html`
- размер: 10 005 484 байта;
- SHA-256: `a8d0dde0f884eaa7dca18eece079ea5635ada14df846734387b67724b5bdb2b0`;
- файлы и `Plugin_Navigator_Windows_Source/resources/index.html` побайтно совпадают.

### Windows x64

`Plugin_Navigator_Full_v2.5.7_Windows_x64.zip`

- ZIP SHA-256: `5a75441cfc0e8a49d1aeddf1954f8d9b47b108e75016e4f27de40265213288d0`;
- EXE SHA-256: `a8bd28be923bc5b94f90bb29cd84ff9f0dfddd3001ec7968a8af4b63f9c61ebd`;
- Neutralinojs 6.9.0;
- Windows 10/11 x64;
- требуется Microsoft Edge WebView2 Runtime;
- цифровой подписи нет;
- HTML внутри EXE побайтно совпадает с HTML 2.5.7.

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
