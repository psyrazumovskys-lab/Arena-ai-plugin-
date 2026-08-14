# Plugin Navigator — текущее состояние проекта

**Дата:** 14 августа 2026
**Актуальная версия:** **2.5.6**
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

## Изменения 2.5.6

- В каталог добавлен `Celemony Melodyne`: 366-й плагин.
- Добавлены официальная product page и Help Center Celemony.
- Подготовлена product-specific карта из 8 Controls с оговоркой о различиях Essential / Assistant / Editor / Studio.
- Melodyne связан с Lead Vocal и Backing Vocals, а Waves Tune / Tune Real-Time указаны как аналоги.
- В двух вокальных пресетах Melodyne добавлен условным первым этапом.
- Проверено: Melodyne получает чистый dry-сигнал через ARA/Transfer и находится до EQ, compression, de-essing, delay и reverb.
- 99 цепочек повторно прошли аудит; теперь в них 353 шага и 27 research sources.
- Все улучшения 2.5.5 по резервным копиям, поиску и защите данных сохранены.
- Windows FileVersion/ProductVersion соответствует 2.5.6.0.

## Финальные файлы

### Общий архив

- `Plugin_Navigator_v2.5.6_Download.zip`;
- содержит HTML, Windows x64, README и checksums;
- SHA-256: `4b89807cb587e328b1c158338450713664c8e56c94b17116b18759f95e9aad30`.

### HTML

- `Plugin_Navigator_Full.html`
- `Plugin_Navigator_Full_v2.5.6.html`
- размер: 10 005 484 байта;
- SHA-256: `a99cef170261e94dd6a495ae19df77ae48d61cf7d29e279e059e32bc3252a215`;
- файлы и `Plugin_Navigator_Windows_Source/resources/index.html` побайтно совпадают.

### Windows x64

`Plugin_Navigator_Full_v2.5.6_Windows_x64.zip`

- ZIP SHA-256: `16a4a955e2ca4533f76b477915d52c9a9e494b8ddeb9e5c79815913cab07df6f`;
- EXE SHA-256: `17d33edc6defc305b9253a5c16edb3a01d41f0190b0a654a7f391268fccdd568`;
- Neutralinojs 6.9.0;
- Windows 10/11 x64;
- требуется Microsoft Edge WebView2 Runtime;
- цифровой подписи нет;
- HTML внутри EXE побайтно совпадает с HTML 2.5.6.

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
