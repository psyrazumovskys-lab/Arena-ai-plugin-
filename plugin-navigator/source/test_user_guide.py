import hashlib
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "current" / "Plugin_Navigator_User_Guide_RU.md"
OUTPUT = ROOT.parent / "current" / "Plugin_Navigator_User_Guide_RU.html"

subprocess.run(["python3", str(ROOT / "build_user_guide.py")], check=True, capture_output=True, text=True)
first = OUTPUT.read_bytes()
subprocess.run(["python3", str(ROOT / "build_user_guide.py")], check=True, capture_output=True, text=True)
second = OUTPUT.read_bytes()
assert first == second

soup = BeautifulSoup(first.decode("utf-8"), "html.parser")
assert soup.html.get("lang") == "ru"
assert "Plugin Navigator 2.7.4" in soup.title.string
assert not soup.select("script[src], link[rel=stylesheet]")
assert len(soup.select("article h2")) == 23
assert len(soup.select("nav a")) == 23
assert len({h.get("id") for h in soup.select("article h2")}) == 23
assert all(soup.select_one(a.get("href")) for a in soup.select("nav a"))
text = soup.get_text(" ", strip=True)
for token in (
    "Как запустить программу",
    "Простой и экспертный режимы",
    "Как использовать Melodyne",
    "Резервная копия данных",
    "Локальный ИИ",
    "Второй движок: Ollama",
    "Загрузка модели без терминала",
    "Действия ИИ: составление цепочек",
    "ИИ-панель на всех экранах",
    "Частые проблемы",
):
    assert token in text
style = soup.style.string
assert "@media(max-width:900px)" in style and "@media print" in style
assert "```" not in first.decode("utf-8")
assert len(first) < 100_000
print({
    "status": "PASS",
    "sections": 23,
    "html_bytes": len(first),
    "sha256": hashlib.sha256(first).hexdigest(),
    "source_lines": len(SOURCE.read_text(encoding="utf-8").splitlines()),
})
