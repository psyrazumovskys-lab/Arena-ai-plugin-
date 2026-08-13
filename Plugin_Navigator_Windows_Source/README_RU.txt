PLUGIN NAVIGATOR 2.4.0 — WINDOWS x64

Этот проект упаковывает существующий автономный Plugin Navigator v2.4 в настольную оболочку Windows без изменения содержимого приложения.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- SHA-256: 124d3eaaf30ea82c7a85b65f69037ed482e8c5a30b71e3a75d56ba88f6315a46
- Размер: 8 363 001 байт

ЦЕЛЕВАЯ СИСТЕМА
- Windows 10/11 x64
- Microsoft Edge WebView2 Runtime

СБОРКА
1. Установить Node.js.
2. В каталоге проекта выполнить:
   npx @neutralinojs/neu build --embed-resources
3. Готовый Windows-файл появится в:
   dist/Plugin_Navigator_Full/Plugin_Navigator_Full-win_x64.exe

ОБОЛОЧКА
Neutralinojs 6.9.0. Интерфейс, база плагинов и логика Plugin Navigator не модифицируются. Отключён доступ HTML-приложения к нативным API операционной системы. Ресурсы встроены внутрь исполняемого файла.
