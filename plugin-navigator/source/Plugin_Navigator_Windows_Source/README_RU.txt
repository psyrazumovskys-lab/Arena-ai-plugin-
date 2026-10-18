PLUGIN NAVIGATOR 2.8.1 — WINDOWS x64

Этот каталог содержит конфигурацию и воспроизводимые инструменты упаковки Plugin Navigator в оболочку Neutralinojs 6.9.0.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- resources/ai/worker.js
- WebLLM 0.2.84 копируется из node_modules внутрь EXE во время сборки
- версия: 2.8.1
- HTML совпадает с Plugin_Navigator_Full_v2.8.1.html

ЛОКАЛЬНЫЙ ИИ
- модель: Qwen3.5 2B Q4 (`Qwen3.5-2B-q4f16_1-MLC`)
- движок WebLLM встроен в Windows-приложение
- веса модели около 1,1 ГБ загружаются пользователем один раз
- после загрузки модель хранится в WebView2 cache и работает без облачного сервера
- без WebGPU весь обычный справочник и Помощник порядка продолжают работать

ЦЕЛЕВАЯ СИСТЕМА
- Windows 10/11 x64
- Microsoft Edge WebView2 Runtime с WebGPU
- минимум 8 ГБ RAM, рекомендуется 16 ГБ

СБОРКА

Из корня репозитория:

1. cd Plugin_Navigator_Windows_Source && npm ci
2. cd ..
3. python3 build_windows.py

Скрипт:
- собирает resources.neu через @electron/asar;
- кладёт neutralino.config.json в корень ASAR, HTML и AI runtime в resources;
- обновляет FileVersion и ProductVersion EXE;
- встраивает ресурс через postject;
- извлекает и проверяет конфигурацию, HTML, WebLLM и AI Worker;
- создаёт portable ZIP и CHECKSUMS_SHA256.txt.

ОБОЛОЧКА
Neutralinojs 6.9.0. Native API отключён. Внешние официальные ссылки открываются в системном браузере. Иконка не изменяется. Trial, ключей и функциональных ограничений нет.

EXE не подписан коммерческим сертификатом, поэтому SmartScreen может показать предупреждение «Неизвестный издатель».
