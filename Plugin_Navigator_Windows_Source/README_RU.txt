PLUGIN NAVIGATOR 2.4.8 — WINDOWS x64

Этот проект упаковывает существующий автономный Plugin Navigator v2.4.8 в настольную оболочку Windows без изменения содержимого приложения.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- версия: 2.4.8-beginner-guides
- SHA-256: 9d169236b91fed72bc32bd37f90ba0d74af917d87727f218dc6fe5d165a56a0a
- Размер: 9 544 627 байт

ЦЕЛЕВАЯ СИСТЕМА
- Windows 10/11 x64
- Microsoft Edge WebView2 Runtime

СБОРКА
1. Установить Node.js.
2. Собрать resources.neu через @electron/asar и встроить в Neutralino 6.9.0 EXE через postject (--embed-resources / overwrite).
3. Каталог dist в этой среде не сохраняется — копировать EXE сразу наружу.

ОБОЛОЧКА
Neutralinojs 6.9.0. Интерфейс, база плагинов и логика Plugin Navigator не модифицируются. Отключён доступ HTML-приложения к нативным API операционной системы. Ресурсы встроены внутрь исполняемого файла.
