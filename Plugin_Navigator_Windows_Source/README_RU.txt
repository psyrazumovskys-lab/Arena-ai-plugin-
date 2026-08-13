PLUGIN NAVIGATOR 2.4.5 — WINDOWS x64

Этот проект упаковывает существующий автономный Plugin Navigator v2.4.5 в настольную оболочку Windows без изменения содержимого приложения.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- версия: 2.4.5-nav-groups
- SHA-256: c6130ceac2369c7730c4cb6f38640ac51e4e5fd142f18a24a0b9298e29e2a6a0
- Размер: 8 384 991 байт

ЦЕЛЕВАЯ СИСТЕМА
- Windows 10/11 x64
- Microsoft Edge WebView2 Runtime

СБОРКА
1. Установить Node.js.
2. Собрать resources.neu через @electron/asar и встроить в Neutralino 6.9.0 EXE через postject (--embed-resources / overwrite).
3. Каталог dist в этой среде не сохраняется — копировать EXE сразу наружу.

ОБОЛОЧКА
Neutralinojs 6.9.0. Интерфейс, база плагинов и логика Plugin Navigator не модифицируются. Отключён доступ HTML-приложения к нативным API операционной системы. Ресурсы встроены внутрь исполняемого файла.
