# 2.4.9 — сверка описаний с официальными страницами

Проверены живые страницы Waves, Soundtoys, AudioLoom, Plugin Boutique / KVR (bx_rockrack). Страницы Plugin Alliance `/en/products/...` сейчас отдают 404 (сайт уехал на коллекции).

## Совпало с официальным текстом

- Crystallizer — reverse/granular pitch echo, H3000 Crystal Echoes.
- Decapitator — analog saturation, 5 models, Punish.
- CLA MixDown — mix-bus finishing (Waves: four processors on the mix bus).
- Busboy — shelves + filters + bus compression + finishing limiter (не «просто лимитер»).
- ExoDelay — modulation delay нескольких эр, chorus/flange/doubling как *режимы delay*, не doubler.
- Ampeg B-15N — vintage flip-top bass combo (подтверждено каталогом и общепринятым описанием модели).
- Pro-Q 3 / Pro-L 2 / CLA-2A — тип инструмента верный.

## Ошибки 2.4.8, исправленные в 2.4.9

- Слово `limiter` в kind/desc цепляло Busboy, консольные strips и HawkEye как «потолок пиков».
- `doubl` в тексте delay (ExoDelay) превращал его в «второй дубль».
- Семейство «riders» вешало на UltraPump «автоматический фейдер»; по kind это sidechain-pump.
- bx_rockrack сведён только к high-gain; у V3 восемь amp от clean JCM-800 до metal.

## Честные ограничения

- «В этой базе указан для …» — это карта каталога, не «официально только для этих источников». Pro-Q 3 в базе часто висит на барабанах, хотя это универсальный EQ.
- Описания остаются практическим пересказом, не цитатой manual.
