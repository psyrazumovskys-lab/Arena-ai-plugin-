#!/usr/bin/env python3
"""Create and verify the portable Windows x64 release archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
DIST = ROOT.parent / "current"      # готовые файлы: plugin-navigator/current
VERSIONS = ROOT.parent / "versions"  # архивные версии: plugin-navigator/versions
REPORTS = ROOT.parent / "reports"    # отчёты: plugin-navigator/reports
WIN = ROOT / "Plugin_Navigator_Windows_Source"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str | Path) -> None:
    command = [str(arg) for arg in args]
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def version_tuple(value: str) -> tuple[int, int, int]:
    return tuple(map(int, value.split(".")))  # type: ignore[return-value]


def find_base_zip(current: str) -> Path:
    choices: list[tuple[tuple[int, int, int], Path]] = []
    pattern = re.compile(r"Plugin_Navigator_Full_v(\d+\.\d+\.\d+)_Windows_x64\.zip$")
    for path in [*DIST.glob("Plugin_Navigator_Full_v*_Windows_x64.zip"), *VERSIONS.glob("Plugin_Navigator_Full_v*_Windows_x64.zip")]:
        match = pattern.match(path.name)
        if match and version_tuple(match.group(1)) < version_tuple(current):
            choices.append((version_tuple(match.group(1)), path))
    if not choices:
        raise SystemExit("Не найден предыдущий Windows ZIP. Передайте --base-exe.")
    return max(choices)[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-exe", type=Path, help="Neutralino Windows x64 EXE from a previous release")
    args = parser.parse_args()

    data = json.loads((ROOT / "plugin_navigator_database.json").read_text(encoding="utf-8"))
    version = data["version"]
    html = DIST / f"Plugin_Navigator_Full_v{version}.html"
    generic_html = DIST / "Plugin_Navigator_Full.html"
    database = ROOT / "plugin_navigator_database.json"
    guide_html = DIST / "Plugin_Navigator_User_Guide_RU.html"
    guide_source = DIST / "Plugin_Navigator_User_Guide_RU.md"
    ai_report = REPORTS / f"Plugin_Navigator_v{version}_Local_AI_Report.md"
    if not guide_html.exists() or not guide_source.exists():
        raise SystemExit("Сначала выполните: python3 build_user_guide.py")
    if not ai_report.exists():
        raise SystemExit(f"Не найден отчёт локального ИИ: {ai_report.name}")
    config = json.loads((WIN / "neutralino.config.json").read_text(encoding="utf-8"))
    if config["version"] != version:
        raise SystemExit(f"neutralino.config.json={config['version']}, database={version}")
    if html.read_bytes() != generic_html.read_bytes() or html.read_bytes() != (WIN / "resources/index.html").read_bytes():
        raise SystemExit("HTML release copies differ")

    node = shutil.which("node")
    asar = WIN / "node_modules/.bin/asar"
    postject = WIN / "node_modules/.bin/postject"
    webllm_module = WIN / "node_modules/@mlc-ai/web-llm/lib/index.js"
    webllm_license = WIN / "node_modules/@mlc-ai/web-llm/LICENSE"
    ai_worker = WIN / "resources/ai/worker.js"
    if not node or not asar.exists() or not postject.exists() or not webllm_module.exists():
        raise SystemExit("Сначала выполните: cd Plugin_Navigator_Windows_Source && npm ci")
    if not webllm_license.exists() or not ai_worker.exists():
        raise SystemExit("Не найдены локальные ресурсы или лицензия WebLLM")

    output_zip = DIST / f"Plugin_Navigator_Full_v{version}_Windows_x64.zip"
    exe_name = f"Plugin_Navigator_Full_v{version}_Windows_x64.exe"
    with tempfile.TemporaryDirectory(prefix="plugin-navigator-win-") as temp_raw:
        temp = Path(temp_raw)
        base_exe = args.base_exe
        if base_exe:
            shutil.copy2(base_exe, temp / "base.exe")
        else:
            base_zip = find_base_zip(version)
            print(f"Base shell: {base_zip.name}")
            with zipfile.ZipFile(base_zip) as archive:
                exe_members = [name for name in archive.namelist() if name.lower().endswith(".exe")]
                if len(exe_members) != 1:
                    raise SystemExit(f"Expected one EXE in {base_zip.name}")
                (temp / "base.exe").write_bytes(archive.read(exe_members[0]))

        # Neutralino expects neutralino.config.json at the ASAR root and the
        # document root below /resources/. Packing index.html alone makes the
        # framework fall back to its default neutralinojs.org page.
        bundle_root = temp / "bundle"
        resources = bundle_root / "resources"
        # Keep the UI and the WebLLM runtime inside the executable. The 1.1 GB
        # Qwen model itself is downloaded once by the user and remains in the
        # WebView2 cache, so normal application updates stay small.
        shutil.copytree(WIN / "resources", resources)
        shutil.copy2(html, resources / "index.html")
        shutil.copy2(webllm_module, resources / "ai/webllm.js")
        shutil.copy2(WIN / "neutralino.config.json", bundle_root / "neutralino.config.json")
        archive_neu = temp / "resources.neu"
        versioned_exe = temp / exe_name
        run(asar, "pack", bundle_root, archive_neu)
        run(node, WIN / "update-version.mjs", temp / "base.exe", versioned_exe, version)
        run(postject, versioned_exe, "NEUTRALINOJS_RESOURCES_NEU", archive_neu, "--overwrite")
        run(node, WIN / "verify-windows.mjs", versioned_exe, html, version)

        exe_hash = sha256(versioned_exe)
        html_hash = sha256(html)
        readme = f"""Plugin Navigator {version} — portable Windows x64
Полная автономная версия, без Trial и ключей.
Нужен Microsoft Edge WebView2 Runtime.
Цифровой подписи нет — SmartScreen может показать предупреждение.

Новое в {version}:
- добавлен локальный ИИ Qwen3.5 2B Q4 без API и облачного сервера;
- WebLLM runtime встроен непосредственно в Windows EXE;
- модель загружается один раз и затем работает из локального WebView2 cache;
- ИИ объясняет текущую цепочку, Controls и Starting Settings по локальной базе;
- строгий Помощник порядка остаётся авторитетнее предположений ИИ;
- без WebGPU весь справочник, каталог и 99 проверенных цепочек работают как прежде;
- сохранены все исправления карточек версии 2.6.1.
"""
        inner_checks = f"{exe_hash}  {exe_name}\n{html_hash}  {html.name} (embedded)\n"
        third_party_licenses = (
            "NEUTRALINOJS\n============\n".encode()
            + (WIN / "LICENSE").read_bytes()
            + "\n\nWEBLLM — APACHE LICENSE 2.0\n===========================\n".encode()
            + webllm_license.read_bytes()
        )
        files = {
            exe_name: versioned_exe.read_bytes(),
            "README_RU.txt": readme.encode(),
            "CHECKSUMS_SHA256.txt": inner_checks.encode(),
            "THIRD_PARTY_LICENSES.txt": third_party_licenses,
        }
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, content in files.items():
                info = zipfile.ZipInfo(name, date_time=(2026, 8, 15, 16, 15, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, content, compresslevel=9)

    checksums = (
        f"{sha256(generic_html)}  {generic_html.name}\n"
        f"{sha256(html)}  {html.name}\n"
        f"{sha256(WIN / 'resources/index.html')}  Plugin_Navigator_Windows_Source/resources/index.html\n"
        f"{sha256(database)}  {database.name}\n"
        f"{sha256(guide_html)}  {guide_html.name}\n"
        f"{sha256(guide_source)}  {guide_source.name}\n"
        f"{sha256(ai_report)}  {ai_report.name}\n"
        f"{sha256(output_zip)}  {output_zip.name}\n"
        f"# EXE inside ZIP SHA-256: {exe_hash}  {exe_name}\n"
    )
    checks_path = DIST / "CHECKSUMS_SHA256.txt"
    checks_path.write_text(checksums, encoding="utf-8")

    download_zip = DIST / f"Plugin_Navigator_v{version}_Download.zip"
    download_files = {
        html.name: html.read_bytes(),
        output_zip.name: output_zip.read_bytes(),
        checks_path.name: checks_path.read_bytes(),
        "README.md": (ROOT.parent / "README.md").read_bytes(),
        guide_html.name: guide_html.read_bytes(),
        guide_source.name: guide_source.read_bytes(),
        ai_report.name: ai_report.read_bytes(),
    }
    with zipfile.ZipFile(download_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in download_files.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 8, 15, 16, 30, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, content, compresslevel=9)
    checksums += f"{sha256(download_zip)}  {download_zip.name}\n"
    checks_path.write_text(checksums, encoding="utf-8")

    print(f"Built {output_zip.name} ({output_zip.stat().st_size} bytes)")
    print(f"Built {download_zip.name} ({download_zip.stat().st_size} bytes)")
    print(checksums)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
