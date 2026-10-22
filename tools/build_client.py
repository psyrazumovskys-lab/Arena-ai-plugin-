#!/usr/bin/env python3
"""Собирает один самодостаточный HTML-файл по клиенту.

Один клиент → один файл: всё внутри (сводка, динамика, все встречи,
разборы), читается на телефоне, печатается, не требует интернета
и не зависит от других файлов.

    python3 tools/build_client.py <папка-клиента> [выходной-файл]
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import md  # noqa: E402
from build import METRICS, parse_session, parse_tetrad  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def fmt_date(iso: str) -> str:
    if not iso:
        return ""
    try:
        y, m, d = iso.split("-")
        return f"{int(d)} {MONTHS[int(m) - 1]} {y}"
    except (ValueError, IndexError):
        return iso


def spark(points: list[int], color: str) -> str:
    if not points:
        return ""
    W, H, pad = 100, 26, 4
    if len(points) == 1:
        x, y = W / 2, H - pad - (points[0] / 3) * (H - 2 * pad)
        return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">'
                f'<circle cx="{x}" cy="{y:.1f}" r="2.4" fill="{color}"/></svg>')
    step = (W - 2 * pad) / (len(points) - 1)
    y = lambda v: H - pad - (v / 3) * (H - 2 * pad)
    d = " ".join(
        f'{"M" if i == 0 else "L"}{(pad + i * step):.1f},{y(v):.1f}'
        for i, v in enumerate(points)
    )
    dots = "".join(
        f'<circle cx="{(pad + i * step):.1f}" cy="{y(v):.1f}" r="2.1" fill="{color}"/>'
        for i, v in enumerate(points)
    )
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity=".8"/>{dots}</svg>')


def score_bars(scores: dict, colors: dict) -> str:
    parts = []
    for key, _label, color in METRICS:
        v = scores.get(key)
        bars = "".join(
            f'<i style="height:{4 + i * 3}px;background:{color if v is not None and i <= v else "#dfe6ec"}"></i>'
            for i in range(4)
        )
        parts.append(
            f'<span class="sb" title="{_label}: {v if v is not None else "—"}/3">{bars}</span>'
        )
    return "".join(parts)


def client_html(folder: Path) -> str:
    code = folder.name
    t = parse_tetrad(folder / "_тетрадь.md") if (folder / "_тетрадь.md").exists() else {}
    sessions = []
    for f in sorted(folder.glob("*.md")):
        if f.name.startswith("_"):
            continue
        s = parse_session(f)
        if s:
            sessions.append(s)
    sessions.sort(key=lambda s: (s["date"], s["n"]))

    risk = (t.get("riski") or "").strip()
    has_risk = bool(risk) and risk.lower() not in ("нет", "—", "-", "no")

    colors = {k: c for k, _l, c in METRICS}

    # ---- метрики ----
    metrics_html = []
    for key, label, color in METRICS:
        pts = [s["scores"][key] for s in sessions if key in (s.get("scores") or {})]
        last = pts[-1] if pts else None
        metrics_html.append(f"""
        <div class="metric">
          <div class="lab">{html.escape(label)}</div>
          <div class="val">{last if last is not None else "—"}<span> / 3</span></div>
          {spark(pts, color)}
        </div>""")

    # ---- гипотезы ----
    hyps = []
    for g in t.get("gipotezy", []):
        st = g["status"]
        cls = "ok" if "подтвер" in st and "не" not in st else "no" if "не" in st else "check" if "пров" in st else "new"
        hyps.append(
            f'<li><span class="tag {cls}">{html.escape(st)}</span>'
            f"<span>{html.escape(g['text'])}</span></li>"
        )

    # ---- встречи ----
    sess_html = []
    for i, s in enumerate(reversed(sessions)):
        open_attr = " open" if i == 0 else ""
        risk_line = (
            f'<div class="risk"><b>Риск.</b> {html.escape(s["risk"])}</div>'
            if s.get("risk") else ""
        )
        sess_html.append(f"""
    <details class="session"{open_attr}>
      <summary>
        <span class="date">{fmt_date(s["date"])}</span>
        <span class="num">№ {html.escape(s["n"])}</span>
        <span class="focus">{html.escape(s.get("focus") or "")}</span>
        <span class="bars">{score_bars(s.get("scores") or {}, colors)}</span>
        <svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2.5"><path d="M9 6l6 6-6 6"/></svg>
      </summary>
      <div class="body">
        {risk_line}
        <section class="block rec">
          <header><span class="t">Запись</span><span class="d">слова терапевта, не редактируется</span></header>
          <div class="prose">{md.render(s.get("zapis", "")) or '<p class="empty">не записано</p>'}</div>
        </section>
        <section class="block">
          <header><span class="t">Отклик</span><span class="d">{fmt_date(s.get("otklikDate"))}</span></header>
          <div class="prose">{md.render(s.get("otklik", "")) or '<p class="empty">нет</p>'}</div>
        </section>
        <section class="block">
          <header><span class="t">Разбор</span><span class="d">{fmt_date(s.get("razborDate"))}</span></header>
          <div class="prose">{md.render(s.get("razbor", "")) or '<p class="empty">разбора по этой встрече нет</p>'}</div>
        </section>
      </div>
    </details>""")

    nav = "".join(
        f'<a href="#s-{html.escape(s["date"])}">{fmt_date(s["date"])}</a>'
        for s in reversed(sessions)
    )

    zapros = md.render(t.get("zapros", "")) if t.get("zapros") else ""
    formul = md.render(t.get("formulirovka", "")) if t.get("formulirovka") else ""
    dinamika = md.render(t.get("dinamika", "")) if t.get("dinamika") else ""
    prover = md.render(t.get("proveryayu", "")) if t.get("proveryayu") else ""

    count = len(sessions)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
<title>{html.escape(code)} — тетрадь</title>
<style>
{CSS}
</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <div class="code">{html.escape(code)}</div>
    <div class="meta">
      <span>{count} {plural(count)}</span>
      {f'<span>обновлено {fmt_date(t.get("updated", ""))}</span>' if t.get("updated") else ''}
      <span>{'есть риск' if has_risk else 'без риска'}</span>
    </div>
  </div>
</header>

<main class="wrap">
  {f'<div class="risk big"><b>Риск.</b> {html.escape(risk)}</div>' if has_risk else ''}

  <section class="hero">
    <h1>{html.escape(code)}</h1>
    <div class="lede">{formul or zapros}</div>
  </section>

  <section class="metrics">
    {''.join(metrics_html)}
  </section>

  <section class="case">
    <h2>Случай</h2>
    {f'<div class="field"><div class="k">Запрос</div><div class="v">{zapros}</div></div>' if zapros else ''}
    {f'<div class="field"><div class="k">Динамика</div><div class="v">{dinamika}</div></div>' if dinamika else ''}
    {f'<div class="field"><div class="k">Что проверяю</div><div class="v">{prover}</div></div>' if prover else ''}
    {f'<div class="field"><div class="k">Гипотезы</div><ul class="hyps">{"".join(hyps)}</ul></div>' if hyps else ''}
  </section>

  <section class="sessions">
    <div class="sec-head">
      <h2>Встречи</h2>
      <div class="jump">{nav}</div>
    </div>
    {''.join(sess_html) if sessions else '<p class="empty">Записей пока нет.</p>'}
  </section>

  <footer>
    <p>Источник: markdown-файлы на Google Диске. Этот файл — собранная версия для чтения;
    правки в нём не сохраняются. Записи не содержат имён — только код {html.escape(code)}.</p>
  </footer>
</main>
</body>
</html>
"""


def plural(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "встреча"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return "встречи"
    return "встреч"


CSS = """
:root{
  --ink:#101820;--body:#26333f;--muted:#64727f;--faint:#93a2af;
  --line:#e2e9ee;--soft:#eef3f6;--bg:#f6f8fa;--card:#fff;
  --accent:#0e7490;--accent-soft:#eaf5f8;
  --danger:#b42318;--danger-soft:#fdf1f0;
  --ok:#166534;--ok-soft:#eef7f0;--warn:#9a5b00;--warn-soft:#fdf6e8;
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{background:var(--bg);color:var(--body);font-family:var(--font);font-size:15.5px;line-height:1.65;-webkit-font-smoothing:antialiased}
.wrap{max-width:820px;margin:0 auto;padding:0 22px}

.top{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
.top .wrap{display:flex;align-items:baseline;gap:14px;padding:12px 22px}
.top .code{font-weight:650;font-size:15px;color:var(--ink);letter-spacing:-.01em}
.top .meta{margin-left:auto;display:flex;gap:14px;font-size:12px;color:var(--faint);flex-wrap:wrap}

.hero{padding:34px 0 4px}
.hero h1{font-size:34px;line-height:1.1;letter-spacing:-.03em;color:var(--ink);font-weight:700;margin-bottom:10px}
.lede{font-size:16.5px;color:var(--muted);max-width:66ch}
.lede p{margin:0}

.metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin:24px 0 6px}
.metric{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 12px 6px}
.metric .lab{font-size:10.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--faint);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.metric .val{font-size:21px;font-weight:650;color:var(--ink);line-height:1.25;font-variant-numeric:tabular-nums}
.metric .val span{font-size:11.5px;color:var(--faint);font-weight:400}
.metric svg{display:block;width:100%;height:24px;margin-top:3px;overflow:visible}

.case{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 24px;margin-top:22px}
.case h2,.sec-head h2{font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:var(--faint);font-weight:650}
.case h2{margin-bottom:14px}
.field + .field{margin-top:18px;padding-top:18px;border-top:1px solid var(--soft)}
.field .k{font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:var(--faint);font-weight:600;margin-bottom:5px}
.field .v{font-size:14.8px}
.field .v p + p{margin-top:8px}

.hyps{list-style:none;display:flex;flex-direction:column;gap:8px}
.hyps li{display:flex;gap:9px;align-items:flex-start;font-size:14.4px}
.tag{flex:none;font-size:10.5px;font-weight:650;padding:2px 8px;border-radius:999px;white-space:nowrap;margin-top:3px;letter-spacing:.01em}
.tag.ok{background:var(--ok-soft);color:var(--ok)}
.tag.no{background:#f1f4f6;color:#64727f}
.tag.check{background:var(--warn-soft);color:var(--warn)}
.tag.new{background:var(--accent-soft);color:var(--accent)}

.sessions{margin-top:34px}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:12px;flex-wrap:wrap}
.jump{display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end}
.jump a{font-size:11.5px;color:var(--faint);text-decoration:none;padding:3px 7px;border-radius:6px;background:#fff;border:1px solid var(--line);white-space:nowrap}
.jump a:hover{color:var(--accent);border-color:var(--accent)}

.session{background:var(--card);border:1px solid var(--line);border-radius:14px;margin-bottom:11px;overflow:hidden}
.session > summary{list-style:none;cursor:pointer;padding:15px 20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.session > summary::-webkit-details-marker{display:none}
.session > summary:hover{background:#fcfdfe}
.session[open] > summary{border-bottom:1px solid var(--soft)}
.date{font-weight:650;color:var(--ink);font-size:14.5px;font-variant-numeric:tabular-nums}
.num{font-size:11.5px;color:var(--faint);font-variant-numeric:tabular-nums}
.focus{flex:1;min-width:150px;font-size:13px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bars{display:flex;gap:5px;flex:none;align-items:flex-end}
.sb{display:flex;flex-direction:column;gap:2px;align-items:center;justify-content:flex-end}
.sb i{display:block;width:4px;border-radius:1px}
.chev{flex:none;color:var(--faint);transition:transform .15s}
.session[open] .chev{transform:rotate(90deg)}
.body{padding:2px 20px 18px}
.block{padding:16px 0;border-bottom:1px solid var(--soft)}
.block:last-child{border-bottom:0;padding-bottom:2px}
.block header{display:flex;align-items:baseline;gap:9px;margin-bottom:7px}
.block .t{font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;font-weight:650;color:var(--faint)}
.block.rec .t{color:var(--accent)}
.block .d{font-size:11.5px;color:var(--faint)}
.prose{font-size:14.6px;line-height:1.68;max-width:72ch}
.prose p + p{margin-top:9px}
.prose h2,.prose h3,.prose h4,.prose h5{font-weight:650;color:var(--ink);margin:14px 0 5px;font-size:14.2px;letter-spacing:-.005em}
.prose ul,.prose ol{margin:6px 0 0 19px}
.prose li{margin-bottom:4px}
.prose strong{font-weight:650;color:var(--ink)}
.prose code{font-family:var(--mono);font-size:12.4px;background:var(--bg);padding:1px 5px;border-radius:4px}
.prose em{color:var(--muted)}
.prose blockquote{border-left:3px solid var(--line);padding-left:13px;color:var(--muted);margin:9px 0}
.prose pre{background:#f3f6f8;border:1px solid var(--line);border-radius:9px;padding:11px 13px;overflow-x:auto;margin:10px 0}
.prose pre code{background:none;padding:0;white-space:pre;font-size:12.3px;line-height:1.55}
.empty{color:var(--faint);font-style:italic;font-size:14px}

.tw{overflow-x:auto;margin:10px 0 14px}
table{width:100%;border-collapse:collapse;font-size:13.6px}
th{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--faint);font-weight:650;padding:7px 9px;border-bottom:1px solid var(--line)}
td{padding:9px 9px;border-bottom:1px solid var(--soft);vertical-align:top}
tr:last-child td{border-bottom:0}

.risk{background:var(--danger-soft);border:1px solid #f2cfcb;border-left:3px solid var(--danger);border-radius:9px;padding:11px 14px;font-size:13.8px;color:#7a1a13;margin:12px 0 0}
.risk.big{margin:22px 0 0}
.risk b{color:var(--danger)}

footer{margin:44px 0 60px;padding-top:16px;border-top:1px solid var(--line);font-size:12px;color:var(--faint);max-width:70ch}

@media (max-width:700px){
  .wrap{padding:0 15px}
  .top .wrap{padding:10px 15px}
  .top .meta span:nth-child(2){display:none}
  .hero{padding:24px 0 2px}
  .hero h1{font-size:28px}
  .metrics{grid-template-columns:repeat(2,1fr)}
  .metric:last-child{grid-column:span 2}
  .case{padding:17px 16px}
  .session > summary{padding:13px 15px;gap:9px}
  .focus{order:5;flex-basis:100%;white-space:normal;color:var(--muted)}
  .body{padding:2px 15px 16px}
  .jump{display:none}
}
@media print{
  .top{position:static;border:0;padding:0}
  .top .meta,.jump,.chev{display:none}
  body{background:#fff;font-size:11pt}
  .case,.session{border:0;padding:0;page-break-inside:avoid}
  .session > summary{cursor:default;padding:8px 0}
  .session > .body{display:block!important}
  details{page-break-inside:avoid}
  details:not([open]) > .body{display:block!important}
}
"""


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    folder = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "build_app" / f"{folder.name}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(client_html(folder), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
