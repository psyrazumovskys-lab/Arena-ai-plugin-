import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "build_plugin_navigator.py").read_text(encoding="utf-8")
HTML = (ROOT.parent / "current" / "Plugin_Navigator_Full.html").read_text(encoding="utf-8")
PACKAGE = json.loads((ROOT / "Plugin_Navigator_Windows_Source/package.json").read_text(encoding="utf-8"))
WORKER = (ROOT / "Plugin_Navigator_Windows_Source/resources/ai/worker.js").read_text(encoding="utf-8")
WINDOWS_BUILD = (ROOT / "build_windows.py").read_text(encoding="utf-8")
WINDOWS_VERIFY = (ROOT / "Plugin_Navigator_Windows_Source/verify-windows.mjs").read_text(encoding="utf-8")
REPORT = (ROOT.parent / "reports" / "Plugin_Navigator_v2.7.0_Local_AI_Report.md").read_text(encoding="utf-8")

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
assert "slice(0,8000)" in HTML and "max_tokens:800" in HTML

# Ollama connector (2.7.1): второй движок рядом с WebLLM. Использует тот же
# строгий retrieval-контекст и system prompt; стриминг через локальный /api/chat.
OLLAMA_REPORT = (
    ROOT.parent / "reports" / "Plugin_Navigator_v2.7.6_Local_AI_Report.md"
).read_text(encoding="utf-8")
for marker in (
    "aiOllamaPing",
    "aiOllamaChat",
    "aiOllamaPersist",
    "aiOllamaPickModel",
    "aiOllamaError",
    "/api/tags",
    "/api/chat",
    "127.0.0.1:11434",
    "pn-ai-backend",
    "aiBackend",
    "OLLAMA_ORIGINS",
    "num_predict:800",
    "num_ctx:8192",
    "/api/pull",
    "aiOllamaPull",
    "data-ai-pull",
    "aiOllamaPullBtn",
    "qwen3.5:2b-q4_K_M",
    # Actions (2.7.3): chain proposals require explicit user confirmation.
    "aiParseAction",
    "aiApplyChain",
    "apply_chain",
    "data-ai-apply",
    "ТРЕБУЕТ ПОДТВЕРЖДЕНИЯ",
    "ДОСТУПНЫЕ ЭТАПЫ",
    "Изменения цепочки применяются только после вашего подтверждения",
    # Floating panel (2.7.4): assistant available on every screen.
    "aiPanelInit",
    "aiPanelSync",
    "aiPanelQuestion",
    "ai-fab",
    "ai-float",
    "pn-ai-panel",
    "ТЕКУЩИЙ ЭКРАН ПОЛЬЗОВАТЕЛЯ",
    "ОТКРЫТАЯ КАРТОЧКА",
    # My plugins (2.7.5): ownership + category-wide context.
    "persistOwned",
    "aiCategoryContext",
    "toggleOwned",
    "ownedFilter",
    "pn-owned",
    "ПЛАГИНЫ ПОЛЬЗОВАТЕЛЯ",
    "ВСЕ ПЛАГИНЫ КАТЕГОРИИ",
    "КОЛЛЕКЦИЯ ПОЛЬЗОВАТЕЛЯ",
    # Bulk ownership (2.7.6): mark all / filtered / import from DAW list.
    "ownedApplyNames",
    "ownedImportPanel",
    "ownedImportText",
    "ownedMarkAll",
    "ownedMarkFiltered",
    "ownedImportBtn",
    "Импорт списка",
):
    assert marker in SOURCE and marker in HTML, marker
assert "Движок локального ИИ" in HTML
assert "Ollama на этом компьютере" in HTML
assert "Строгая защита фактов" in HTML
assert "Ollama" in OLLAMA_REPORT and "2.7.5" in OLLAMA_REPORT

print(
    json.dumps(
        {"status": "PASS", "version": "2.7.6", "model": MODEL_ID, "ollama": True},
        ensure_ascii=False,
    )
)
