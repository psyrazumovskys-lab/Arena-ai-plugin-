#!/usr/bin/env python3
"""Build the standalone offline HTML user guide from the Russian Markdown guide."""

from __future__ import annotations

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Plugin_Navigator_User_Guide_RU.md"
OUTPUT = ROOT / "Plugin_Navigator_User_Guide_RU.html"


def inline(text: str) -> str:
    value = escape(text, quote=False)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    return value


def render(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    lines = markdown.splitlines()
    body: list[str] = []
    toc: list[tuple[str, str]] = []
    paragraph: list[str] = []
    code_lines: list[str] = []
    in_code = False
    list_type: str | None = None
    section_number = 0

    def flush_paragraph() -> None:
        if paragraph:
            body.append(f"<p>{inline(' '.join(part.strip() for part in paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            body.append(f"</{list_type}>")
            list_type = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            close_list()
            if in_code:
                body.append("<pre><code>" + escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not stripped:
            flush_paragraph()
            close_list()
            continue
        if stripped == "---":
            flush_paragraph()
            close_list()
            body.append("<hr>")
            continue
        heading = re.match(r"^(#{1,2})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            title = heading.group(2)
            if level == 1:
                ident = "top"
            else:
                section_number += 1
                ident = f"section-{section_number}"
                toc.append((ident, re.sub(r"^\d+\.\s*", "", title)))
            body.append(f'<h{level} id="{ident}">{inline(title)}</h{level}>')
            continue
        if stripped.startswith("> "):
            flush_paragraph()
            close_list()
            body.append(f"<blockquote>{inline(stripped[2:])}</blockquote>")
            continue
        item = re.match(r"^[-*]\s+(.+)$", stripped)
        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if item or numbered:
            flush_paragraph()
            wanted = "ul" if item else "ol"
            if list_type != wanted:
                close_list()
                list_type = wanted
                body.append(f"<{wanted}>")
            body.append(f"<li>{inline((item or numbered).group(1))}</li>")
            continue
        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    if in_code:
        body.append("<pre><code>" + escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(body), toc


def main() -> None:
    content, toc = render(SOURCE.read_text(encoding="utf-8"))
    toc_html = "\n".join(
        f'<a href="#{ident}"><span>{index}</span>{inline(title)}</a>'
        for index, (ident, title) in enumerate(toc, 1)
    )
    html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Plugin Navigator 2.5.7 — инструкция пользователя</title>
<style>
:root{{--bg:#0c111b;--panel:#121a28;--panel2:#172235;--line:#26344a;--text:#eef4ff;--muted:#aebdd1;--blue:#5b8cff;--cyan:#32c6d4;--green:#59d68b;--yellow:#f7c65c;--shadow:0 18px 60px rgba(0,0,0,.32)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 Inter,"Segoe UI",Arial,sans-serif}}button,a{{font:inherit}}a{{color:#9ec0ff}}.layout{{display:grid;grid-template-columns:310px minmax(0,1fr);min-height:100vh}}aside{{position:sticky;top:0;height:100vh;overflow:auto;background:#0f1724;border-right:1px solid var(--line);padding:22px 16px}}.brand{{padding:8px 10px 18px;border-bottom:1px solid var(--line);margin-bottom:12px}}.brand b{{display:block;font-size:18px}}.brand small{{color:var(--muted)}}nav{{display:grid;gap:3px}}nav a{{display:grid;grid-template-columns:28px 1fr;gap:7px;align-items:start;color:var(--muted);text-decoration:none;padding:7px 9px;border-radius:9px;font-size:13px;line-height:1.35}}nav a span{{color:#6f829e}}nav a:hover,nav a.active{{background:var(--panel2);color:var(--text)}}main{{min-width:0}}.topbar{{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 22px;background:rgba(12,17,27,.9);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}}.topbar b{{font-size:14px}}.tools{{display:flex;gap:8px}}button,.button{{border:1px solid var(--line);background:var(--panel);color:var(--text);padding:9px 12px;border-radius:9px;text-decoration:none;cursor:pointer}}button:hover,.button:hover{{border-color:#4a607e}}#menu{{display:none}}article{{width:min(920px,100%);margin:auto;padding:34px 38px 80px}}h1{{font-size:38px;line-height:1.12;margin:0 0 24px;padding:28px;border:1px solid var(--line);border-radius:20px;background:linear-gradient(135deg,#17233a,#121a28 55%,#10222a);box-shadow:var(--shadow)}}h2{{font-size:25px;line-height:1.25;margin:52px 0 17px;padding-top:8px;scroll-margin-top:76px}}p,li{{color:#d2dbea}}strong{{color:#fff}}ul,ol{{padding-left:24px}}li{{margin:6px 0}}hr{{border:0;border-top:1px solid var(--line);margin:36px 0}}pre{{overflow:auto;padding:14px 16px;background:#08101b;border:1px solid var(--line);border-radius:11px;color:#d9e9ff}}code{{font-family:"Cascadia Code",Consolas,monospace;background:#101b2c;border:1px solid #263a56;padding:2px 6px;border-radius:6px;color:#cbe0ff}}pre code{{background:none;border:0;padding:0}}blockquote{{margin:20px 0;padding:15px 18px;border-left:4px solid var(--cyan);background:#101a29;border-radius:0 11px 11px 0;color:#e6f7ff;font-weight:650}}.notice{{padding:13px 15px;border:1px solid rgba(89,214,139,.3);background:rgba(89,214,139,.07);border-radius:11px;color:#a8f0c2;margin:0 0 22px}}
@media(max-width:900px){{.layout{{grid-template-columns:1fr}}aside{{position:fixed;left:-330px;z-index:20;width:310px;transition:.2s;box-shadow:var(--shadow)}}aside.open{{left:0}}#menu{{display:block}}article{{padding:24px 18px 70px}}h1{{font-size:29px;padding:20px}}h2{{font-size:22px}}.topbar{{padding:10px 12px}}}}
@media print{{aside,.topbar{{display:none}}.layout{{display:block}}article{{width:100%;padding:0}}body{{background:#fff;color:#111}}h1{{box-shadow:none}}p,li,strong,blockquote{{color:#111}}pre,code{{color:#111;background:#f4f4f4;border-color:#bbb}}h2{{break-after:avoid}}}}
</style>
</head>
<body>
<div class="layout">
<aside id="sidebar"><div class="brand"><b>Plugin Navigator 2.5.7</b><small>Инструкция пользователя</small></div><nav>{toc_html}</nav></aside>
<main>
<div class="topbar"><div class="tools"><button id="menu" aria-label="Открыть оглавление">☰</button><b>Инструкция пользователя</b></div><div class="tools"><a class="button" href="#top">В начало</a><button onclick="window.print()">Печать / PDF</button></div></div>
<article><div class="notice">Автономный документ: интернет для чтения не требуется.</div>{content}</article>
</main>
</div>
<script>
const sidebar=document.getElementById('sidebar');document.getElementById('menu').onclick=()=>sidebar.classList.toggle('open');
document.querySelectorAll('nav a').forEach(a=>a.onclick=()=>sidebar.classList.remove('open'));
const links=[...document.querySelectorAll('nav a')],map=new Map(links.map(a=>[a.getAttribute('href').slice(1),a]));
const observer=new IntersectionObserver(entries=>entries.forEach(e=>{{if(!e.isIntersecting)return;links.forEach(a=>a.classList.remove('active'));map.get(e.target.id)?.classList.add('active')}}),{{rootMargin:'-15% 0px -75% 0px'}});
document.querySelectorAll('h2').forEach(h=>observer.observe(h));
</script>
</body>
</html>'''
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Built {OUTPUT.name} ({OUTPUT.stat().st_size} bytes, {len(toc)} sections)")


if __name__ == "__main__":
    main()
