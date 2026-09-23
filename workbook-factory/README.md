# workbook-factory — фабрика терапевтических рабочих тетрадей

Сборка авторских тетрадей (интерактивных веб-журналов и печатных воркбуков) из
JSON-спеки в **один автономный HTML-файл**. Принцип из
[`WORKBOOK_GENERATOR_GUIDE.md`](../therapy-workbooks/WORKBOOK_GENERATOR_GUIDE.md):
форма следует за клиентом и темой, а технические стандарты качества — неизменны.
Фабрика отвечает за второе: чтобы каждая новая тетрадь автоматически получала
офлайн-работу, мобильную вёрстку, автосохранение, экспорт и хорошую печать.

## Быстрый старт

```bash
cd workbook-factory
python3 build_workbook.py specs/separation_client.json     # собрать одну тетрадь
python3 build_workbook.py "specs/*.json"                   # собрать все
python3 build_workbook.py --list                           # список доступных блоков
python3 run_checks.py                                      # сборка + валидация + тесты
python3 publish_to_download_center.py specs/*.json         # в корневой index.html
```

Тесты рантайма требуют node и jsdom (один раз):

```bash
cd test-runtime && npm install jsdom@26 && cd ..
node test_workbook_runtime.js
```

## Структура

| Путь | Что это |
|---|---|
| `engine/template.html` | Каркас страницы: шапка, оглавление, разделы, подключение движка |
| `engine/engine.css` | Токены тем (light/dark/auto), все компоненты, мобильная адаптация, `@media print` |
| `engine/engine.js` | Навигация, автосохранение, счётчик, реестр механик, «Моя карта», экспорт, печать |
| `specs/*.json` | Содержание тетрадей: шаги, вопросы, механики |
| `build_workbook.py` | Сборщик: спека → single-file HTML + валидация |
| `run_checks.py` | Единые проверки: сборка, синтаксис JS, jsdom-тесты, центр скачиваний |
| `test_workbook_runtime.js` | Функциональные тесты готового файла в jsdom (102 проверки на тетрадь) |
| `publish_to_download_center.py` | Публикация карточек в корневой `index.html` (base64, идемпотентно) |
| `test-runtime/` | node_modules для тестов (в git не попадает) |

Готовые файлы кладутся в `therapy-workbooks/` (`meta.output_dir`).

## Спека тетради

```jsonc
{
  "meta": {
    "id": "separation-client",
    "filename": "separation_workbook.html",   // имя готового файла
    "output_dir": "../../therapy-workbooks",  // относительно папки specs/
    "title": "…",            // <title> и заголовок вкладки
    "bar_title": "…",        // название в шапке
    "bar_sub": "…",          // подпись в шапке (версия, аудитория)
    "version": "1.0",
    "description": "…",      // meta description
    "storage_key": "sep-client-v1",          // ключ localStorage (у каждой тетради свой!)
    "export_title": "…",     // первая строка отчёта .txt
    "export_filename": "otchet_….txt",
    "toc_note": "…",         // подпись под оглавлением
    "sos": { "label": "…", "href": "s5", "title": "…" },  // красная кнопка в шапке
    "css": "…",              // переопределение токенов темы (акцент тетради)
    "download_center": { "title": "…", "desc": "…", "badge": "…", "highlight": true }
  },
  "steps": [ { "id": "front", … }, { "id": "s1", … }, … ],
  "map":   { "title": "…", "blocks": [ … ], "privacy": "…" }
}
```

Шаг:

```jsonc
{
  "id": "s1",                    // обязателен, уникален (id раздела и якорь)
  "num": "1",                    // номер в кружке и в оглавлении
  "toc": "Где я сейчас",         // короткий пункт оглавления
  "export_name": "ШАГ 1 · …",    // заголовок раздела в отчёте .txt
  "badge": "Неделя 1 · Встреча 1",
  "badge_tone": "succ",          // acc | sos | succ | warn | pro
  "title": "Шаг 1 · …",
  "lead": "Одна вводная фраза",
  "blocks": [ … ]
}
```

Первый шаг — титул (`id: "front"`, печатается `h1`, без разрыва страницы).
Раздел «Моя карта» (`id: "map"`) достраивается автоматически: прогресс по шагам,
кнопки экспорта/печати/очистки, блок приватности.

## Палитра блоков

### Текст и структура
| Блок | Назначение | Ключевые поля |
|---|---|---|
| `para` | Абзац | `text` |
| `html` | Произвольная разметка (теория, списки) | `html` |
| `callout` | Акцентная рамка | `tone`: `core`, `flags`, `warn`, `succ`, `note`, `card`; `title`, `html`/`text`/`list` |
| `lesson` | Карточка психообразования | `title`, `badge`, `html`/`list` |
| `course_map` | Карта курса (недели) | `items: [{label, text}]` |
| `deeper` | Сворачиваемый уровень глубины | `level`: `full` / `childhood` / `practice` / `extra`; `title`, `blocks` |
| `session` | Блок «★ Для встречи с психологом» | `title`, `blocks` |
| `therapist` | Блок «для специалиста» (фиолетовый) | `title`, `tag`, `blocks` |
| `lines` | Линейки для письма от руки (экран + печать) | `count`, `label` |

### Задания
| Блок | Механика | Ключевые поля |
|---|---|---|
| `question` | Вопрос с полем | `id`, `label`, `hint`, `placeholder`, `rows`, `kind`: `textarea`/`text`/`select` (+`options`), `tone` |
| `grid` | Сетка карточек-вопросов | `cols` (2 или 3), `items` |
| `checklist` | Чек-лист | `title`, `hint`, `cols`, `items: [{id, label, hint}]` |
| `scale` | Шкала 0–10 с якорями | `id`, `label`, `min`, `max`, `anchors: {"0": "…", "5": "…", "10": "…"}` |
| `sort_matrix` | Сортировочная матрица | `columns: [{key,label}]`, `items: [{id,label,hint}]` |
| `cog_table` | Когнитивная таблица с добавлением строк | `columns: [{key,label,placeholder}]`, `rows`, `max_rows` |
| `diary` | Дневник повторяющихся записей | `fields: [{key,label,placeholder,kind,options}]`, `badge_field`, `badge_label`, `quick: [{field,value,label}]`, `empty` |
| `circles` | Круги близости | `rings: [{key,label,tone,hint,placeholder}]` |
| `rating_list` | Рейтинги зон (телесная карта) | `items: [{id,label}]`, `levels: [{value,label,tone}]` |
| `dialog_trainer` | Тренажёр фраз | `scenario`, `turns: [{label, options:[{text,note}]}]`, `target` (вопрос-скрипт, куда вставляются фразы) |
| `permission_cards` | Карточки-разрешения | `preset: [строки]`, `custom_placeholder` |
| `breather` | Дыхание и таймер паузы | `inhale`, `hold`, `exhale`, `countdown_minutes`, `tone`, `start_label` |

`diary` — универсальная механика: дневник тяги, дневник согласий, дневник своих
решений и трекер микро-побед собираются одним блоком с разным набором `fields`.

## Варианты: клиентская и профессиональная версии из одной базы

Профессиональная версия не дублирует содержание — она наследует клиентскую и
добавляет методический слой:

```jsonc
{
  "variant_of": "separation_client.json",
  "meta": { "filename": "…_therapist_workbook.html", "storage_key": "sep-pro-v1", … },
  "step_patch":    [ { "step": "front", "title": "…", "badge": "…", "badge_tone": "pro" } ],
  "inject":        [ { "step": "s1", "at": "start", "blocks": [ { "type": "therapist", … } ] } ],
  "map_inject":    [ { "at": "end", "blocks": [ … ] } ],
  "remove_blocks": [ { "step": "s3", "bids": ["s3_breath"] } ],
  "append_steps":  [ { "id": "s8", … } ]
}
```

* `at` — `"start"`, `"end"` или `{"after_bid": "…"}` / `{"before_bid": "…"}`
  (для якоря у блока в базовой спеке должно быть поле `bid`).
* `meta` варианта переопределяет поля базовой (обязательно меняйте `filename`,
  `storage_key`, `export_filename` — иначе две тетради затрут данные друг друга).
* Порядок `inject` сохраняется: блоки добавляются в указанной последовательности.

## Стандарты качества (что фабрика гарантирует)

1. **Один файл, офлайн.** Никаких внешних зависимостей, шрифтов и сети.
2. **Темы.** `light / dark / auto` переключателем в шапке; акцент темы задаётся в `meta.css`.
3. **Автосохранение.** Каждое поле, чекбокс, шкала и состояние механики пишется в
   `localStorage` сразу; есть индикатор «сохранено ✓» и счётчик заполнения.
4. **Экспорт.** Кнопка в шапке и на «Моей карте» собирает ответы в `.txt`
   (BOM + UTF-8): разделы по шагам, вопросы, чек-листы, состояния механик.
5. **Печать.** `@media print` раскрывает все разделы и блоки глубины, прячет
   кнопки, оставляет линейки для письма, не рвёт карточки между страницами.
6. **Мобильная вёрстка.** Оглавление — drawer, сетки сворачиваются в одну
   колонку, размер шрифта полей 16px (iOS не зумит при фокусе).
7. **Навигация.** Оглавление с поиском, «←/→» между шагами, горячая клавиша `M`, хэш в URL.
8. **Валидация сборки.** Сборщик и `run_checks.py` проверяют: уникальность id,
   незаполненные токены шаблона, баланс тегов, соответствие `WB_SPEC` разделам,
   наличие реализации у каждой механики, синтаксис JS, поведение в jsdom,
   совпадение base64 в центре скачиваний с файлом на диске.

## Как сделать новую тетрадь (рецепт)

1. Скопируйте ближайшую по духу спеку (`specs/*.json`) в новый файл, например
   `specs/anxiety_client.json`.
2. Замените `meta`: **обязательно новые** `id`, `filename`, `storage_key`,
   `export_filename`; подберите акцент в `meta.css`.
3. Соберите шаги: `front` (титул + экран безопасности + карта курса), 3–12 шагов,
   каждый со своей механикой (не копируйте набор заданий из прошлой тетради).
4. Соберите и посмотрите: `python3 build_workbook.py specs/anxiety_client.json`,
   затем откройте файл в браузере или через `python3 -m http.server`.
5. `python3 run_checks.py` — прогонит валидацию и тесты.
6. Добавьте карточку в `therapy-workbooks/index.html` и опубликуйте в корневом
   центре скачиваний: `python3 publish_to_download_center.py specs/anxiety_client.json`.
7. Обновите `therapy-workbooks/README.md` и корневой `README.md`.

## Безопасность содержания (не техники, а клиники)

* В каждой тетради на титуле — **экран безопасности**: когда самостоятельная работа
  противопоказана и что делать вместо неё.
* Глубокие блоки (`childhood`) всегда предупреждают о риске и отсылают к
  стоп-протоколу: остановить письмо → заземление «5-4-3-2-1» → живой человек.
* Поля со ★ попадают в экспорт — клиент сам решает, что показать специалисту.
* Профессиональная версия не передаётся клиенту (см. блок «Этика версий»).
