# Plugin Navigator — текущее состояние проекта

**Дата:** 21 августа 2026
**Актуальная версия:** **2.6.1**
**Язык приложения и общения:** русский

## Инструкция следующему агенту

1. Считать этот файл и актуальные исходники источником текущего состояния.
2. Не менять интерфейс, базу, иконку или готовые цепочки без прямой команды пользователя.
3. Сохранять автономную офлайн-работу HTML и Windows-версии.
4. Объяснения писать по-русски, сохраняя оригинальные английские названия Controls.
5. Не выдавать family-level данные за точные элементы конкретного GUI/manual.

## Текущее состояние

- 365 валидных записей;
- 68 смысловых семейств;
- 33 типа источников;
- 99 curated chains / 353 шага;
- 349 exact official product pages;
- 16 vendor hubs без выдуманных dedicated URL;
- 118 product-specific, 215 product-informed и 32 family-level Control maps;
- простой и экспертный режимы;
- быстрые и подробные карточки;
- Controls, Settings, Routing и сравнение;
- пользовательские цепочки, избранное и заметки;
- чеклист подготовки сессии;
- резервная копия и проверяемое восстановление пользовательских данных;
- поиск по карточкам, Controls, настройкам и аналогам;
- фильтр по производителю;
- Помощник порядка: auto-sort, explanations, warnings и creative exceptions;
- 364 source-mapped plugins и 1 standalone utility;
- полностью автономный HTML;
- portable Windows x64 без Trial и ограничений.

Активной незавершённой задачи нет.

## Изменения 2.6.1

- Удалён несуществующий дубль `Soundtoys Sandman Pro`; правильный Unfiltered Audio остаётся.
- `Ozone Spectral Denoiser` исправлен на `iZotope RX Spectral De-noise` с RX 12 manual и точными Controls.
- Исправлены FabFilter Micro URL/Controls и Waves dbx 160 без ложного OverEasy.
- Исправлена 404-ссылка Waves H-Reverb.
- Подготовлены точные stereo maps: bx_control V2, bx_solo, The Util, Center, MS Matrix, S1.
- Исправлен Ozone Vintage Compressor: feedback modes и Detection Filter, без ложного Mix.
- Добавлены точные карты Chakra, Ultimate Snare, Mixing Cheat Sheet и Portable Mono Speaker Check.
- Session Inspector помечен standalone, исключён из plugin chains и не может быть добавлен в Builder.
- 40 generic amp maps и 7 generic Brainworx console maps понижены до честного Product-informed.
- Короткие описания ключевых AudioLoom products индивидуализированы.
- Сохранены Улучшение 1, Melodyne, 99 цепочек и безопасная Windows packaging 2.6.x.

## Финальные файлы

### Общий архив

- `Plugin_Navigator_v2.6.1_Download.zip`;
- содержит HTML, Windows x64, README, инструкцию в HTML/Markdown и checksums;
- SHA-256: `82c46248d9a1d59e687f44c73d00915070d06db1037c0d574e07b73940dc6a5b`.

### Инструкция пользователя

- `Plugin_Navigator_User_Guide_RU.html` — автономная HTML-инструкция с оглавлением;
- SHA-256: `033f4504a70aca825148e35b92ccd6962298f3bd21c5ed6ccc35ff8d35591ae0`;
- `Plugin_Navigator_User_Guide_RU.md` — исходный текст;
- SHA-256: `445d46e092bb00fed110b0aaa53ea39dc899022262aed59ca06ec98af1d97ed4`.

### HTML

- `Plugin_Navigator_Full.html`
- `Plugin_Navigator_Full_v2.6.1.html`
- размер: 9 975 301 байта;
- SHA-256: `cfdb05c825765164d92d66dd55cd32bee2b9bad964580b67e574518905e1024f`;
- файлы и `Plugin_Navigator_Windows_Source/resources/index.html` побайтно совпадают.

### Windows x64

`Plugin_Navigator_Full_v2.6.1_Windows_x64.zip`

- ZIP SHA-256: `d8341ad5194b2defd3ef9006652b761eeb11fcf0cb95ea9b31875b89c0564d72`;
- EXE SHA-256: `252a8c9d53e9746429e59443d0edd1a765c49bdb0e367bb7c1aedb26f175225b`;
- Neutralinojs 6.9.0;
- Windows 10/11 x64;
- требуется Microsoft Edge WebView2 Runtime;
- цифровой подписи нет;
- HTML внутри EXE побайтно совпадает с HTML 2.6.1.

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
