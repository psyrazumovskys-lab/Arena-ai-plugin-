import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = json.loads((ROOT / 'plugin_navigator_database.json').read_text())
plugins = DB['plugins']
assert DB['version'] == '2.7.1'
assert len(plugins) == 365
assert DB['coverage']['pluginGuides'] == 365
assert DB['coverage']['productSpecificControlMaps'] >= 80

status = Counter()
settings_status = Counter()
curated_occurrences = 0
for plugin in plugins:
    guide = plugin.get('guide')
    assert guide, plugin['name']
    assert len(guide['fullDescription']) >= 280, plugin['name']
    simple = guide.get('simple') or ''
    assert len(simple) >= 80, plugin['name']
    cyr = sum(('а' <= ch.lower() <= 'я') or ch.lower() == 'ё' for ch in simple)
    assert cyr >= 35, (plugin['name'], cyr, simple[:140])
    assert 'Практическая роль:' not in guide['fullDescription'], plugin['name']
    assert len(guide['controls']) >= 4, plugin['name']
    assert 3 <= len(guide['settings']) <= 4, plugin['name']
    assert len(guide['workflow']) >= 6, plugin['name']
    assert len(guide['notFor']) >= 3, plugin['name']
    assert guide['useCases'], plugin['name']
    assert guide['evidence'], plugin['name']
    assert guide['controlStatus'] in {'Product-specific curated map', 'Product-informed curated map', 'Family-level control model'}
    status[guide['controlStatus']] += 1
    if ' / ' in plugin['name']:
        assert len(guide['variants']) >= 2, plugin['name']
    for control in guide['controls']:
        assert all(control.get(k) for k in ('name', 'role', 'hear', 'start', 'evidence')), (plugin['name'], control)
    for recipe in guide['settings']:
        assert all(recipe.get(k) for k in ('title', 'source', 'task', 'goal', 'status', 'routing', 'values', 'order', 'listenFor', 'stopWhen')), (plugin['name'], recipe['title'])
        assert len(recipe['values']) >= 3, (plugin['name'], recipe['title'])
        assert len(recipe['order']) >= 4, (plugin['name'], recipe['title'])
        settings_status[recipe['status']] += 1
        curated_occurrences += recipe['status'] == 'Curated preset occurrence'

by_name = {p['name']: p for p in plugins}
assert 'держит пики у потолка' not in by_name['Busboy']['guide']['simple']
assert 'sidechain' in by_name['UltraPump']['guide']['simple'].casefold() or 'pump' in by_name['UltraPump']['guide']['simple'].casefold()
assert 'второй дубль' not in by_name['ExoDelay']['guide']['simple']
assert all('роль записана' not in p['guide']['simple'] for p in plugins)
assert 'сатурац' in by_name['Soundtoys Decapitator']['guide']['simple'].casefold() or 'характер' in by_name['Soundtoys Decapitator']['guide']['simple']
assert 'FabFilter Pro-Q 4' in by_name
assert 'Celemony Melodyne' in by_name
# 2.7.0 confirmed description/control fixes.
assert 'Soundtoys Sandman Pro' not in by_name and 'Unfiltered Audio Sandman Pro' in by_name
assert 'Ozone Spectral Denoiser' not in by_name and 'iZotope RX Spectral De-noise' in by_name
rx=by_name['iZotope RX Spectral De-noise']
assert rx['official']['productPage'].endswith('/products/rx.html')
assert rx['official']['manualHub']=='https://docs.izotope.com/rx12/en/spectral-de-noise.html'
assert {'Learn','Threshold: Noisy / Tonal','Reduction: Noisy / Tonal','Artifact Control'} <= {c['name'] for c in rx['guide']['controls']}
micro=by_name['FabFilter Micro']
assert micro['official']['productPage'].endswith('/micro-mini-filter-plug-in')
assert {'Filter Display / Cutoff','Envelope Follower','Input Gain','Output Gain'} <= {c['name'] for c in micro['guide']['controls']}
assert not any('Ratio' in c['name'] for c in micro['guide']['controls'])
dbx=by_name['dbx 160']
assert {'Input','SC-HP','Mix','Noise','Stereo / Duo / MS'} <= {c['name'] for c in dbx['guide']['controls']}
assert not any('Over Easy' in c['name'] for c in dbx['guide']['controls'])
assert by_name['Waves H-Reverb']['official']['productPage'].endswith('/h-reverb-hybrid-reverb')
for name in ['bx_control V2','bx_solo','The Util','Waves Center','Waves MS Matrix','Waves S1 Stereo Imager']:
    assert by_name[name]['guide']['controlStatus']=='Product-specific curated map'
    assert not {'Rate','Depth','Delay / Detune','Feedback'} & {c['name'] for c in by_name[name]['guide']['controls']}
standalone=by_name['Session Inspector']
assert standalone['standalone'] and not standalone['uses'] and 'не является vst' in standalone['guide']['routing'].casefold()
assert {'Mode: Sharp / Balanced / Smooth','Detection Filter','Gain / Auto Gain'} <= {c['name'] for c in by_name['Ozone Vintage Compressor']['guide']['controls']}
assert {'Chakra','Tone EQ','THD','Delta'} <= {c['name'] for c in by_name['Chakra']['guide']['controls']}
assert {'Heat','Body','Crack','Air','Punch','Plate','Bomb'} == {c['name'] for c in by_name['Ultimate Snare']['guide']['controls']}
assert by_name['Archetype: Gojira']['guide']['controlStatus']=='Product-informed curated map'
assert by_name['bx_console AMEK 9099']['guide']['controlStatus']=='Product-informed curated map'
melodyne=by_name['Celemony Melodyne']
assert melodyne['developer']=='Celemony' and melodyne['family']=='Pitch correction'
assert melodyne['guide']['controlStatus']=='Product-specific curated map'
assert {'ARA / Transfer','Algorithm / Note Assignment','Correct Pitch Macro','Quantize Time Macro'} <= {c['name'] for c in melodyne['guide']['controls']}
assert {'Lead Vocal','Backing Vocals'} <= {u['source'] for u in melodyne['uses']}
assert {'Waves Tune','Waves Tune Real-Time'} <= set(melodyne['analogues'])
assert melodyne['official']['productPage']=='https://www.celemony.com/en/melodyne/what-is-melodyne'
assert 'первым insert' in melodyne['guide']['workflow'][1] and 'EQ, compression' in melodyne['guide']['workflow'][-1]
assert 'указан для' not in by_name['FabFilter Pro-Q 3']['guide']['simple']
assert 'карта' in by_name['FabFilter Pro-Q 3']['guide']['simple']
q4s = by_name['FabFilter Pro-Q 4']['guide']['simple'].casefold()
assert 'spectral' in q4s or 'sketch' in q4s or 'pro-q 4' in q4s
assert by_name['FabFilter Pro-Q 4']['official']['productPage'].endswith('pro-q-4-equalizer-plug-in')
assert 'audioloom' not in (by_name['FabFilter Pro-Q 4']['official'].get('vendorSite') or '')
assert by_name['bx_rockrack V3']['official']['productPage'].endswith('/products/bx_rockrack-v3')
assert by_name['ADPTR Sculpt']['official']['productPage'].endswith('/products/sculpt')
assert not by_name['bx_rockrack V3']['official']['productPage'].endswith('.html')
assert by_name['Friedman Dirty Shirley']['official']['productPage'].endswith('/products/ds-40')
assert by_name['Ampeg SVT-VR Classic']['official']['productPage'].endswith('/products/svt-vr-classic')
assert not by_name['bx_pultec / bx_pultec Pro']['official']['productPage']
assert not by_name['Shadow Hills Dual Vandergraph']['official']['productPage']
assert DB['coverage']['officialExactProductPages'] == 349
assert DB['coverage']['officialVendorManualHubs'] == 16
assert 'EQ Sketch' not in by_name['Ozone Spectral Shaper']['guide']['simple']
assert 'EQ Sketch' not in by_name['ADPTR Sculpt']['guide']['simple']
assert 'удар начала' not in by_name['Overloud Gem Dopamine']['guide']['simple']
assert 'тише делает то, что ниже порога' not in by_name['Renaissance Vox']['guide']['simple']
assert 'маленькой акустике' not in by_name['Waves LoAir']['guide']['simple']
assert 'sub' in by_name['Waves LoAir']['guide']['simple'].casefold() or 'ниже' in by_name['Waves LoAir']['guide']['simple']
assert 'boost+cut низа' not in by_name['PuigTec MEQ-5']['guide']['simple']
assert 'кабинета' not in by_name['Waves H-Reverb']['guide']['simple']
assert 'классическая редакция' in (by_name['bx_masterdesk / Classic']['guide']['variants'][1]['note'] if by_name['bx_masterdesk / Classic']['guide']['variants'] else '')

assert curated_occurrences > 200
assert status['Product-specific curated map'] == DB['coverage']['productSpecificControlMaps']
assert status['Product-informed curated map'] == DB['coverage']['productInformedControlMaps']
assert status['Product-specific curated map'] >= 80
assert all(p.get('official', {}).get('manualHub') and p['official'].get('verifiedOn') for p in plugins)
assert sum(bool(p['official']['productPage']) for p in plugins) >= 250
assert sum(bool(p['official']['productPage']) for p in plugins) == DB['coverage']['officialExactProductPages']
assert all(p['uses'] or p.get('standalone') for p in plugins)
html_bytes = (ROOT.parent / 'current' / 'Plugin_Navigator_Full.html').read_bytes()
assert html_bytes == (ROOT / 'Plugin_Navigator_Windows_Source' / 'resources' / 'index.html').read_bytes()
assert html_bytes == (ROOT.parent / 'current' / f"Plugin_Navigator_Full_v{DB['version'].split('-',1)[0]}.html").read_bytes()
print({
    'status': 'PASS',
    'version': DB['version'],
    'plugins': len(plugins),
    'control_status': dict(status),
    'settings_status': dict(settings_status),
    'curated_occurrence_recipes': curated_occurrences,
    'exact_product_pages': DB['coverage']['officialExactProductPages'],
})
