import hashlib, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build():
    subprocess.run(['python3', str(ROOT / 'build_plugin_navigator.py')], check=True, capture_output=True, text=True)
    data = (ROOT / 'Plugin_Navigator_Full.html').read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)

first = build()
second = build()
assert first == second, (first, second)
print({'status': 'PASS', 'sha256': first[0], 'bytes': first[1]})
