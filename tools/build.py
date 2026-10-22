#!/usr/bin/env python3
"""Собирает однофайловое веб-приложение «Тетрадь практики» из markdown.

Источник — папка с записями (по умолчанию examples/): папки К-NN,
_индекс.md, _неделя/*.md. Плюс START.md и format.md для вкладки «Как это работает».

Результат — app/тетрадь.html: один файл, данные внутри, работает офлайн
и без авторизации. Его же загружаем на Google Диск.

    python3 tools/build.py [источник] [выход]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

METRICS = [
    ("контакт", "Контакт", "#0e7490"),
    ("напряжение", "Напряжение", "#b45309"),
    ("вовлечённость", "Вовлечённость", "#15803d"),
    ("ясность", "Моя ясность", "#4f46e5"),
    ("усталость", "Моя усталость", "#b91c1c"),
]
METRIC_KEYS = [m[0] for m in METRICS]

TETRAD_FIELDS = [
    ("zapros", "Запрос"),
    ("formulirovka", "Формулировка"),
    ("dinamika", "Динамика"),
    ("riski", "Риски"),
    ("gipotezy", "Гипотезы"),
    ("proveryayu", "Что проверяю"),
    ("vstrechi", "Встречи"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_scores(line: str) -> dict[str, int]:
    scores: dict[str, int] = {}
    for key in METRIC_KEYS:
        m = re.search(rf"{key}\s*[:\-]?\s*([0-3])", line, re.IGNORECASE)
        if m:
            scores[key] = int(m.group(1))
    return scores


def split_sections(text: str) -> dict[str, str]:
    """Делит файл по '## Заголовок' на словарь нижний_регистр -> тело."""
    out: dict[str, str] = {}
    current = ""
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            out[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    out[current] = "\n".join(buf).strip()
    return out


def parse_session(path: Path) -> dict | None:
    text = read(path)
    lines = text.splitlines()
    head = ""
    for line in lines:
        if line.startswith("# "):
            head = line[2:].strip()
            break
    m = re.match(r"(?P<code>[^\s·]+)\s*·\s*встреча\s*(?P<n>\d+)\s*·\s*(?P<date>\d{4}-\d{2}-\d{2})", head)
    if not m:
        return None

    scores: dict[str, int] = {}
    focus = ""
    risk = ""
    for line in lines[:12]:
        s = line.strip()
        if s.lower().startswith("шкалы:"):
            scores = parse_scores(s)
        elif s.lower().startswith("фокус:"):
            focus = s[6:].strip()
        elif s.startswith("!") and "иск" in s:
            risk = s.lstrip("! ").replace("Риск:", "").strip()

    sections = split_sections(text)
    zapis = sections.get("Запись", "")
    otklik = ""
    otklik_date = ""
    razbor = ""
    razbor_date = ""
    for name, body in sections.items():
        low = name.lower()
        if low.startswith("отклик"):
            otklik = body
            otklik_date = name.split("·")[-1].strip() if "·" in name else ""
        elif low.startswith("разбор"):
            razbor = body
            razbor_date = name.split("·")[-1].strip() if "·" in name else ""

    return {
        "code": m.group("code"),
        "n": m.group("n"),
        "date": m.group("date"),
        "scores": scores,
        "focus": focus,
        "risk": risk,
        "zapis": zapis,
        "otklik": otklik,
        "otklikDate": otklik_date,
        "razbor": razbor,
        "razborDate": razbor_date,
        "file": path.name,
    }


def parse_tetrad(path: Path) -> dict:
    text = read(path)
    data: dict = {"updated": "", "gipotezy": []}
    m = re.search(r"Обновлено:\s*(\d{4}-\d{2}-\d{2})", text)
    if m:
        data["updated"] = m.group(1)

    # разбиваем по строкам вида **Метка:**
    marks = []
    for line in text.splitlines():
        mm = re.match(r"\*\*(.+?):\*\*\s*(.*)$", line.strip())
        if mm:
            marks.append((mm.group(1), mm.group(2), line))

    positions = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        mm = re.match(r"\*\*(.+?):\*\*", line.strip())
        if mm:
            positions.append((i, mm.group(1)))

    for idx, (i, label) in enumerate(positions):
        end = positions[idx + 1][0] if idx + 1 < len(positions) else len(lines)
        body_lines = lines[i:end]
        first = re.sub(r"^\*\*(.+?):\*\*\s*", "", body_lines[0].strip())
        rest = [ln.rstrip() for ln in body_lines[1:]]
        body = "\n".join([first] + rest).strip()

        key = None
        for attr, ru in TETRAD_FIELDS:
            if label.strip().lower() == ru.lower():
                key = attr
                break
        if not key:
            continue
        if key == "gipotezy":
            for ln in body.splitlines():
                gm = re.match(r"[-*]\s*\[(.+?)\]\s*(.+)", ln.strip())
                if gm:
                    data["gipotezy"].append({"status": gm.group(1).strip(), "text": gm.group(2).strip()})
        else:
            data[key] = body
    return data


def parse_index(path: Path) -> list[dict]:
    rows = []
    for line in read(path).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        if cells[0] in ("Код", "") or set(cells[0]) <= set("-: "):
            continue
        rows.append(
            {
                "code": cells[0],
                "zapros": cells[1],
                "vstrech": cells[2],
                "last": cells[3],
                "status": cells[4],
                "risk": cells[5],
            }
        )
    return rows


def collect(src: Path) -> dict:
    clients = []
    for folder in sorted(p for p in src.iterdir() if p.is_dir() and p.name.upper().startswith("К")):
        tetrad_path = folder / "_тетрадь.md"
        tetrad = parse_tetrad(tetrad_path) if tetrad_path.exists() else {}
        sessions = []
        for f in sorted(folder.glob("*.md")):
            if f.name.startswith("_"):
                continue
            s = parse_session(f)
            if s:
                sessions.append(s)
        sessions.sort(key=lambda s: (s["date"], s["n"]))
        clients.append(
            {
                "code": folder.name,
                "tetrad": tetrad,
                "sessions": sessions,
                "count": len(sessions),
                "last": sessions[-1]["date"] if sessions else "",
            }
        )

    index_path = src / "_индекс.md"
    index = parse_index(index_path) if index_path.exists() else []

    weeks = []
    week_dir = src / "_неделя"
    if week_dir.exists():
        for f in sorted(week_dir.glob("*.md")):
            weeks.append({"file": f.name, "text": read(f)})

    guide = []
    for name, title in [("START.md", "Начать здесь"), ("format.md", "Формат записей")]:
        p = (ROOT / name) if (ROOT / name).exists() else (src / name)
        if p.exists():
            guide.append({"title": title, "text": read(p)})

    return {
        "clients": clients,
        "index": index,
        "weeks": weeks,
        "guide": guide,
        "metrics": [{"key": k, "label": l, "color": c} for k, l, c in METRICS],
    }


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "examples"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "app" / "тетрадь.html"

    data = collect(src)
    template = read(ROOT / "app" / "template.html")
    html = template.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    # копия для локального просмотра: открывается по корню сервера
    (out.parent / "index.html").write_text(html, encoding="utf-8")
    print(f"{out} · клиентов: {len(data['clients'])} · встреч: {sum(c['count'] for c in data['clients'])}")


if __name__ == "__main__":
    main()
