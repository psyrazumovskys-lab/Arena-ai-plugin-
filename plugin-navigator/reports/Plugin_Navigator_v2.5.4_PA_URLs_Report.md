# 2.5.4 — живые URL Plugin Alliance

Дата: 14.08.2026

Старый формат `/en/products/{slug}.html` после переезда PA на Shopify часто 404.
Живые страницы: `https://www.plugin-alliance.com/products/{handle}`.
В каталог записаны только подтверждённые handle (fetch/search, title = продукт, не 404).

## Результат

- 69 PA-карточек → живой shop URL (было 81 старых `.html` + BAX уже в новом виде).
- 12 без dedicated page → vendor hub (коллекция бренда). Не выдумывал slugs.
- Плюс прежние 4 hub-only: UltraPump, Dangerous Compressor, RIR, bx_console British Class A.
- Итого: 349 exact product pages, 16 vendor hubs, 365 плагинов.

## Примеры живых handle

| Каталог | Handle |
|---|---|
| bx_rockrack V3 | `bx_rockrack-v3` |
| ADPTR Sculpt | `sculpt` |
| Friedman Dirty Shirley | `ds-40` (страница Dirty Shirley) |
| Ampeg SVT-VR Classic | `svt-vr-classic` (не полный SVT-VR) |
| SPL De-Esser | `de-esser-collection` |
| Looptrotter SA2RATE | `sa2rate-2` |
| AMEK EQ 200 | `eq-200` |
| Purple Audio MC77 | `mc77` |

## Hub-only в этом срезе

bx_pultec / bx_pultec Pro; Shadow Hills Dual Vandergraph; Ampeg SGT-DI, SVT-4PRO, SVT-7PRO; Friedman Smallbox 50, JJ-100, Pink Taco; Diezel Hagen, Schmidt; Suhr Badger 30, Koji Comp.

Коллекции брендов эти продукты не показывают. Старые `.html` тоже 404. UltraPump не маппил на Pumper, RIR — не на SuperCabinet.

## Vendor hubs

`/en/products.html` и `/en/brand/…` редиректят на `/collections/…`. В базе сразу коллекции (`all-products`, `brainworx`, `ampeg`, `friedman` и т.д.).

HTML SHA-256: `72bade58a5e744d6ea941b9f0e74eae0824417f5709edc8f3967ab6316503d60`  
Windows ZIP: `689c236649c84114935afd1fd03c77d3297a79f0d9b6962a45fb3ff68d8d9f39`
