import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = json.loads((ROOT / 'plugin_navigator_database.json').read_text())
plugins = DB['plugins']
assert DB['version'] == '2.4.5-nav-groups'
assert len(plugins) == 364
assert DB['coverage']['pluginGuides'] == 364
assert DB['coverage']['productSpecificControlMaps'] >= 80

status = Counter()
settings_status = Counter()
curated_occurrences = 0
for plugin in plugins:
    guide = plugin.get('guide')
    assert guide, plugin['name']
    assert len(guide['fullDescription']) >= 280, plugin['name']
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

assert curated_occurrences > 200
assert status['Product-specific curated map'] == DB['coverage']['productSpecificControlMaps']
assert status['Product-informed curated map'] == DB['coverage']['productInformedControlMaps']
assert status['Product-specific curated map'] >= 80
assert all(p.get('official', {}).get('manualHub') and p['official'].get('verifiedOn') for p in plugins)
assert sum(bool(p['official']['productPage']) for p in plugins) >= 250
assert sum(bool(p['official']['productPage']) for p in plugins) == DB['coverage']['officialExactProductPages']
assert all(p['uses'] for p in plugins)
assert (ROOT / 'Plugin_Navigator_Full.html').read_bytes() == (ROOT / 'Plugin_Navigator_Windows_Source' / 'resources' / 'index.html').read_bytes()
print({
    'status': 'PASS',
    'version': DB['version'],
    'plugins': len(plugins),
    'control_status': dict(status),
    'settings_status': dict(settings_status),
    'curated_occurrence_recipes': curated_occurrences,
    'exact_product_pages': DB['coverage']['officialExactProductPages'],
})
