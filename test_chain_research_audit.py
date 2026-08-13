import json
from collections import Counter
from pathlib import Path

DB=json.loads(Path(__file__).resolve().parent.joinpath('plugin_navigator_database.json').read_text())
chains=DB['chains'];sources=DB['researchSources']
assert DB['version']=='2.4.3-session-checklist'
assert len(chains)==99 and len(sources)>=20
assert len({s['id'] for s in sources})==len(sources)
assert {'iZotope','FabFilter','Waves','Sound On Sound'} <= {s['publisher'] for s in sources}

steps=[s for c in chains for s in c['steps']]
assert len(steps)==351
assert all(s.get('settings','').strip() and len(s['settings'])>=70 for s in steps)
from collections import defaultdict
signatures=defaultdict(list)
for c in chains: signatures[tuple((s['name'],s['task'],s['lane']) for s in c['steps'])].append(c['id'])
assert not [v for v in signatures.values() if len(v)>1]
assert len({s['name'] for s in steps})>=113
assert all(c.get('webAudit',{}).get('status','').startswith('WEB-RESEARCH') for c in chains)
assert all(c['webAudit']['sourceKeys'] and c['webAudit']['checks'] for c in chains)
assert all(c.get('preflight') for c in chains)
for c in chains:
    for s in c['steps']:
        assert all(s.get(k) for k in ('necessity','necessityLabel','purpose','condition','skipWhen','listenFor','how')), (c['id'],s['name'])
necessity=Counter(s['necessity'] for s in steps)
assert necessity=={'start':197,'conditional':108,'creative':34,'monitor':12}
kick_rock=next(c for c in chains if c['id']=='curated-kick-rock')
pro_g=next(s for s in kick_rock['steps'] if s['name']=='FabFilter Pro-G')
assert pro_g['necessity']=='conditional' and 'bleed' in pro_g['condition'] and 'Чистый sample' in pro_g['skipWhen']
assert any('polarity' in x for x in kick_rock['preflight'])
known={s['id'] for s in sources}
assert all(set(c['webAudit']['sourceKeys'])<=known for c in chains)

# Time effects are explicit send returns.
time_sends=[s for s in steps if s['lane']=='send' and s['task'] in {'Delay / echo','Reverb / пространство'}]
assert time_sends
assert all('100% wet' in s['settings'] and 'post-fader' in s['settings'].casefold() for s in time_sends)

# Monitoring cannot accidentally print.
monitor=[s for s in steps if s['lane']=='monitor']
assert monitor and all('не экспорт' in s['settings'].casefold() for s in monitor)

# Three parallel chains are one serial return, not three unrelated sends.
parallel=[c for c in chains if 'parallel' in (c['style']+' '+c['goal']).casefold()]
assert len(parallel)==3
for c in parallel:
    sends=[s for s in c['steps'] if s['lane']=='send']
    assert sends and {s['bus'] for s in sends}=={'Parallel A'}, c['id']
    assert c['chain'].count('Parallel A:')==1 and ' → '.join(s['name'] for s in sends) in c['chain']
    assert 'parallel' in c['webAudit']['sourceKeys']

# Mastering ends with limiting, followed only by monitoring.
masters=[c for c in chains if c['source']=='Premaster / Mastering']
assert len(masters)==3
for c in masters:
    audible=[s for s in c['steps'] if s['lane']!='monitor']
    assert audible[-1]['task']=='Limiter / clipper'
    assert {'mastering','limiter'}<=set(c['webAudit']['sourceKeys'])

# Mix-bus peak trimming is optional and preserves a clean premaster.
mixbus=[c for c in chains if c['source']=='Mix Bus / Stereo Bus']
assert len(mixbus)==3
for c in mixbus:
    for s in c['steps']:
        if s['task']=='Limiter / clipper':
            assert 'optional peak trim' in s['settings'] and 'clean pre-master' in s['settings']

by_risk=Counter(c['webAudit']['risk'] for c in chains)
by_publisher=Counter()
source_by_id={s['id']:s for s in sources}
for c in chains:
    for key in c['webAudit']['sourceKeys']: by_publisher[source_by_id[key]['publisher']]+=1

print({'status':'PASS','chains':len(chains),'steps':len(steps),'research_sources':len(sources),'time_sends':len(time_sends),'monitoring':len(monitor),'parallel_chains':len(parallel),'necessity':dict(necessity),'risk':dict(by_risk),'evidence_usage':dict(by_publisher)})
