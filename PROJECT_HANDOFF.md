# Plugin Navigator — текущее состояние проекта

**Дата:** 21 августа 2026
**Актуальная версия:** **2.7.0**
**Язык приложения и общения:** русский

## Инструкция следующему агенту

1. Считать этот файл и актуальные исходники источником текущего состояния.
2. Не менять интерфейс, базу, иконку или готовые цепочки без прямой команды пользователя.
3. Сохранять автономную офлайн-работу основной HTML- и Windows-версии.
4. Объяснения писать по-русски, сохраняя оригинальные English Control names.
5. Не выдавать Family-level данные за точные элементы конкретного GUI/manual.
6. Детерминированный Помощник порядка всегда авторитетнее предположений локального ИИ.

## Текущее состояние

- 365 валидных записей;
- 68 смысловых семейств;
- 33 типа источников;
- 99 curated chains / 353 шага;
- 349 exact official product pages;
- 16 vendor hubs;
- 118 Product-specific, 215 Product-informed и 32 Family-level Control maps;
- простой и экспертный режимы;
- карточки, Controls, Settings, Routing и сравнение;
- пользовательские цепочки, избранное, заметки и резервные копии;
- Помощник порядка: auto-sort, explanations, warnings и creative exceptions;
- 364 source-mapped plugins и 1 standalone utility;
- опциональный локальный ИИ Qwen3.5 2B Q4;
- полностью автономный HTML-справочник;
- portable Windows x64 без Trial и ограничений.

## Изменения 2.7.0 — локальный ИИ

Добавлен отдельный раздел **«Локальный ИИ»**.

Модель:

```text
Qwen3.5 2B Q4
Qwen3.5-2B-q4f16_1-MLC
```

Архитектура:

- WebLLM 0.2.84 встроен непосредственно в Windows EXE;
- inference выполняется в отдельном Web Worker;
- API-ключ, облачный сервер, Python, Ollama и CUDA не нужны;
- веса модели около 1,1 ГБ загружаются один раз;
- после загрузки модель хранится в WebView2 cache и работает офлайн;
- модель можно удалить из интерфейса;
- без WebGPU весь основной Plugin Navigator продолжает работать.

ИИ умеет:

- объяснять текущую цепочку;
- проверять порядок и routing;
- объяснять Controls;
- предлагать безопасные Starting Settings;
- подбирать варианты из локального каталога.

Защита фактов:

- в запрос передаются только текущая цепочка, строгая диагностика порядка и до пяти релевантных карточек;
- системный prompt запрещает выдумывать Controls, URL и официальные функции;
- Product-specific, Product-informed и Family-level должны различаться;
- все этапы нельзя называть обязательными;
- модель не должна утверждать, что слышит аудио или видит DAW;
- ответ явно помечается как рекомендация локального ИИ.

HTML, открытый через `file://`, сохраняет все обычные функции, но честно сообщает, что локальный ИИ предназначен для Windows-приложения.

## Сохранённые исправления 2.6.1

- удалён ложный `Soundtoys Sandman Pro`;
- исправлен `iZotope RX Spectral De-noise`;
- исправлены FabFilter Micro, Waves dbx 160, H-Reverb и stereo utilities;
- добавлены точные карты Chakra, Ultimate Snare и diagnostic utilities;
- Session Inspector остаётся standalone utility;
- generic amp/console maps честно помечены Product-informed;
- сохранены Melodyne, Улучшение 1 и 99 цепочек.

## Финальные файлы 2.7.0

### Общий архив

`Plugin_Navigator_v2.7.0_Download.zip`

- содержит HTML, Windows x64, README, HTML/Markdown-инструкцию и checksums;
- включает `Plugin_Navigator_v2.7.0_Local_AI_Report.md`;
- SHA-256: `dcf5229e002bfad37d3e8290dd3eb768c9b6a0a4e44df6e61abdb30fd8f0f0ee`.

### HTML

- `Plugin_Navigator_Full.html`;
- `Plugin_Navigator_Full_v2.7.0.html`;
- `Plugin_Navigator_Windows_Source/resources/index.html`;
- все три файла побайтно совпадают;
- SHA-256: `75b762b837efc6562b1d54d5945b68614d3767f0eeb389c5393439e88eb5029a`.

### Windows x64

`Plugin_Navigator_Full_v2.7.0_Windows_x64.zip`

- ZIP SHA-256: `0f376b008d0c5157b781a8aa575abfe3dd115ff50c1b0b6568fc0ed2a95a35c0`;
- EXE SHA-256: `72669a1860d3cc37e87b2db577c51e90f872c22ec10168d8ce3c01f1c478f4f5`;
- Neutralinojs 6.9.0;
- Windows 10/11 x64;
- Microsoft Edge WebView2 Runtime с WebGPU;
- цифровой подписи нет;
- embedded config, HTML, WebLLM и AI Worker извлечены и проверены.

### Инструкция пользователя

- `Plugin_Navigator_User_Guide_RU.html` — 23 раздела;
- SHA-256: `7a0bcc758577bb9550ccdda10914d699d261d8842883e2c9df6f8b20d0e61dae`;
- `Plugin_Navigator_User_Guide_RU.md`;
- SHA-256: `296f57a9aaf6ecfeaacaa18326ec984b49165aec296d9e41a5773d35a26140a7`.

### Видео

Актуальная видеоинструкция пока относится к 2.6.1 и не показывает новый локальный ИИ:

- `Plugin_Navigator_2.6.1_Video_Instruction_RU_Clean.mp4`;
- `Plugin_Navigator_2.6.1_Video_Instruction_RU_Clean.srt`;
- `Plugin_Navigator_2.6.1_Video_Instruction_RU_Compact_Subtitles.mp4`.

## Сборка и тесты

Установка:

```bash
python3 -m pip install -r requirements.txt
cd test-runtime && npm ci && cd ..
cd Plugin_Navigator_Windows_Source && npm ci && cd ..
```

Полная основная проверка:

```bash
python3 build_and_test.py
```

Результат 2.7.0:

```text
BUILD + ALL TESTS PASS
365 plugins
99 chains
353 steps
local AI guardrails PASS
JSDOM UI PASS
Windows embedded config PASS
embedded HTML PASS
embedded WebLLM + AI Worker PASS
ZIP integrity PASS
```

Windows:

```bash
python3 build_windows.py
```

Дополнительная Playwright-проверка не была выполнена в текущей Arena-сессии: Chromium CDN несколько раз оборвал TLS-загрузку. Это ограничение среды тестирования, не подтверждение ошибки приложения.

Реальную первую загрузку и ответ модели необходимо дополнительно проверить на Windows-компьютере с WebGPU. В Linux-среде Arena нет подходящего Windows WebView2/WebGPU. Нельзя утверждать, что этот аппаратный тест уже пройден.

## Основные исходники

| Файл | Назначение |
|---|---|
| `build_plugin_navigator.py` | Генератор HTML/JSON, UI локального ИИ, retrieval и guardrails |
| `Plugin_Navigator_Windows_Source/resources/ai/worker.js` | Изолированный WebLLM Worker |
| `build_windows.py` | Встраивает HTML, WebLLM и Worker в EXE |
| `Plugin_Navigator_Windows_Source/verify-windows.mjs` | Проверяет embedded config, HTML и AI runtime |
| `test_local_ai.py` | Статический аудит модели, packaging и guardrails |
| `test-runtime/ui-test-v2.js` | DOM-тест UI и AI grounding context |
| `plugin_guide_enrichment.py` | Карточки, Controls и настройки |
| `product_control_maps.py` | Product-specific Control maps |
| `curated_chain_presets.py` | 99 подготовленных цепочек |

## Постоянные требования пользователя

- сохранять максимальное количество валидных плагинов;
- не выделять AudioLoom в отдельную экосистему;
- сохранять оригинальные English Control names;
- не представлять все стадии цепи обязательными;
- различать официальные сведения, практические рекомендации и provenance;
- не менять иконки без прямой команды;
- Windows-версия полная, без Trial, ключей и ограничений;
- основная программа должна работать без ИИ и без интернета.

## Не реализовано

- Cubase Plug-in Report import;
- Installed/Not Found badges и My Collection;
- VST3 scanner;
- unknown plugin draft cards;
- коммерческая цифровая подпись Windows;
- аппаратный smoke-test Qwen на реальном Windows WebView2/WebGPU;
- обновлённое видео с разделом ИИ 2.7.0.
