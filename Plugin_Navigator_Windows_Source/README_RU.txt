PLUGIN NAVIGATOR 2.5.7 — WINDOWS x64

Этот каталог содержит конфигурацию и воспроизводимые инструменты упаковки автономного Plugin Navigator в оболочку Neutralinojs 6.9.0.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- версия: 2.5.7
- содержимое совпадает с Plugin_Navigator_Full_v2.5.7.html

ЦЕЛЕВАЯ СИСТЕМА
- Windows 10/11 x64
- Microsoft Edge WebView2 Runtime

СБОРКА

Из корня репозитория:

1. cd Plugin_Navigator_Windows_Source && npm ci
2. cd ..
3. python3 build_windows.py

Скрипт:
- собирает resources.neu через @electron/asar;
- кладёт neutralino.config.json в корень ASAR и HTML в resources/index.html;
- обновляет FileVersion и ProductVersion EXE;
- встраивает ресурс через postject;
- извлекает и проверяет встроенную конфигурацию и побайтовое совпадение HTML;
- создаёт portable ZIP и CHECKSUMS_SHA256.txt.

ОБОЛОЧКА
Neutralinojs 6.9.0. Native API отключён. Внешние официальные ссылки открываются в системном браузере. Иконка не изменяется. Trial, ключей и функциональных ограничений нет.

EXE не подписан коммерческим сертификатом, поэтому SmartScreen может показать предупреждение «Неизвестный издатель».
