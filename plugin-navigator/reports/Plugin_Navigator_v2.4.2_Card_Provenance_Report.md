# Plugin Navigator 2.4.2 — hub product pages

Дата: 13.08.2026  
Версия: **2.4.2-hub-pages**  
Цепочки, Simple/Expert, Controls, Windows-логика и иконки не менялись.

## Provenance

| | 2.4.1 после аудита | 2.4.2 |
|---|---:|---:|
| Exact official product page | 346 | **360** |
| Vendor/manual hub only | 18 | **4** |

См. `Plugin_Navigator_v2.4.2_Hub_Pages_Report.md`.

Ozone-модули по-прежнему ведут на suite-страницу и так подписаны. MS Matrix подписан как utility S1. Gyraf Gyratec X ведёт на текущую licensed page Antelope, не на снятую PA-страницу.

## Controls

Без изменений относительно 2.4.1:

| | Значение |
|---|---:|
| Product-specific curated map | 152 |
| Product-informed curated map | 174 |
| Family-level control model | 38 |

## Проверки

- `test_plugin_guides.py` — PASS
- `test_design_audit.py` — PASS
- `test_chain_research_audit.py` — PASS
- HTML и `Plugin_Navigator_Windows_Source/resources/index.html` совпадают.
