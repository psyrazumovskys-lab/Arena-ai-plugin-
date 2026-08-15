# Plugin Navigator

Автономный русскоязычный справочник по аудиоплагинам и конструктор цепочек обработки.

**Актуальная версия: 2.5.7** — 15 августа 2026.

## Готовые файлы

- `Plugin_Navigator_v2.5.7_Download.zip` — общий архив: HTML + Windows x64 + инструкции;
- `Plugin_Navigator_Full.html` — актуальное автономное HTML-приложение;
- `Plugin_Navigator_Full_v2.5.7.html` — версия с номером выпуска;
- `Plugin_Navigator_Full_v2.5.7_Windows_x64.zip` — portable Windows 10/11 x64;
- `CHECKSUMS_SHA256.txt` — контрольные суммы.

HTML работает без установки и без интернета. Windows-версия полная, без Trial и ключей. Для неё требуется Microsoft Edge WebView2 Runtime, обычно уже установленный в Windows 10/11. EXE не подписан коммерческим сертификатом, поэтому SmartScreen может показать предупреждение.

## Что есть в программе

- 366 плагинов, включая Celemony Melodyne;
- 68 смысловых семейств;
- 33 типа источников;
- 99 подготовленных цепочек;
- простой и экспертный режимы;
- подробные карточки, Controls и стартовые настройки;
- конструктор и сохранение собственных цепочек;
- избранное и личные заметки;
- резервная копия пользовательских данных;
- поиск по описаниям, Controls и настройкам;
- фильтр по производителю;
- Celemony Melodyne в Lead Vocal и Backing Vocals как условный первый этап до EQ/dynamics;
- полностью автономная офлайн-работа.

## Пользовательские данные

Избранное, заметки, чеклист и цепочки сохраняются локально на устройстве. В разделе **«Ещё»** можно:

- скачать общую резервную копию;
- восстановить данные из ранее сохранённого JSON-файла.

Перед очисткой, удалением или заменой текущей цепочки программа запрашивает подтверждение.

## Сборка HTML

Требуются Python 3.11+ и зависимости:

```bash
python3 -m pip install -r requirements.txt
python3 build_plugin_navigator.py
```

## Полная проверка

```bash
cd test-runtime
npm ci
cd ..
python3 build_and_test.py
```

Дополнительная проверка реальной вёрстки Chromium:

```bash
cd test-runtime
npx playwright install chromium
npm run test:browser
```

## Сборка Windows

```bash
cd Plugin_Navigator_Windows_Source
npm ci
cd ..
python3 build_windows.py
```

Скрипт берёт Neutralinojs x64 shell из предыдущего Windows ZIP, обновляет Windows-версию файла, встраивает актуальный HTML, проверяет его побайтовое совпадение и создаёт новый ZIP.

## Основные исходники

- `plugin_usage_semantic_hybrid_corrected.xlsx` — исходный каталог;
- `build_plugin_navigator.py` — генератор HTML и базы;
- `plugin_guide_enrichment.py` — карточки и практические руководства;
- `product_control_maps.py` — карты Controls;
- `curated_chain_presets.py` — подготовленные цепочки;
- `official_plugin_references.py` и `official_product_pages.py` — официальные ссылки;
- `Plugin_Navigator_Windows_Source/` — конфигурация и инструменты Windows-сборки.
