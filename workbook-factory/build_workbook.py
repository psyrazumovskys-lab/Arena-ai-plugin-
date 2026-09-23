#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборщик терапевтических рабочих тетрадей (workbook-factory).

Превращает JSON-спеку тетради в один автономный HTML-файл:
офлайн, адаптив под телефон, light/dark/auto, автосохранение в localStorage,
экспорт ответов .txt для психолога, аккуратная печать.

Использование:
    python3 build_workbook.py specs/separation_client.json
    python3 build_workbook.py specs/*.json --check      # собрать и провалидировать
    python3 build_workbook.py --list                    # список типов блоков

Спека может быть «вариантом» другой спеки (variant_of) — так из одной базы
собираются клиентская и профессиональная версии тетради.
"""
from __future__ import annotations

import argparse
import copy
import glob
import html
import json
import os
import sys
from pathlib import Path

FACTORY_VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
ENGINE_DIR = HERE / "engine"
TEMPLATE = ENGINE_DIR / "template.html"
ENGINE_CSS = ENGINE_DIR / "engine.css"
ENGINE_JS = ENGINE_DIR / "engine.js"

TONES = {"acc", "sos", "succ", "warn", "pro", "plain"}
CALLOUT_CLASS = {
    "core": "core",
    "flags": "flags",
    "warn": "warn-box",
    "succ": "succ-box",
    "note": "note-box",
    "card": "card",
}
DEPTH_LABEL = {
    "full": "полный формат",
    "childhood": "из детства",
    "extra": "дополнительно",
    "practice": "практика",
}


# --------------------------------------------------------------------------- #
#  Утилиты
# --------------------------------------------------------------------------- #
def esc(text) -> str:
    """Экранирование для HTML-текста."""
    if text is None:
        return ""
    return html.escape(str(text), quote=False)


def attr(text) -> str:
    """Экранирование для значения атрибута."""
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def spec_attr(obj) -> str:
    """JSON-конфигурация механики в атрибуте data-spec."""
    return html.escape(json.dumps(obj, ensure_ascii=False), quote=True)


def content_html(node: dict) -> str:
    """Содержимое блока: html | text | list | items."""
    if not isinstance(node, dict):
        return ""
    if node.get("html"):
        return str(node["html"])
    parts = []
    if node.get("text"):
        parts.append("<p>%s</p>" % esc(node["text"]))
    lst = node.get("list") or node.get("items")
    if lst:
        ordered = node.get("ordered")
        tag = "ol" if ordered else "ul"
        parts.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % esc(x) for x in lst), tag))
    return "".join(parts)


class Ctx:
    """Контекст сборки: шаг, уникальные id, предупреждения."""

    def __init__(self):
        self.step = ""
        self.ids: set[str] = set()
        self.dupes: list[str] = []
        self.warnings: list[str] = []
        self.widget_seq = 0
        self.stats = {"fields": 0, "checks": 0, "widgets": 0}

    def uniq(self, base: str) -> str:
        if not base:
            base = "id"
        if base not in self.ids:
            self.ids.add(base)
            return base
        self.dupes.append(base)
        n = 2
        while "%s_%d" % (base, n) in self.ids:
            n += 1
        new = "%s_%d" % (base, n)
        self.ids.add(new)
        return new

    def wid(self, kind: str) -> str:
        self.widget_seq += 1
        return "w_%s_%d" % (kind, self.widget_seq)


# --------------------------------------------------------------------------- #
#  Рендереры блоков
# --------------------------------------------------------------------------- #
RENDERERS = {}


def block(kind):
    def deco(fn):
        RENDERERS[kind] = fn
        return fn
    return deco


def render_blocks(blocks, ctx: Ctx) -> str:
    out = []
    for b in blocks or []:
        out.append(render_block(b, ctx))
    return "\n".join(x for x in out if x)


def render_block(b, ctx: Ctx) -> str:
    if not isinstance(b, dict):
        ctx.warnings.append("блок не является объектом: %r" % (b,))
        return ""
    kind = b.get("type")
    fn = RENDERERS.get(kind)
    if fn is None:
        raise SystemExit("Неизвестный тип блока: %r (доступные: %s)"
                         % (kind, ", ".join(sorted(RENDERERS))))
    return fn(b, ctx)


@block("para")
def r_para(b, ctx):
    return "<p>%s</p>" % esc(b.get("text", ""))


@block("html")
def r_html(b, ctx):
    return str(b.get("html", ""))


@block("callout")
def r_callout(b, ctx):
    cls = CALLOUT_CLASS.get(b.get("tone", "note"), "note-box")
    title = "<h4 style=\"margin-top:0;\">%s</h4>" % esc(b["title"]) if b.get("title") else ""
    return '<div class="%s">%s%s</div>' % (cls, title, content_html(b))


@block("lesson")
def r_lesson(b, ctx):
    title = "<h3 style=\"margin-top:0;\">%s</h3>" % esc(b["title"]) if b.get("title") else ""
    badge = '<span class="badge">%s</span>' % esc(b["badge"]) if b.get("badge") else ""
    return '<div class="card">%s%s%s</div>' % (badge, title, content_html(b))


@block("course_map")
def r_course_map(b, ctx):
    title = "<h3>%s</h3>" % esc(b["title"]) if b.get("title") else ""
    cells = "".join(
        '<div class="course-week"><b>%s</b>%s</div>' % (esc(i.get("label", "")), esc(i.get("text", "")))
        for i in b.get("items", [])
    )
    return '%s<div class="course-map">%s</div>' % (title, cells)


def _field(b, ctx, *, card=False) -> str:
    """Одно поле ввода (textarea / text / select)."""
    fid = ctx.uniq(b.get("id") or "q")
    ctx.stats["fields"] += 1
    kind = b.get("kind", "textarea")
    rows = int(b.get("rows", 4))
    ph = attr(b.get("placeholder", ""))
    label = b.get("label", "")
    data = ('class="qf" id="%s" data-step="%s" data-q="%s" data-export="field"'
            % (attr(fid), attr(ctx.step), attr(label)))
    if kind == "text":
        ctl = '<input type="text" %s placeholder="%s">' % (data, ph)
    elif kind == "select":
        opts = "".join('<option value="">— выберите —</option>') + "".join(
            "<option>%s</option>" % esc(o) for o in b.get("options", []))
        ctl = "<select %s>%s</select>" % (data, opts)
    else:
        ctl = '<textarea %s rows="%d" placeholder="%s"></textarea>' % (data, rows, ph)
    hint = '<p class="qhint">%s</p>' % esc(b["hint"]) if b.get("hint") else ""
    sav = '<span class="sav" data-for="%s">— сохранено ✓</span>' % attr(fid)
    if card:
        tone = b.get("tone", "acc")
        tone_attr = "" if tone not in TONES else ' data-tone="%s"' % tone
        return ('<div class="qcard"%s><div class="qcard-title">%s</div>%s%s%s</div>'
                % (tone_attr, esc(label), hint, ctl, sav))
    return ('<div class="qblock"><div class="qlabel"><span>%s</span>%s</div>%s%s</div>'
            % (esc(label), sav, hint, ctl))


@block("question")
def r_question(b, ctx):
    return _field(b, ctx, card=False)


@block("grid")
def r_grid(b, ctx):
    cols = int(b.get("cols", 2))
    inner = "".join(_field(i, ctx, card=True) if i.get("type", "question") == "question"
                    else render_block(i, ctx) for i in b.get("items", []))
    return '<div class="grid-2x2" data-cols="%d">%s</div>' % (cols, inner)


@block("checklist")
def r_checklist(b, ctx):
    title = b.get("title", "")
    head = '<div class="chk-title">%s</div>' % esc(title) if title else ""
    hint = '<p class="qhint">%s</p>' % esc(b["hint"]) if b.get("hint") else ""
    rows = []
    for it in b.get("items", []):
        iid = ctx.uniq(it.get("id") or "chk")
        ctx.stats["checks"] += 1
        h = '<span class="chk-hint">%s</span>' % esc(it["hint"]) if it.get("hint") else ""
        rows.append('<label class="chk-card"><input type="checkbox" id="%s" data-step="%s">'
                    "<span>%s%s</span></label>" % (attr(iid), attr(ctx.step), esc(it.get("label", "")), h))
    cols = int(b.get("cols", 1))
    return ('<div class="chk-wrap" data-export="checklist" data-q="%s" data-step="%s">%s%s'
            '<div class="chk-grid" data-cols="%d">%s</div></div>'
            % (attr(title), attr(ctx.step), head, hint, cols, "".join(rows)))


@block("scale")
def r_scale(b, ctx):
    fid = ctx.uniq(b.get("id") or "scale")
    ctx.stats["fields"] += 1
    lo, hi = int(b.get("min", 0)), int(b.get("max", 10))
    val = b.get("value", lo)
    anchors = b.get("anchors") or {}
    a_html = ""
    if anchors:
        keys = sorted(anchors.keys(), key=lambda x: int(x))
        a_html = '<div class="scale-anchors">%s</div>' % "".join(
            "<span>%s — %s</span>" % (esc(k), esc(anchors[k])) for k in keys)
    label = b.get("label", "")
    hint = '<p class="qhint">%s</p>' % esc(b["hint"]) if b.get("hint") else ""
    sav = '<span class="sav" data-for="%s">— сохранено ✓</span>' % attr(fid)
    return (
        '<div class="scale-widget">'
        '<div class="scale-head"><div style="flex:1;min-width:200px;">'
        '<div class="qlabel"><span>%s</span>%s</div>%s</div>'
        '<output class="scale-value" data-for="%s">%s</output></div>'
        '<input type="range" class="rng" id="%s" min="%d" max="%d" step="%s" value="%s" '
        'data-step="%s" data-q="%s" data-export="field">'
        "%s</div>"
        % (esc(label), sav, hint, attr(fid), esc(val), attr(fid), lo, hi,
           attr(b.get("step", 1)), attr(val), attr(ctx.step), attr(label), a_html)
    )


@block("lines")
def r_lines(b, ctx):
    n = int(b.get("count", 5))
    label = '<div class="wlines-label">%s</div>' % esc(b["label"]) if b.get("label") else ""
    return '<div class="wlines">%s%s</div>' % (label, '<div class="wline"></div>' * n)


@block("deeper")
def r_deeper(b, ctx):
    level = b.get("level", "full")
    tag = esc(b.get("tag") or DEPTH_LABEL.get(level, level))
    body = render_blocks(b.get("blocks", []), ctx)
    return ('<details class="deeper" data-level="%s" data-export="section" data-q="[%s] %s" '
            'data-step="%s"><summary><span>%s</span>'
            '<span class="depth-tag">%s</span></summary><div class="deeper-body">%s</div></details>'
            % (attr(level), attr(tag), attr(b.get("title", "Глубже")), attr(ctx.step),
               esc(b.get("title", "Глубже")), tag, body))


@block("session")
def r_session(b, ctx):
    title = b.get("title", "Для встречи с психологом")
    body = render_blocks(b.get("blocks", []), ctx)
    return ('<div class="session-block" data-export="section" data-q="★ %s" data-step="%s">'
            '<div class="sb-title">★ %s</div>%s</div>'
            % (attr(title), attr(ctx.step), esc(title), body))


@block("therapist")
def r_therapist(b, ctx):
    title = b.get("title", "Комментарий для специалиста")
    body = render_blocks(b.get("blocks", []), ctx)
    return ('<div class="pro-block"><span class="pro-tag">%s</span>'
            '<div class="sb-title">🧭 %s</div>%s</div>'
            % (esc(b.get("tag", "для специалиста")), esc(title), body))


def _widget_root(b, ctx, kind: str, inner: str, title: str) -> str:
    wid = ctx.uniq(b.get("wid") or ctx.wid(kind))
    ctx.stats["widgets"] += 1
    wspec = {k: v for k, v in b.items()
             if k not in {"type", "id", "wid", "title", "hint", "step", "bid"}}
    head = "<h3>%s</h3>" % esc(title) if title else ""
    hint = '<p class="qhint">%s</p>' % esc(b["hint"]) if b.get("hint") else ""
    return ('<div class="widget widget-%s" data-widget="%s" data-wid="%s" data-spec="%s" '
            'data-step="%s" data-export="widget" data-q="%s">%s%s%s</div>'
            % (attr(kind), attr(kind), attr(wid), spec_attr(wspec), attr(ctx.step),
               attr(title), head, hint, inner))


MATRIX_PALETTE = ["var(--acc)", "var(--warn)", "var(--mut)", "var(--succ)", "var(--sos)", "var(--pro)"]


@block("sort_matrix")
def r_sort_matrix(b, ctx):
    cols = b.get("columns", [])
    legend = '<div class="matrix-legend">%s</div>' % "".join(
        '<b><i style="background:%s"></i>%s</b>'
        % (c.get("color") or MATRIX_PALETTE[i % len(MATRIX_PALETTE)], esc(c.get("label", "")))
        for i, c in enumerate(cols))
    return _widget_root(b, ctx, "sort_matrix", '<div class="matrix">%s</div>' % legend,
                        b.get("title", ""))


@block("cog_table")
def r_cog_table(b, ctx):
    inner = ('<div class="ctable"></div>'
             '<button type="button" class="btn btn-sm" data-act="add-row">+ Добавить строку</button>')
    return _widget_root(b, ctx, "cog_table", inner, b.get("title", ""))


@block("diary")
def r_diary(b, ctx):
    inner = (
        '<div class="chip-container"></div>'
        '<div class="diary-form"><div class="diary-form-grid"></div>'
        '<div style="margin-top:.85rem;display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;">'
        '<button type="button" class="btn btn-primary btn-sm" data-act="add-entry">+ Добавить запись</button>'
        '<span class="counter" data-role="count">0 записей</span></div></div>'
        '<div class="diary-list"></div>'
    )
    return _widget_root(b, ctx, "diary", inner, b.get("title", ""))


@block("circles")
def r_circles(b, ctx):
    return _widget_root(b, ctx, "circles", '<div class="rings"></div>', b.get("title", ""))


@block("rating_list")
def r_rating_list(b, ctx):
    return _widget_root(b, ctx, "rating_list", '<div class="rating-list"></div>', b.get("title", ""))


@block("permission_cards")
def r_permission_cards(b, ctx):
    inner = (
        '<div class="pcards"></div>'
        '<div class="diary-form"><div class="ring-input">'
        '<input type="text" data-role="new-card" placeholder="%s">'
        '<button type="button" class="btn btn-sm" data-act="add-card">Добавить</button>'
        "</div></div>" % attr(b.get("custom_placeholder", "Моя формулировка разрешения…"))
    )
    return _widget_root(b, ctx, "permission_cards", inner, b.get("title", ""))


@block("dialog_trainer")
def r_dialog_trainer(b, ctx):
    parts = []
    if b.get("scenario"):
        parts.append('<div class="dlg-scenario">🎭 %s</div>' % esc(b["scenario"]))
    parts.append('<div class="dlg">')
    for turn in b.get("turns", []):
        opts = []
        for o in turn.get("options", []):
            text = o.get("text") if isinstance(o, dict) else o
            note = o.get("note") if isinstance(o, dict) else None
            note_html = '<span class="dlg-note">%s</span>' % esc(note) if note else ""
            opts.append('<button type="button" class="dlg-opt" data-text="%s">%s%s</button>'
                        % (attr(text), esc(text), note_html))
        parts.append('<div class="dlg-turn"><div class="dlg-turn-label">%s</div>%s</div>'
                     % (esc(turn.get("label", "")), "".join(opts)))
    parts.append("</div>")
    tgt = b.get("target")
    if tgt:
        parts.append('<div class="dlg-target">')
        old_step = ctx.step
        rendered = _field(dict(tgt, type="question"), ctx)
        ctx.step = old_step
        # помечаем целевое поле для вставки фраз
        rendered = rendered.replace('<textarea class="qf"', '<textarea data-role="target-field" class="qf"', 1)
        parts.append(rendered + "</div>")
    return _widget_root(b, ctx, "dialog_trainer", "".join(parts), b.get("title", ""))


@block("breather")
def r_breather(b, ctx):
    minutes = int(b.get("countdown_minutes", 0) or 0)
    display = ""
    if minutes:
        display = '<div class="timer-display">%02d:00</div>' % minutes
    reset_btn = ('<button type="button" class="btn btn-ghost btn-sm" data-act="reset">↺ Сброс</button>'
                 if minutes else "")
    start_label = esc(b.get("start_label", "▶ Начать"))
    inner = (
        '<div class="timer-widget" data-tone="%s">'
        "%s%s"
        '<div class="timer-controls">'
        '<button type="button" class="btn btn-primary" data-act="start">%s</button>'
        '<button type="button" class="btn" data-act="pause" style="display:none">⏸ Пауза</button>'
        "%s</div>"
        '<div class="breather-container"><div class="breather-circle"></div>'
        '<div class="breather-text">%s</div></div></div>'
        % (attr(b.get("tone", "acc")),
           ("<h3>%s</h3>" % esc(b["title"]) if b.get("title") else ""),
           display, start_label, reset_btn,
           esc(b.get("idle_text", "Нажмите «Начать», когда будете готовы.")))
    )
    # breather — декоративная механика, в отчёт не экспортируется
    wid = ctx.uniq(b.get("wid") or ctx.wid("breather"))
    ctx.stats["widgets"] += 1
    wspec = {k: v for k, v in b.items()
             if k not in {"type", "id", "wid", "title", "hint", "step", "bid", "tone",
                          "start_label", "idle_text"}}
    hint = '<p class="qhint">%s</p>' % esc(b["hint"]) if b.get("hint") else ""
    return ('<div class="widget widget-breather" data-widget="breather" data-wid="%s" data-spec="%s" '
            'data-step="%s">%s%s</div>' % (attr(wid), spec_attr(wspec), attr(ctx.step), hint, inner))


# --------------------------------------------------------------------------- #
#  Разделы (шаги)
# --------------------------------------------------------------------------- #
def render_step(step: dict, ctx: Ctx, *, is_first=False) -> str:
    sid = step["id"]
    ctx.step = sid
    badge = '<span class="badge%s">%s</span>' % (
        " badge-%s" % step["badge_tone"] if step.get("badge_tone") else "", esc(step["badge"])) \
        if step.get("badge") else ""
    lead = '<p class="lead">%s</p>' % esc(step["lead"]) if step.get("lead") else ""
    body = render_blocks(step.get("blocks", []), ctx)
    act = " act" if is_first else ""
    if sid == "front":
        head = "<h1>%s</h1>" % esc(step.get("title", ""))
    else:
        num = step.get("num", "")
        num_html = '<span class="num">%s</span>' % esc(num) if num != "" else ""
        head = "<h2>%s%s</h2>" % (num_html, esc(step.get("title", "")))
    return '<section class="lec%s" id="%s">\n%s\n%s%s\n%s\n</section>' % (act, attr(sid), badge, head, lead, body)


def render_map(spec: dict, ctx: Ctx) -> str:
    m = spec.get("map") or {}
    sid = "map"
    ctx.step = sid
    blocks = render_blocks(m.get("blocks", []), ctx)
    title = m.get("title", "Моя карта и итоги")
    privacy = m.get("privacy", "Все ответы хранятся только в этом браузере на этом устройстве "
                              "и никуда не отправляются автоматически. Экспорт — по вашей кнопке.")
    return (
        '<section class="lec" id="map">\n'
        '<span class="badge badge-succ">%s</span>\n'
        "<h2><span class=\"num\">★</span>%s</h2>\n"
        "%s\n"
        '<div class="card"><div id="mapStats"></div></div>\n'
        '<div class="map-actions">'
        '<button class="btn btn-primary" id="btnExport">⬇ Экспорт для психолога (.txt)</button>'
        '<button class="btn" id="btnPrint">🖨 Распечатать / сохранить в PDF</button>'
        '<button class="btn btn-ghost btn-danger" id="btnClear">🗑 Очистить все записи</button>'
        "</div>\n"
        '<div class="note-box">%s</div>\n'
        "</section>" % (esc(m.get("badge", "Итоги")), esc(title), blocks, esc(privacy))
    )


# --------------------------------------------------------------------------- #
#  Варианты (variant_of + inject)
# --------------------------------------------------------------------------- #
def deep_merge(base, over):
    if isinstance(base, dict) and isinstance(over, dict):
        out = dict(base)
        for k, v in over.items():
            out[k] = deep_merge(out.get(k), v) if k in out else copy.deepcopy(v)
        return out
    return copy.deepcopy(over)


def find_step(spec, step_id):
    for s in spec.get("steps", []):
        if s.get("id") == step_id:
            return s
    return None


def apply_variant(spec: dict, spec_dir: Path) -> dict:
    """Накладывает вариант (профессиональную версию) на базовую спеку."""
    base_ref = spec.get("variant_of")
    if not base_ref:
        return spec
    base_path = (spec_dir / base_ref).resolve()
    if not base_path.exists():
        raise SystemExit("variant_of: базовая спека не найдена: %s" % base_path)
    base = json.loads(base_path.read_text(encoding="utf-8"))
    base = apply_variant(base, base_path.parent)  # вариант может наследовать вариант

    merged = deep_merge(base, {k: v for k, v in spec.items()
                              if k not in {"variant_of", "inject", "step_patch", "remove_blocks", "append_steps"}})
    merged.setdefault("meta", {})

    for patch in spec.get("step_patch", []):
        step = find_step(merged, patch["step"])
        if step is None:
            raise SystemExit("step_patch: шаг не найден: %s" % patch["step"])
        for k, v in patch.items():
            if k == "step":
                continue
            step[k] = deep_merge(step.get(k), v) if k == "meta" else v

    for rem in spec.get("remove_blocks", []):
        step = find_step(merged, rem["step"])
        if step is None:
            raise SystemExit("remove_blocks: шаг не найден: %s" % rem["step"])
        bids = set(rem.get("bids", []))
        step["blocks"] = [b for b in step.get("blocks", []) if b.get("bid") not in bids]

    for inj in spec.get("inject", []):
        step = find_step(merged, inj["step"])
        if step is None:
            raise SystemExit("inject: шаг не найден: %s" % inj["step"])
        blocks = step.setdefault("blocks", [])
        at = inj.get("at", "end")
        new = inj.get("blocks", [])
        if at == "start":
            blocks[:0] = new
        elif at == "end":
            blocks.extend(new)
        elif isinstance(at, dict):
            anchor = at.get("after_bid") or at.get("before_bid")
            idx = next((i for i, b in enumerate(blocks) if b.get("bid") == anchor), None)
            if idx is None:
                raise SystemExit("inject: якорь не найден: %s" % anchor)
            pos = idx + 1 if at.get("after_bid") else idx
            blocks[pos:pos] = new
        else:
            raise SystemExit("inject: непонятная позиция %r" % at)

    for inj in spec.get("map_inject", []):
        m = merged.setdefault("map", {})
        blocks = m.setdefault("blocks", [])
        new = inj.get("blocks", [])
        if inj.get("at", "end") == "start":
            blocks[:0] = new
        else:
            blocks.extend(new)

    for extra in spec.get("append_steps", []):
        merged["steps"].append(extra)

    return merged


# --------------------------------------------------------------------------- #
#  Сборка
# --------------------------------------------------------------------------- #
def build(spec_path: Path, *, check_only=False) -> dict:
    raw = json.loads(spec_path.read_text(encoding="utf-8"))
    spec = apply_variant(raw, spec_path.parent)
    meta = spec.get("meta") or {}

    for key in ("title", "bar_title", "storage_key", "filename"):
        if not meta.get(key):
            raise SystemExit("meta.%s обязателен в %s" % (key, spec_path.name))

    ctx = Ctx()
    steps = spec.get("steps", [])
    if not steps:
        raise SystemExit("В спеке нет ни одного шага")

    sections, toc = [], []
    for i, step in enumerate(steps):
        sections.append(render_step(step, ctx, is_first=(i == 0)))
        toc.append('      <li data-t="%s"%s><a href="#%s"><em>%s</em> <span>%s</span></a></li>'
                   % (attr(step["id"]), ' class="on"' if i == 0 else "", attr(step["id"]),
                      esc(step.get("num") or "★"), esc(step.get("toc") or step.get("title", ""))))

    sections.append(render_map(spec, ctx))
    toc.append('      <li data-t="map"><a href="#map"><em>★</em> <span>%s</span></a></li>'
               % esc((spec.get("map") or {}).get("toc", "Моя карта и экспорт")))

    bar_actions = []
    sos = meta.get("sos")
    if sos:
        bar_actions.append('    <a href="#%s" class="btn btn-sos" title="%s">⚡ %s</a>'
                           % (attr(sos.get("href", "map")), attr(sos.get("title", "")), esc(sos.get("label", "SOS"))))

    runtime = {
        "storageKey": meta["storage_key"],
        "themeKey": meta.get("theme_key", meta["storage_key"] + "-theme"),
        "exportTitle": meta.get("export_title", meta["title"]),
        "exportFilename": meta.get("export_filename", "otchet.txt"),
        "steps": [{"id": s["id"], "name": s.get("toc") or s.get("title", s["id"]),
                   "exportName": s.get("export_name") or s.get("title") or s.get("toc", s["id"])}
                  for s in steps] + [{"id": "map", "name": (spec.get("map") or {}).get("toc", "Моя карта"),
                                      "exportName": (spec.get("map") or {}).get("export_name", "ИТОГИ И ПЛАН")}],
    }

    out_html = TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "@@TITLE@@": esc(meta["title"]),
        "@@DESCRIPTION@@": attr(meta.get("description", "")),
        "@@FACTORY_VERSION@@": FACTORY_VERSION,
        "@@ENGINE_CSS@@": ENGINE_CSS.read_text(encoding="utf-8"),
        "@@SPEC_CSS@@": meta.get("css", ""),
        "@@BAR_TITLE@@": esc(meta.get("bar_title", "")),
        "@@BAR_SUB@@": esc(meta.get("bar_sub", "")),
        "@@BAR_ACTIONS@@": "\n".join(bar_actions),
        "@@TOC@@": "\n".join(toc),
        "@@TOC_NOTE@@": ('<div class="toc-note">%s</div>' % esc(meta["toc_note"])) if meta.get("toc_note") else "",
        "@@SECTIONS@@": "\n\n".join(sections),
        "@@SPEC_JSON@@": json.dumps(runtime, ensure_ascii=False),
        "@@ENGINE_JS@@": ENGINE_JS.read_text(encoding="utf-8"),
    }
    for token, value in replacements.items():
        out_html = out_html.replace(token, value)

    left = sorted(set(t for t in re_tokens(out_html)))
    if left:
        raise SystemExit("В шаблоне остались незаполненные токены: %s" % ", ".join(left))

    out_dir = (spec_path.parent / meta.get("output_dir", "..")).resolve()
    out_path = out_dir / meta["filename"]

    result = {
        "spec": str(spec_path),
        "out": str(out_path),
        "bytes": len(out_html.encode("utf-8")),
        "steps": len(steps),
        "fields": ctx.stats["fields"],
        "checks": ctx.stats["checks"],
        "widgets": ctx.stats["widgets"],
        "dupes": ctx.dupes,
        "warnings": ctx.warnings,
        "html": out_html,
        "variant": bool(raw.get("variant_of")),
    }

    if not check_only:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_html, encoding="utf-8")
    return result


def re_tokens(text):
    import re
    return re.findall(r"@@[A-Z_]+@@", text)


# --------------------------------------------------------------------------- #
#  Валидация готового HTML
# --------------------------------------------------------------------------- #
def validate(result: dict) -> list[str]:
    from html.parser import HTMLParser

    doc = result["html"]
    errors = []
    if result["dupes"]:
        errors.append("дубликаты id (переименованы автоматически): %s" % ", ".join(sorted(set(result["dupes"]))))

    class P(HTMLParser):
        VOID = {"meta", "link", "br", "hr", "img", "input", "source", "area", "base", "col", "embed",
                "param", "track", "wbr"}

        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack = []
            self.ids = {}
            self.problems = []

        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            if "id" in d:
                self.ids[d["id"]] = self.ids.get(d["id"], 0) + 1
            if tag not in self.VOID:
                self.stack.append((tag, self.getpos()))

        def handle_startendtag(self, tag, attrs):
            d = dict(attrs)
            if "id" in d:
                self.ids[d["id"]] = self.ids.get(d["id"], 0) + 1

        def handle_endtag(self, tag):
            if tag in self.VOID:
                return
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
            self.problems.append("закрывающий тег без открывающего: </%s> (строка %d)" % (tag, self.getpos()[0]))

    p = P()
    p.feed(doc)
    p.close()
    dup_ids = {k: v for k, v in p.ids.items() if v > 1}
    if dup_ids:
        errors.append("повторяющиеся id в HTML: %s" % dup_ids)
    if p.problems:
        errors.extend(p.problems[:10])
    if p.stack:
        errors.append("незакрытые теги: %s" % [t for t, _ in p.stack][:10])

    # обязательные точки входа движка
    for token in ("id=\"tocList\"", "window.WB_SPEC", "id=\"mapStats\"", "id=\"btnExport\"",
                  "id=\"themeToggle\"", "@media print"):
        if token not in doc:
            errors.append("в готовом файле нет %s" % token)

    # все data-widget должны быть известны движку
    import re
    js = ENGINE_JS.read_text(encoding="utf-8")
    known = set(re.findall(r"WB\.widget\('([a-z_]+)'", js))
    used = set(re.findall(r'data-widget="([a-z_]+)"', doc))
    unknown = used - known
    if unknown:
        errors.append("механики без реализации в движке: %s" % sorted(unknown))

    # экспорт: у каждого шага из WB_SPEC должен быть section
    spec_ids = re.findall(r'"id":\s*"([a-z0-9_]+)"', doc.split("window.WB_SPEC", 1)[1][:4000])
    for sid in spec_ids:
        if ('id="%s"' % sid) not in doc:
            errors.append("шаг %s заявлен в WB_SPEC, но раздела нет" % sid)

    errors.extend(result.get("warnings", []))
    return errors


# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(description="Сборка терапевтических тетрадей в single-file HTML")
    ap.add_argument("specs", nargs="*", help="файлы спек (.json); можно с glob")
    ap.add_argument("--check", action="store_true", help="собрать, провалидировать, но не записывать файл")
    ap.add_argument("--list", action="store_true", help="показать доступные типы блоков")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.list:
        print("Доступные блоки (%d):" % len(RENDERERS))
        for k in sorted(RENDERERS):
            print("  -", k)
        return 0

    paths = []
    for p in args.specs:
        matched = sorted(glob.glob(p))
        if matched:
            paths.extend(Path(m) for m in matched)
        else:
            paths.append(Path(p))
    if not paths:
        ap.error("укажите спеку, например: specs/separation_client.json")

    failed = 0
    for path in paths:
        if not path.exists():
            print("✗ %s — файл не найден" % path)
            failed += 1
            continue
        res = build(path, check_only=args.check)
        errs = validate(res)
        mark = "✓" if not errs else "✗"
        if not args.quiet:
            print("%s %s → %s" % (mark, path.name, res["out"]))
            print("   шагов: %d · полей: %d · чекбоксов: %d · механик: %d · %d КБ%s"
                  % (res["steps"], res["fields"], res["checks"], res["widgets"],
                     res["bytes"] // 1024, " · вариант базовой спеки" if res["variant"] else ""))
        for e in errs:
            print("   ! %s" % e)
        if errs:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
