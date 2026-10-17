# Plugin Navigator 2.6.1 — исправление карточек и Controls

Дата: 21.08.2026
Статус: **PASS**

## Исправленные фактические ошибки

1. Удалён ложный дубль `Soundtoys Sandman Pro`. Правильный `Unfiltered Audio Sandman Pro` сохранён.
2. `Ozone Spectral Denoiser` переименован в `iZotope RX Spectral De-noise`.
3. RX-карточка привязана к RX 12 product/manual и получила точные Controls.
4. FabFilter Micro получил правильную product page и filter Controls вместо compressor Controls.
5. Waves dbx 160 больше не содержит ложный OverEasy switch; добавлены Input, SC-HP, Mix, Noise и Stereo/Duo/MS.
6. H-Reverb направлен на живую страницу `h-reverb-hybrid-reverb`.

## Исправленные stereo/M/S utilities

Product-specific maps подготовлены для:

- bx_control V2;
- bx_solo;
- The Util;
- Waves Center;
- Waves MS Matrix;
- Waves S1 Stereo Imager.

Удалены ошибочные generic modulation Controls `Rate`, `Depth`, `Delay / Detune`, `Feedback`.

## Исправленные product cards

### Ozone Vintage Compressor

- Sharp / Balanced / Smooth;
- Detection Filter;
- Threshold / Ratio;
- Attack / Release;
- Gain / Auto Gain;
- без ложного Mix.

### Chakra

- Chakra macro;
- Tone EQ;
- THD;
- Input / Mix / Output Link;
- Delta;
- ECO / Bass-Width logic.

### Ultimate Snare

- Heat;
- Body;
- Crack;
- Air;
- Punch;
- Plate;
- Bomb.

### Diagnostic utilities

Точные карты добавлены для:

- Mixing Cheat Sheet;
- Portable Mono Speaker Check.

## Session Inspector

- помечен `standalone=true`;
- не имеет source/plugin-chain mappings;
- отображается с badge `STANDALONE · НЕ INSERT`;
- не показывает кнопку «Добавить в цепь»;
- импорт старой пользовательской цепочки удаляет standalone utility из Builder;
- placement/routing явно говорят Mac + Safari + separate HTML app;
- точная карта описывает Session Metadata, Track List, Plugin List и Audio Preview.

## Provenance correction

40 generic amp maps и 7 generic Brainworx console maps больше не выдаются за точные GUI maps.

Новые статусы:

- Product-specific: 118;
- Product-informed: 215;
- Family-level: 32.

## Итоговое покрытие

- 365 валидных записей;
- 364 source-mapped plugins;
- 1 standalone utility;
- 68 семейств;
- 33 источника;
- 99 цепочек / 353 шага;
- 349 exact official product pages;
- 16 vendor hubs;
- 27 research sources.

## Проверки

- старые ошибочные имена отсутствуют: PASS;
- corrected Controls присутствуют: PASS;
- standalone utility не попадает в Builder: PASS;
- Помощник порядка 2.6.0 продолжает работать: PASS;
- все 99 chain audits: PASS;
- card/control audit: PASS;
- deterministic HTML build: PASS;
- Windows embedded config + HTML: PASS;
- ZIP integrity: PASS.

## Контрольные суммы

- HTML: `cfdb05c825765164d92d66dd55cd32bee2b9bad964580b67e574518905e1024f`
- JSON: `6e92e04e1ef4d3fb61dd8582fffdbe2b3d76d42934ad048c8fb2d37667ae819f`
- Windows EXE внутри ZIP: `252a8c9d53e9746429e59443d0edd1a765c49bdb0e367bb7c1aedb26f175225b`
- Windows ZIP: `d8341ad5194b2defd3ef9006652b761eeb11fcf0cb95ea9b31875b89c0564d72`
- общий Download ZIP: `82c46248d9a1d59e687f44c73d00915070d06db1037c0d574e07b73940dc6a5b`
