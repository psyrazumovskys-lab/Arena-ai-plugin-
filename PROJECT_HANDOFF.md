# Plugin Navigator — текущее состояние проекта

**Дата:** 14 августа 2026
**Актуальная версия:** **2.5.5**
**Язык приложения и общения:** русский

## Инструкция следующему агенту

1. Считать этот файл и актуальные исходники источником текущего состояния.
2. Не менять интерфейс, базу, иконку или готовые цепочки без прямой команды пользователя.
3. Сохранять автономную офлайн-работу HTML и Windows-версии.
4. Объяснения писать по-русски, сохраняя оригинальные английские названия Controls.
5. Не выдавать family-level данные за точные элементы конкретного GUI/manual.

## Текущее состояние

- 365 плагинов;
- 68 смысловых семейств;
- 33 типа источников;
- 99 curated chains / 351 шаг;
- 349 exact official product pages;
- 16 vendor hubs без выдуманных dedicated URL;
- 153 product-specific, 174 product-informed и 38 family-level Control maps;
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

## Изменения 2.5.5

- Добавлена безопасная нормализация старого или повреждённого локального состояния.
- Формат экспортируемых данных получил `schemaVersion` и `appVersion`.
- Источник и preset конструктора сохраняются между запусками.
- Резервная копия доступна в простом режиме через «Ещё».
- Опасные удаления, очистка и замена цепочки требуют подтверждения.
- Поиск строится после обогащения карточек и видит Controls/Settings.
- Добавлен фильтр производителей.
- Улучшены ARIA-вкладки, подписи маленьких кнопок и мобильные overlay-элементы.
- Добавлены воспроизводимые команды HTML- и Windows-сборки.
- Windows FileVersion/ProductVersion теперь соответствует 2.5.5.0.

## Финальные файлы

### HTML

- `Plugin_Navigator_Full.html`
- `Plugin_Navigator_Full_v2.5.5.html`
- размер: 9 969 506 байта;
- SHA-256: `cc4a7dec8c4cf8b63430d74f44d7ee2da994afb8de220d6208ded6bb809498cd`;
- файлы и `Plugin_Navigator_Windows_Source/resources/index.html` побайтно совпадают.

### Windows x64

`Plugin_Navigator_Full_v2.5.5_Windows_x64.zip`

- ZIP SHA-256: `7f470c28032b589d16b423bb35c9b43a8d44edaf4ef22fd51efe3c318bafee98`;
- EXE SHA-256: `53f573bd712566b251f05d5659e4fb5f5be48803ce34699d9d4a52daa9156a0c`;
- Neutralinojs 6.9.0;
- Windows 10/11 x64;
- требуется Microsoft Edge WebView2 Runtime;
- цифровой подписи нет;
- HTML внутри EXE побайтно совпадает с HTML 2.5.5.

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
