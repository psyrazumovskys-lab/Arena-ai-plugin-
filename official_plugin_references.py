"""Official vendor provenance for every catalog entry.

Exact product links are kept where the source workbook contains one (all 51
AudioLoom pages). For other products we provide an official vendor/manual hub,
clearly labelled as a hub rather than pretending it is an exact product manual.
"""

PA_SITE='https://www.plugin-alliance.com/collections/all-products'
PA_SUPPORT='https://support.plugin-alliance.com/'
PA_COL='https://www.plugin-alliance.com/collections/'

VENDORS={
'Waves':('Waves','https://www.waves.com/plugins','https://www.waves.com/downloads/manuals'),
'Brainworx':('Brainworx / Plugin Alliance',PA_COL+'brainworx',PA_SUPPORT),
'Soundtoys':('Soundtoys','https://www.soundtoys.com/product/','https://www.soundtoys.com/support/'),
'Neural DSP':('Neural DSP','https://neuraldsp.com/plugins','https://neuraldsp.com/downloads'),
'iZotope':('iZotope','https://www.izotope.com/en/products.html','https://docs.izotope.com/'),
'FabFilter':('FabFilter','https://www.fabfilter.com/products','https://www.fabfilter.com/help/'),
'Celemony':('Celemony','https://www.celemony.com/en/melodyne/what-is-melodyne','https://helpcenter.celemony.com/M5/'),
'Overloud':('Overloud','https://www.overloud.com/products','https://www.overloud.com/downloads'),
'Unfiltered Audio':('Unfiltered Audio / Plugin Alliance',PA_COL+'unfiltered-audio',PA_SUPPORT),
'SPL':('SPL / Plugin Alliance',PA_COL+'spl',PA_SUPPORT),
'Ampeg / Brainworx':('Ampeg / Brainworx',PA_COL+'ampeg',PA_SUPPORT),
'Friedman / Brainworx':('Friedman / Brainworx',PA_COL+'friedman',PA_SUPPORT),
'Lindell Audio':('Lindell Audio / Plugin Alliance',PA_COL+'lindell-audio',PA_SUPPORT),
'elysia':('elysia','https://www.elysia.com/software/','https://www.elysia.com/support/'),
'elysia / Plugin Alliance':('elysia / Plugin Alliance',PA_COL+'elysia',PA_SUPPORT),
'Diezel / Brainworx':('Diezel / Brainworx',PA_COL+'diezel',PA_SUPPORT),
'Newfangled Audio':('Newfangled Audio','https://www.newfangledaudio.com/','https://www.newfangledaudio.com/'),
'Bettermaker':('Bettermaker','https://www.bettermaker.com/plugins','https://www.bettermaker.com/downloads'),
'Suhr / Brainworx':('Suhr / Brainworx',PA_COL+'suhr',PA_SUPPORT),
'ADPTR Audio':('ADPTR Audio / Plugin Alliance',PA_COL+'adptr-audio',PA_SUPPORT),
'Dangerous Music':('Dangerous Music / Plugin Alliance',PA_SITE,PA_SUPPORT),
'ENGL / Brainworx':('ENGL / Brainworx',PA_COL+'engl',PA_SUPPORT),
'Vertigo Sound':('Vertigo Sound / Plugin Alliance',PA_COL+'vertigo',PA_SUPPORT),
'AMEK / Brainworx':('AMEK / Brainworx',PA_COL+'amek',PA_SUPPORT),
'Black Box Analog Design':('Black Box Analog Design / Plugin Alliance',PA_COL+'black-box-analog-design',PA_SUPPORT),
'IK Multimedia':('IK Multimedia','https://www.ikmultimedia.com/products/','https://www.ikmultimedia.com/userarea/manuals/'),
'Mäag Audio':('Mäag Audio / Plugin Alliance',PA_COL+'maag-audio',PA_SUPPORT),
'Purple Audio':('Purple Audio / Plugin Alliance',PA_COL+'purple-audio',PA_SUPPORT),
'Shadow Hills Industries':('Shadow Hills Industries / Plugin Alliance',PA_COL+'shadow-hills',PA_SUPPORT),
'Millennia':('Millennia / Plugin Alliance',PA_COL+'millennia',PA_SUPPORT),
'Gyraf Audio':('Gyraf Audio / Antelope Audio','https://en.antelopeaudio.com/','https://support.antelopeaudio.com/'),
'Looptrotter':('Looptrotter / Plugin Alliance',PA_COL+'looptrotter',PA_SUPPORT),
}


from official_product_pages import PRODUCT_PAGES, SUITE_NOTES, CURRENT_LICENSE_NOTES, COMPONENT_NOTES


def _product_note(name):
    if name in CURRENT_LICENSE_NOTES:
        return 'Текущая официальная licensed product page. Отдельной страницы Plugin Alliance больше нет; это не manual снятой PA-версии. Сверьте установленную версию.'
    if name == 'Waves MS Matrix':
        return 'Официальная страница S1 Stereo Imager: MS Matrix — utility-компонент S1, отдельного product page нет.'
    if name in COMPONENT_NOTES:
        return 'Официальная страница продукта, в который входит этот module/режим; это не отдельный mini-site модуля. Сверьте установленную версию.'
    if name in SUITE_NOTES:
        return 'Официальная страница suite, в которую входит этот module; это не отдельный mini-site модуля. Сверьте установленную версию.'
    return 'Точная официальная product page. Manual конкретной версии может быть отдельным download на сайте производителя.'


def apply_official_references(plugins):
    for p in plugins:
        if p.get('link'):
            link=p['link']
            audioloom='audioloom.com' in link.casefold()
            if audioloom:
                p['official']={
                    'vendor':p['developer'],
                    'productPage':link,
                    'vendorSite':'https://www.audioloom.com/',
                    'manualHub':link,
                    'referenceType':'Exact official product page',
                    'verifiedOn':'2026-08-14',
                    'note':'Точная официальная product page; manual может быть отдельным download внутри страницы/сайта.',
                }
                continue
            vendor,site,manual=VENDORS.get(p['developer'], (p['developer'], '', link))
            p['official']={
                'vendor':vendor,
                'productPage':link,
                'vendorSite':site or link,
                'manualHub':manual or link,
                'referenceType':'Exact official product page',
                'verifiedOn':'2026-08-14',
                'note':_product_note(p['name']),
            }
            continue
        assert p['developer'] in VENDORS,p['developer']
        vendor,site,manual=VENDORS[p['developer']]
        exact=PRODUCT_PAGES.get(p['name'],'')
        if exact:
            p['official']={
                'vendor':vendor,
                'productPage':exact,
                'vendorSite':site,
                'manualHub':manual,
                'referenceType':'Exact official product page',
                'verifiedOn':'2026-08-13',
                'note':_product_note(p['name']),
            }
            continue
        p['official']={
            'vendor':vendor,
            'productPage':'',
            'vendorSite':site,
            'manualHub':manual,
            'referenceType':'Official vendor/manual hub',
            'verifiedOn':'2026-08-13',
            'note':'Официальный vendor/manual hub, не точная ссылка на manual конкретной версии. Найдите продукт по оригинальному названию и сверьте установленную версию.',
        }
    return plugins
