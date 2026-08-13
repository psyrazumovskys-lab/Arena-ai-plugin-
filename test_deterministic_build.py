import hashlib,subprocess
from pathlib import Path

def build():
    subprocess.run(['python3','/home/user/build_plugin_navigator.py'],check=True,capture_output=True,text=True)
    data=Path('/home/user/Plugin_Navigator_Full.html').read_bytes()
    return hashlib.sha256(data).hexdigest(),len(data)
first=build();second=build()
assert first==second,(first,second)
Path('/home/user/index.html').write_bytes(Path('/home/user/Plugin_Navigator_Full.html').read_bytes())
print({'status':'PASS','sha256':first[0],'bytes':first[1]})
