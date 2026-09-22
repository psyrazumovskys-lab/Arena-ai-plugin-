# Plugin Navigator

Автономный русскоязычный справочник по аудиоплагинам и конструктор цепочек обработки.

**Актуальная версия: 2.7.0** — 21 августа 2026.

## Готовые файлы

- `Plugin_Navigator_v2.7.0_Download.zip` — общий архив: HTML + Windows x64 + инструкции;
- `Plugin_Navigator_Full.html` — актуальное автономное HTML-приложение;
- `Plugin_Navigator_Full_v2.7.0.html` — версия с номером выпуска;
- `Plugin_Navigator_Full_v2.7.0_Windows_x64.zip` — portable Windows 10/11 x64;
- `Plugin_Navigator_User_Guide_RU.html` — инструкция пользователя в формате HTML;
- `Plugin_Navigator_User_Guide_RU.md` — исходный текст инструкции;
- `Plugin_Navigator_v2.7.0_Local_AI_Report.md` — устройство ИИ, ограничения и проверки;
- `CHECKSUMS_SHA256.txt` — контрольные суммы.

HTML-справочник работает без установки и интернета. Windows-версия полная, без Trial и ключей. Для неё требуется Microsoft Edge WebView2 Runtime, обычно уже установленный в Windows 10/11. EXE не подписан коммерческим сертификатом, поэтому SmartScreen может показать предупреждение.

## Новое в 2.7.0 — локальный ИИ

В Windows-приложение встроен движок **WebLLM 0.2.84** и интерфейс для одной модели:

```text
Qwen3.5 2B Q4
Qwen3.5-2B-q4f16_1-MLC
```

- облачный сервер, API-ключ, Python, Ollama и CUDA не требуются;
- модель загружается кнопкой внутри программы один раз, объём — около 1,1 ГБ;
- после загрузки она хранится в локальном WebView2 cache и формирует ответы офлайн;
- модель можно удалить из того же раздела;
- ИИ объясняет текущую цепочку, порядок, Controls и Starting Settings;
- в запрос передаются только подходящие карточки локального каталога и текущая цепочка;
- ответы ИИ помечены как практические рекомендации, а не официальные факты;
- строгий Помощник порядка остаётся авторитетнее модели;
- без WebGPU весь обычный справочник продолжает работать без ограничений.

Рекомендуется Windows 10/11, 16 ГБ RAM и актуальные WebView2/драйвер видеокарты. Минимально — 8 ГБ RAM и примерно 2,3 ГБ доступной GPU/shared memory.

## Видеоинструкция

Текущая видеоинструкция показывает основные функции и исправления версии 2.6.1. Новый раздел локального ИИ 2.7.0 в неё пока не включён.

- `Plugin_Navigator_2.6.1_Video_Instruction_RU_Clean.mp4` — чистое видео без вшитых субтитров;
- `Plugin_Navigator_2.6.1_Video_Instruction_RU_Clean.srt` — отдельные отключаемые русские субтитры;
- `Plugin_Navigator_2.6.1_Video_Instruction_RU_Compact_Subtitles.mp4` — версия с компактными субтитрами максимум в две строки.

Длительность обеих версий — 8 минут 34 секунды, разрешение — Full HD 1920×1080.

## Что есть в программе

- 365 валидных записей, включая Celemony Melodyne;
- 68 смысловых семейств;
- 33 типа источников;
- 99 подготовленных цепочек;
- простой и экспертный режимы;
- подробные карточки, Controls и стартовые настройки;
- конструктор и сохранение собственных цепочек;
- Помощник порядка: автоматическая расстановка, объяснения и предупреждения;
- опциональный локальный ИИ Qwen3.5 2B;
- исправленные карточки RX Spectral De-noise, Micro, dbx 160 и stereo utilities;
- Session Inspector помечен как standalone utility и исключён из plugin chains;
- избранное и личные заметки;
- резервная копия пользовательских данных;
- поиск по описаниям, Controls и настройкам;
- фильтр по производителю;
- Celemony Melodyne в Lead Vocal и Backing Vocals как условный первый этап до EQ/dynamics.

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

Скрипт берёт Neutralinojs x64 shell из предыдущего Windows ZIP, обновляет Windows-версию файла, встраивает актуальный HTML, WebLLM runtime и AI Worker, затем извлекает и проверяет все встроенные ресурсы.

## Основные исходники

- `plugin_usage_semantic_hybrid_corrected.xlsx` — исходный каталог;
- `build_plugin_navigator.py` — генератор HTML и базы;
- `plugin_guide_enrichment.py` — карточки и практические руководства;
- `product_control_maps.py` — карты Controls;
- `curated_chain_presets.py` — подготовленные цепочки;
- `official_plugin_references.py` и `official_product_pages.py` — официальные ссылки;
- `Plugin_Navigator_Windows_Source/` — конфигурация и инструменты Windows-сборки.

## Прочие разделы

- `books/` — психологические книги и тетради: лекции по клинической психологии, конспекты по СТ/ACT, тетради 12 шагов ВДА/ACA, тетрадь восстановления при алкоголизме; `books/index.html` — центр скачиваний;
- `therapy-workbooks/` — терапевтические тетради (границы, дневник 12 шагов);
- `AI_Photos_Catalog/` — каталог фото, обработанных с помощью ИИ (готовые — в `processed/`, исходники — в `originals/`).
