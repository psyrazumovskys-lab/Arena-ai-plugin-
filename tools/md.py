"""Минимальный markdown → HTML для сборки документов.

Без зависимостей: только то, что реально используется в записях —
заголовки, списки, таблицы, блоки кода, цитаты, выделения.
"""

from __future__ import annotations

import html
import re


def esc(s: str) -> str:
    return html.escape(s, quote=False).replace('"', "&quot;")


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"(^|[\s(])_([^_]+)_(?=[\s).,;!?]|$)", r"\1<em>\2</em>", s)
    s = re.sub(r"\[(.+?)\]\((https?:[^)]+)\)", r"\1", s)
    return s


def render(src: str) -> str:
    if not src or not src.strip():
        return ""

    out: list[str] = []
    para: list[str] = []
    table: list[str] = []
    lst: str | None = None
    fence = False
    fence_buf: list[str] = []

    def flush_para() -> None:
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list() -> None:
        nonlocal lst
        if lst:
            out.append(f"</{lst}>")
            lst = None

    def close_table() -> None:
        if not table:
            return
        rows = [r for r in table if not re.match(r"^\|[\s:|-]+\|$", r)]
        cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
        if rows:
            head = cells(rows[0])
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>"
                for r in rows[1:]
            )
            out.append(
                '<div class="tw"><table><thead><tr>'
                + "".join(f"<th>{inline(c)}</th>" for c in head)
                + f"</tr></thead><tbody>{body}</tbody></table></div>"
            )
        table.clear()

    for raw in src.replace("\r", "").split("\n"):
        line = raw.strip()

        if line.startswith("```"):
            if not fence:
                flush_para(); close_list(); close_table()
                fence, fence_buf = True, []
            else:
                out.append("<pre><code>" + esc("\n".join(fence_buf)) + "</code></pre>")
                fence = False
            continue
        if fence:
            fence_buf.append(raw)
            continue

        if not line:
            flush_para(); close_list(); close_table()
            continue

        if line.startswith("|"):
            flush_para(); close_list()
            table.append(line)
            continue
        close_table()

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_para(); close_list()
            lvl = min(len(m.group(1)) + 1, 5)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            continue

        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            flush_para()
            if lst != "ul":
                close_list(); out.append("<ul>"); lst = "ul"
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        m = re.match(r"^\d+[.)]\s+(.*)$", line)
        if m:
            flush_para()
            if lst != "ol":
                close_list(); out.append("<ol>"); lst = "ol"
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        m = re.match(r"^>\s?(.*)$", line)
        if m:
            flush_para(); close_list()
            out.append(f"<blockquote>{inline(m.group(1))}</blockquote>")
            continue

        flush_para(); close_list()
        para.append(line)

    flush_para(); close_list(); close_table()
    return "\n".join(out)
