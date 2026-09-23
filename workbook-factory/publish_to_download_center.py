#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Публикация собранных тетрадей в корневой центр скачиваний (index.html).

Центр скачиваний хранит файлы прямо в странице (base64), чтобы всё работало
офлайн и в один клик. Скрипт идемпотентен: карточка с тем же именем файла
заменяется, а не дублируется.

Использование:
    python3 publish_to_download_center.py specs/separation_client.json specs/separation_therapist.json
    python3 publish_to_download_center.py specs/*.json --dry-run
    python3 publish_to_download_center.py specs/separation_client.json --remove
"""
from __future__ import annotations

import argparse
import base64
import glob
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
INDEX = REPO_ROOT / "index.html"

CARD = """  <!-- {comment} -->
  <div class="card"{style}>
    <div class="card-header">
      <span class="title">{title}</span>
      <span class="badge{badge_class}">{badge}</span>
    </div>
    <div class="desc">
      {desc}
    </div>
    <div class="btn-group">
      <button class="btn btn-primary" onclick="downloadB64('{b64}', '{filename}', 'text/html')">⬇ Скачать файл (.html)</button>
      <button class="btn btn-secondary" onclick="openB64InTab('{b64}', 'text/html')">👁 Открыть в браузере</button>
    </div>
  </div>

"""

INSERT_ANCHORS = [
    "  <!-- ОБЩИЙ ZIP АРХИВ -->",
    '  <div class="card" style="background: #eff6ff;',
]


def esc(text) -> str:
    return html.escape(str(text or ""), quote=False)


def load_spec(path: Path):
    """Возвращает (merged_meta, путь к собранному файлу). Варианты наследуют meta базовой спеки."""
    spec = json.loads(path.read_text(encoding="utf-8"))
    merged = dict(spec.get("meta", {}))
    base_ref = spec.get("variant_of")
    guard = 0
    cur = path
    while base_ref and guard < 5:
        cur = (cur.parent / base_ref).resolve()
        base = json.loads(cur.read_text(encoding="utf-8"))
        base_meta = dict(base.get("meta", {}))
        base_meta.update(merged)
        merged = base_meta
        base_ref = base.get("variant_of")
        guard += 1
    out = (path.parent / merged.get("output_dir", "..")).resolve() / merged["filename"]
    return merged, out


def base_dir(path: Path) -> Path:
    return path.parent


def card_for_file(html_path: Path, title=None, desc=None, badge=None,
                  comment=None, style="", highlight=False):
    """Карточка для готового HTML-файла, собранного не фабрикой."""
    if not html_path.exists():
        raise SystemExit("Файл не найден: %s" % html_path)
    payload = html_path.read_bytes()
    doc = payload.decode("utf-8", "ignore")
    if not title:
        m = re.search(r"<title>(.*?)</title>", doc, re.S)
        title = m.group(1).strip() if m else html_path.stem
    if not desc:
        m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', doc, re.S)
        desc = m.group(1).strip() if m else ""
    desc = re.sub(r"\s+", " ", desc)
    if len(desc) > 340:
        desc = desc[:337].rstrip() + "…"
    b64 = base64.b64encode(payload).decode("ascii")
    if base64.b64decode(b64) != payload:
        raise SystemExit("base64 не сошёлся при проверке: %s" % html_path)
    return CARD.format(
        comment=esc(comment or ("ТЕТРАДЬ: %s" % html_path.name.upper())), style=style,
        title=esc(title), badge_class=" badge-new" if highlight else "",
        badge=esc(badge or "Тетрадь"), desc=esc(desc),
        b64=b64, filename=esc(html_path.name),
    ), html_path.name


def card_for(spec_path: Path):
    meta, out = load_spec(spec_path)
    if not out.exists():
        raise SystemExit("Файл не собран: %s — сначала запустите build_workbook.py" % out)
    payload = out.read_bytes()
    b64 = base64.b64encode(payload).decode("ascii")
    if base64.b64decode(b64) != payload:  # страховка от повреждённой вставки
        raise SystemExit("base64 не сошёлся при проверке: %s" % out)

    dc = meta.get("download_center") or {}
    title = dc.get("title") or meta.get("title") or out.stem
    desc = dc.get("desc") or meta.get("description") or ""
    if len(desc) > 340:
        desc = desc[:337].rstrip() + "…"
    badge = dc.get("badge") or ("Версия %s" % meta.get("version", "1.0"))
    badge_class = " badge-new" if dc.get("highlight") else ""
    style = dc.get("style") or ""
    comment = dc.get("comment") or ("ТЕТРАДЬ: %s" % out.name.upper())

    return CARD.format(
        comment=esc(comment), style=style, title=esc(title),
        badge_class=badge_class, badge=esc(badge), desc=esc(desc),
        b64=b64, filename=esc(out.name),
    ), out.name


def remove_card(doc: str, filename: str):
    """Удаляет существующую карточку с этим именем файла (вместе с комментарием над ней)."""
    marker = "'%s', 'text/html')" % filename
    idx = doc.find(marker)
    if idx < 0:
        return doc, False
    start = doc.rfind('  <div class="card"', 0, idx)
    if start < 0:
        return doc, False
    comment = doc.rfind("  <!--", 0, start)
    if comment >= 0 and start - comment < 220:
        start = comment
    # ищем конец карточки, считая вложенность <div>
    depth, pos = 0, start
    tag_re = re.compile(r"</?div\b")
    while True:
        m = tag_re.search(doc, pos)
        if not m:
            return doc, False
        if m.group(0) == "<div":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = doc.find("\n", m.end()) + 1
                if doc[end:end + 1] == "\n":
                    end += 1
                return doc[:start] + doc[end:], True
        pos = m.end()


def insert(doc: str, card: str) -> str:
    for anchor in INSERT_ANCHORS:
        i = doc.find(anchor)
        if i > 0:
            return doc[:i] + card + doc[i:]
    marker = '<div class="toast"'
    i = doc.rfind("</div>", 0, doc.find(marker))
    if i < 0:
        raise SystemExit("Не нашёл, куда вставить карточку в index.html")
    return doc[:i] + card + doc[i:]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Публикация тетрадей в корневой центр скачиваний")
    ap.add_argument("specs", nargs="+",
                    help="спеки тетрадей (.json) или готовые HTML-файлы (.html)")
    ap.add_argument("--title", help="заголовок карточки (для .html)")
    ap.add_argument("--desc", help="описание карточки (для .html)")
    ap.add_argument("--badge", help="бейдж карточки (для .html)")
    ap.add_argument("--highlight", action="store_true", help="подсветить карточку как новую")
    ap.add_argument("--index", default=str(INDEX), help="путь к центру скачиваний")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--remove", action="store_true", help="убрать карточки этих файлов")
    args = ap.parse_args(argv)

    index = Path(args.index)
    doc = index.read_text(encoding="utf-8")
    before = len(doc.encode("utf-8"))

    paths = []
    for p in args.specs:
        matched = sorted(glob.glob(p))
        paths.extend(Path(m) for m in matched) if matched else paths.append(Path(p))

    for path in paths:
        standalone = path.suffix.lower() == ".html"
        if args.remove:
            out_name = path.name if standalone else load_spec(path)[1].name
            doc, removed = remove_card(doc, out_name)
            print("%s %s" % ("− удалена карточка" if removed else "= карточка не найдена", out_name))
            continue
        if standalone:
            card, name = card_for_file(path, title=args.title, desc=args.desc,
                                       badge=args.badge, highlight=args.highlight)
        else:
            card, name = card_for(path)
        doc, existed = remove_card(doc, name)
        doc = insert(doc, card)
        print("%s %s (%d КБ в base64)"
              % ("↻ обновлена" if existed else "+ добавлена", name, len(card) // 1024))

    after = len(doc.encode("utf-8"))
    print("index.html: %d КБ → %d КБ (%+d КБ)" % (before // 1024, after // 1024, (after - before) // 1024))

    # целостность страницы
    if doc.count("<div") != doc.count("</div>"):
        print("! внимание: количество <div> и </div> не совпадает — проверьте файл вручную")
    if "@@" in doc or "<BASE64>" in doc:
        raise SystemExit("в index.html остались служебные маркеры")

    if args.dry_run:
        print("(dry-run: файл не записан)")
        return 0
    index.write_text(doc, encoding="utf-8")
    print("✓ %s обновлён" % index)
    return 0


if __name__ == "__main__":
    sys.exit(main())
