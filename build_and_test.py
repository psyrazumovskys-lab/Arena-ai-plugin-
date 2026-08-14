#!/usr/bin/env python3
"""Build Plugin Navigator and run the complete reproducible audit suite."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(*command: str, cwd: Path = ROOT) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    run(sys.executable, "build_plugin_navigator.py")
    for test in (
        "test_design_audit.py",
        "test_chain_research_audit.py",
        "test_plugin_guides.py",
        "test_deterministic_build.py",
    ):
        run(sys.executable, test)

    npm = shutil.which("npm")
    node_modules = ROOT / "test-runtime" / "node_modules"
    if not npm:
        raise SystemExit("Node.js/npm не найден: UI-тест не может быть запущен.")
    if not node_modules.exists():
        raise SystemExit("Сначала выполните: cd test-runtime && npm ci")
    run(npm, "test", cwd=ROOT / "test-runtime")
    print("\nPlugin Navigator: BUILD + ALL TESTS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
