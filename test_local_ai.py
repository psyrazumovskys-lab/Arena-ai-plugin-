import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "build_plugin_navigator.py").read_text(encoding="utf-8")
HTML = (ROOT / "Plugin_Navigator_Full.html").read_text(encoding="utf-8")
PACKAGE = json.loads((ROOT / "Plugin_Navigator_Windows_Source/package.json").read_text(encoding="utf-8"))
WORKER = (ROOT / "Plugin_Navigator_Windows_Source/resources/ai/worker.js").read_text(encoding="utf-8")
WINDOWS_BUILD = (ROOT / "build_windows.py").read_text(encoding="utf-8")
WINDOWS_VERIFY = (ROOT / "Plugin_Navigator_Windows_Source/verify-windows.mjs").read_text(encoding="utf-8")
REPORT = (ROOT / "Plugin_Navigator_v2.7.0_Local_AI_Report.md").read_text(encoding="utf-8")

MODEL_ID = "Qwen3.5-2B-q4f16_1-MLC"

assert MODEL_ID in SOURCE and MODEL_ID in HTML
assert "@mlc-ai/web-llm" in PACKAGE["devDependencies"]
assert PACKAGE["devDependencies"]["@mlc-ai/web-llm"] == "0.2.84"
assert "WebWorkerMLCEngineHandler" in WORKER
assert "./webllm.js" in WORKER
assert "node_modules/@mlc-ai/web-llm/lib/index.js" in WINDOWS_BUILD
assert "resources / \"ai/webllm.js\"" in WINDOWS_BUILD
assert "resources/ai/webllm.js" in WINDOWS_VERIFY
assert "embeddedWebLLM" in WINDOWS_VERIFY
assert MODEL_ID in REPORT and "аппаратный запуск" in REPORT

# The strict deterministic core remains authoritative. The model must be
# grounded with a small local retrieval context instead of receiving or
# replacing the whole database.
for guardrail in (
    "Детерминированная проверка порядка",
    "Не выдумывай Controls",
    "Product-specific, Product-informed и Family-level",
    "Не представляй все этапы цепочки обязательными",
    "не слышит аудио",
):
    assert guardrail in HTML

for function_name in (
    "aiRetrievePlugins",
    "aiBuildContext",
    "aiSystemPrompt",
    "aiLoadModel",
    "aiRemoveModel",
    "aiSend",
    "aiStop",
):
    assert f"function {function_name}" in HTML

# Model weights are intentionally not committed or embedded: they are about
# 1.1 GB and are downloaded once into the WebView2 cache.
assert not list(ROOT.glob("**/params_shard_*.bin"))
assert "≈1,1 ГБ" in HTML
assert "Первая загрузка требует интернет" in HTML
assert "после этого ответы формируются локально" in HTML.lower()
assert "slice(0,5800)" in HTML and "max_tokens:600" in HTML

print(json.dumps({"status": "PASS", "version": "2.7.0", "model": MODEL_ID}, ensure_ascii=False))
