PLUGIN NAVIGATOR 2.4.6 — WINDOWS x64

Этот проект упаковывает существующий автономный Plugin Navigator v2.4.6 в настольную оболочку Windows без изменения содержимого приложения.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- версия: 2.4.6-session-balance
- SHA-256: 61aa7e9d81f72aa05ec1a10da631f6c8c7934801bbfcf085203632215e375c47
- Размер: 8 388 779 байт

ЦЕЛЕВАЯ СИСТЕМА
- Windows 10/11 x64
- Microsoft Edge WebView2 Runtime

СБОРКА
1. Установить Node.js.
2. Собрать resources.neu через @electron/asar и встроить в Neutralino 6.9.0 EXE через postject (--embed-resources / overwrite).
3. Каталог dist в этой среде не сохраняется — копировать EXE сразу наружу.

ОБОЛОЧКА
Neutralinojs 6.9.0. Интерфейс, база плагинов и логика Plugin Navigator не модифицируются. Отключён доступ HTML-приложения к нативным API операционной системы. Ресурсы встроены внутрь исполняемого файла.
