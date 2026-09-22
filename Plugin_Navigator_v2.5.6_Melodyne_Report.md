# Plugin Navigator 2.5.6 — Celemony Melodyne

Дата: 14.08.2026
Статус: **PASS**

## Что добавлено

- В исходную таблицу и каталог добавлен `Celemony Melodyne`.
- Каталог теперь содержит 366 плагинов.
- Категория: `Cleanup и restoration`.
- Семейство: `Pitch correction`.
- Аналоги: `Waves Tune`, `Waves Tune Real-Time`.
- Источники: `Lead Vocal`, `Backing Vocals`.
- Добавлены подробное русское описание, 8 Controls, 4 стартовых Settings, workflow и официальный provenance.
- В карточке явно указано, что набор инструментов зависит от edition: Essential, Assistant, Editor или Studio.

## Официальные источники

- Product page: `https://www.celemony.com/en/melodyne/what-is-melodyne`
- Help Center: `https://helpcenter.celemony.com/M5/`
- ARA / Transfer workflow: `https://helpcenter.celemony.com/M5/doc/melodyneEssential5/en/M5tour_TransferARA?env=live`

## Проверка цепочек

Melodyne добавлен в два пресета:

1. `Lead Vocal · Базовый vocal`
   - Melodyne → Pro-Q 3 → Pro-C 2 → Pro-DS;
   - Pro-R остаётся отдельным send.
2. `Backing Vocals · Clean pop`
   - Melodyne → F6 → Pro-C 2 → Sibilance;
   - Double Dare и Room Service остаются отдельными sends.

В обоих случаях Melodyne:

- помечен `ЕСЛИ НУЖЕН TUNING`;
- находится первым среди inserts;
- получает чистый dry-сигнал через ARA или Transfer;
- стоит до EQ, compression, de-essing, delay и reverb;
- не применяется автоматически ко всем нотам или дублям.

Все 99 цепочек повторно проверены: 353 шага, 27 research sources, PASS.

## Покрытие

- 366 плагинов;
- 154 product-specific Control maps;
- 174 product-informed maps;
- 38 family-level maps;
- 350 exact official product pages;
- 16 vendor hubs.

## Контрольные суммы

- Исходная таблица: `3504f7818e78bb1147c824c9aff6424829eb2024d3d611b6fb01d5b76fe06400`
- HTML: `a99cef170261e94dd6a495ae19df77ae48d61cf7d29e279e059e32bc3252a215`
- JSON: `c3326b436a38ec6f08aeec0c847dd6bc5d1ca95e987a93604a46a89a01237737`
- Общий Download ZIP: `4b89807cb587e328b1c158338450713664c8e56c94b17116b18759f95e9aad30`
