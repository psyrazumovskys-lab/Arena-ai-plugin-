# Аудит remaining hub pages — 13.08.2026

Версия: **2.4.2-hub-pages**  
Цепочки, Controls, Simple/Expert, Windows-логика и иконки не менялись.

Проверены живые product pages для 18 карточек, у которых после 2.4.1 оставался только vendor hub. Старые Overloud slug `/products/gem-*` и старые PA `.html` для Dangerous/Gyraf не используются.

## Итог

| | После 2.4.1 | После 2.4.2 |
|---|---:|---:|
| Exact official product page | 346 | **360** |
| Vendor/manual hub | 18 | **4** |

## Добавлены живые страницы

Overloud (новые публичные slug):

- Gem Voice → `/products/voice`
- Overloud Gem Comp 76 → `/products/comp76-fet-compressor-limiter`
- Overloud Gem Comp LA → `/products/comp-la`
- Overloud Gem Comp 670 → `/products/comp670-compressor-limiter`
- Gem EQ550 → `/products/eq550`
- Gem EQ84 → `/products/eq84`
- Gem EQP-1A → `/products/eqp` (официальный продукт Gem EQP, режим EQP-1A)
- Mark Studio 2 → `/products/mark-studio-2`
- Overloud Breverb 2 → `/products/breverb-2`
- Overloud Gem Dopamine → `/products/dopamine`
- Overloud Gem Tapedesk → `/products/tapedesk`

Plugin Alliance / лицензии:

- Dangerous BAX EQ → `https://www.plugin-alliance.com/products/bax-eq`
- Gyraf Gyratec X → `https://en.antelopeaudio.com/products/gyratec-x/` (текущая licensed recreation; PA-страницы нет)

Waves:

- Waves MS Matrix → страница S1 Stereo Imager. Отдельного product page нет; MS Matrix — utility внутри S1. Карточка так подписана.

## Остаются vendor hub

- **UltraPump** — у Waves нет продукта с таким именем и нет живой `/plugins/ultrapump`.
- **Dangerous Compressor** — у Plugin Alliance в бренде Dangerous Music сейчас только BAX EQ; отдельного compressor plugin нет.
- **bx_console British Class A** — отдельной PA-страницы нет; нельзя подставлять `bx_console N` или Helios.
- **RIR** — `/products/rir` даёт 404. SuperCabinet — другой продукт, не подставляется как та же страница.

## Проверки

- `test_plugin_guides.py` — PASS
- `test_design_audit.py` — PASS
- `test_chain_research_audit.py` — PASS
- HTML и `Plugin_Navigator_Windows_Source/resources/index.html` совпадают.
