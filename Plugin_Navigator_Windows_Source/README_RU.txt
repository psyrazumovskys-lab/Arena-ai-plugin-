PLUGIN NAVIGATOR 2.4.4 — WINDOWS x64

Этот проект упаковывает существующий автономный Plugin Navigator v2.4.4 в настольную оболочку Windows без изменения содержимого приложения.

ИСХОДНОЕ ПРИЛОЖЕНИЕ
- resources/index.html
- версия: 2.4.4-session-lessons
- SHA-256: c0e2f379eb18ed7c4705c3e1a1a33676e5e167eb907e78089e42586ede658da6
- Размер: 8 385 046 байт

ЦЕЛЕВАЯ СИСТЕМА
- Windows 10/11 x64
- Microsoft Edge WebView2 Runtime

СБОРКА
1. Установить Node.js.
2. В каталоге проекта выполнить:
   npx @neutralinojs/neu@11.6.0 build --embed-resources
3. Готовый Windows-файл появится в:
   dist/Plugin_Navigator_Full/Plugin_Navigator_Full-win_x64.exe

ОБОЛОЧКА
Neutralinojs 6.9.0. Интерфейс, база плагинов и логика Plugin Navigator не модифицируются. Отключён доступ HTML-приложения к нативным API операционной системы. Ресурсы встроены внутрь исполняемого файла.
