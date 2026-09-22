# Plugin Navigator 2.5.2 — сверка плагинов, цепочек и описаний

Дата: 14.08.2026  
Статус: **PASS**

## Что проверено

- 365 плагинов = 364 из xlsx + FabFilter Pro-Q 4. Дублей имён/id нет. Поля каталога совпадают с таблицей.
- Все 51 AudioLoom-ссылки на месте; AudioLoom не выделен в отдельный раздел.
- 99 цепочек / 351 шаг: все имена есть в каталоге, этапы совпадают с категорией (кроме осознанных: Devil-Loc как crush, Erebos как cinematic layer).
- 361 exact official page, 4 hub-only без выдуманных URL: UltraPump, Dangerous Compressor, bx_console British Class A, RIR.
- Тесты: `test_plugin_guides.py`, `test_design_audit.py`, `test_chain_research_audit.py` — PASS.

## Ошибки в текстах 2.5.1, исправленные здесь

Ключевой матчер смотрел на `name+kind` слишком широко и подписывал чужие продукты:

| Плагин | Было неверно | Стало |
|---|---|---|
| Ozone Spectral Shaper, ADPTR Sculpt | «EQ Sketch» от Pro-Q 4 (`spectral dynamics`) | свои описания, без Sketch |
| Overloud Gem Dopamine | «меняет удар начала» — kind содержит «не transient shaper» | tape encoder, не transient |
| Renaissance Vox | только gate | vocal leveling |
| Waves LoAir | «гармоники для маленькой колонки» как у RBass | subharmonic: частоты *ниже* исходника |
| PuigTec MEQ-5 | Pultec-трюк boost+cut низа (это EQP-1A) | midrange peak/dip |
| Waves H-Reverb | «помещение из IR / кабинета» | FIR/algorithmic hybrid, не cabinet IR |
| Waves OneKnob Pressure | «прозрачное выравнивание» | плотность и pump |
| Waves Torque | «тело бочки и баса» | резонанс/pitch барабана |
| Pro-Q 4 | vendorSite = AudioLoom из-за поля `link` | FabFilter |
| bx_masterdesk / Classic | Classic помечен как «более новая редакция» | классическая/простая редакция |

Карточки каталога снова показывают `guide.simple`, а не сырой `description` (заявлено в 2.4.12, в шаблоне оставался description).  
В экспертной главной: «365 плагинов», не «365 плагина и семейства».

## Цепочки

Порядок и состав 99 пресетов сверены. Менять curated chains не пришлось: плагины на своих этапах, send 100% wet, monitoring не в export, mastering заканчивается limiter.

## Что не трогал (отдельная команда)

- 81 старых URL Plugin Alliance `/en/products/….html`
- 4 hub-only без выдуманных страниц
- 38 family-level Control maps
- «Не нужно» на базовых пунктах сессии
- VST / DAW / Lite-Trial

## Файлы

- `Plugin_Navigator_Full.html` / `Plugin_Navigator_Full_v2.5.2.html`
- SHA-256: `db2591ebcaafe8847a1a94fc2e736a2f3e25840a51ef0a9b19831754a4b8cfe9`
- размер: 9 762 084 байт
- Windows: `Plugin_Navigator_Full_v2.5.2_Windows_x64.zip`  
  SHA-256: `4bfaa9f61d23492d9c4d22ca7ad41c2f7cd71d866641eae4979987b9fc43a6f5`  
  HTML внутри EXE совпадает с 2.5.2.
