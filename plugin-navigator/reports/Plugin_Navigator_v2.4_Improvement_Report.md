# Plugin Navigator 2.4 — отчёт по улучшениям 1–6

Дата: 12.08.2026  
Версия: **2.4.0-priority-improvements**  
Статус: **PASS**

## 1. Source × Stage coverage — выполнено

Ранее 22 продукта были доступны только в общем каталоге. Теперь все **364/364** плагина имеют хотя бы одно релевантное Source × Stage назначение.

Добавлены conservative alternative mappings для:

- CLA MixDown;
- Maserati GRP;
- JJP Percussion;
- Maserati ACG;
- C1 Compressor/Gate;
- Waves MaxxVolume;
- Waves OneKnob Louder;
- bx_opto;
- Vertigo VSC-2;
- Waves PuigChild 660;
- bx_digital V3;
- Waves Q-Clone;
- Waves Q10 / Q2 / Q1;
- Friedman Buxom Betty;
- Tone King Imperial MKII;
- ENGL E765 Retro Tube;
- Suhr Koji Comp;
- Abbey Road Studio 3;
- Session Inspector;
- Waves PS22 Stereo Maker;
- bx_solo;
- Manny Marroquin Tone Shaper.

Они добавлены как alternatives, а не искусственно повышены до основных рекомендаций.

## 2. Короткие Starting settings — выполнено

До изменения:

- 125 chain settings короче 30 символов;
- 212 короче 50 символов.

После изменения:

- 0 короче 30;
- 0 короче 50;
- минимальная длина — 71 символ;
- каждый короткий старт дополнен listening check и условием Skip/Reduce.

Все 351 звено сохраняет отдельные Purpose, Include when, Skip when, How и Listen for.

## 3. Controls coverage для 80 приоритетных продуктов — выполнено

- 17 `Product-specific curated map`;
- 63 `Product-informed curated map`;
- суммарно 80 приоритетных продуктов;
- оставшиеся 284 честно обозначены как `Family-level control model`.

`Product-informed` означает адаптацию по роли конкретного продукта, curated chains и family profile. Этот уровень намеренно не выдаётся за дословную карту официального GUI/manual.

## 4. Official provenance — выполнено

Все 364 карточки получили официальный reference block:

- 51 `Exact official product page` — AudioLoom;
- 313 `Official vendor/manual hub` — остальные производители.

В карточке показываются:

- тип reference;
- дата проверки;
- точная product page, если она известна;
- официальный Manual/Support hub;
- каталог производителя при необходимости.

Важно: vendor/manual hub явно маркируется как hub, а не как exact manual конкретной версии. Проверены и исправлены устаревшие/неработающие hub URLs для Soundtoys, Newfangled Audio, iZotope, IK Multimedia и elysia.

## 5. Повторяющиеся chain skeletons — выполнено

Ранее было семь групп точных duplicate signatures. Они переработаны source-specific alternatives без случайной ротации плагинов ради разнообразия.

Примеры изменений:

- Synth Bass: bx_opto вместо универсального Pro-C 2;
- Guitar Bus: Vertigo VSC-2 + Forge;
- Synth/Keys Bus: Dangerous Compressor + J37 Tape;
- Bass Bus: bx_opto / Busboy;
- Vocal Bus: GilderVox;
- Guitar Bus fast: Maserati GRP;
- Brass/Woodwinds: AMEK EQ 200 + Gem Comp LA + Abbey Road Chambers;
- Samples/Loops: MaxxVolume + Cactus Clipper;
- Drum Loop tight: Trans-X + Mixtape.

После изменения:

- точных duplicate chain signatures: **0**;
- curated chains используют 113 уникальных продуктов;
- общее количество осталось 99 chains / 351 steps.

## 6. Lazy rendering — выполнено

Раньше страница 99 chains сразу создавала в DOM все 351 подробные step cards.

Теперь:

- initial chains view создаёт только компактные chain cards;
- подробности конкретной цепочки загружаются по кнопке `Подробно о N плагинах`;
- раскрытую цепочку можно свернуть;
- другие цепочки не создают тяжёлый подробный DOM;
- Wizard по-прежнему показывает полностью только один выбранный вариант.

Автотест отдельно проверяет initial, expanded и collapsed состояния.

## Дополнительные исправления

- После замены плагина новый продукт получает собственный source/task recipe, а не How от предыдущего processor.
- Сборка остаётся детерминированной.
- Все внешние ссылки используют `noopener noreferrer`.
- Official provenance отображается в Deep view и панели действий карточки.

## Проверки

- Python generator — PASS;
- deterministic double build — PASS;
- JavaScript `node --check` — PASS;
- jsdom UI — PASS;
- 364 plugin guides — PASS;
- 99 chains / 351 steps — PASS;
- research/routing audit — PASS;
- design/accessibility audit — PASS;
- HTML и `index.html` идентичны.

Итоговый SHA-256:

`124d3eaaf30ea82c7a85b65f69037ed482e8c5a30b71e3a75d56ba88f6315a46`

Размер автономного HTML: 8,363,001 байт.

## Что осталось за рамками пунктов 1–6

- exact product/manual URL для каждого из 313 hub-level references;
- строгая schema migration и preview импорта;
- desktop scanner установленных VST/AU/AAX;
- optional audio analysis;
- реальная DAW/plugin-host интеграция.
