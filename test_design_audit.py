import json,re
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

html=Path(__file__).resolve().parent.joinpath('Plugin_Navigator_Full.html').read_text()
soup=BeautifulSoup(html,'html.parser')
DB=json.loads(soup.select_one('#db').string)
assert DB['version']=='2.4.5-nav-groups'

# Autonomous/offline shell and static accessibility.
assert not soup.select('script[src],link[rel="stylesheet"]')
ids=[x['id'] for x in soup.select('[id]')]
assert len(ids)==len(set(ids)), 'duplicate static ids'
for ident in ['menuBtn','modeToggle','clearBtn','compareClear']:
    el=soup.select_one('#'+ident);assert el and el.get('aria-label'),ident
assert 'aria-label="Закрыть карточку"' in html
assert 'aria-label="Добавить ${esc(p.name)} в избранное"' in html
assert soup.select_one('#search').get('aria-label')
assert soup.select_one('.drawer').get('role')=='dialog' and soup.select_one('.drawer').get('aria-modal')=='true'
assert soup.select_one('#toast').get('aria-live')=='polite'
assert 'rel="noopener noreferrer"' in html and 'function trapDrawerFocus' in html

# Responsive design and keyboard/focus behavior.
style='\n'.join(x.get_text() for x in soup.select('style'))
for token in ['@media(max-width:900px)','@media(max-width:560px)','@media(max-width:600px)','@media(prefers-reduced-motion:reduce)','focus-visible','.topbar #modeToggle{display:block']:
    assert token in style,token
script=soup.find_all('script')[-1].string
assert "['more','⋯','More']" in script
assert "const bottom=[['dashboard','⌂','Главная'],['wizard','◎','Подбор'],['builder','＋','Цепочка'],['plugins','◫','Каталог'],['more','⋯','More']]" in script
assert 'function navGroups' in script and 'Подготовка' in script and 'nav-group' in script
assert 'id="sideSources"' not in html
assert "['Enter',' ']" in script and 'function activate(' in script
assert 'tabindex="0"' in script

# Honest language and progressive disclosure.
assert 'ПРОВЕРЕННЫЙ PRESET' not in html
assert 'Выберите проверенный preset' not in html
for token in ['CURATED STARTING POINT','БАЗОВЫЙ СТАРТ — НЕ ОБЯЗАТЕЛЬНО','ЕСЛИ ТРЕБУЕТСЯ','CREATIVE — ПРОСЛУШАТЬ','MONITORING — НЕ EXPORT','Полное описание и порядок настройки','Включить, когда','Пропустить, когда','Что слушать','Сессия — до плагинов','Это чеклист подготовки','Типичная ошибка','Что сделать','Когда пропустить']:
    assert token in html,token
assert '<details' in html and '<summary' in html
assert 'expandedChains:new Set()' in script and 'data-expand-chain' in script and 'data-collapse-chain' in script
assert 'function sessionView' in script and 'SESSION_CHECKS' in script and 'data-check' in script and 'pn-session-checks' in script
assert "kind:'base'" in script and "kind:'conditional'" in script and 'sessionProgressLabel' in script and 'baseDone' in script
assert DB['coverage']['officialExactProductPages']>=250 and DB['coverage']['officialVendorManualHubs']==364-DB['coverage']['officialExactProductPages']
assert DB['coverage']['sourceMappedPlugins']==364

# Every curated step carries full conditional guidance.
steps=[s for c in DB['chains'] for s in c['steps']]
assert len(steps)==351
fields=('necessity','necessityLabel','purpose','condition','skipWhen','listenFor','how')
assert all(all(s.get(k) for k in fields) for s in steps)
necessity=Counter(s['necessity'] for s in steps)
assert necessity=={'start':197,'conditional':108,'creative':34,'monitor':12}
assert DB['coverage']['conditionalStepGuides']==351
assert all(c.get('preflight') for c in DB['chains'])

# Readability: sufficient contrast for core text/muted text using WCAG formula.
def rgb(h): return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lum(h):
    vals=[]
    for c in rgb(h): vals.append(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4)
    return .2126*vals[0]+.7152*vals[1]+.0722*vals[2]
def contrast(a,b):
    x,y=sorted((lum(a),lum(b)),reverse=True);return (x+.05)/(y+.05)
assert contrast('#eef4ff','#0c111b')>=7
assert contrast('#9dadc3','#121a28')>=4.5

# Keep the autonomous program in a practical size range.
assert len(html.encode())<12_000_000
print({'status':'PASS','version':DB['version'],'steps':len(steps),'necessity':dict(necessity),'static_ids':len(ids),'html_bytes':len(html.encode()),'contrast_text':round(contrast('#eef4ff','#0c111b'),2),'contrast_muted':round(contrast('#9dadc3','#121a28'),2)})
