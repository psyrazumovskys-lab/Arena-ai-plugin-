import json,re
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

html=Path(__file__).resolve().parent.parent.joinpath('current','Plugin_Navigator_Full.html').read_text()
soup=BeautifulSoup(html,'html.parser')
DB=json.loads(soup.select_one('#db').string)
assert DB['version']=='2.7.4'

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
assert "['more','⋯','Ещё']" in script
assert "const bottom=[['dashboard','⌂','Главная'],['wizard','◎','Подбор'],['builder','＋','Цепочка'],['plugins','◫','Каталог'],['more','⋯','Ещё']]" in script
assert 'function navGroups' in script and 'Подготовка' in script and 'nav-group' in script
assert 'id="sideSources"' not in html
assert "['Enter',' ']" in script and 'function activate(' in script
assert 'tabindex="0"' in script
assert 'USER_DATA_SCHEMA=1' in script and 'normalizeBuilder' in script and 'builder-context' in script
assert 'moreExportData' in script and 'moreImportData' in script and 'confirmReplaceBuilder' in script
assert 'devFilter' in script and "p.developer!==state.developer" in script
assert 'role="tablist"' in script and 'aria-selected' in script
# Improvement 1: deterministic order assistant remains available without AI.
for token in ['function orderSpec','function orderDiagnostics','function autoOrderBuilder','function orderAssistantHTML','Расставить автоматически','Почему такой порядок','Pitch и timing корректируют','Sends являются параллельными ветками']:
    assert token in script,token
assert '.analysis-item.error{' in style and '.analysis-item.creative{' in style and '.order-flow{' in style

# Honest language and progressive disclosure.
assert 'ПРОВЕРЕННЫЙ PRESET' not in html
assert 'Выберите проверенный preset' not in html
for token in ['CURATED STARTING POINT','БАЗОВЫЙ СТАРТ — НЕ ОБЯЗАТЕЛЬНО','ЕСЛИ ТРЕБУЕТСЯ','CREATIVE — ПРОСЛУШАТЬ','MONITORING — НЕ EXPORT','Полное описание и порядок настройки','Включить, когда','Пропустить, когда','Что слушать','Сессия — до плагинов','Это чеклист подготовки','Типичная ошибка','Что сделать','Когда пропустить']:
    assert token in html,token
assert '<details' in html and '<summary' in html
assert 'expandedChains:new Set()' in script and 'data-expand-chain' in script and 'data-collapse-chain' in script
assert 'function sessionView' in script and 'SESSION_CHECKS' in script and 'data-check' in script and 'pn-session-checks' in script
assert "kind:'base'" in script and "kind:'conditional'" in script and 'sessionProgressLabel' in script and 'baseDone' in script
assert 'SESSION_LEADS' in script and 'sessionLead' in script and 'Главный элемент' in script and "title:'Панорама'" in script
assert "id:'setup'" in script and 'Рабочий уровень — Clip Gain' in script and 'Clip Gain внутри источника' in script
assert 'function analogueSelectHTML' in script and 'data-simple-alt' in script and 'data-wizard-alt' in script and 'То же семейство' in script
assert 'function pluginBlurb' in script and 'Чем отличается' in script and 'pluginBlurb(p)' in script
assert '.check-lesson>p{margin:0 0 8px;color:#c6d3e4;font-size:15px' in style
assert '.step-fact{' in style and 'font-size:13px' in style
assert 'не сдвиг клипа' in script and '−12…−6' in html and '−18 dBFS RMS' in script
assert DB['coverage']['officialExactProductPages']>=250 and DB['coverage']['officialVendorManualHubs']==365-DB['coverage']['officialExactProductPages']
assert DB['coverage']['sourceMappedPlugins']==364
assert DB['coverage']['standaloneUtilities']==1

# Every curated step carries full conditional guidance.
steps=[s for c in DB['chains'] for s in c['steps']]
assert len(steps)==353
fields=('necessity','necessityLabel','purpose','condition','skipWhen','listenFor','how')
assert all(all(s.get(k) for k in fields) for s in steps)
necessity=Counter(s['necessity'] for s in steps)
assert necessity=={'start':197,'conditional':110,'creative':34,'monitor':12}
assert DB['coverage']['conditionalStepGuides']==353
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
