# Plugin Navigator 2.5.7 — исправление запуска Windows

Дата: 15.08.2026
Статус: **PASS**

## Симптом

EXE открывал стандартную страницу Neutralinojs вместо Plugin Navigator.

## Причина

Предыдущая ручная Windows-упаковка создавала ASAR только с `index.html` в корне. Neutralinojs ожидает другую структуру:

- `neutralino.config.json` — в корне `resources.neu`;
- `resources/index.html` — по пути, указанному в `documentRoot: /resources/`.

Без встроенной конфигурации Neutralinojs запускался с настройками по умолчанию и открывал свою стандартную страницу.

## Исправление

- Выпущена версия `2.5.7`.
- Внутренний `resources.neu` теперь содержит правильную конфигурацию и HTML.
- Сохранён embedded mode: `POSTJECT_SENTINEL...:1`.
- Проверка сборки извлекает `neutralino.config.json` из EXE и проверяет:
  - `applicationName = Plugin Navigator`;
  - `defaultMode = window`;
  - `documentRoot = /resources/`;
  - `url = /`;
  - `enableServer = true`;
  - `version = 2.5.7`.
- Затем извлекается `/resources/index.html` и побайтно сравнивается с HTML-релизом.

## Проверки

- embedded configuration: PASS;
- embedded document root: PASS;
- embedded HTML byte comparison: PASS;
- postject sentinel enabled: PASS;
- FileVersion / ProductVersion `2.5.7.0`: PASS;
- ZIP integrity: PASS;
- все тесты каталога, Melodyne и 99 цепочек: PASS.

## Контрольные суммы

- HTML: `a8d0dde0f884eaa7dca18eece079ea5635ada14df846734387b67724b5bdb2b0`
- JSON: `9ae4936892bcd4e6569de7c99d33d6a0a6f0322cc16bc9284786a496fbdfea74`
- EXE внутри ZIP: `a8bd28be923bc5b94f90bb29cd84ff9f0dfddd3001ec7968a8af4b63f9c61ebd`
- Windows ZIP: `5a75441cfc0e8a49d1aeddf1954f8d9b47b108e75016e4f27de40265213288d0`
- общий Download ZIP: `1b6070cb7d082ef37ec97adcb28a21959742b8efec10e0dc75c201fd9abf66c1`

Запуск EXE всё равно следует подтвердить на реальном Windows-компьютере, так как в Linux-среде Windows GUI не запускается.
