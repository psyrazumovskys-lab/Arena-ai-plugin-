# Plugin Navigator 2.4.1 — точность карточек и provenance

Дата: 13.08.2026  
Версия: **2.4.1-card-provenance**  
Цепочки, Simple/Expert, Windows-логика и иконки не менялись.

## Provenance

| | Было | Стало |
|---|---:|---:|
| Exact official product page | 51 | 346 после аудита |
| Vendor/manual hub only | 313 | 18 |

См. `Plugin_Navigator_v2.4.1_Link_Audit_Report.md`.

Ozone-модули ведут на официальную страницу suite и так подписаны.

## Controls

| | Было | Стало |
|---|---:|---:|
| Product-specific curated map | 17 | 152 |
| Product-informed curated map | 63 | 174 |
| Family-level control model | 284 | 38 |

Family-level оставлен в основном у boutique/AudioLoom-плагинов, где нет проверяемой карты GUI. Это по-прежнему не выдаётся за точный manual.

## Проверки

- `test_plugin_guides.py` — PASS
- `test_design_audit.py` — PASS
- `test_chain_research_audit.py` — PASS
- HTML и `Plugin_Navigator_Windows_Source/resources/index.html` совпадают.

## Windows EXE

Готовый `Plugin_Navigator_Full_v2.4.0_Windows_x64.zip` всё ещё содержит HTML 2.4.0. Чтобы встроить 2.4.1, нужна повторная Neutralino-сборка из обновлённого `resources/index.html`.
