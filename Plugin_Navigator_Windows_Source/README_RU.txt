PLUGIN NAVIGATOR 2.4.1 — WINDOWS x64

Этот проект упаковывает существующий автономный Plugin Navigator v2.4.1 в настольную оболочку Windows без изменения содержимого приложения.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- SHA-256: 51867c3329ef0f28a24ce72755a91dd1322724ef27648d00e7604a5648c78117
- Размер: 8 370 199 байт

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
