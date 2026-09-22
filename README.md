# Arena-ai-plugin-

Личный репозиторий проектов: офлайн-справочник аудиоплагинов, психологические книги и тетради, каталог обработанных фото.

## Структура

| Папка | Что внутри |
|---|---|
| `plugin-navigator/` | **Plugin Navigator 2.7.0** — автономный русскоязычный справочник аудиоплагинов и конструктор цепочек. `current/` — готовые файлы (HTML, Windows x64, инструкция, видео), `versions/` — архив версий 2.4.0–2.6.1, `reports/` — отчёты и аудиты, `source/` — исходники и сборка. Подробнее: [`plugin-navigator/README.md`](plugin-navigator/README.md) |
| `books/` | Психологические книги и тетради: лекции по клинической психологии, конспекты по СТ/ACT, тетради 12 шагов ВДА/ACA, тетрадь восстановления при алкоголизме |
| `therapy-workbooks/` | Терапевтические тетради: рабочая тетрадь «границы», дневник 12 шагов, гайд по генерации тетрадей |
| `AI_Photos_Catalog/` | Фото, обработанные с помощью ИИ: `processed/` — готовые, `originals/` — исходники «до» |
| `docs/` | Документы: `PROJECT_HANDOFF.md` — передаточный документ проекта |

## Быстрые ссылки

- Открыть приложение (офлайн HTML, без установки): `plugin-navigator/current/Plugin_Navigator_Full.html`
- Windows 10/11 x64 (portable): `plugin-navigator/current/Plugin_Navigator_Full_v2.7.0_Windows_x64.zip`
- Инструкция пользователя: `plugin-navigator/current/Plugin_Navigator_User_Guide_RU.html`
- Видеоинструкция (8:34, Full HD): `plugin-navigator/current/Plugin_Navigator_2.6.1_Video_Instruction_RU_Clean.mp4`
- Всё приложение одним архивом: `plugin-navigator/current/Plugin_Navigator_v2.7.0_Download.zip`
- Центр скачиваний книг: `index.html` в корне репозитория

## Сборка и проверка

Все сборочные скрипты — в `plugin-navigator/source/`:

```bash
cd plugin-navigator/source
python3 -m pip install -r requirements.txt
python3 build_and_test.py
```

Подробности — в [`plugin-navigator/README.md`](plugin-navigator/README.md).
